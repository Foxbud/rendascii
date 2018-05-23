"""
TBA.
"""


class S1Vertex:

  def __init__(
      self,
      vertex,
      cam_focus,
      cam_rot_matrix,
      cam_position,
      inst_rot_matrix,
      inst_position,
      inst_scale
      ):
    # Initialize instance attributes.
    self.vertex = vertex
    self.cam_focus = cam_focus
    self.cam_rot_matrix = cam_rot_matrix
    self.cam_position = cam_position
    self.inst_rot_matrix = inst_rot_matrix
    self.inst_position = inst_position
    self.inst_scale = inst_scale


class S3Vertex:

  def __init__(
      self,
      vertex,
      cam_focus
      ):
    # Initialize instance attributes.
    self.vertex = vertex
    self.cam_focus = cam_focus


class S4Vertex:

  def __init__(
      self,
      vertex,
      depth
      ):
    # Initialize instance attributes.
    self.vertex = vertex
    self.depth = depth


class S1Polygon:

  def __init__(
      self,
      v_polygon,
      texture,
      normal,
      center,
      cam_focus,
      cam_rot_matrix,
      cam_position,
      inst_rot_matrix,
      inst_position,
      inst_scale
      ):
    # Initialize instance attributes.
    self.v_polygon = v_polygon
    self.texture = texture
    self.normal = normal
    self.center = center
    self.cam_focus = cam_focus
    self.cam_rot_matrix = cam_rot_matrix
    self.cam_position = cam_position
    self.inst_rot_matrix = inst_rot_matrix
    self.inst_position = inst_position
    self.inst_scale = inst_scale


class S4Polygon:

  def __init__(
      self,
      v_polygon,
      texture
      ):
    # Initialize instance attributes.
    self.v_polygon = v_polygon
    self.texture = texture


class S5Polygon:

  def __init__(
      self,
      polygon,
      depths,
      aabb,
      texture
      ):
    # Initialize instance attributes.
    self.polygon = polygon
    self.depths = depths
    self.aabb = aabb
    self.texture = texture


class S4Fragment:

  def __init__(
      self,
      fragment
      ):
    # Initialize instance attributes.
    self.fragment = fragment


class S5Fragment:

  def __init__(
      self,
      fragment,
      polygons
      ):
    # Initialize instance attributes.
    self.fragment = fragment
    self.polygons = polygons


class SEFragment:

  def __init__(
      self,
      texture
      ):
    # Initialize instance attributes.
    self.texture = texture
