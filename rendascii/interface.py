"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


import math
from multiprocessing import Pool
from rendascii import resource
from rendascii.geometry import X, Y
from rendascii.geometry import matrix
from rendascii.pipeline import stage


class Engine:

  def __init__(
      self,
      colormap_dir='',
      sprite_dir='',
      model_dir='',
      material_dir='',
      num_workers=0
      ):
    # Initialize instance attributes.
    self._cameras = []
    self._colormaps = {}
    self._models = {}
    self._model_instances = []
    self._sprites = {}
    self._sprite_instances = []
    self._colormap_dir = self._format_resource_dir(colormap_dir)
    self._sprite_dir = self._format_resource_dir(sprite_dir)
    self._model_dir = self._format_resource_dir(model_dir)
    self._material_dir = self._format_resource_dir(material_dir)
    self._workers = Pool(num_workers) if num_workers > 0 else None

  def create_camera(
      self,
      resolution,
      near=1.0,
      far=11.0,
      fov=math.radians(70),
      ratio=1.0,
      fog_char=' ',
      culling=True
      ):
    camera = Camera(resolution, near, far, fov, ratio, fog_char, culling)
    self._cameras.append(camera)
    return camera

  def delete_camera(self, camera):
    self._cameras = [
        next_camera
        for next_camera 
        in self._cameras
        if next_camera is not camera
        ]

  def load_colormap(self, colormap_name, colormap_filename):
    self._colormaps[colormap_name] = resource.load_colormap(
        colormap_filename,
        self._colormap_dir
        )

  def unload_colormap(self, colormap_name):
    del self._colormaps[colormap_name]

  def load_sprite(self, sprite_name, sprite_filename):
    self._sprites[sprite_name] = resource.load_sprite(
        sprite_filename,
        self._sprite_dir
        )

  def unload_sprite(self, sprite_name):
    del self._sprites[sprite_name]

  def load_model(self, model_name, model_filename, right_handed=False):
    self._models[model_name] = resource.load_model(
        model_filename,
        self._model_dir,
        self._material_dir,
        right_handed
        )

  def unload_model(self, model_name):
    del self._models[model_name]

  def create_sprite_instance(self, sprite_name, colormap_name):
    sprite_instance = SpriteInstance(sprite_name, colormap_name)
    self._sprite_instances.append(sprite_instance)
    return sprite_instance

  def delete_sprite_instance(self, sprite_instance):
    self._sprite_instances = [
        instance
        for instance
        in self._sprite_instances
        if instance is not sprite_instance
        ]

  def create_model_instance(self, model_name, colormap_name):
    model_instance = ModelInstance(model_name, colormap_name)
    self._model_instances.append(model_instance)
    return model_instance

  def delete_model_instance(self, model_instance):
    self._model_instances = [
        instance
        for instance
        in self._model_instances
        if instance is not model_instance
        ]

  def render_frame(self, camera, overlay=None, as_str=False):
    # Prepare overlay.
    flat_overlay = (
        tuple(
          '\0'
          for fragment
          in range(len(camera._fragments))
          )
        if overlay is None
        else sum(overlay, [])
        if type(overlay[0]) is list
        else sum(overlay, ())
        )

    # Pass data through pipeline to generate pixel fragments.
    out_data = (
        stage.stage_three(
          stage.sync_two(
            stage.stage_two(
              stage.sync_one(
                stage.stage_one(
                  self._seed_pipeline(camera, flat_overlay)
                  )
                )
              )
            )
          )
        )

    # Unpack output data.
    (
        workers,
        out_vertex_data,
        out_polygon_data,
        out_sprite_data,
        out_fragment_data
        ) = out_data

    # Reshape fragment data to camera resolution.
    frame = tuple(
        tuple(
          out_fragment_data[y * camera._resolution[X] + x][0]
          for x
          in range(camera._resolution[X])
          )
        for y
        in range(camera._resolution[Y])
        )

    # Convert frame to printable string if requested.
    if as_str:
      frame = '\n'.join(
          tuple(
            ''.join(
              row
              )
            for row
            in frame[::-1]
            )
          )

    return frame

  def _format_resource_dir(self, resource_dir):
    new_dir = resource_dir
    if len(new_dir) > 0 and new_dir[-1] != '/':
      new_dir += '/'
    return new_dir

  def _seed_pipeline(self, camera, overlay):
    # Create seed data.
    out_vertex_data, out_polygon_data = self._seed_model_instances(camera)
    out_sprite_data = self._seed_sprite_instances(camera)
    out_fragment_data = self._seed_camera_instance(camera, overlay)

    # Pack output data.
    return (
        self._workers,
        out_vertex_data,
        out_polygon_data,
        out_sprite_data,
        out_fragment_data,
        )

  def _seed_model_instances(self, camera):
    # Initialize output data.
    out_vertex_data = []
    out_polygon_data = []

    # Create model instances.
    for instance in self._model_instances:
      if not instance._hidden:
        # Transformation from model to clip space.
        full_transformation = matrix.compose(
            camera._projection,
            matrix.compose(
              camera._transformation,
              instance._transformation
              )
            )
        colormap = self._colormaps[instance._colormap_name]

        # Unpack model data.
        (
            vertices,
            polygons,
            colors
            ) = self._models[instance._resource_name]
        vert_offset = len(out_vertex_data)

        # Pack vertex data.
        out_vertex_data += [
            (
              vertex,
              full_transformation,
              )
            for vertex
            in vertices
            ]

        # Pack polygon data.
        out_polygon_data += [
            (
              (
                polygons[polygon][0] + vert_offset,
                polygons[polygon][1] + vert_offset,
                polygons[polygon][2] + vert_offset,
                ),
              colormap[colors[polygon]],
              camera._view_frustum,
              )
            for polygon
            in range(len(polygons))
            ]

    return tuple(out_vertex_data), tuple(out_polygon_data)

  def _seed_sprite_instances(self, camera):
    # Initialize output data.
    out_sprite_data = []

    # Create sprite instances.
    for instance in self._sprite_instances:
      if not instance._hidden:
        # Transformation from sprite to camera space.
        part_transformation = matrix.compose(
            camera._transformation,
            instance._transformation
            )
        colormap = self._colormaps[instance._colormap_name]

        # Unpack sprite data.
        (
            sprite
            ) = self._sprites[instance._resource_name]

        # Colormap sprite.
        mapped_sprite = tuple(
            tuple(
              colormap[pixel]
              for pixel
              in row
              )
            for row
            in sprite
            )

        # Pack sprite data.
        out_sprite_data += [
            (
              mapped_sprite,
              (0.0, 0.0, 0.0,),
              (0.0, 0.5, 0.0,),
              part_transformation,
              camera._projection,
              camera._ratio,
              camera._view_frustum[:2],
              ),
            ]

    return tuple(out_sprite_data)

  def _seed_camera_instance(self, camera, overlay):
    # Pack fragment data.
    out_fragment_data = tuple(
        (
          camera._fog_char,
          overlay[fragment],
          camera._fragments[fragment],
          )
        for fragment
        in range(len(camera._fragments))
        )

    return out_fragment_data


class Camera:

  def __init__(self, resolution, near, far, fov, ratio, fog_char, culling):
    # Initialize instance attributes.
    self._resolution = resolution
    self._near = near
    self._far = far
    self._fov = fov
    self._ratio = ratio
    self._fog_char = fog_char
    self._projection = matrix.projection_h(near, far, fov, ratio)
    self._fragments = sum(
        self._gen_fragments(resolution),
        ()
        )
    self._transformation = matrix.IDENTITY_H
    self._view_plane_ub = self._gen_view_plane_ub(near, fov, ratio)
    self._view_frustum = [
        # Near plane.
        (
          (0.0, 0.0, 0.0, 0.0,),
          (0.0, 0.0, 1.0, 0.0,),
          ),
        # Far plane.
        (
          (0.0, 0.0, far - near, 0.0,),
          (0.0, 0.0, -1.0, 0.0,),
          ),
        ]
    if culling:
      theta = math.pi / 4.0
      vert_y = math.cos(theta)
      vert_z = math.sin(theta)
      horz_x = vert_y
      horz_z = vert_z
      self._view_frustum += [
          # North plane.
          (
            (0.0, 0.0, -near, 0.0,),
            (0.0, -vert_y, vert_z, 0.0,),
            ),
          # South plane.
          (
            (0.0, 0.0, -near, 0.0,),
            (0.0, vert_y, vert_z, 0.0,),
            ),
          # East plane.
          (
            (0.0, 0.0, -near, 0.0,),
            (-horz_x, 0.0, horz_z, 0.0,),
            ),
          # West plane.
          (
            (0.0, 0.0, -near, 0.0,),
            (horz_x, 0.0, horz_z, 0.0,),
            ),
          ]

  def set_transformation(self, transformation):
    self._transformation = transformation

  def get_view_upper_bound(self):
    return self._view_plane_ub

  def _gen_view_plane_ub(self, near, fov, ratio):
    y_pos = near * math.tan(fov  / 2)

    view_plane_ub = (
        y_pos * ratio,
        y_pos,
        near,
        )

    return view_plane_ub

  def _gen_fragments(self, resolution):
    frag_size = (2 / resolution[X], 2 / resolution[Y],)
  
    fragments = tuple(
        tuple(
          (
            -1 + frag_size[X] * (x + 0.5),
            -1 + frag_size[Y] * (y + 0.5),
            )
          for x
          in range(resolution[X])
          )
        for y
        in range(resolution[Y])
        )
    
    return fragments


class _ResourceInstance:

  def __init__(self, resource_name, colormap_name):
    # Initialize instance attributes.
    self._resource_name = resource_name
    self._colormap_name = colormap_name
    self._transformation = matrix.IDENTITY_H
    self._hidden = False

  def set_colormap(self, colormap_name):
    self._colormap_name = colormap_name

  def set_transformation(self, transformation):
    self._transformation = transformation

  def hide(self):
    self._hidden = True

  def unhide(self):
    self._hidden = False


class SpriteInstance(_ResourceInstance):

  def __init__(self, sprite_name, colormap_name):
    # Initialize instance attributes.
    super().__init__(sprite_name, colormap_name)


class ModelInstance(_ResourceInstance):

  def __init__(self, model_name, colormap_name):
    # Initialize instance attributes.
    super().__init__(model_name, colormap_name)
