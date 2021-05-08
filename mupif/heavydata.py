'''

Sample schema documentation
----------------------------

schema atom
~~~~~~~~~~~~~~

* ``identity``

   * ``element``: dtype: ``bytes16``
   * ``atomicNumber``: dtype: ``int64``, read-only: table look-up by ``identity.element``
   * ``atomicMass``: dtype: ``float32``, unit: ``u``, read-only: table look-up by ``identity.element``
* ``properties``

   * ``physical``

      * ``partialCharge``

         * ``neutral``: dtype: ``float64``, unit: ``e``, default: ``nan``
         * ``anion``: dtype: ``float64``, unit: ``e``, default: ``nan``
         * ``cation``: dtype: ``float64``, unit: ``e``, default: ``nan``
      * ``polarizability``

         * ``neutral``: dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
         * ``anion``: dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
         * ``cation``: dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
   * ``topology``

      * ``parent``: dtype: ``int64``, default: ``0``
      * ``type``: shape: dynamic, dtype: string (utf-8 encoded)
      * ``name``: shape: dynamic, dtype: string (utf-8 encoded)
      * ``position``: shape: [3], dtype: ``float64``, unit: ``Angstrom``, default: ``nan``
      * ``velocity``: shape: [3], dtype: ``float64``, unit: ``Angstrom / ps``, default: ``nan``
      * ``structure``: shape: dynamic, dtype: ``[int64,…]``

schema molecule
~~~~~~~~~~~~~~~~~~

* ``identity``

   * ``chemicalName``: shape: dynamic, dtype: string (utf-8 encoded)
   * ``molecularWeight``: dtype: ``float64``, unit: ``u``, default: ``nan``
* ``properties``

   * ``electrical``

      * ``HOMO``: dtype: ``float64``, unit: ``eV``, default: ``nan``
      * ``LUMO``: dtype: ``float64``, unit: ``eV``, default: ``nan``
      * ``siteEnergy``

         * ``orbital``: dtype: ``float64``, unit: ``eV``, default: ``nan``
         * ``electrostatic``: dtype: ``float64``, unit: ``eV``, default: ``nan``
         * ``polarization``: dtype: ``float64``, unit: ``eV``, default: ``nan``
      * ``transferIntegrals``: shape: dynamic, dtype: ``[float64,…]``
      * ``reorganizationEnergyInternal``

         * ``anion``: dtype: ``float64``, unit: ``eV``, default: ``nan``
         * ``cation``: dtype: ``float64``, unit: ``eV``, default: ``nan``
   * ``physical``

      * ``polarizability``

         * ``neutral``: shape: [3×3], dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
         * ``anion``: shape: [3×3], dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
         * ``cation``: shape: [3×3], dtype: ``float64``, unit: ``Angstrom2 s4 / kg``, default: ``nan``
   * ``chemical``

* ``topology``

   * ``parent``: dtype: ``int64``, unit: ``none``, default: ``0``
   * ``centerOfMass``: shape: [3], dtype: ``float64``, unit: ``Angstrom``, default: ``nan``
   * ``symmetryAxis``: shape: [3], dtype: ``float64``, unit: ``Angstrom``, default: ``nan``
   * ``structureNeighbors``: shape: dynamic, dtype: ``[int64,…]``
* ``implementation``

   * ``forceFieldType``: shape: dynamic, dtype: string (utf-8 encoded)
* ``atoms``: nested data at ``molecule_{ROW}/atoms``, schema ``atom``.

schema grain
~~~~~~~~~~~~~~~

* ``identity``

   * ``material``: shape: dynamic, dtype: string (utf-8 encoded)
* ``properties``

   * ``eletrical``

      * ``freeElectrons``: dtype: ``int64``, unit: ``none``, default: ``0``
      * ``freeHoles``: dtype: ``int64``, unit: ``none``, default: ``0``
   * ``physical``

      * ``reorganizationEnergyExternal``: dtype: ``float64``, unit: ``eV``, default: ``nan``
   * ``chemical``

* ``topology``

   * ``parent``: dtype: ``int64``, default: ``0``
   * ``cellSize``: shape: [3], dtype: ``float64``, unit: ``m``, default: ``nan``
* ``implementation``

   * ``boundaryCondition``: dtype: string (utf-8 encoded), shape: dynamic
* ``molecules``: nested data at ``grain_{ROW}/molecules``, schema ``molecule``.



'''





sampleSchemas_json='''
[
    {
        "_schema": "atom",
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
            "path": "molecule_{ROW}/atoms",
            "schema": "atom"
        }
    },
    {
        "_schema": "grain",
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
            "path": "grain_{ROW}/molecules",
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
import os
log=logging.getLogger(__name__)

def _cookSchema(desc,prefix='',schemaName='',fakeModule=''):
    '''
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
        T: Any=None    # nested context type
        doc: typing.List[str]=dataclasses.field(default_factory=list) # accumulates documentation (as markdown nested list)
        def append(self,other):
            self.dtypes+=other.dtypes
            self.defaults.update(other.defaults)
            self.doc+=other.doc

            
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
            log.warning('defaults for non-scalar quantities (dtype.subdtype) not yet supported.')
            # basedtype=(dtype if (not hasattr(dtype,'subdtype') or dtype.subdtype is None) else dtype.subdtype[0])
            basedtype=dtype # workaround
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
    
    ret=CookedSchemaFragment(dtypes=[],defaults={})
    meth={} # accumulate attribute access methods
    docLevel=(0 if not schemaName else prefix.count('.')+1)

    # top-level only
    if not schemaName:
        schemaName=desc['_schema']
        assert len(prefix)==0
        T_name='Context_'+schemaName
        import hashlib
        h=hashlib.blake2b(digest_size=6)
        h.update(json.dumps(desc).encode('utf-8'))
        fakeModule=types.ModuleType('_mupif_heavydata_'+h.hexdigest(),'Synthetically generated module for mupif.HeavyDataHandle schemas')
        if fakeModule.__name__ in sys.modules: return getattr(sys.modules[fakeModule.__name__],T_name)
        sys.modules[fakeModule.__name__]=fakeModule
        ret.doc+=[f'## schema {schemaName}','']
    else:
        T_name='Context_'+schemaName+prefix.replace('.','_')

    
    for key,val in desc.items():
        # fully-qualified name: for messages and compound field name in h5py
        fq=(f"{prefix}.{key}" if prefix else key)
        docHead=docLevel*3*' '+f'* `{key}`'
        # special keys start with underscore, so far only _schema is used
        if key.startswith('_'):
            if key=='_schema': continue
            else: raise ValueError(f"Unrecognized special key '{key}' in prefix '{prefix}'.")
        if not isinstance(val,dict): raise TypeError("{fq}: value is not a dictionary.")
        # attribute defined via lookup, not stored
        if 'lookup' in val:
            dtype,unit,default,doc=dtypeUnitDefaultDoc(val)
            ret.doc+=[docHead+': '+doc]
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
            ret.dtypes+=[(fq,dtype)] # add to the compound type
            ret.doc+=[docHead+': '+doc]
            if default is not None: ret.defaults[fq]=default # add to the defaults
            def getter(self,*,fq=fq,unit=unit):
                _T_assertDataset(self,f"when getting the value of '{fq}'")
                if self.row is not None: value=self.ctx.dataset[fq,self.row]
                else: value=self.ctx.dataset[fq]
                if isinstance(value,bytes): value=value.decode('utf-8')
                if unit is None: return value
                return units.Quantity(value=value,unit=unit)
            def setter(self,val,*,fq=fq,unit=unit,dtype=dtype):
                # print(f'{fq}: setter')
                _T_assertDataset(self,f"when setting the value of '{fq}'")
                if unit: val=(units.Quantity(val).to(unit)).value
                if isinstance(val,str): val=val.encode('utf-8')
                casting='safe'
                if not np.can_cast(np.array(val),dtype,casting=casting): raise ValueError(f'Unable to cast the value {val} to {str(dtype)} (using "{casting}" casting).')
                # print(f'{fq}: casting {val} to {str(dtype)} is okay.')
                if self.row is None: self.ctx.dataset[fq]=val
                else:
                    # this should cover h5py.vlen_dtype and h5py.string_dtype (with variable length only)
                    if dtype.kind=='O': 
                        # workaround for a bug in h5py: for variable-length fields, read the row, modify, write back
                        # see https://stackoverflow.com/q/67192725/761090
                        rowdata=self.ctx.dataset[self.row]
                        rowdata[self.ctx.dataset.dtype.names.index(fq)]=val
                        self.ctx.dataset[self.row]=rowdata
                    else: self.ctx.dataset[self.row,fq]=val   
            meth['get'+capitalize(key)]=getter
            meth['set'+capitalize(key)]=setter
        elif 'path' in val:
            path,schema=val['path'],val['schema']
            for s in ('{ROW}','/'):
                if s not in path:
                    raise ValueError(f"'{fq}': schema ref path '{path}' does not contain '{s}'.")
            def subschemaGetter(self,row=None,*,fq=fq,path=path,schema=schema):
                rr=[self.row is None,row is None]
                if sum(rr)==2: raise AttributeError(f"'{fq}': row index not set (or given as arg), unable to follow schema ref.")
                if sum(rr)==0: raise AttributeError(f"'{fq}': row given both as index ({self.row}) and arg ({row}).")
                if row is None: row=self.row
                #_T_assertDataset(self,f"when accessing subschema '{path}'.")
                #self.ctx.dataset[self.row] # catch invalid row index, data unused
                #print(f"{fq}: getting {path}")
                path=path.replace('{ROW}',str(row))
                dir,name=path.rsplit('/',1)
                subgrp=self.ctx.h5group.require_group(dir)
                SchemaT=self.ctx.schemaRegistry[schema]
                ret=SchemaT(RootContext(h5group=subgrp,h5name=name,schemaRegistry=self.ctx.schemaRegistry),row=None)
                if hasattr(self,'_pyroDaemon'): self._pyroDaemon.register(ret)
                # print(f"{fq}: schema is {SchemaT}, returning: {ret}.")
                return ret
            ret.doc+=[docHead+f': nested data at `{path}`, schema `{schema}`.']
            meth['get'+capitalize(key)]=subschemaGetter
        else:
            # recurse
            ret.doc+=[docHead,''] # empty line for nesting in restructured text
            cooked=_cookSchema(val,prefix=fq,schemaName=schemaName,fakeModule=fakeModule)
            ret.append(cooked)
            def nestedGetter(self,*,T=cooked.T):
                ret=T(self)
                if hasattr(self,'_pyroDaemon'): self._pyroDaemon.register(ret)
                return ret
            meth['get'+capitalize(key)]=nestedGetter # lambda self, T=cooked.T: T(self)
    # define common methods for the context type
    def T_init(self,other=None,row=None,baseClass=None,**kw):
        'Context constructor; copies h5 context and row from *other*, optionally sets *row* as well'
        # print(self.__class__.__bases__)
        for B in self.__class__.__bases__: B.__init__(self,**kw)
        if isinstance(other,RootContext):
            self.ctx,self.row=other,row
            # print(f"[ROOT] {self}, other={other}")
        else:
            if other.row is not None and row is not None: raise IndexError(f'Context already indexed, with row={row}.')
            self.ctx,self.row=other.ctx,(other.row if row is None else row)
            # print(f"[LEAF] {self}, other={other}")
    def T_str(self):
        'Context string representation'
        return F"<{self.__class__.__name__}, row={self.row}, ctx={self.ctx}>"
    def T_getitem(self,row):
        'Indexing access; checks index validity and returns new context with the row set'
        _T_assertDataset(self,msg=f'when trying to index row {row}')
        if(row<0 or row>=self.ctx.dataset.shape[0]): raise IndexError(f"{fq}: row index {row} out of range 0…{self.ctx.dataset.shape[0]}.")
        # self.ctx.dataset[row] # this would raise ValueError but iteration protocol needs IndexError
        # print(f'Item #{row}: returning {self.__class__(self,row=row)}')
        ret=self.__class__(self,row=row)
        if hasattr(self,'_pyroDaemon'): self._pyroDaemon.register(ret)
        return ret
    def T_len(self):
        'Return sequence length'
        _T_assertDataset(self,msg=f'querying dataset length')
        if self.row is not None: return IndexError('Row index already set, not behaving as sequence.')
        return self.ctx.dataset.shape[0]
    def _T_assertDataset(T,msg=''):
        'checks that the backing dataset it present/open. Raises exception otherwise.'
        if T.ctx.dataset is None:
            if T.ctx.h5name in T.ctx.h5group: T.ctx.dataset=T.ctx.h5group[T.ctx.h5name]
            else: raise RuntimeError(f'Dataset not yet initialized, use _allocate first{" ("+msg+")" if msg else ""}.')
    def T_allocate(self,size):
        'allocates the backing dataset, setting them to default values.'
        if self.ctx.dataset: raise RuntimeError(f'Dataset already exists (shape {self._values.shape}), re-allocation not supported.')
        self.ctx.dataset=self.ctx.h5group.create_dataset(self.ctx.h5name,shape=(size,),dtype=ret.dtypes,compression='gzip')
        # FIXME: default scalar should broadcast to all rows, but does not (see subdtype above)
        for fq,val in ret.defaults.items():
            # sys.stderr.write(f'{fq}: setting default value of {val}\n')
            self.ctx.dataset[fq]=val
        # TODO: store schema JSON into dataset attributes
    def T_iter(self):
        _T_assertDataset(self,msg=f'when iterating')
        for row in range(self.ctx.dataset.shape[0]): yield self[row]

    meth['__init__']=T_init
    meth['__str__']=meth['__repr__']=T_str
    meth['__getitem__']=T_getitem
    meth['__len__']=T_len
    meth['row']=None
    meth['ctx']=None
    # pydantic needs this
    #meth['__annotations__']=dict(row=typing.Optional[int],ctx=typing.Any)
    #meth['__fields_set__']=set()


    # those are defined only for the "root" context
    if not prefix:
        meth['allocate']=T_allocate
        ret.dtypes=np.dtype(ret.dtypes)
        T_bases=()
    else:
        T_bases=() # only top-level has metadata

    T=type(T_name,T_bases,meth)
    T.__module__=fakeModule.__name__ ## make the (T.__module__,T.__name__) tuple used in serialization unique
    T=Pyro5.api.expose(T)
    setattr(fakeModule,T_name,T)

    # FIXME: this is misplaced
    # Pyro5.api.register_class_to_dict(T,dumpable.Dumpable.to_dict)
    # Pyro5.api.register_dict_to_class(T.__module__+'.'+T.__name__,dumpable.Dumpable.from_dict_with_name)

    if not prefix:
        T.name=schemaName # schema knows its own name, for convenience of creating schema registry
        T.__doc__='\n'.join(ret.doc)+'\n'
        # pydantic defines __iter__; it cannot be deleted, thus we have to redefine instead
        # T.__iter__=T_iter
        return T
    else:
        ret.T=T
        return ret

@dataclass
@Pyro5.api.expose
class RootContext():
    h5group: Any
    h5name: str
    schemaRegistry: dict
    dataset: Any=None

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
        grp=h5.require_group('grains')
        grp.attrs['schemas']=sampleSchemas_json
        grp.attrs['schema']='grain'
        grains=schemaRegistry['grain'](RootContext(h5group=grp,h5name='grains',schemaRegistry=schemaRegistry))
        grains.allocate(size=5)
        print(f"There is {len(grains)} grains.")
        for ig,g in enumerate(grains):
            #g=grains[ig]
            print('grain',ig,g)
            g.getMolecules().allocate(size=random.randint(5,50))
            print(f"Grain #{ig} has {len(g.getMolecules())} molecules")
            for m in g.getMolecules():
                #for im in range(len(g.getMolecules())):
                #m=g.getMolecules()[im]
                # print('molecule: ',m)
                m.getIdentity().setMolecularWeight(random.randint(1,10)*u.yg)
                m.getAtoms().allocate(size=random.randint(30,60))
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
        grp=h5['grains']
        schemaRegistry=makeSchemaRegistry(json.loads(grp.attrs['schemas']))
        grains=schemaRegistry[grp.attrs['schema']](RootContext(h5group=grp,h5name='grains',schemaRegistry=schemaRegistry))
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
    h5path: str
    h5group: str
    h5uri: typing.Optional[str]=None
    def getSchemaRegistry(self,compile=False):
        'Return schema registry as JSON string'
        self._openRead()
        ssh=self._h5obj[self.h5group].attrs['schemas']
        return ssh if not compile else makeSchemaRegistry(json.loads(ssh))
    def _returnProxy(self,v):
        if hasattr(self,'_pyroDaemon'): self._pyroDaemon.register(v)
        return v
    def _openRead(self):
        if self._h5obj is None: self._h5obj=h5py.File(self.h5path,'r')
    def readRoot(self):
        self._openRead()
        grp=self._h5obj[self.h5group]
        schemaRegistry=makeSchemaRegistry(json.loads(grp.attrs['schemas']))
        h5name=self.h5group.rsplit('/',1)[-1]
        root=schemaRegistry[grp.attrs['schema']](RootContext(h5group=grp,h5name=h5name,schemaRegistry=schemaRegistry))
        # sys.stderr.write(f'root: {root}\n')
        return self._returnProxy(root)
    def makeRoot(self,*,schema,schemasJson):
        if self._h5obj: raise RuntimeError(f'Backing storage {self._h5obj} already open.')
        self._h5obj=h5py.File(self.h5path,'w')
        grp=self._h5obj.require_group(self.h5group)
        grp.attrs['schemas']=schemasJson
        grp.attrs['schema']=schema
        h5name=self.h5group.rsplit('/',1)[-1]
        schemaRegistry=makeSchemaRegistry(json.loads(schemasJson))
        root=schemaRegistry[grp.attrs['schema']](RootContext(h5group=grp,h5name=h5name,schemaRegistry=schemaRegistry))
        return self._returnProxy(root)
    def exposeData(self):
        if (daemon:=getattr(self,'_pyroDaemon',None)) is None: raise RuntimeError(f'{self.__class__.__name__} not registered in a Pyro5.api.Daemon.')
        if self.h5uri: return # already exposed
        # binary mode is necessary!
        # otherwise: remote UnicodeDecodeError somewhere, and then 
        # TypeError: a bytes-like object is required, not 'dict'
        self.h5uri=str(daemon.register(pyrofile.PyroFile(self.h5path,mode='rb')))
    def __init__(self,**kw):
        super().__init__(**kw) # this calls the real ctor
        #sys.stderr.write(f'{self.__class__.__name__}.__init__(**kw={str(kw)})\n')
        #import traceback
        #traceback.print_stack(file=sys.stderr)
        self._h5obj=None
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

import h5py
h5py.Group.__getstate__=lambda *args, **kw: None

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
    # print(json.dumps(json.loads(sampleSchemas_json),indent=2))
    #_make_grains('/tmp/grains.h5')
    #_read_grains('/tmp/grains.h5')

    # this won't work through Pyro yet
    pp=HeavyDataHandle(h5path='/tmp/grains.h5',h5group='grains')
    for key,val in pp.getSchemaRegistry(compile=True).items():
        print(val.__doc__.replace('`','``'))
    root=pp.readRoot()
    print(pp.readRoot()[0].getMolecules())
    print(root.getMolecules(0).getAtoms(5).getIdentity().getElement())
    print(root[0].getMolecules()[5].getAtoms().getIdentity().getElement())


