"""
TBA.
"""


from rendascii.geometry import matrix3d, poly2d, vec3d
from rendascii.geometry import X, Y, Z


def stage_one(in_vertex_data, in_polygon_data):
  """
  This function handles the first block of parallelizable
  rendering work. This includes transforming all vertices and polygon
  normals from model space to camera space and culling back-face
  polygons.
  """
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


def stage_two(in_vertex_data, in_polygon_data):
  """
  This function handles the first block of non-parallelizable
  rendering work. This includes culling and clipping polygons outside
  the viewing frustum.
  """
  return in_vertex_data, in_polygon_data


def stage_three(in_vertex_data, in_polygon_data):
  """
  This function handles the second block of parallelizable
  rendering work. This includes projecting all vertices to the
  camera plane.
  """
  out_vertex_data = tuple(
      _vertex_shader_b(packed_vertex_data)
      for packed_vertex_data
      in in_vertex_data
      )
  return out_vertex_data, in_polygon_data


def stage_four(in_vertex_data, in_polygon_data):
  """
  This function handles the second block of non-parallelizable
  rendering work. This includes replacing vertex indices with vertices
  and calculating an AABB for each polygon.
  """
  out_polygon_data = tuple(
      (
        (
          in_vertex_data[packed_polygon_data[0][0]][0],
          in_vertex_data[packed_polygon_data[0][1]][0],
          in_vertex_data[packed_polygon_data[0][2]][0],
          ),
        (
          in_vertex_data[packed_polygon_data[0][0]][1],
          in_vertex_data[packed_polygon_data[0][1]][1],
          in_vertex_data[packed_polygon_data[0][2]][1],
          ),
        poly2d.generate_aabb(
          (
            in_vertex_data[packed_polygon_data[0][0]][0],
            in_vertex_data[packed_polygon_data[0][1]][0],
            in_vertex_data[packed_polygon_data[0][2]][0],
            )
          ),
        packed_polygon_data[1],
        )
      for packed_polygon_data
      in in_polygon_data
      )
  return out_polygon_data


def _vertex_shader_a(packed_vertex_data):
  # Unpack vertex data from previous stage of pipeline.
  (
      vertex,
      cam_focus,
      cam_rot_matrix,
      cam_position,
      position,
      inst_rot_matrix,
      scale
      ) = packed_vertex_data

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
      cam_focus,
      )


def _vertex_shader_b(packed_vertex_data):
  # Unpack vertex data from previous stage of pipeline.
  (
      vertex,
      cam_focus
      ) = packed_vertex_data

  # Calculate vertex z depth.
  depth = vec3d.squared_dist(cam_focus, vertex)

  # Project vertex onto camera plane.
  ratio = -cam_focus[Z] / (vertex[Z] - cam_focus[Z])
  vert_projected = (
      cam_focus[X] + ratio * (vertex[X] - cam_focus[X]),
      cam_focus[Y] + ratio * (vertex[Y] - cam_focus[Y]),
      )

  # Pack vertex data for next stage of pipeline.
  return (
      vert_projected,
      depth,
      )


def _geometry_shader_a(packed_polygon_data):
  # Unpack polygon data from previous stage of pipeline.
  (
      polygon,
      texture,
      normal,
      cam_rot_matrix,
      inst_rot_matrix
      ) = packed_polygon_data

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
