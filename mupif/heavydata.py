

sampleSchemas_json='''
[
    {
        "_schema": "atom",
        "_datasetName": "atoms",
        "identity": {
            "element": {
                "dtype": "a2"
            },
            "atomicNumber": {
                "dtype": "l",
                "key": "identity.element",
                "lookup": {
                    "H": 1,
                    "C": 6,
                    "N": 7,
                    "Na": 11,
                    "Cl": 17,
                    "Fe": 26
                }
            },
            "atomicMass": {
                "dtype": "f",
                "key": "identity.element",
                "unit": "Dalton",
                "lookup": {
                    "H": 1.0079,
                    "C": 12.0107,
                    "N": 14.0067,
                    "Na": 22.9897,
                    "Cl": 35.453,
                    "Fe": 55.845
                }
            }
        },
        "properties": {
            "physical": {
                "partialCharge": {
                    "neutral": {
                        "dtype": "d",
                        "unit": "e"
                    },
                    "anion": {
                        "dtype": "d",
                        "unit": "e"
                    },
                    "cation": {
                        "dtype": "d",
                        "unit": "e"
                    }
                },
                "polarizability": {
                    "neutral": {
                        "dtype": "d",
                        "unit": "AA^2 s^4 kg^-1"
                    },
                    "anion": {
                        "dtype": "d",
                        "unit": "AA^2 s^4 kg^-1"
                    },
                    "cation": {
                        "dtype": "d",
                        "unit": "AA^2 s^4 kg^-1"
                    }
                }
            },
            "topology": {
                "parent": {
                    "dtype": "l"
                },
                "type": {
                    "dtype": "a",
                    "shape": "variable"
                },
                "name": {
                    "dtype": "a",
                    "shape": "variable"
                },
                "position": {
                    "dtype": "d",
                    "shape": [
                        3
                    ],
                    "unit": "AA"
                },
                "velocity": {
                    "dtype": "d",
                    "shape": [
                        3
                    ],
                    "unit": "AA/ps"
                },
                "structure": {
                    "dtype": "l",
                    "shape": "variable"
                }
            }
        }
    },
    {
        "_schema": "molecule",
        "_datasetName": "molecules",
        "identity": {
            "chemicalName": {
                "dtype": "a",
                "shape": "variable"
            },
            "molecularWeight": {
                "dtype": "d",
                "unit": "Dalton"
            }
        },
        "properties": {
            "electrical": {
                "HOMO": {
                    "dtype": "d",
                    "unit": "eV"
                },
                "LUMO": {
                    "dtype": "d",
                    "unit": "eV"
                },
                "siteEnergy": {
                    "orbital": {
                        "dtype": "d",
                        "unit": "eV"
                    },
                    "electrostatic": {
                        "dtype": "d",
                        "unit": "eV"
                    },
                    "polarization": {
                        "dtype": "d",
                        "unit": "eV"
                    }
                },
                "transferIntegrals": {
                    "dtype": "d",
                    "shape": "variable"
                },
                "reorganizationEnergyInternal": {
                    "anion": {
                        "dtype": "d",
                        "unit": "eV"
                    },
                    "cation": {
                        "dtype": "d",
                        "unit": "eV"
                    }
                }
            },
            "physical": {
                "polarizability": {
                    "neutral": {
                        "dtype": "d",
                        "shape": [
                            3,
                            3
                        ],
                        "unit": "AA^2 s^4 kg^-1"
                    },
                    "anion": {
                        "dtype": "d",
                        "shape": [
                            3,
                            3
                        ],
                        "unit": "AA^2 s^4 kg^-1"
                    },
                    "cation": {
                        "dtype": "d",
                        "shape": [
                            3,
                            3
                        ],
                        "unit": "AA^2 s^4 kg^-1"
                    }
                }
            },
            "chemical": {}
        },
        "topology": {
            "parent": {
                "dtype": "l",
                "unit": "none"
            },
            "centerOfMass": {
                "dtype": "d",
                "shape": [
                    3
                ],
                "unit": "AA"
            },
            "symmetryAxis": {
                "dtype": "d",
                "shape": [
                    3
                ],
                "unit": "AA"
            },
            "structureNeighbors": {
                "dtype": "l",
                "shape": "variable"
            }
        },
        "implementation": {
            "forceFieldType": {
                "dtype": "a",
                "shape": "variable"
            }
        },
        "atoms": {
            "path": "molecule/{ROW}/",
            "schema": "atom"
        }
    },
    {
        "_schema": "grain",
        "_datasetName": "grains",
        "identity": {
            "material": {
                "dtype": "a",
                "shape": "variable"
            }
        },
        "properties": {
            "eletrical": {
                "freeElectrons": {
                    "dtype": "l",
                    "unit": "none"
                },
                "freeHoles": {
                    "dtype": "l",
                    "unit": "none"
                }
            },
            "physical": {
                "reorganizationEnergyExternal": {
                    "dtype": "d",
                    "unit": "eV"
                }
            },
            "chemical": {}
        },
        "topology": {
            "parent": {
                "dtype": "l"
            },
            "cellSize": {
                "dtype": "d",
                "shape": [
                    3
                ],
                "unit": "m"
            }
        },
        "implementation": {
            "boundaryCondition": {
                "dtype": "a"
            }
        },
        "molecules": {
            "path": "grain/{ROW}/",
            "schema": "molecule"
        }
    }
]
'''

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
from . import units, pyroutil, dumpable, pyrofile
import types
import json
import tempfile
import logging
import deprecated
import os
import pydantic
import subprocess
import shutil
log=logging.getLogger(__name__)

def _cookSchema(desc,prefix='',schemaName='',fakeModule='',datasetName=''):
    __doc0__='''
    Transform dictionary-structured data schema into context access types.
    The access types are created using the "type" builtin and only stored
    in closures of the functions returning them. The top-level context is
    returned from this function to the user.
    
    get/set methods (and others) are not created on the fly but are instead
    put into those context types. This is substantially more efficient than
    hijacking __getattr__ and __setattr__.
    
    Closures in Python are somewhat unintuitive, since e.g. loop does not
    create a new scope (thus variable reference would later have the value
    in the last iteration step). Therefore local variables are captured via
    local function defaults, which makes some of the code less readable.
    '''

    @dataclass
    class CookedSchemaFragment:
        'Internal data used when cookSchema is called recursively'
        dtypes: list   # accumulates numpy dtypes for compound datatype 
        defaults: dict # default values, nan for floats and 0 for integers
        subpaths: list # accumulates nested paths (for deletion when resizing)
        T: Any=None    # nested context type
        doc: typing.List[str]=dataclasses.field(default_factory=list) # accumulates documentation (as markdown nested list)
        def append(self,other):
            self.dtypes+=other.dtypes
            self.defaults.update(other.defaults)
            self.doc+=other.doc
            self.subpaths+=other.subpaths


    def dtypeUnitDefaultDoc(v):
        'Parse dictionary *v* (part of the schema) and return (dtype,unit,default,doc) tuple'
        shape=v['shape'] if 'shape' in v else ()
        if isinstance(shape,list): shape=tuple(shape)
        ddoc={}
        if shape: ddoc['shape']=f'[{"×".join([str(s) for s in shape])}]'
        unit=units.Unit(v['unit']) if 'unit' in v else None
        dtype=v['dtype']
        default=None
        if dtype=='a':
            dtype=h5py.string_dtype(encoding='utf-8')
            shape=None
            ddoc['dtype']='string (utf-8 encoded)'
            ddoc['shape']='dynamic'
        elif shape=='variable':
            ddoc['dtype']=f'`[{np.dtype(dtype).name},…]`'
            dtype=h5py.vlen_dtype(np.dtype(dtype))
            shape=None
            ddoc['shape']='dynamic'
        else:
            dtype=np.dtype((dtype,shape))
            # log.warning(f'{fq}: defaults for non-scalar quantities (dtype.subdtype) not yet supported.')
            basedtype=(dtype if (not hasattr(dtype,'subdtype') or dtype.subdtype is None) else dtype.subdtype[0])
            #basedtype=dtype # workaround
            if basedtype.kind=='f': default=np.nan
            elif basedtype.kind in 'iu': default=0 
            ddoc['dtype']=f'`{basedtype.name}`'
        if unit: ddoc['unit']=f"`{str(unit)}`"
        if 'lookup' in v:
            ddoc['read-only']=f'table look-up by `{v["key"]}`'
            default=None
        if default is not None: ddoc['default']=f"`{str(default)}`"
        return dtype,unit,default,', '.join(f'{k}: {v}' for k,v in ddoc.items())

    def capitalize(k):
        'Turn the first letter into uppercase'
        return k[0].upper()+k[1:]  

    ret=CookedSchemaFragment(dtypes=[],defaults={},subpaths=[])
    meth={} # accumulate attribute access methods
    docLevel=(0 if not schemaName else prefix.count('.')+1)

    # top-level only
    if not schemaName:
        schemaName=desc['_schema']
        datasetName=desc['_datasetName']
        assert len(prefix)==0
        T_name='Context_'+schemaName
        import hashlib
        h=hashlib.blake2b(digest_size=6)
        h.update(json.dumps(desc).encode('utf-8'))
        fakeModule=types.ModuleType('_mupif_heavydata_'+h.hexdigest(),'Synthetically generated module for mupif.HeavyDataHandle schemas')
        # this somehow breaks imports, so better to avoid it until understood
        # if fakeModule.__name__ in sys.modules: return getattr(sys.modules[fakeModule.__name__],T_name)
        # sys.modules[fakeModule.__name__]=fakeModule
        ret.doc+=[f'**schema {schemaName}**','']
    else:
        T_name='Context_'+schemaName+'_'+prefix.replace('.','_')

    for key,val in desc.items():
        # fully-qualified name: for messages and compound field name in h5py
        fq=(f"{prefix}.{key}" if prefix else key)
        docHead=docLevel*3*' '+f'* `{key}`'
        # special keys start with underscore, so far only _schema is used
        if key.startswith('_'):
            if key=='_schema': continue
            elif key=='_datasetName': continue
            else: raise ValueError(f"Unrecognized special key '{key}' in prefix '{prefix}'.")
        if not isinstance(val,dict): raise TypeError("{fq}: value is not a dictionary.")
        # attribute defined via lookup, not stored
        if 'lookup' in val:
            dtype,unit,default,doc=dtypeUnitDefaultDoc(val)
            ret.doc+=[docHead+f': `get{capitalize(key)}()`: '+doc]
            lKey,lDict=val['key'],val['lookup']
            if isinstance(lKey,bytes): lKey=lKey.decode('utf8')
            # bind local values via default args (closure)
            def inherentGetter(self,*,fq=fq,dtype=dtype,unit=unit,lKey=lKey,lDict=lDict):
                _T_assertDataset(self,f"when looking up '{fq}' based on '{lKey}'.")
                def _lookup(row):
                    k=self.ctx.dataset[lKey,row]
                    if isinstance(k,bytes): k=k.decode('utf8')
                    try: val=np.array(lDict[k],dtype=dtype)[()] # [()] unpacks rank-0 scalar
                    except KeyError: raise KeyError(f"{fq}: key '{k}' ({lKey}) not found in the lookup table with keys {list(lDict.keys())}") from None
                    return val
                # fake broadcasting
                if self.row is None: val=np.array([_lookup(r) for r in range(self.ctx.dataset.shape[0])])
                else: val=_lookup(self.row)
                if unit: return units.Quantity(value=val,unit=unit)
                else: return val
            meth['get'+capitalize(key)]=inherentGetter
        # normal data attribute
        elif 'dtype' in val:
            dtype,unit,default,doc=dtypeUnitDefaultDoc(val)
            basedtype=(b[0] if (b:=getattr(dtype,'subdtype',None)) else dtype)
            ret.dtypes+=[(fq,dtype)] # add to the compound type
            ret.doc+=[docHead+f': `get{capitalize(key)}()`, `set{capitalize(key)}(…)`: '+doc]
            if default is not None: ret.defaults[fq]=default # add to the defaults
            def getter(self,*,fq=fq,unit=unit):
                _T_assertDataset(self,f"when getting the value of '{fq}'")
                if self.row is not None: value=self.ctx.dataset[fq,self.row]
                else: value=self.ctx.dataset[fq]
                if isinstance(value,bytes): value=value.decode('utf-8')
                if unit is None: return value
                return units.Quantity(value=value,unit=unit)
            def _cookValue(val,unit=unit,dtype=dtype,basedtype=basedtype):
                'Unit conversion, type conversion before assignment'
                if unit: val=(units.Quantity(val).to(unit)).value
                if isinstance(val,str): val=val.encode('utf-8')
                #sys.stderr.write(f"{fq}: {basedtype}\n")
                ret=np.array(val).astype(basedtype,casting='safe',copy=False)
                # for object (variable-length) types, convertibility was checked but the result is discarded
                if basedtype.kind=='O': return val 
                #sys.stderr.write(f"{fq}: cook {val} → {ret}\n")
                return ret
            def setter_direct(self,val,*,fq=fq,unit=unit,dtype=dtype):
                _T_assertDataset(self,f"when setting the value of '{fq}'")
                val=_cookValue(val)
                # sys.stderr.write(f'{fq}: direct setting {val}\n')
                if self.row is None: self.ctx.dataset[fq]=val
                else: self.ctx.dataset[self.row,fq]=val
            def setter_wholeRow(self,val,*,fq=fq,unit=unit,dtype=dtype):
                _T_assertDataset(self,f"when setting the value of '{fq}'")
                val=_cookValue(val)
                #sys.stderr.write(f'{fq}: wholeRow setting {repr(val)}\n')
                # workaround for bugs in h5py: for variable-length fields, and dim>1 subarrays:
                # direct assignment does not work; must read the whole row, modify, write it back
                # see https://stackoverflow.com/q/67192725/761090 and https://stackoverflow.com/q/67451714/761090
                # kind=='O' covers h5py.vlen_dtype and strings (h5py.string_dtype) with variable length
                if self.row is None: raise NotImplementedError('Broadcasting to variable-length fields or multidimensional subarrays not yet implemented.')
                rowdata=self.ctx.dataset[self.row]
                rowdata[self.ctx.dataset.dtype.names.index(fq)]=val
                self.ctx.dataset[self.row]=rowdata
            meth['get'+capitalize(key)]=getter
            meth['set'+capitalize(key)]=(setter_wholeRow if (dtype.kind=='O' or dtype.ndim>1) else setter_direct)
        elif 'path' in val:
            path,schema=val['path'],val['schema']
            if '{ROW}' not in path: raise ValueError(f"'{fq}': schema ref path '{path}' does not contain '{{ROW}}'.")
            if not path.endswith('/'): raise ValueError(f"'{fq}': schema ref path '{path}' does not end with '/'.")
            ret.subpaths.append(path)
            # path=path[:-1] # remove trailing slash
            def subschemaGetter(self,row=None,*,fq=fq,path=path,schema=schema):
                rr=[self.row is None,row is None]
                if sum(rr)==2: raise AttributeError(f"'{fq}': row index not set (or given as arg), unable to follow schema ref.")
                if sum(rr)==0: raise AttributeError(f"'{fq}': row given both as index ({self.row}) and arg ({row}).")
                if row is None: row=self.row
                #_T_assertDataset(self,f"when accessing subschema '{path}'.")
                #self.ctx.dataset[self.row] # catch invalid row index, data unused
                #print(f"{fq}: getting {path}")
                path=path.replace('{ROW}',str(row))
                subgrp=self.ctx.h5group.require_group(path)
                SchemaT=self.ctx.schemaRegistry[schema]
                ret=SchemaT(top=HeavyDataHandle.TopContext(h5group=subgrp,schemaRegistry=self.ctx.schemaRegistry,pyroIds=self.ctx.pyroIds),row=None)
                # if hasattr(self,'_pyroDaemon'):
                #    self._pyroDaemon.register(ret)
                #    self.ctx.pyroIds.append(ret._pyroId)
                # print(f"{fq}: schema is {SchemaT}, returning: {ret}.")
                return _registeredWithDaemon(self,ret)
            ret.doc+=[docHead+f': `get{capitalize(key)}()`: nested data at `{path}`, schema `{schema}`.']
            meth['get'+capitalize(key)]=subschemaGetter
        else:
            # recurse
            ret.doc+=[docHead+f': `get{capitalize(key)}()`',''] # empty line for nesting in restructured text
            cooked=_cookSchema(val,prefix=fq,schemaName=schemaName,fakeModule=fakeModule,datasetName=datasetName)
            ret.append(cooked)
            def nestedGetter(self,*,T=cooked.T):
                #print('nestedGetter',T)
                ret=T(other=self)
                # if hasattr(self,'_pyroDaemon'):
                #    self._pyroDaemon.register(ret)
                #    self.ctx.pyroIds.append(ret._pyroId)
                return _registeredWithDaemon(self,ret)
            meth['get'+capitalize(key)]=nestedGetter # lambda self, T=cooked.T: T(self)
    def _registeredWithDaemon(context,obj):
        if not hasattr(context,'_pyroDaemon'): return obj
        context._pyroDaemon.register(obj)
        context.ctx.pyroIds.append(obj._pyroId)
        return obj
    def T_init(self,*,top=None,other=None,row=None):
        '''
        The constructor is a bit hairy, as the new context either:
        (1) nests inside TopContext (think of dataset);
        (2) nests inside an already nested context (think of sub-dataset);
        (3) adds row information, not changing location (row in (sub)dataset)
        (4) nests & adds row, such as in getMolecules(0) which is a shorthand for getMolecules()[0]
        '''
        if top is not None:
            assert isinstance(top,HeavyDataHandle.TopContext)
            self.ctx,self.row=top,row
        elif other is not None:
            assert not isinstance(other,HeavyDataHandle.TopContext)
            # print(f'other.row={other.row}, row={row}')
            if (other.row is not None) and (row is not None): raise IndexError(f'Context already indexed, with row={row}.')
            self.ctx,self.row=other.ctx,(other.row if row is None else row)
           # print(f"[LEAF] {self}, other={other}")
        else: raise ValueError('One of *top* or *other* must be given.')
    def T_str(self):
        'Context string representation'
        return F"<{self.__class__.__name__}, row={self.row}, ctx={self.ctx}{', _pyroId='+self._pyroId if hasattr(self,'_pyroDaemon') else ''}>"
    def T_getitem(self,row):
        'Indexing access; checks index validity and returns new context with the row set'
        _T_assertDataset(self,msg=f'when trying to index row {row}')
        if(row<0 or row>=self.ctx.dataset.shape[0]): raise IndexError(f"{fq}: row index {row} out of range 0…{self.ctx.dataset.shape[0]}.")
        # self.ctx.dataset[row] # this would raise ValueError but iteration protocol needs IndexError
        # print(f'Item #{row}: returning {self.__class__(self,row=row)}')
        ret=self.__class__(other=self,row=row)
        return _registeredWithDaemon(self,ret)
        #if hasattr(self,'_pyroDaemon'):
        #    self._pyroDaemon.register(ret)
        #    self.ctx.pyroIds.append(ret._pyroId)
        return ret
    def T_len(self):
        'Return sequence length'
        _T_assertDataset(self,msg=f'querying dataset length')
        if self.row is not None: return IndexError('Row index already set, not behaving as sequence.')
        return self.ctx.dataset.shape[0]
    def _T_assertDataset(self,msg=''):
        'checks that the backing dataset it present/open. Raises exception otherwise.'
        if self.ctx.dataset is None:
            if self.__class__.datasetName in self.ctx.h5group: self.ctx.dataset=self.ctx.h5group[self.__class__.datasetName]
            else: raise RuntimeError(f'Dataset not yet initialized, use resize first{" ("+msg+")" if msg else ""}: {self.ctx.h5group.name}/{self.__class__.datasetName}.')

    def T_resize(self,size,reset=False,*,ret=ret):
        'Resizes the backing dataset; this will, as necessary, create a new dataset, or grow/shrink size of an existing dataset. New records are always default-initialized.'
        def _initrows(ds,rowmin,rowmax):
            'default-initialize contiguous range of rows rmin…rmax (inclusive)'
            defrow=ds[rowmin] # use first row as storage, assign all defaults into it, then copy over all other rows
            for fq,val in ret.defaults.items(): defrow[fq]=val
            self.ctx.dataset[rowmin+1:rowmax+1]=defrow
        if reset: self.resize(size=0)
        assert size>=0
        dsname=self.__class__.datasetName
        if self.ctx.dataset is None:
            if dsname not in self.ctx.h5group:
                self.ctx.dataset=self.ctx.h5group.create_dataset(dsname,shape=(size,),maxshape=(None,),dtype=ret.dtypes,compression='gzip')
                _initrows(self.ctx.dataset,rowmin=0,rowmax=size-1)
                return
            else: self.ctx.dataset=self.ctx.h5group[dsname]
        oldSize=self.ctx.dataset.shape[0]
        self.ctx.dataset.resize((size,))
        if oldSize<size: _initrows(self.ctx.dataset,rowmin=oldSize,rowmax=size-1)
        else:
            # sys.stderr.write(f'Removing stale subpaths {str(ret.subpaths)}, {oldSize} → {size}…\n')
            # remove stale subpaths
            for subpath in ret.subpaths:
                for r in range(size,oldSize):
                    p=subpath.replace('{ROW}',str(r))
                    # sys.stderr.write(f'Resizing {self.ctx.dataset}, {oldSize} → {size}: deleting {p}\n')
                    if p in self.ctx.h5group: del self.ctx.h5group[p]
                    else: pass # sys.stderr.write(f'{self.ctx.h5group}: does not contain {p}, not deleted')

            # log.warning('Deleting nested data not yet done when shrinking datasets')
    def T_iter(self):
        _T_assertDataset(self,msg=f'when iterating')
        for row in range(self.ctx.dataset.shape[0]): yield self[row]

    meth['__init__']=T_init
    meth['__str__']=meth['__repr__']=T_str
    meth['__getitem__']=T_getitem
    meth['__len__']=T_len
    meth['row']=None
    meth['ctx']=None
    # __del__ note: it would be nice to use context destructor to unregister contexts from Pyro
    # (those which registered automatically). Since the daemon is holding one reference, however,
    # the dtor will never be called, unfortunately

    # those are defined only for the "root" context
    if not prefix:
        meth['resize']=T_resize
        # meth['pyroIds']=[]
        ret.dtypes=np.dtype(ret.dtypes)
        T_bases=()
    else:
        T_bases=() # only top-level has metadata

    T=type(T_name,T_bases,meth)
    T.__module__=fakeModule.__name__ ## make the (T.__module__,T.__name__) tuple used in serialization unique
    T.datasetName=datasetName
    T=Pyro5.api.expose(T)
    setattr(fakeModule,T_name,T)

    if not prefix:
        T.name=schemaName # schema knows its own name, for convenience of creating schema registry
        T.__doc__='\n'.join(ret.doc)+'\n'
        return T
    else:
        ret.T=T
        return ret


def makeSchemaRegistry(dd):
    return dict([((T:=_cookSchema(d)).name,T) for d in dd])


def _make_grains(h5name):
    import time, random
    from mupif.units import U as u
    t0=time.time()
    atomCounter=0
    # precompiled schemas
    schemaRegistry=makeSchemaRegistry(json.loads(sampleSchemas_json))
    with h5py.File(h5name,'w') as h5:
        grp=h5.require_group('test')
        schemaT=schemaRegistry['grain']
        grp.attrs['schemas']=sampleSchemas_json
        grp.attrs['schema']=schemaT.name
        grains=schemaT(top=HeavyDataHandle.TopContext(h5group=grp,schemaRegistry=schemaRegistry,pyroIds=[]))
        print(f"{grains}")
        grains.resize(size=5)
        print(f"There is {len(grains)} grains.")
        for ig,g in enumerate(grains):
            #g=grains[ig]
            print('grain',ig,g)
            g.getMolecules().resize(size=random.randint(5,50))
            print(f"Grain #{ig} has {len(g.getMolecules())} molecules")
            for m in g.getMolecules():
                #for im in range(len(g.getMolecules())):
                #m=g.getMolecules()[im]
                # print('molecule: ',m)
                m.getIdentity().setMolecularWeight(random.randint(1,10)*u.yg)
                m.getAtoms().resize(size=random.randint(30,60))
                for a in m.getAtoms():
                    #for ia in range(len(m.getAtoms())):
                    #a=m.getAtoms()[ia]
                    a.getIdentity().setElement(random.choice(['H','N','Cl','Na','Fe']))
                    a.getProperties().getTopology().setPosition((1,2,3)*u.nm)
                    a.getProperties().getTopology().setVelocity((24,5,77)*u.m/u.s)
                    # not yet, see https://stackoverflow.com/q/67192725/761090
                    struct=np.array([random.randint(1,20) for i in range(random.randint(5,20))],dtype='l')
                    a.getProperties().getTopology().setStructure(struct)
                    atomCounter+=1
    t1=time.time()
    print(f'{atomCounter} atoms created in {t1-t0:g} sec ({atomCounter/(t1-t0):g}/sec).')

def _read_grains(h5name):
    import time
    # note how this does NOT need any schemas defined, they are all pulled from the HDF5
    t0=time.time()
    atomCounter=0
    with h5py.File(h5name,'r') as h5:
        grp=h5['test']
        schemaRegistry=makeSchemaRegistry(json.loads(grp.attrs['schemas']))
        grains=schemaRegistry[grp.attrs['schema']](top=HeavyDataHandle.TopContext(h5group=grp,schemaRegistry=schemaRegistry,pyroIds=[]))
        for g in grains:
            # print(g)
            print(f'Grain #{g.row} has {len(g.getMolecules())} molecules.')
            for m in g.getMolecules():
                m.getIdentity().getMolecularWeight()
                for a in m.getAtoms():
                    a.getIdentity().getElement()
                    a.getProperties().getTopology().getPosition()
                    a.getProperties().getTopology().getVelocity()
                    a.getProperties().getTopology().getStructure()
                    atomCounter+=1
    t1=time.time()
    print(f'{atomCounter} atoms read in {t1-t0:g} sec ({atomCounter/(t1-t0):g}/sec).')



@Pyro5.api.expose
class HeavyDataHandle(MupifObject):
    h5path: str=''
    h5group: str='/'
    h5uri: typing.Optional[str]=None

    # __doc__ is a computed property which will add documentation for the sample JSON schemas
    __doc0__='''This will be the normal documentation of HeavyDataHandle.

    '''

    # from https://stackoverflow.com/a/3203659/761090
    class _classproperty(object):
        def __init__(self, getter): self.getter=getter
        def __get__(self, instance, owner): return self.getter(owner)

    @_classproperty
    def __doc__(cls):
        ret=cls.__doc0__
        reg=makeSchemaRegistry(json.loads(sampleSchemas_json))
        for key,val in reg.items():
            ret+='\n\n'+val.__doc__.replace('`','``')
        return ret

    @dataclass
    @Pyro5.api.expose
    class TopContext():
        h5group: Any
        pyroIds: list
        schemaRegistry: dict
        dataset: Any=None
        def __str__(self):
            return f'{self.__module__}.{self.__class__.__name__}(h5group={str(self.h5group)},dataset={str(self.dataset)},schemaRegistry=<<{",".join(self.schemaRegistry.keys())}>>)'


    def getSchemaRegistry(self,compile=False):
        'Return schema registry as JSON string'
        self._openRead()
        ssh=self._h5obj[self.h5group].attrs['schemas']
        return ssh if not compile else makeSchemaRegistry(json.loads(ssh))

    def _returnProxy(self,v):
        if hasattr(self,'_pyroDaemon'):
            self._pyroDaemon.register(v)
            self.pyroIds.append(v._pyroId)
        return v

    def _openRead(self):
        #if self.h5path==':memory:': raise ValueError('Impossible to open in-memory HDF5 for reading')
        if self._h5obj is None: self._h5obj=h5py.File(self.h5path,'r')
    def _openReadWrite(self):
        #if self.h5path==':memory:': raise ValueError('Impossible to open in-memory HDF5 for reading/writing')
        if self._h5obj is None: self._h5obj=h5py.File(self.h5path,'r+')
        elif self._h5obj.mode=='r': raise RuntimeError(f'Backing storage {self._h5obj} already open as read-only.')

    @pydantic.validate_arguments
    def getData(self, mode: typing.Literal['readonly','readwrite','overwrite','create','create-memory'], schemaName: typing.Optional[str]=None, schemasJson: typing.Optional[str]=None):
        if mode in ('readonly','readwrite'):
            if mode=='readonly':
                if self._h5obj:
                    if self._h5obj.mode!='r': raise RuntimeError(f'HDF5 file {self.h5path} already open for writing.')
                else: self._h5obj=h5py.File(self.h5path,'r')
            elif mode=='readwrite':
                if self._h5obj:
                    if self._h5obj.mode!='r+': raise RuntimeError(f'HDF5 file {self.h5path} already open read-only.')
                else:
                    if not os.path.exists(self.h5path): raise RuntimeError(f'HDF5 file {self.h5path} does not exist (use mode="create" to create a new file.')
                    self._h5obj=h5py.File(self.h5path,'r+')
            assert self._h5obj
            grp=self._h5obj[self.h5group]
            schemaRegistry=makeSchemaRegistry(json.loads(grp.attrs['schemas']))
            top=schemaRegistry[grp.attrs['schema']](top=HeavyDataHandle.TopContext(h5group=grp,schemaRegistry=schemaRegistry,pyroIds=self.pyroIds))
            return self._returnProxy(top)
        elif mode in ('overwrite','create','create-memory'):
            if not schemaName or not schemasJson: raise ValueError(f'Both *schema* abd *schemaJson* must be given (opening {self.h5path} in mode {mode})')
            if self._h5obj: raise RuntimeError(f'HDF5 file {self.h5path} already open.')
            if mode=='create-memory':
                import uuid
                p=(self.h5path if self.h5path else str(uuid.uuid4()))
                # hdf5 uses filename for lock management (even if the file is memory block only)
                # therefore pass if something unique if filename is not given
                self._h5obj=h5py.File(p,mode='x',driver='core',backing_store=(self.h5path is not None))
            else:
                if useTemp:=(not self.h5path):
                    fd,self.h5path=tempfile.mkstemp(suffix='.h5',prefix='mupif-tmp-',text=False)
                    log.info('Using new temporary file {self.h5path}')
                if mode=='overwrite' or useTemp: self._h5obj=h5py.File(self.h5path,'w')
                # 'create' mode should fail if file exists already
                # it would fail also with new temporary file; *useTemp* is therefore handled as overwrite
                else: self._h5obj=h5py.File(self.h5path,'x')
            grp=self._h5obj.require_group(self.h5group)
            grp.attrs['schemas']=schemasJson
            grp.attrs['schema']=schemaName
            schemaRegistry=makeSchemaRegistry(json.loads(schemasJson))
            top=schemaRegistry[grp.attrs['schema']](top=HeavyDataHandle.TopContext(h5group=grp,schemaRegistry=schemaRegistry,pyroIds=self.pyroIds))
            return self._returnProxy(top)

    @deprecated.deprecated
    def getDataReadonly(self): return self.getData(mode='readonly')
    @deprecated.deprecated
    def getDataReadWrite(self): return self.getData(mode='readwrite')
    @deprecated.deprecated
    def getDataNew(self,schema,schemasJson): return self.getData(mode='overwrite',schemaName=schema,schemasJson=schemasJson)

    def closeData(self,repack=False):
        '''
        * Flush and close the backing HDF5 file;
        * unregister all contexts from Pyro (if registered)
        * optionally repack the HDF5 file if it was open for writing and *repack* is `True`.
        '''
        if self._h5obj:
            rw=self._h5obj.mode=='r+'
            self._h5obj.close()
            self._h5obj=None
            if rw and repack:
                try:
                    log.warning(f'Repacking {self.h5path} via h5repack [experimental]')
                    out=self.h5path+'.~repacked~'
                    subprocess.run(['h5repack',self.h5path,out],check=True)
                    shutil.copy(out,self.h5path)
                except subprocess.CalledProcessError:
                    log.warning('Repacking HDF5 file failed, unrepacked version was retained.')

        daemon=getattr(self,'_pyroDaemon',None)
        if daemon:
            for i in self.pyroIds:
                # sys.stderr.write(f'Unregistering {i}\n')
                daemon.unregister(i)
    def exposeData(self):
        if (daemon:=getattr(self,'_pyroDaemon',None)) is None: raise RuntimeError(f'{self.__class__.__name__} not registered in a Pyro5.api.Daemon.')
        if self.h5uri: return # already exposed
        # binary mode is necessary!
        # otherwise: remote UnicodeDecodeError somewhere, and then 
        # TypeError: a bytes-like object is required, not 'dict'
        self.h5uri=str(daemon.register(pf:=pyrofile.PyroFile(self.h5path,mode='rb')))
        self.pyroIds.append(pf._pyroId)
    def __init__(self,**kw):
        super().__init__(**kw) # this calls the real ctor
        #sys.stderr.write(f'{self.__class__.__name__}.__init__(**kw={str(kw)})\n')
        #import traceback
        #traceback.print_stack(file=sys.stderr)
        self._h5obj=None
        self.pyroIds=[]
        if self.h5uri is not None:
            sys.stderr.write(f'HDF5 transfer: starting…\n')
            uri=Pyro5.api.URI(self.h5uri)
            remote=Pyro5.api.Proxy(uri)
            #sys.stderr.write(f'Remote is {remote}\n')
            fd,self.h5path=tempfile.mkstemp(suffix='.h5',prefix='mupif-tmp-',text=False)
            log.warning(f'Cleanup of temporary {self.h5path} not yet implemented.')
            pyroutil.downloadPyroFile(self.h5path,remote)
            sys.stderr.write(f'HDF5 transfer: finished, {os.stat(self.h5path).st_size} bytes.\n')
            # local copy is not the original, the URI is no longer valid
            self.h5uri=None


'''
future ideas:
* Create all context classes as Ctx_<md5 of the JSON schema> so that the name is unique.\
* Register classes to Pyro when the schema is read
* Register classes to remote Pyro when the heavy file is transferred?
'''

# uses relative imports, therefore run stand-alone as as:
#
# PYTHONPATH=.. python3 -m mupif.heavydata
#
if __name__=='__main__':
    import json, pprint
    print(HeavyDataHandle.__doc__)
    # print(json.dumps(json.loads(sampleSchemas_json),indent=2))
    _make_grains('/tmp/grains.h5')
    _read_grains('/tmp/grains.h5')

    # this won't work through Pyro yet
    pp=HeavyDataHandle(h5path='/tmp/grains.h5',h5group='test')
    for key,val in pp.getSchemaRegistry(compile=True).items():
        print(val.__doc__.replace('`','``'))
    root=pp.getData('readonly')
    print(pp.getData(mode='readonly')[0].getMolecules())
    print(root.getMolecules(0).getAtoms(5).getIdentity().getElement())
    print(root[0].getMolecules()[5].getAtoms().getIdentity().getElement())
    pp.closeData()
    pp.getData('readwrite')


