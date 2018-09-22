"""
This file is part of RendASCII which is released under MIT.
See file LICENSE.txt for full license details.
"""


from rendascii.pipeline import shader


def stage_one(in_data):
  # Unpack input data.
  (
      workers,
      in_vertex_data,
      in_polygon_data,
      in_sprite_data,
      in_fragment_data
      ) = in_data

  # Declare/initialize output data.
  out_vertex_data = None
  out_polygon_data = in_polygon_data
  out_sprite_data = None
  out_fragment_data = in_fragment_data

  # Process data.
  if workers is None:
    out_vertex_data = tuple(
        shader.s1_vertex_shader(vertex_packet)
        for vertex_packet
        in in_vertex_data
        )
    out_sprite_data = tuple(
        shader.s1_sprite_shader(sprite_packet)
        for sprite_packet
        in in_sprite_data
        )
  else:
    out_vertex_data = workers.map(
        shader.s1_vertex_shader,
        in_vertex_data
        )
    out_sprite_data = workers.map(
        shader.s1_sprite_shader,
        in_sprite_data
        )

  # Pack output data.
  return (
      workers,
      out_vertex_data,
      out_polygon_data,
      out_sprite_data,
      out_fragment_data,
      )


def stage_two(in_data):
  # Unpack input data.
  (
      workers,
      in_vertex_data,
      in_polygon_data,
      in_sprite_data,
      in_fragment_data
      ) = in_data

  # Declare/initialize output data.
  out_vertex_data = in_vertex_data
  out_polygon_data = None
  out_sprite_data = in_sprite_data
  out_fragment_data = in_fragment_data

  # Process data.
  if workers is None:
    out_polygon_data = tuple(
        shader.s2_polygon_shader(polygon_packet)
        for polygon_packet
        in in_polygon_data
        )
  else:
    out_polygon_data = workers.map(
        shader.s2_polygon_shader,
        in_polygon_data
        )

  # Pack output data.
  return (
      workers,
      out_vertex_data,
      out_polygon_data,
      out_sprite_data,
      out_fragment_data,
      )


def stage_three(in_data):
  # Unpack input data.
  (
      workers,
      in_vertex_data,
      in_polygon_data,
      in_sprite_data,
      in_fragment_data
      ) = in_data

  # Declare/initialize output data.
  out_vertex_data = in_vertex_data
  out_polygon_data = in_polygon_data
  out_sprite_data = in_sprite_data
  out_fragment_data = None

  # Process data.
  if workers is None:
    out_fragment_data = tuple(
        shader.s3_fragment_shader(fragment_packet)
        for fragment_packet
        in in_fragment_data
        )
  else:
    out_fragment_data = workers.map(
        shader.s3_fragment_shader,
        in_fragment_data
        )

  # Pack output data.
  return (
      workers,
      out_vertex_data,
      out_polygon_data,
      out_sprite_data,
      out_fragment_data,
      )


def sync_one(in_data):
  # Unpack input data.
  (
      workers,
      in_vertex_data,
      in_polygon_data,
      in_sprite_data,
      in_fragment_data
      ) = in_data

  # Declare/initialize output data.
  out_vertex_data = in_vertex_data
  out_polygon_data = None
  out_sprite_data = None
  out_fragment_data = in_fragment_data

  # Synchronize data.
  out_polygon_data = tuple(
      (
        (
          in_vertex_data[polygon_packet[0][0]][0],
          in_vertex_data[polygon_packet[0][1]][0],
          in_vertex_data[polygon_packet[0][2]][0],
          ),
        polygon_packet[1],
        polygon_packet[2],
        )
      for polygon_packet
      in in_polygon_data
      )
  out_sprite_data = tuple(
      sprite_packet
      for sprite_packet
      in in_sprite_data
      if sprite_packet is not None
      )

  # Pack output data.
  return (
      workers,
      out_vertex_data,
      out_polygon_data,
      out_sprite_data,
      out_fragment_data,
      )


def sync_two(in_data):
  # Unpack input data.
  (
      workers,
      in_vertex_data,
      in_polygon_data,
      in_sprite_data,
      in_fragment_data
      ) = in_data

  # Declare/initialize output data.
  out_vertex_data = in_vertex_data
  out_polygon_data = None
  out_sprite_data = in_sprite_data
  out_fragment_data = None

  # Synchronize data.
  out_polygon_data = sum(in_polygon_data, ())
  out_fragment_data = tuple(
      (
        fragment_packet[0],
        fragment_packet[1],
        fragment_packet[2],
        out_polygon_data,
        out_sprite_data,
        )
      for fragment_packet
      in in_fragment_data
      )

  # Pack output data.
  return (
      workers,
      out_vertex_data,
      out_polygon_data,
      out_sprite_data,
      out_fragment_data,
      )
