"""
TBA.
"""


from rendascii.geometry import Vec3D


class Model:

  def __init__(self, objmesh_name, resource_dir):
    # Initialize instance attributes.
    self.vertices = []
    self.faces = []
    self.face_normals = []
    self.face_colors = []

    # Load mesh data.
    self._load_objmesh(objmesh_name, resource_dir)

  def _load_objmesh(self, objmesh_name, resource_dir):
    vertex_normals = []
    face_vert_norms = []
    materials = None
    with open(resource_dir + objmesh_name, 'r') as obj_f:
      cur_mtl = None
      for line in obj_f:
        words = line.split()
        if len(words) > 0:

          # Check for vertex definition.
          if words[0] == 'v':
            self.vertices.append(
                Vec3D(
                  [
                    float(component)
                    for component
                    in words[1:]
                    ]
                  )
                )

          # Check for vertex normal definition.
          elif words[0] == 'vn':
            vertex_normals.append(
                Vec3D(
                  [
                    float(component)
                    for component
                    in words[1:]
                    ]
                  )
                )

          # Check for face definition.
          elif words[0] == 'f':
            # Assign face color.
            self.face_colors.append(materials[cur_mtl])
            # Extract vertex and normal indices.
            verts = []
            norms = []
            for component in words[1:]:
              vert_info = component.split('/')
              verts.append(int(vert_info[0]) - 1)
              norms.append(int(vert_info[2]) - 1)
            # Construct face data.
            self.faces.append(verts)
            face_vert_norms.append(norms)

          # Check for material to use.
          elif words[0] == 'usemtl':
            cur_mtl = words[1]

          # Check for material library.
          elif words[0] == 'mtllib':
            materials = self._load_mtllib(words[1], resource_dir)

    # Calculate face normals from vertex normals.
    for i in range(len(self.faces)):
      # Calculate average of vertex normals.
      avg_vert_norm = Vec3D()
      for j in range(len(face_vert_norms[i])):
        avg_vert_norm.add(vertex_normals[face_vert_norms[i][j]])
      avg_vert_norm.mul(1 / len(face_vert_norms[i]))

      # Calculate face normal with arbitrary direction.
      origin = self.vertices[self.faces[i][0]]
      u = Vec3D(origin)
      u.sub(self.vertices[self.faces[i][1]])
      v = Vec3D(origin)
      v.sub(self.vertices[self.faces[i][2]])
      face_normal = Vec3D(u)
      face_normal.cross(v)

      # Point face normal in correct direction.
      if face_normal.dot(avg_vert_norm) < 0:
        face_normal.neg()

      # Assign new face normal to face.
      self.face_normals.append(face_normal)

  def _load_mtllib(self, mtllib_name, resource_dir):
    materials = {}
    with open(resource_dir + mtllib_name, 'r') as mtl_f:
      cur_mtl = None
      for line in mtl_f:
        words = line.split()
        if len(words) > 0:

          # Check for new material.
          if words[0] == 'newmtl':
            cur_mtl = words[1]

          # Check for material color (diffuse).
          elif words[0] == 'Kd':
            materials[cur_mtl] = ''.join(
                [
                  '{0:02x}'.format(round(float(component) * 255))
                  for component
                  in words[1:]
                  ]
                )

    return materials
