"""
TBA.
"""


from rendascii.geometry import matrix3d
from rendascii.geometry import vec3d


def stage_one(in_vertex_data, in_polygon_data):
  out_vertex_data = tuple(
      _vertex_shader_a(packed_vertex_data)
      for packed_vertex_data
      in in_vertex_data
      )
  out_polygon_data = tuple(
      _geometry_shader_a(packed_polygon_data)
      for packed_polygon_data
      in in_polygon_data
      )
  return out_vertex_data, out_polygon_data


def _vertex_shader_a(packed_vertex_data):
  # Unpack vertex data from previous stage of pipeline.
  vertex, cam_rot_matrix, cam_position, position, inst_rot_matrix, scale = (
      packed_vertex_data
      )

  # Transform vertex to world space.
  vert_world = vec3d.add(
      position,
      matrix3d.transform_vector(
        inst_rot_matrix,
        vec3d.multiply(
          vertex,
          scale
          )
        )
      )

  # Transform vertex to camera space.
  vert_camera = matrix3d.transform_vector(
      cam_rot_matrix,
      vec3d.add(
        cam_position,
        vert_world
        )
      )

  # Pack vertex data for next stage of pipeline.
  return (
      vert_camera,
      )


def _geometry_shader_a(packed_polygon_data):
  # Unpack polygon data from previous stage of pipeline.
  polygon, texture, normal, cam_rot_matrix, inst_rot_matrix = (
      packed_polygon_data
      )

  # Transform normal to world space.
  normal_world = matrix3d.transform_vector(
      inst_rot_matrix,
      normal
      )

  # Transform normal to camera space.
  normal_camera = matrix3d.transform_vector(
      cam_rot_matrix,
      normal_world
      )

  # Pack polygon data for next stage of pipeline.
  return (
      polygon,
      texture,
      normal_camera,
      )
