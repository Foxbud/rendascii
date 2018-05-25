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
      cam_focus,
      transformation
      ) = in_packet

  # Transform vertex from model to camera space.
  vert_camera = matrix.transform_3d(
      transformation,
      vertex
      )

  # Create output packet.
  out_packet = (
      vert_camera,
      cam_focus,
      )

  return out_packet


def s3_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      vertex,
      cam_focus
      ) = in_packet

  # Calculate vertex z depth.
  depth = vec3d.squared_dist(
      vertex,
      cam_focus
      )

  # Project vertex from camera space onto camera plane.
  ratio = -cam_focus[Z] / (
      vertex[Z] - cam_focus[Z]
      )
  vert_projected = (
      cam_focus[X] + ratio * (
        vertex[X] - cam_focus[X]
        ),
      cam_focus[Y] + ratio * (
        vertex[Y] - cam_focus[Y]
        ),
      )

  # Create output packet.
  out_packet = (
      vert_projected,
      depth,
      )

  return out_packet


def s3_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      v_polygon,
      texture,
      cam_focus,
      polygon
      ) = in_packet

  # Test for back-face polygon.
  direction = vec3d.dot(
      poly3d.normal(polygon),
      vec3d.subtract(
        polygon[0],
        cam_focus
        )
      )
  if direction <= 0.0:
    # Create output packet.
    out_packet = (
        v_polygon,
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
