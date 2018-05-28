"""
TBA.
"""


from rendascii.geometry import matrix, poly2d, poly3d, vec3d, vech
from rendascii.geometry import X, Y, Z, W


def s1_vertex_shader(in_packet):
  # Declare output packet.
  out_packet = None
  # Unpack input packet.
  (
      vertex,
      transformation
      ) = in_packet

  # Transform vertex from model to clip space.
  vert_clip = matrix.transform_3d(
      transformation,
      vech.homogenize(vertex)
      )

  # Transform vertex from clip to NDC space.
  vert_ndc = vech.normalize(vert_clip)

  # Create output packet.
  out_packet = (
      vert_clip,
      vert_ndc,
      )

  return out_packet


def s3_geometry_shader(in_packet):
  # Declare output packet.
  out_packet = []
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
      out_packet.append(
          (
            (
              polygon_ndc[0],
              polygon_ndc[1],
              polygon_ndc[2],
              ),
            texture,
            )
          )

    # One vertex outside.
    elif len(outside) == 1:
      i0 = inside[0]
      i1 = inside[1]
      o0 = outside[0]
      p0 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o0]))
      p1 = vech.normalize(vech.project_z(polygon_clip[i1], polygon_clip[o0]))
      new_poly0 = [None,] * 3
      new_poly1 = [None,] * 3
      new_poly0[i0] = polygon_ndc[i0]
      new_poly0[i1] = polygon_ndc[i1]
      new_poly0[o0] = p1
      new_poly1[i0] = polygon_ndc[i0]
      new_poly1[i1] = p0
      new_poly1[o0] = p1
      out_packet.append(
          (
            tuple(new_poly0),
            texture,
            )
          )
      out_packet.append(
          (
            tuple(new_poly1),
            texture,
            )
          )

    # Two vertices outside.
    elif len(outside) == 2:
      i0 = inside[0]
      o0 = outside[0]
      o1 = outside[1]
      p0 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o0]))
      p1 = vech.normalize(vech.project_z(polygon_clip[i0], polygon_clip[o1]))
      new_poly0 = [None,] * 3
      new_poly0[i0] = polygon_ndc[i0]
      new_poly0[o0] = p0
      new_poly0[o1] = p1
      out_packet.append(
          (
            tuple(new_poly0),
            texture,
            )
          )

  return tuple(out_packet)


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
