"""
TBA.
"""

from rendascii import pipeline
from rendascii import resource
from rendascii.geometry import matrix3d, vec3d
from rendascii.geometry import DEFAULT_ANGLE_ORDER
from rendascii.geometry import X, Y


class Engine:

  def __init__(self):
    # Initialize instance attributes.
    self._cameras = []
    self._colormap = None
    self._models = {}
    self._model_instances = []

  def create_camera(self, resolution, size=(1.0, 1.0,), focal_distance=1.0):
    camera = Camera(resolution, size, focal_distance)
    self._cameras.append(camera)
    return camera

  def delete_camera(self, camera):
    self._cameras = [
        next_camera
        for next_camera 
        in self._cameras
        if next_camera is not camera
        ]

  def load_colormap(self, colormap_name, resource_dir=''):
    self._colormap = resource.load_color_texture_map(
        colormap_name,
        resource_dir
        )

  def load_model(self, model_name, objmesh_name, resource_dir=''):
    self._models[model_name] = resource.load_mesh(
        objmesh_name,
        resource_dir
        )

  def unload_model(self, model_name):
    self._model_instances = [
        instance
        for instance
        in self._model_instances
        if instance._model_name != model_name
        ]
    del self._models[model_name]

  def create_model_instance(self, model_name):
    model_instance = ModelInstance(model_name)
    self._model_instances.append(model_instance)
    return model_instance

  def delete_model_instance(self, model_instance):
    self._model_instances = [
        instance
        for instance
        in self._model_instances
        if instance is not model_instance
        ]

  def render_frame(self, camera):
    # Pass data through pipeline to generate pixel fragments.
    fragment_data = (
        pipeline.stage_five(
          pipeline.stage_four(
            *pipeline.stage_three(
              *pipeline.stage_two(
                *pipeline.stage_one(
                  *self._seed_pipeline(camera)
                  )
                )
              )
            )
          )
        )

    # Reshape fragment data to camera resolution.
    structured_fragment_data = tuple(
        tuple(
          fragment_data[y * camera._resolution[X] + x][0]
          for x
          in range(camera._resolution[X])
          )
        for y
        in range(camera._resolution[Y])
        )

    # Convert structured fragment data into string.
    return '\n'.join(
        tuple(
          ''.join(row)
          for row
          in structured_fragment_data[::-1]
          )
        )

  def _seed_pipeline(self, camera):
    out_vertex_data = []
    out_geometry_data = []
    # Change active camera transformations to passive.
    cam_orientation = vec3d.negate(camera._orientation[::-1])
    cam_angle_order = camera._angle_order[::-1]
    cam_position = vec3d.negate(camera._position)
    cam_rot_matrix = matrix3d.generate_rotation_matrix(
        cam_orientation,
        cam_angle_order
        )
    for instance in self._model_instances:
      if not instance._hidden:
        inst_rot_matrix = matrix3d.generate_rotation_matrix(
            instance._orientation,
            instance._angle_order
            )
        vertices, polygons, normals, colors = (
            self._models[instance._model_name]
            )
        vert_offset = len(out_vertex_data)

        # Pack vertex data.
        out_vertex_data += tuple(
            (
              vertex,
              camera._focal_point,
              cam_rot_matrix,
              cam_position,
              instance._position,
              inst_rot_matrix,
              instance._scale,
              )
            for vertex
            in vertices
            )

        # Pack polygon data.
        out_geometry_data += tuple(
            (
              (
                polygons[polygon][0] + vert_offset,
                polygons[polygon][1] + vert_offset,
                polygons[polygon][2] + vert_offset,
                ),
              self._colormap[colors[polygon]],
              normals[polygon],
              cam_rot_matrix,
              inst_rot_matrix,
              )
            for polygon
            in range(len(polygons))
            )

    # Pack fragment data.
    out_fragment_data = tuple(
        (
          fragment,
          )
        for fragment
        in camera._fragments
        )

    return out_vertex_data, out_geometry_data, out_fragment_data


class Camera:

  def __init__(self, resolution, size, focal_distance):
    # Initialize instance attributes.
    self._resolution = resolution
    self._size = size
    self._focal_point = (0.0, 0.0, -focal_distance,)
    self._fragments = sum(
        resource.generate_camera_fragments(
          self._size[X],
          self._size[Y],
          self._resolution[X],
          self._resolution[Y]
          ),
        ()
        )
    self._orientation = (0.0, 0.0, 0.0,)
    self._angle_order = DEFAULT_ANGLE_ORDER
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )
    self._position = (0.0, 0.0, 0.0,)

  def set_orientation(self, orientation, angle_order=DEFAULT_ANGLE_ORDER):
    self._orientation = orientation
    self._angle_order = angle_order
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )

  def set_position(self, position):
    self._position = position


class ModelInstance:

  def __init__(self, model_name):
    # Initialize instance attributes.
    self._model_name = model_name
    self._scale = 1.0
    self._orientation = (0.0, 0.0, 0.0,)
    self._angle_order = DEFAULT_ANGLE_ORDER
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )
    self._position = (0.0, 0.0, 0.0,)
    self._hidden = False

  def set_scale(self, scale):
    self._scale = scale

  def set_orientation(self, orientation, angle_order=DEFAULT_ANGLE_ORDER):
    self._orientation = orientation
    self._angle_order = angle_order
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )

  def set_position(self, position):
    self._position = position

  def hide(self):
    self._hidden = True

  def unhide(self):
    self._hidden = False
