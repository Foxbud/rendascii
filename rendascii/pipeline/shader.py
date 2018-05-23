"""
TBA.
"""


from rendascii.geometry import matrix3d, poly2d, vec3d
from rendascii.geometry import X, Y, Z
from rendascii.pipeline import packet


def s1_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Transform vertex from model to world space.
  vert_world = vec3d.add(
      in_packet.inst_position,
      matrix3d.transform_vector(
        in_packet.inst_rot_matrix,
        vec3d.multiply(
          in_packet.vertex,
          in_packet.inst_scale
          )
        )
      )

  # Transform vertex from world to camera space.
  vert_camera = matrix3d.transform_vector(
      in_packet.cam_rot_matrix,
      vec3d.add(
        in_packet.cam_position,
        vert_world
        )
      )

  # Create output packet.
  out_packet = packet.S3Vertex(
      vertex=vert_camera,
      cam_focus=in_packet.cam_focus
      )

  return out_packet


def s3_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Calculate vertex z depth.
  depth = vec3d.squared_dist(
      in_packet.vertex,
      in_packet.cam_focus
      )

  # Project vertex from camera space onto camera plane.
  ratio = -in_packet.cam_focus[Z] / (
      in_packet.vertex[Z] - in_packet.cam_focus[Z]
      )
  vert_projected = (
      in_packet.cam_focus[X] + ratio * (
        in_packet.vertex[X] - in_packet.cam_focus[X]
        ),
      in_packet.cam_focus[Y] + ratio * (
        in_packet.vertex[Y] - in_packet.cam_focus[Y]
        ),
      )

  # Create output packet.
  out_packet = packet.S4Vertex(
      vertex=vert_projected,
      depth=depth
      )

  return out_packet


def s1_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Transform normal from model to world space.
  normal_world = matrix3d.transform_vector(
      in_packet.inst_rot_matrix,
      in_packet.normal
      )
  # Transform center from model to world space.
  center_world = vec3d.add(
      in_packet.inst_position,
      matrix3d.transform_vector(
        in_packet.inst_rot_matrix,
        vec3d.multiply(
          in_packet.center,
          in_packet.inst_scale
          )
        )
      )

  # Transform normal from world to camera space.
  normal_camera = matrix3d.transform_vector(
      in_packet.cam_rot_matrix,
      normal_world
      )
  # Transform center from world to camera space.
  center_camera = matrix3d.transform_vector(
      in_packet.cam_rot_matrix,
      vec3d.add(
        in_packet.cam_position,
        center_world
        )
      )

  # Test for back-face polygon.
  direction = vec3d.dot(
      normal_camera,
      vec3d.subtract(
        center_camera,
        in_packet.cam_focus
        )
      )
  if direction <= 0:
    # Create output packet.
    out_packet = packet.S4Polygon(
        v_polygon=in_packet.v_polygon,
        texture=in_packet.texture
        )

  return out_packet


def s5_fragment_shader(in_packet):
  # Declare output packet.
  out_packet = None

  # Rasterize fragment.
  current_min_depth = -1
  current_texture = ' '
  for polygon_packet in in_packet.polygons:
    # Determine if polygon contains fragment.
    if poly2d.aabb_contains_point(
        polygon_packet.aabb,
        in_packet.fragment
        ):
      if poly2d.poly_contains_point(
          polygon_packet.polygon,
          in_packet.fragment
          ):
        # Interpolate fragment z depth.
        depth = poly2d.interpolate_attribute(
            polygon_packet.polygon,
            polygon_packet.depths,
            in_packet.fragment
            )
        if current_min_depth < 0 or depth < current_min_depth:
          if polygon_packet.texture != '\0':
            current_texture = polygon_packet.texture
            current_min_depth = depth

  # Create fragment data.
  out_packet = packet.SEFragment(
      current_texture
      )

  return out_packet
