from distutils.core import setup, Extension

mplane = Extension('plane', 
  libraries=['m'], 
  sources=['plane.c'])

msphere = Extension('sphere', 
  libraries=['m'], 
  sources=['sphere.c'])

setup(name='pytrace', 
  version='1.0', 
  description='intersection routines', 
  ext_modules=[msphere, mplane])

