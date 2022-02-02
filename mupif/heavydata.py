import dataclasses
from dataclasses import dataclass
from typing import Any
import typing
import sys
import numpy as np
# backing storage
import h5py
import Pyro5.api
# metadata support
from .mupifobject import MupifObject
from . import units, pyroutil, dumpable
from . import dataid
from .pyrofile import PyroFile
import types
import json
import tempfile
import logging
import os
import pydantic
import subprocess
import shutil
log = logging.getLogger(__name__)


from .dumpable import addPydanticInstanceValidator
addPydanticInstanceValidator(h5py.Dataset)

from .units import RefQuantity
import astropy

class Hdf5RefQuantity(RefQuantity):
    'Quantity stored in HDF5 dataset, the HDF5 file being managed somewhere else.'
    dataset: typing.Optional[h5py.Dataset]=None
    unit: astropy.units.UnitBase
    def __len__(self): return self.value_.shape[0]
    # make setting value more natural
    @property
    def value(self): return self.value_
    @value.setter
    def value(self,val): self.value_[:]=val

    # accessing quantity (value + unit)

    class Hdf5DatasetRowAccessor(object):
        def __init__(self,refq): self.refq=refq
        def __getitem__(self,row): return self.refq.dataset[row]*self.refq.unit
        def __setitem__(self,row: int,q: units.Quantity):
            if not isinstance(q,units.Quantity): raise ValueError('quantity must be an instance of mupif.units.Quantity (not a {q.__class__.__name__})')
            self.refq.dataset[row]=q.to(self.refq.unit)

    @property
    def quantity(self): return Hdf5RefQuantity.Hdf5RowAccessor(self)
    @quantity.setter
    def quantity(self,q): self.dataset[:]=q.to(self.unit)


HeavyDataBase_ModeChoice=typing.Literal['readonly', 'readwrite', 'overwrite', 'create', 'create-memory']

@Pyro5.api.expose
class HeavyDataBase(MupifObject):

    '''
    Base class for various HDF5-backed objects with automatic HDF5 transfer when copied to remote location. This class is to be used internally only.
    '''
    h5path: str = ''
    h5group: str = '/'
    h5uri: typing.Optional[str] = None
    mode: HeavyDataBase_ModeChoice='readonly'

    def __init__(self,**kw):
        super().__init__(**kw)  # calls the real ctor
        self._h5obj = None      # assigned in openStorage
        self.pyroIds = []
        if self.h5uri is not None:
            sys.stderr.write(f'HDF5 transfer: starting…\n')
            uri = Pyro5.api.URI(self.h5uri)
            remote = Pyro5.api.Proxy(uri)
            # sys.stderr.write(f'Remote is {remote}\n')
            fd, self.h5path = tempfile.mkstemp(suffix='.h5', prefix='mupif-tmp-', text=False)
            log.warning(f'Cleanup of temporary {self.h5path} not yet implemented.')
            PyroFile.copy(remote, self.h5path)
            sys.stderr.write(f'HDF5 transfer: finished, {os.stat(self.h5path).st_size} bytes.\n')
            # local copy is not the original, the URI is no longer valid
            self.h5uri = None



    def _returnProxy(self, v):
        if hasattr(self, '_pyroDaemon'):
            self._pyroDaemon.register(v)
            self.pyroIds.append(v._pyroId)
        return v

    @pydantic.validate_arguments
    def openStorage(self):
        '''

        '''
        if self.mode in ('readonly', 'readwrite'):
            if self.mode == 'readonly':
                if self._h5obj:
                    if self._h5obj.mode != 'r':
                        raise RuntimeError(f'HDF5 file {self.h5path} already open for writing.')
                else:
                    self._h5obj = h5py.File(self.h5path, 'r')
            elif self.mode == 'readwrite':
                if self._h5obj:
                    if self._h5obj.mode != 'r+':
                        raise RuntimeError(f'HDF5 file {self.h5path} already open read-only.')
                else:
                    if not os.path.exists(self.h5path):
                        raise RuntimeError(f'HDF5 file {self.h5path} does not exist (use mode="create" to create a new file.')
                    self._h5obj = h5py.File(self.h5path, 'r+')
        elif self.mode in ('overwrite', 'create', 'create-memory'):
            if self._h5obj:
                raise RuntimeError(f'HDF5 file {self.h5path} already open.')
            if self.mode == 'create-memory':
                import uuid
                doSave = bool(self.h5path)
                p = (self.h5path if doSave else str(uuid.uuid4()))
                if not doSave:
                    log.warning(f'Data will eventually disappear with mode="create-memory" and h5path="" (empty).')
                # hdf5 uses filename for lock management (even if the file is memory block only)
                # therefore pass if something unique if filename is not given
                self._h5obj = h5py.File(p, mode='x', driver='core', backing_store=doSave)
            else:
                if useTemp := (not self.h5path):
                    fd, self.h5path = tempfile.mkstemp(suffix='.h5', prefix='mupif-tmp-', text=False)
                    log.info(f'Using new temporary file {self.h5path}')
                if self.mode == 'overwrite' or useTemp:
                    self._h5obj = h5py.File(self.h5path, 'w')
                # 'create' mode should fail if file exists already
                # it would fail also with new temporary file; *useTemp* is therefore handled as overwrite
                else:
                    self._h5obj = h5py.File(self.h5path, 'x')
        return self._h5obj

    def exposeData(self):
        '''
        If *self* is registered in a Pyro daemon, the underlying HDF5 file will be exposed as well. This modifies the :obj:`h5uri` attribute which causes transparent download of the HDF5 file when the :obj:`HeavyDataBase` object is reconstructed remotely by Pyro (e.g. by using :obj:`Dumpable.copyRemote`).
        '''
        if (daemon := getattr(self, '_pyroDaemon', None)) is None:
            raise RuntimeError(f'{self.__class__.__name__} not registered in a Pyro5.api.Daemon.')
        if self.h5uri:
            return  # already exposed
        # binary mode is necessary!
        # otherwise: remote UnicodeDecodeError somewhere, and then 
        # TypeError: a bytes-like object is required, not 'dict'
        self.h5uri = str(daemon.register(pf := PyroFile(filename=self.h5path, mode='rb')))
        self.pyroIds.append(pf._pyroId)

    def closeData(self):
        '''
        * Flush and close the backing HDF5 file;
        * unregister all contexts from Pyro (if registered)
        '''
        if self._h5obj:
            self._h5obj.close()
            self._h5obj = None
        if daemon := getattr(self, '_pyroDaemon', None):
            for i in self.pyroIds:
                # sys.stderr.write(f'Unregistering {i}\n')
                daemon.unregister(i)

    @pydantic.validate_arguments
    def cloneHandle(self, newPath: str=''):
        '''Return clone of the handle; the underlying storage is copied into *newPath* (or a temporary file, if not given). All handle attributes (besides :obj:`h5path`) are preserved.'''
        if self._h5obj:
            raise RuntimeError(f'HDF5 file {self.h5path} is open (call closeData() first).')
        if not newPath:
            _fd, newPath = tempfile.mkstemp(suffix='.h5', prefix='mupif-tmp-', text=False)
        shutil.copy(self.h5path, newPath)
        ret = self.copy(deep=True)  # this is provided by pydantic
        ret.h5path = newPath
        return ret

    def repack(self):
        '''Repack the underlying storage (experimental, untested). Data must not be open.'''
        if self._h5obj:
            raise RuntimeError(f'Cannot repack while {self._h5obj} is open (call closeData first).')
        try:
            log.warning(f'Repacking {self.h5path} via h5repack [experimental]')
            out = self.h5path+'.~repacked~'
            subprocess.run(['h5repack', self.h5path, out], check=True)
            shutil.copy(out, self.h5path)
        except subprocess.CalledProcessError:
            log.warning('Repacking HDF5 file failed, unrepacked version was retained.')


class Hdf5OwningRefQuantity(Hdf5RefQuantity,HeavyDataBase):
    'Quantity stored in HDF5 dataset, managing the HDF5 file itself.'
    def __len__(self): return self.dataset.shape[0]
    # make setting value more natural
    @property
    def value(self): return self.dataset
    @value.setter
    def value(self,val): self.dataset[:]=val

    def allocateDataset(self,name,shape,**kw):
        if self.dataset: raise RuntimeError(f'dataset is already assigned (shape {"×".join(self.dataset.shape)})')
        if not self._h5obj: raise RuntimeError('Backing storage not open, call openStorage() first.')
        self.dataset=self._h5grp.create_dataset(name,shape=shape,**kw)

