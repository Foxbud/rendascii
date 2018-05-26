"""
TBA.
"""


from rendascii.geometry import matrix, poly2d, poly3d, vec3d
from rendascii.geometry import X, Y, Z


def s1_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      vertex,
      transformation
      ) = in_packet

  # Transform vertex from model to view space.
  vert_camera = matrix.transform_3d(
      transformation,
      vertex
      )

  # Create output packet.
  out_packet = (
      vert_camera,
      )

  return out_packet


def s3_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      polygon,
      texture
      ) = in_packet

  # Test for back-face polygon.
  direction = vec3d.dot(
      poly3d.normal(polygon),
      vec3d.subtract(
        polygon[0],
        (0.0, 0.0, 0.0,)
        )
      )
  if direction <= 0.0:
    # Create output packet.
    out_packet = (
        polygon,
        texture,
        )

  return out_packet


def s5_fragment_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      overlay,
      fragment,
      polygons
      ) = in_packet

  # Determine whether to overlay or rasterize fragment.
  current_min_depth = -1.0
  current_texture = ' '
  if overlay != '\0':
    # Overlay fragment.
    current_texture = overlay
  else:

    # Rasterize fragment.
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
          if current_min_depth < 0.0 or depth < current_min_depth:
            if texture != '\0':
              current_texture = texture
              current_min_depth = depth

  # Create output packet.
  out_packet = (
      current_texture,
      )

  return out_packet
