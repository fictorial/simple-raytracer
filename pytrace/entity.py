class Entity(object):
  _num_ents = 1
  def __init__(self, name = None):
    if name is None:
      name = "Entity %d" % Entity._num_ents
    self.name = name
    Entity._num_ents += 1
