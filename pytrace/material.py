# <<Description Here>>
#
# Module : $File$
# Author : $Author$
# Version: $Version$
# Status : $Status$
#
# Copyright (C) 2002 Brian Hammond. All Rights Reserved

from pytrace.color import RGB, RGBA

class Material(object):
  _num_materials=1
  
  def __init__(self, diffuse=RGB(1,1,1), Kd=1.0, specular=RGB(1,1,1), Ks=0.0, 
    shininess=8.0, Kt=0.0, ior=1.0, name=None):
    """
    diffuse      - diffuse color (RGB)
    Kd           - diffuse intensity [0,1]
    specular     - specular color (RGB)
    Ks           - specular intensity [0,1]
    shininess    - specular falloff; lower values means higher spreading out
                   of specular highlight.
    Kt           - How transmissive the material is. Clear glass is fully 
                   transmissive.  Stained glass only so much so. [0,1]
    ior          - Index of refraction

    Examples of IOR:
      Vacuum      1.0
      Air         1.00029
      Ice         1.31
      Water       1.33
      Crown Glass 1.5
      Flint Glass 1.65
      Sapphire    1.77
      Diamond     2.42
    """
    
    if name is None:
      name = "Material %d" % Material._num_materials
    
    Material._num_materials += 1
    
    self.name = name
    self.diffuse = diffuse
    self.Kd = Kd
    self.specular = specular
    self.Ks = Ks
    self.shininess = shininess
    self.Kt = Kt
    self.ior = ior

  def reflective(self):
    return self.Ks > 0.0

  def transmissive(self):
    return self.Kt > 0.0

  def __str__(self):
    return "Material \"%s\" diffuse=%s Kd=%.2f specular=%s Ks=%.2f " \
           "shininess=%.2f Kt=%.2f IoR=%.2f" % \
           (self.name, self.diffuse, self.Kd, self.specular, self.Ks,
            self.shininess, self.Kt, self.ior)

DEFAULT_MATERIAL = Material('DefaultMaterial')

