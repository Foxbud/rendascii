"""
TBA.
"""


from rendascii.geometry import matrix3d


class Engine:

  def __init__(self):
    # Initialize instance attributes.
    self._models = {}
    self._verts_model_space = []
    self._verts_world_space = []
    self._verts_camera_space = []
    self._verts_projected = []


class ModelInstance:

  def __init__(self, model_name):
    # Initialize instance attributes.
    self._model_name = model_name
    self._scale = tuple(0.0, 0.0, 0.0)
    self._orientation = tuple(0.0, 0.0, 0.0)
    self._angle_order = 'xzy'
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )
    self._position = tuple(0.0, 0.0, 0.0)
    self._hidden = False

  def update_scale(self, scale):
    self._scale = scale

    # Return self for convenience.
    return self

  def update_orientation(self, orientation, angle_order='xzy'):
    self._orientation = orientation
    self._angle_order = angle_order
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )

    # Return self for convenience.
    return self

  def update_position(self, position):
    self._position = position

    # Return self for convenience.
    return self

  def hide(self):
    self._hidden = True

    # Return self for convenience.
    return self

  def unhide(self):
    self.hidden = False

    # Return self for convenience.
    return self
