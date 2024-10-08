import unittest,sys
sys.path.append('../..')

from mupif import *
import mupif
import tempfile
from mupif.tests import demo

tstep = timestep.TimeStep(time=0., dt=1., targetTime=1., unit=mupif.U.s)


# check for python-vtk before running related tests
try:
    import vtk
    vtkAvailable=True
except ImportError:
    vtkAvailable=False


class TestSaveLoad(unittest.TestCase):
    def setUp(self):
        self.app1=demo.AppGridAvg()
        #register assertEqual operation for physicalquantities
        # self.addTypeEqualityFunc(PQ.PhysicalQuantity, self.assertphysicalquantitiesEqual)

        self.tmpdir=tempfile.TemporaryDirectory()
        self.tmp=self.tmpdir.name

    def tearDown(self):
        self.tmpdir.cleanup()


    # unit tests support
    def assertphysicalquantitiesEqual (self, first, second, msg=None):
        if not first.__cmp__(second):
            raise self.failureException('%s != %s: %s'%(first,second,msg))

    @unittest.skip('Does not work currently')
    def testFieldDictDump(self):
        f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
        t22a=f.evaluate((2.0,2.0,0.)).getValue()[0] # temperature at (2,2)
        dic=f.to_dict()
        if 1:
            import pprint
            pprint.pprint(dict([(k,v) if len(str(v))<1000 else (k,'<too long to show>') for k,v in dic.items()]))
        f2=mupif.data.Data.from_dict(dic)
        t22b=f2.evaluate((2.,2.,0.)).getValue()[0]
        self.assert_(not id(f)==id(f2))
        self.assertAlmostEqual(t22a,t22b)
        self.assertEqual(f.unit,f2.unit)

    def _disabled_testFieldSerpent(self):
        f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
        t22a=f.evaluate((2.0,2.0,0.)).getValue()[0] # temperature at (2,2)
        import serpent
        dump=serpent.dumps(f)
        if 0:
            import pprint
            print(type(dump))
            pprint.pprint(dict([(k,v) if len(str(v))<1000 else (k,'<too long to show>') for k,v in dump.items()]))
        f2=serpent.loads(dump)
        t22b=f2.evaluate((2.,2.,0.)).getValue()[0]
        self.assert_(not id(f)==id(f2))
        self.assertAlmostEqual(t22a,t22b)
        self.assertEqual(f.unit,f2.unit)

    def testFieldPickle(self):
        # get field from the app
        f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
        t22a=f.evaluate((2.0,2.0,0.)).getValue()[0] # temperature at (2,2)
        import pickle
        p=pickle.dumps(f)
        f2=pickle.loads(p)
        t22b=f2.evaluate((2.,2.,0.)).getValue()[0]
        self.assertTrue(not id(f)==id(f2))
        self.assertAlmostEqual(t22a,t22b)
    def testFieldHdf5SaveLoad(self):
        f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
        v=self.tmp+'/aa2.h5'
        f.toHdf5(fileName=v)
        ff2=mupif.field.Field.makeFromHdf5(fileName=v)
        self.assertEqual(len(ff2),1)
        f2=ff2[0]
        self.assertEqual(f.getMesh().dataDigest(),f2.getMesh().dataDigest())

    if 0:
        @unittest.skipUnless(vtkAvailable,'vtk (python-vtk/python-vtk6) not importable') # vtkAvailable defined above
        def testFieldVtk3SaveLoad(self):
            f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
            v=self.tmp+'/aa.vtu'
            f.toVTK3(v)
            ff2=mupif.field.Field.makeFromVTK3(v, f.getUnits())
            self.assertEqual(len(ff2),1)
            f2=ff2[0]
            # just compare coordinates of the first point
            self.assertEqual(f.getMesh().getVertex(0).getCoordinates(),f2.getMesh().getVertex(0).getCoordinates())
            # data hash comparison is too strict and fails
            # as tried, however, saving to VTK again yields byte-to-byte identical .vtu
            ## self.assertEqual(f.getMesh().internalArraysDigest(),f2.getMesh().internalArraysDigest())
        def _testFieldVtk2SaveLoad(self,format):
            f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
            v=self.tmp+'/aa.vtk'
            f.toVTK2(v,format=format)
            ff2=mupif.field.Field.makeFromVTK2(v, f.getUnits())
            self.assertEqual(len(ff2),1)
            f2=ff2[0]
            # just compare coordinates of the first point
            self.assertEqual(f.getMesh().getVertex(0).getCoordinates(),f2.getMesh().getVertex(0).getCoordinates())
        def testFieldVtk2SaveLoad_ascii(self):
            self._testFieldVtk2SaveLoad(format='ascii')
        @unittest.skipUnless(vtkAvailable,'Reading binary not supported by pyvtk, vtk (python-vtk/python-vtk6) would be used transparently instead but is not importable.') # vtkAvailable defined above
        def testFieldVtk2SaveLoad_binary(self):
            self._testFieldVtk2SaveLoad(format='binary')

    def testOctreeNotPickled(self):
        f=self.app1.get(mupif.DataID.FID_Temperature,tstep.getTime())
        import pickle
        m=f.getMesh()
        # this creates localizers on-request
        m.getVertexLocalizer()
        m.getCellLocalizer()
        # check localizers are there (break encapsulation, sorry)
        self.assertTrue(m._vertexOctree is not None)
        self.assertTrue(m._cellOctree is not None)
        # but that they were not pickled
        m2=pickle.loads(pickle.dumps(m))
        print(m._vertexOctree,m2._vertexOctree)
        self.assertTrue(m2._vertexOctree is None)
        self.assertTrue(m2._cellOctree is None)
        
        



