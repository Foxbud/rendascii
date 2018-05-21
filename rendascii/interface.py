"""
TBA.
"""


from rendascii.geometry import matrix3d
from rendascii.geometry import X, Y
from rendascii.resources import generate_camera_fragments


class Engine:

  def __init__(self, camera_scale, camera_resolution):
    # Initialize instance attributes.
    # Camera.
    self._camera_scale = camera_scale
    self._camera_orientation = (0.0, 0.0, 0.0)
    self._camera_angle_order = 'xzy'
    self._camera_rot_matrix = matrix3d.generate_rotation_matrix(
        self._camera_orientation,
        self._camera_angle_order
        )
    self._camera_position = (0.0, 0.0, 0.0)
    self._camera_fragments = generate_camera_fragments(
        camera_scale[X],
        camera_scale[Y],
        camera_resolution[X],
        camera_resolution[Y]
        )
    # Static.
    self._models = {}
    self._model_instances = []
    # Pipeline - Stage 1.
    self._verts_model_space = []
    self._vert_world_scales = []
    self._vert_world_orientations = []
    self._vert_world_positions = []
    self._polygons_world_space = []
    self._textures_world_space = []
    self._normals_world_space = []
    self._normal_world_orientations = []
    # Pipeline - Stage 2.
    self._verts_world_space = []
    self._vert_camera_offsets = []
    self._vert_camera_orientations = []
    self._normals_world_space = []
    self._normal_camera_orientations = []
    # Pipeline - Stage 2.
    self._verts_camera_space = []
    self._normals_camera_space = []
    # Pipeline - Stage 3.
    self._verts_projected = []
    self._vert_depths = []
    self._polygons_projected = []
    self._textures_projected = []
    self._aabbs_projected = []
    # Pipeline - Stage 4.
    self._pixel_fragments


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
