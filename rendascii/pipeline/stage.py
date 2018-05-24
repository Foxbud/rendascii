"""
TBA.
"""


from rendascii.geometry import poly2d, poly3d
from rendascii.pipeline import shader


def stage_one(workers, in_vertex_data, in_polygon_data, in_fragment_data):
  out_vertex_data = None
  out_polygon_data = in_polygon_data
  out_fragment_data = in_fragment_data

  if workers is None:
    out_vertex_data = tuple(
        shader.s1_vertex_shader(vertex_packet)
        for vertex_packet
        in in_vertex_data
        )
  else:
    out_vertex_data = workers.map(
        shader.s1_vertex_shader,
        in_vertex_data
        )

  return workers, out_vertex_data, out_polygon_data, out_fragment_data


def stage_two(workers, in_vertex_data, in_polygon_data, in_fragment_data):
  out_vertex_data = in_vertex_data
  out_polygon_data = tuple(
      (
        polygon_packet[0],
        polygon_packet[1],
        polygon_packet[2],
        (
          in_vertex_data[polygon_packet[0][0]][0],
          in_vertex_data[polygon_packet[0][1]][0],
          in_vertex_data[polygon_packet[0][2]][0],
          ),
        )
      for polygon_packet
      in in_polygon_data
      )
  out_fragment_data = in_fragment_data

  return workers, out_vertex_data, out_polygon_data, out_fragment_data


def stage_three(workers, in_vertex_data, in_polygon_data, in_fragment_data):
  out_vertex_data = None
  out_polygon_data = None
  out_fragment_data = in_fragment_data

  if workers is None:
    out_vertex_data = tuple(
        shader.s3_vertex_shader(vertex_packet)
        for vertex_packet
        in in_vertex_data
        )
    out_polygon_data = tuple(
        shader.s3_geometry_shader(polygon_packet)
        for polygon_packet
        in in_polygon_data
        )
  else:
    out_vertex_data = workers.map(
        shader.s3_vertex_shader,
        in_vertex_data
        )
    out_polygon_data = workers.map(
        shader.s3_geometry_shader,
        in_polygon_data
        )

  return workers, out_vertex_data, out_polygon_data, out_fragment_data


def stage_four(workers, in_vertex_data, in_polygon_data, in_fragment_data):
  out_polygon_data = tuple(
      (
        (
          in_vertex_data[polygon_packet[0][0]][0],
          in_vertex_data[polygon_packet[0][1]][0],
          in_vertex_data[polygon_packet[0][2]][0],
          ),
        polygon_packet[1],
        (
          in_vertex_data[polygon_packet[0][0]][1],
          in_vertex_data[polygon_packet[0][1]][1],
          in_vertex_data[polygon_packet[0][2]][1],
          ),
        poly2d.generate_aabb(
          (
            in_vertex_data[polygon_packet[0][0]][0],
            in_vertex_data[polygon_packet[0][1]][0],
            in_vertex_data[polygon_packet[0][2]][0],
            )
          ),
        )
      for polygon_packet
      in in_polygon_data
      if polygon_packet is not None
      )
  out_fragment_data = tuple(
      (
        fragment_packet[0],
        out_polygon_data,
        )
      for fragment_packet
      in in_fragment_data
      )

  return workers, out_fragment_data


def stage_five(workers, in_fragment_data):
  out_fragment_data = None

  if workers is None:
    out_fragment_data = tuple(
        shader.s5_fragment_shader(fragment_packet)
        for fragment_packet
        in in_fragment_data
        )
  else:
    out_fragment_data = workers.map(
        shader.s5_fragment_shader,
        in_fragment_data
        )

  return out_fragment_data
