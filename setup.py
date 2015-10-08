'''
Created 19.6.2015
@author: Vit Smilauer
'''

# A typical workflow
# $ python setup.py install       test your installation locally as a root as it would be downloaded from PyPI server
# $ python setup.py install --user   test your installation locally as a user, installs under /home/user/.local/lib/
# $ python setup.py sdist         creates an archive on local computer
# $ python setup.py register      registers to PyPI server
# $ python setup.py sdist upload  creates an archive on local computer and upload to PyPI server

# The mupif module can be tested under python $ python   and  >> from mupif import * . Correct path is automatically added.
# Uninstall with $ pip uninstall mupif . This also shows you the location of files.

# Alternatively, without default path, $ pip install --user dist/mupif-0.1.tar.gz
# See also https://bashelton.com/2009/04/setuptools-tutorial/#setup.py-package_dir
# See also https://docs.python.org/2/distutils/setupscript.html

import sys
import os
import re

from setuptools import setup, find_packages

inFile = open("mupif/__init__.py")
for line in inFile:
    if line.startswith('__version__'):
        #version = line.split()[2]
        version = re.findall(r'\'(.+?)\'', line)
    #print version[0]
    elif line.startswith('__author__'):
        author = re.findall(r'\'(.+?)\'', line)
        #print author[0]
inFile.close()

setup(name='mupif',
      version=version[0],
      description='Mupif platform for multiscale/multiphysics modeling',
      license='LGPL',
      author=author[0],
      author_email='info@oofem.org',
      #package_dir={'': 'mupif'},#this looks where to find __init__.py
      packages = find_packages(),
      #packages = ['mupif'],
        #Tell what to install (these files must be already in a sdist archive file) - package_data useful only for bdist, not for pip. Extra added files are in MANIFEST.in
      #package_data={'': [ 'README', '*.sh', '*.c', '*.in', 'tools/*.py', 'examples/Ex*/*.py', 'examples/Pi*/*.py', 'examples/Workshop02/*.py', 'doc/refManual/MuPIF.pdf', 'doc/userGuide/MuPIF-userGuide.pdf' ]},
      install_requires=['numpy', 'scipy', 'setuptools', 'pyvtk', 'config', 'future>=0.15', 'Pyro4==4.39'],
      include_package_data=True,
      url='http://sourceforge.net/projects/mupif/',
	  entry_points={
          'console_scripts': ['jobMan2cmd = mupif.tools.JobMan2cmd:main',
                              'jobManStatus = mupif.tools.jobManStatus:main',
                              'jobManTest = mupif.tools.jobManTest:main',
                              'startMupifNameserver = mupif.tools.nameserver:main']
      }
      )

