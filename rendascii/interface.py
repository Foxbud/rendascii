"""
TBA.
"""


from rendascii import pipeline
from rendascii.geometry import matrix3d
from rendascii.geometry import X, Y
from rendascii.resource import generate_camera_fragments
from rendascii.resource import load_color_texture_map, load_mesh


class Engine:

  def __init__(self, camera_size, camera_resolution, camera_focal_distance):
    # Initialize instance attributes.
    self._colormap = None
    self._models = {}
    self._model_instances = []
    # Camera.
    self._camera_size = camera_size
    self._camera_resolution = camera_resolution
    self._camera_orientation_rev = (0.0, 0.0, 0.0,)
    self._camera_angle_order_rev = 'yzx'
    self._camera_position_rev = (0.0, 0.0, 0.0,)
    self._camera_focus = (0.0, 0.0, -camera_focal_distance,)
    self._camera_fragments = sum(
        generate_camera_fragments(
          camera_size[X],
          camera_size[Y],
          camera_resolution[X],
          camera_resolution[Y]
          ),
        ()
        )

  def load_colormap(self, colormap_name, resource_dir=''):
    self._colormap = load_color_texture_map(colormap_name, resource_dir)

  def load_model(self, model_name, objmesh_name, resource_dir=''):
    self._models[model_name] = load_mesh(objmesh_name, resource_dir)

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
        if instance._model_name != model_name
        ]

  def render_frame(self):
    return (
        pipeline.stage_five(
          pipeline.stage_four(
            *pipeline.stage_three(
              *pipeline.stage_two(
                *pipeline.stage_one(
                  *self._seed_pipeline()
                  )
                )
              )
            )
          )
        )

  def _seed_pipeline(self):
    out_vertex_data = []
    out_geometry_data = []
    cam_rot_matrix = matrix3d.generate_rotation_matrix(
        self._camera_orientation_rev,
        self._camera_angle_order_rev
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
              self._camera_focus,
              cam_rot_matrix,
              self._camera_position_rev,
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
        in self._camera_fragments
        )

    return out_vertex_data, out_geometry_data, out_fragment_data


class ModelInstance:

  def __init__(self, model_name):
    # Initialize instance attributes.
    self._model_name = model_name
    self._scale = 1.0
    self._orientation = (0.0, 0.0, 0.0,)
    self._angle_order = 'xzy'
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )
    self._position = (0.0, 0.0, 0.0,)
    self._hidden = False

  def update_scale(self, scale):
    self._scale = scale

  def update_orientation(self, orientation, angle_order='xzy'):
    self._orientation = orientation
    self._angle_order = angle_order
    self._rot_matrix = matrix3d.generate_rotation_matrix(
        self._orientation,
        self._angle_order
        )

  def update_position(self, position):
    self._position = position

  def hide(self):
    self._hidden = True

  def unhide(self):
    self._hidden = False
