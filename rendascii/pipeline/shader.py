"""
TBA.
"""


from rendascii.geometry import matrix3d, poly2d, vec3d
from rendascii.geometry import X, Y, Z


def s1_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      vertex,
      cam_focus,
      cam_rot_matrix,
      cam_position,
      inst_rot_matrix,
      inst_position,
      inst_scale
      ) = in_packet

  # Transform vertex from model to world space.
  vert_world = vec3d.add(
      inst_position,
      matrix3d.transform_vector(
        inst_rot_matrix,
        vec3d.multiply(
          vertex,
          inst_scale
          )
        )
      )

  # Transform vertex from world to camera space.
  vert_camera = matrix3d.transform_vector(
      cam_rot_matrix,
      vec3d.add(
        cam_position,
        vert_world
        )
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


def s1_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      v_polygon,
      texture,
      normal,
      cam_focus,
      cam_rot_matrix,
      inst_rot_matrix
      ) = in_packet

  # Transform normal from model to world space.
  normal_world = matrix3d.transform_vector(
      inst_rot_matrix,
      normal
      )

  # Transform normal from world to camera space.
  normal_camera = matrix3d.transform_vector(
      cam_rot_matrix,
      normal_world
      )

  # Create output packet.
  out_packet = (
      v_polygon,
      texture,
      normal_camera,
      cam_focus,
      )

  return out_packet


def s3_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      v_polygon,
      texture,
      normal,
      cam_focus,
      vertex
      ) = in_packet

  # Test for back-face polygon.
  direction = vec3d.dot(
      normal,
      vec3d.subtract(
        vertex,
        cam_focus
        )
      )
  if direction <= 0:
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
      fragment,
      polygons
      ) = in_packet

  # Rasterize fragment.
  current_min_depth = -1
  current_texture = ' '
  for polygon_packet in polygons:
    # Unpack polygon packet.
    (
        polygon,
        depths,
        aabb,
        texture
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
        if current_min_depth < 0 or depth < current_min_depth:
          if texture != '\0':
            current_texture = texture
            current_min_depth = depth

  # Create output packet.
  out_packet = (
      current_texture,
      )

  return out_packet
