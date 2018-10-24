from pytrace.entity import Entity

class Light(Entity):
  _num_lights=1
  
  def __init__(self, pos, color, intensity=1.0, name=None):
    if name is None:
      name = "Light %d" % Light._num_lights
    Entity.__init__(self, name)
    Light._num_lights += 1
    self.pos = pos
    self.color = color
    self.intensity = intensity
  
  def __str__(self):
    return "Light(pos=%s, color=%s, intensity=%.2f name='%s')" % \
    (self.pos, self.color, self.intensity, self.name)
