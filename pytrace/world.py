from pytrace.entity import Entity
from pytrace.color  import RGB

class WorldError(RuntimeError):
  "Invalid world configuration"

class World(Entity):
  _num_worlds=1
  
  def __init__(self, name=None):
    if name is None:
      name = "World %d" % World._num_worlds
    Entity.__init__(self, name)
    World._num_worlds += 1
    self.entities = []
    self.primitives = []
    self.lights = []
    self.cameras = []
    self.active_camera = None
    self.materials = []
    self.bgcolor = RGB(0.33, 0.33, 0.33)
    self.ambient = RGB(0.33, 0.33, 0.33)
    
  def validate(self):
    if self.active_camera is None:
      if len(self.cameras) == 0:
        raise WorldError("no cameras defined")
      world.active_camera = world.cameras[0]

    if len(self.lights)==0:
      raise WorldError("no lights defined")
  
    if len(self.primitives)==0:
      raise WorldError("no primitives defined")
    
  def __str__(self):
    s = "World: '%s'\n" % self.name
    
    s += "PRIMITIVES =============\n"
    for p in self.primitives:
      s += str(p) + "\n"
    
    s += "LIGHTS ===============\n"
    for l in self.lights:
      s += str(l) + "\n"
      
    s += "CAMERAS ==============\n"
    for c in self.cameras:
      s += str(c) + "\n"
    
    s += "MATERIALS ============\n"
    for m in self.materials:
      s += str(m) + "\n"
    
    return s

