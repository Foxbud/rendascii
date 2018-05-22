"""
TBA.
"""


from rendascii.geometry import matrix3d, poly2d, vec3d
from rendascii.geometry import X, Y, Z


def stage_one(in_vertex_data, in_geometry_data, in_fragment_data):
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
  out_geometry_data = tuple(
      _geometry_shader_a(packed_polygon_data)
      for packed_polygon_data
      in in_geometry_data
      )
  out_fragment_data = in_fragment_data
  return out_vertex_data, out_geometry_data, out_fragment_data


def stage_two(in_vertex_data, in_geometry_data, in_fragment_data):
  """
  This function handles the first block of non-parallelizable
  rendering work. This includes culling and clipping polygons outside
  the viewing frustum.
  """
  out_vertex_data = in_vertex_data
  out_geometry_data = in_geometry_data
  out_fragment_data = in_fragment_data
  return out_vertex_data, out_geometry_data, out_fragment_data


def stage_three(in_vertex_data, in_geometry_data, in_fragment_data):
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
  out_geometry_data = in_geometry_data
  out_fragment_data = in_fragment_data
  return out_vertex_data, out_geometry_data, out_fragment_data


def stage_four(in_vertex_data, in_geometry_data, in_fragment_data):
  """
  This function handles the second block of non-parallelizable
  rendering work. This includes replacing vertex indices with vertices
  and calculating an AABB for each polygon and packaging a copy of
  the geometry data with each fragment.
  """
  out_geometry_data = tuple(
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
      in in_geometry_data
      )
  out_fragment_data = tuple(
      (
        packed_fragment_data[0],
        out_geometry_data,
        )
      for packed_fragment_data
      in in_fragment_data
      )
  return out_fragment_data


def stage_five(in_fragment_data):
  """
  This function handles the third block of parallelizable
  rendering work. This includes rasterizing all pixel fragments.
  """
  out_fragment_data = tuple(
      _fragment_shader_a(packed_fragment_data)
      for packed_fragment_data
      in in_fragment_data
      )
  return out_fragment_data


def _vertex_shader_a(packed_vertex_data):
  # Unpack vertex data.
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

  # Pack vertex data.
  return (
      vert_camera,
      cam_focus,
      )


def _vertex_shader_b(packed_vertex_data):
  # Unpack vertex data.
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

  # Pack vertex data.
  return (
      vert_projected,
      depth,
      )


def _geometry_shader_a(packed_polygon_data):
  # Unpack polygon data.
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

  # Pack polygon data.
  return (
      polygon,
      texture,
      normal_camera,
      )


def _fragment_shader_a(packed_fragment_data):
  # Unpack fragment data.
  (
      fragment,
      polygon_data
      ) = packed_fragment_data

  # Rasterize fragment.
  current_min_depth = -1
  current_texture = ' '
  for packed_polygon_data in polygon_data:
    # Unpack polygon data.
    (
        polygon,
        depths,
        aabb,
        texture
        ) = packed_polygon_data
    # Determine if polygon contains fragment.
    if poly2d.aabb_contains_point(aabb, fragment):
      if poly2d.poly_contains_point(polygon, fragment):
        # Interpolate fragment z depth.
        depth = poly2d.interpolate_attribute(polygon, depths, fragment)
        if current_min_depth < 0 or depth < current_min_depth:
          if texture != '\0':
            current_texture = texture
            current_min_depth = depth

  # Pack fragment data.
  return (
      current_texture,
      )
