"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from rendascii.geometry import matrix, poly2d, poly3d, vec2d, vec3d, vech
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
  vert_clip = matrix.transform_3d(
      full_transformation,
      vech.homogenize(
        vertex
        )
      )

  # Normalize vertex from clip to NDC space.
  vert_ndc = vech.normalize(vert_clip)

  # Create output packet.
  out_packet = (
      vert_clip,
      vert_ndc,
      )

  return out_packet


def s2_polygon_shader(in_packet):
  # Declare output packet.
  out_packet = ()

  # Unpack input packet.
  (
      polygon_clip,
      polygon_ndc,
      texture
      ) = in_packet

  # Perform back-face culling.
  polygon_trunc = tuple(vertex[:W] for vertex in polygon_clip)
  direction = vec3d.dot(
      poly3d.normal(polygon_trunc),
      vec3d.subtract(
        polygon_trunc[0],
        (0.0, 0.0, 0.0,)
        )
      )
  if direction <= 0.0:
    # Declare packet data.
    polys = []
    depths = []

    # Perform frustum culling.
    inside = []
    outside = []
    for v in range(len(polygon_clip)):
      if polygon_clip[v][Z] < 0.0:
        outside.append(v)
      else:
        inside.append(v)

    # No vertices outside.
    if len(outside) == 0:
      # Initialize packet data.
      polys = [[None,] * 3,]
      depths = [[None,] * 3,]
      # Set packet data.
      polys[0][0] = polygon_ndc[0][:Z]
      polys[0][1] = polygon_ndc[1][:Z]
      polys[0][2] = polygon_ndc[2][:Z]
      polys[0] = tuple(polys[0])
      depths[0][0] = polygon_ndc[0][Z]
      depths[0][1] = polygon_ndc[1][Z]
      depths[0][2] = polygon_ndc[2][Z]
      depths[0] = tuple(depths[0])

    # One vertex outside.
    elif len(outside) == 1:
      # Initialize packet data.
      polys = [[None,] * 3,] * 2
      depths = [[None,] * 3,] * 2
      # Calculate new polygons.
      i0 = inside[0]
      i1 = inside[1]
      o0 = outside[0]
      p0 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o0]))
      p1 = vech.normalize(vech.project_z(polygon_clip[i1], polygon_clip[o0]))
      # Set packet data.
      polys[0][i0] = polygon_ndc[i0][:Z]
      polys[0][i1] = polygon_ndc[i1][:Z]
      polys[0][o0] = p1[:Z]
      polys[0] = tuple(polys[0])
      depths[0][i0] = polygon_ndc[i0][Z]
      depths[0][i1] = polygon_ndc[i1][Z]
      depths[0][o0] = 0.0
      depths[0] = tuple(depths[0])
      polys[1][i0] = polygon_ndc[i0][:Z]
      polys[1][i1] = p0[:Z]
      polys[1][o0] = p1[:Z]
      polys[1] = tuple(polys[1])
      depths[1][i0] = polygon_ndc[i0][Z]
      depths[1][i1] = 0.0
      depths[1][o0] = 0.0
      depths[1] = tuple(depths[1])

    # Two vertices outside.
    elif len(outside) == 2:
      # Initialize packet data.
      polys = [[None,] * 3,]
      depths = [[None,] * 3,]
      # Calculate new polygon.
      i0 = inside[0]
      o0 = outside[0]
      o1 = outside[1]
      p0 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o0]))
      p1 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o1]))
      # Set packet data.
      polys[0][i0] = polygon_ndc[i0][:Z]
      polys[0][o0] = p0[:Z]
      polys[0][o1] = p1[:Z]
      polys[0] = tuple(polys[0])
      depths[0][i0] = polygon_ndc[i0][Z]
      depths[0][o0] = 0.0
      depths[0][o1] = 0.0
      depths[0] = tuple(depths[0])

    # Create output packet.
    out_packet = tuple(
        (
          polys[p],
          texture,
          depths[p],
          poly2d.generate_aabb(polys[p]),
          )
        for p
        in range(len(polys))
        )

  return out_packet


def s1_sprite_shader(in_packet):
  # Declare output_packet.
  out_packet = None

  # Unpack input packet.
  (
      sprite,
      origin,
      bound,
      part_transformation,
      projection,
      aspect_ratio
      ) = in_packet

  # Transform origin from model to camera space.
  origin_camera_h = matrix.transform_3d(
      part_transformation,
      vech.homogenize(
        origin
        )
      )

  # Transform origin from camera to clip space.
  origin_clip = matrix.transform_3d(
      projection,
      origin_camera_h
      )

  # Perform frustum culling.
  if origin_clip[Z] >= 0.0:
    # Transform bound from model to camera space.
    bound_camera_h = matrix.transform_3d(
        part_transformation,
        vech.homogenize(
          bound
          )
        )

    # Reorient and transform bound from camera to clip space.
    bound_clip = matrix.transform_3d(
        projection,
        vech.add(
          origin_camera_h,
          (
            0.0,
            vech.distance(origin_camera_h, bound_camera_h),
            0.0,
            0.0,
            )
          )
        )

    # Normalize origin from clip to NDC space.
    origin_ndc = vech.normalize(origin_clip)

    # Normalize bound from clip to NDC space.
    bound_ndc = vech.normalize(bound_clip)

    # Create sprite AABB.
    half_height = vec3d.distance(bound_ndc, origin_ndc)
    half_width = half_height * len(sprite[0]) / len(sprite) / aspect_ratio
    radius = (half_width, half_height,)

    # Create output packet.
    out_packet = (
        sprite,
        origin_ndc[Z],
        (
          vec2d.subtract(origin_ndc[:Z], radius),
          vec2d.add(origin_ndc[:Z], radius),
          ),
        vec2d.multiply(radius, 2.0),
        )

  return out_packet


def s3_fragment_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Unpack input packet.
  (
      overlay,
      fragment,
      polygons,
      sprites
      ) = in_packet

  # Determine whether to overlay or rasterize fragment.
  current_min_depth = -1.0
  current_texture = ' '
  if overlay != '\0':
    # Overlay fragment.
    current_texture = overlay
  else:

    # Rasterize fragment, checking polygons.
    for polygon_packet in polygons:
      # Unpack polygon packet.
      (
          polygon,
          texture,
          depths,
          aabb
          ) = polygon_packet
      # Determine if polygon contains fragment.
      if poly2d.aabb_contains_point(
          aabb,
          fragment
          ):
        if poly2d.poly_contains_point(
            polygon,
            fragment
            ):
          # Interpolate fragment z depth.
          depth = poly2d.interpolate_attribute(
              polygon,
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
      if poly2d.aabb_contains_point(
          aabb,
          fragment
          ):
        # Interpolate fragment texture.
        point = vec2d.subtract(fragment, aabb[0])
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
