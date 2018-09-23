"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from rendascii.geometry import matrix, polygon, vector
from rendascii.geometry import PLANE_POINT
from rendascii.geometry import X, Y, Z, W


def s1_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Unpack input packet.
  (
      vertex,
      full_transformation
      ) = in_packet

  # Transform vertex from model to clip space.
  vert_clip = matrix.transform_h(
      full_transformation,
      vector.conv_3d_to_h(
        vertex
        )
      )

  # Create output packet.
  out_packet = (
      vert_clip,
      )

  return out_packet


def s2_polygon_shader(in_packet):
  # Declare output packet.
  out_packet = ()

  # Unpack input packet.
  (
      poly_clip,
      texture,
      view_frustum,
      ) = in_packet

  # Perform back-face culling.
  poly_trunc = tuple(vertex[:W] for vertex in poly_clip)
  direction = vector.dot(
      polygon.normal_3d(
        poly_trunc
        ),
      poly_trunc[0],
      )
  if direction <= 0.0:
    # Declare output data.
    out_polys = []
    depths = []

    # Perform frustum culling.
    culled_polys = [poly_clip,]
    for plane in view_frustum:
      tmp_polys = []
      for poly in culled_polys:
        tmp_polys += polygon.f_cull_h(
            poly,
            plane
            )
      culled_polys = tmp_polys
    # Transform polygons from clip to NDC space.
    for p in range(len(culled_polys)):
      tmp_poly = [None,] * 3
      tmp_depths = [None,] * 3
      for v in range(3):
        v_3d = vector.conv_h_to_3d(culled_polys[p][v])
        v_2d = vector.conv_3d_to_2d(v_3d)
        tmp_poly[v] = v_2d
        tmp_depths[v] = v_3d[Z]
      out_polys.append(tmp_poly)
      depths.append(tmp_depths)

    # Create output packet.
    out_packet = tuple(
        (
          out_polys[p],
          texture,
          depths[p],
          polygon.generate_aabb_2d(out_polys[p]),
          )
        for p
        in range(len(out_polys))
        )

  return out_packet


def s1_sprite_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Unpack input packet.
  (
      sprite,
      origin,
      bound,
      part_transformation,
      projection,
      aspect_ratio,
      view_frustum
      ) = in_packet

  # Transform origin from model to camera space.
  origin_camera_h = matrix.transform_h(
      part_transformation,
      vector.conv_3d_to_h(
        origin
        )
      )

  # Transform origin from camera to clip space.
  origin_clip = matrix.transform_h(
      projection,
      origin_camera_h
      )

  # Perform frustum culling.
  if (
      origin_clip[Z] >= view_frustum[0][PLANE_POINT][Z]
      and origin_clip[Z] <= view_frustum[1][PLANE_POINT][Z]
      ):
    # Transform bound from model to camera space.
    bound_camera_h = matrix.transform_h(
        part_transformation,
        vector.conv_3d_to_h(
          bound
          )
        )

    # Reorient and transform bound from camera to clip space.
    bound_clip = matrix.transform_h(
        projection,
        vector.add(
          origin_camera_h,
          (
            0.0,
            vector.distance(origin_camera_h, bound_camera_h),
            0.0,
            0.0,
            )
          )
        )

    # Transform origin from clip to NDC space.
    origin_ndc = vector.conv_h_to_3d(origin_clip)

    # Transform bound from clip to NDC space.
    bound_ndc = vector.conv_h_to_3d(bound_clip)

    # Create sprite AABB.
    half_height = vector.distance(bound_ndc, origin_ndc)
    half_width = half_height * len(sprite[0]) / len(sprite) / aspect_ratio
    radius = (half_width, half_height,)

    # Create output packet.
    out_packet = (
        sprite,
        origin_ndc[Z],
        (
          vector.subtract(origin_ndc[:Z], radius),
          vector.add(origin_ndc[:Z], radius),
          ),
        vector.multiply(radius, 2.0),
        )

  return out_packet


def s3_fragment_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Unpack input packet.
  (
      fog,
      overlay,
      fragment,
      polygons,
      sprites
      ) = in_packet

  # Determine whether to overlay or rasterize fragment.
  current_min_depth = -1.0
  current_texture = fog
  if overlay != '\0':
    # Overlay fragment.
    current_texture = overlay
  else:

    # Rasterize fragment, checking polygons.
    for polygon_packet in polygons:
      # Unpack polygon packet.
      (
          poly_verts,
          texture,
          depths,
          aabb
          ) = polygon_packet
      # Determine if polygon contains fragment.
      if polygon.aabb_contains_point_2d(
          aabb,
          fragment
          ):
        if polygon.poly_contains_point_2d(
            poly_verts,
            fragment
            ):
          # Interpolate fragment z depth.
          depth = polygon.interpolate_attribute_2d(
              poly_verts,
              depths,
              fragment
              )
          # Determine whether to update texture.
          if current_min_depth < 0.0 or depth < current_min_depth:
            if texture != '\0':
              current_texture = texture
              current_min_depth = depth

    # Rasterize fragment, checking sprites.
    for sprite_packet in sprites:
      # Unpack sprite data.
      (
          sprite,
          depth,
          aabb,
          size
          ) = sprite_packet
      # Determine if sprite contains fragment.
      if polygon.aabb_contains_point_2d(
          aabb,
          fragment
          ):
        # Interpolate fragment texture.
        point = vector.subtract(fragment, aabb[0])
        x = int(point[X] / size[X] * len(sprite[0]))
        y = int(point[Y] / size[Y] * len(sprite))
        texture = sprite[y][x]
        # Determine whether to update texture.
        if current_min_depth < 0.0 or depth < current_min_depth:
          if texture != '\0':
            current_texture = texture
            current_min_depth = depth

  # Create output packet.
  out_packet = (
      current_texture,
      )

  return out_packet
