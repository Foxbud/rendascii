"""
TBA.
"""

import math
from multiprocessing import Pool
from rendascii import resource
from rendascii.geometry import matrix, vec3d
from rendascii.geometry import X, Y
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
    self._colormap_dir = colormap_dir
    self._sprite_dir = sprite_dir
    self._model_dir = model_dir
    self._material_dir = material_dir
    self._workers = Pool(num_workers) if num_workers > 0 else None

  def create_camera(
      self,
      resolution,
      near=1.0,
      far=11.0,
      fov=math.radians(70),
      ratio=1.0
      ):
    camera = Camera(resolution, near, far, fov, ratio)
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

  def load_model(self, model_name, model_filename):
    self._models[model_name] = resource.load_model(
        model_filename,
        self._model_dir,
        self._material_dir
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

  def render_frame(self, camera, overlay=None):
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

    # Outpack output data.
    (
        workers,
        out_vertex_data,
        out_polygon_data,
        out_sprite_data,
        out_fragment_data
        ) = out_data

    # Reshape fragment data to camera resolution.
    structured_fragment_data = tuple(
        tuple(
          out_fragment_data[y * camera._resolution[X] + x][0]
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

  def _seed_pipeline(self, camera, overlay):
    # Declare output data.
    out_vertex_data = []
    out_polygon_data = []
    out_sprite_data = []
    out_fragment_data = []

    # Create model instances.
    for instance in self._model_instances:
      if not instance._hidden:
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
            ) = self._models[instance._model_name]
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
              )
            for polygon
            in range(len(polygons))
            ]

    # Create sprite instances.
    for instance in self._sprite_instances:
      if not instance._hidden:
        part_transformation = matrix.compose(
            camera._transformation,
            instance._transformation
            )
        colormap = self._colormaps[instance._colormap_name]

        # Unpack sprite data.
        (
            sprite
            ) = self._sprites[instance._sprite_name]

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
              ),
            ]

    # Pack fragment data.
    out_fragment_data += [
        (
          overlay[fragment],
          camera._fragments[fragment],
          )
        for fragment
        in range(len(camera._fragments))
        ]

    return (
        self._workers,
        tuple(out_vertex_data),
        tuple(out_polygon_data),
        tuple(out_sprite_data),
        tuple(out_fragment_data),
        )


class Camera:

  def __init__(self, resolution, near, far, fov, ratio):
    # Initialize instance attributes.
    self._resolution = resolution
    self._near = near
    self._far = far
    self._fov = fov
    self._ratio = ratio
    self._projection = matrix.projection_3d(near, far, fov, ratio)
    self._fragments = sum(
        resource.generate_camera_fragments(resolution),
        ()
        )
    self._transformation = matrix.IDENTITY_3D

  def set_transformation(self, transformation):
    self._transformation = transformation


class SpriteInstance:

  def __init__(self, sprite_name, colormap_name):
    # Initialize instance attributes.
    self._sprite_name = sprite_name
    self._colormap_name = colormap_name
    self._transformation = matrix.IDENTITY_3D
    self._hidden = False

  def set_colormap(self, colormap_name):
    self._colormap_name = colormap_name

  def set_transformation(self, transformation):
    self._transformation = transformation

  def hide(self):
    self._hidden = True

  def unhide(self):
    self._hidden = False


class ModelInstance:

  def __init__(self, model_name, colormap_name):
    # Initialize instance attributes.
    self._model_name = model_name
    self._colormap_name = colormap_name
    self._transformation = matrix.IDENTITY_3D
    self._hidden = False

  def set_colormap(self, colormap_name):
    self._colormap_name = colormap_name

  def set_transformation(self, transformation):
    self._transformation = transformation

  def hide(self):
    self._hidden = True

  def unhide(self):
    self._hidden = False
