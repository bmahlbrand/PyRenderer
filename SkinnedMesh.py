from Shader import *
from VertexArrayObject import *

from shaders.skinning.glsl import SKINNING_VERT
from shaders.color.glsl import COLOR_FRAG

class SkinnedMesh:
    """class of skinned mesh nodes in scene graph """
    def __init__(self, attributes, bone_nodes, bone_offsets, index=None):

        self.vertex_array = VertexArrayObject(attributes, index)
        self.skinning_shader = Shader(SKINNING_VERT, COLOR_FRAG)

        self.bone_nodes = bone_nodes
        self.bone_offsets = bone_offsets

    def draw(self, projection, view, _model, **_kwargs):
        """ skinning object draw method """

        shid = self.skinning_shader.glid
        GL.glUseProgram(shid)

        loc = GL.glGetUniformLocation(shid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)
        loc = GL.glGetUniformLocation(shid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        # LBS skinning data
        for bone_id, node in enumerate(self.bone_nodes):
            bone_matrix = node.world_transform @ self.bone_offsets[bone_id]

            bone_loc = GL.glGetUniformLocation(shid, 'boneMatrix[%d]' % bone_id)
            GL.glUniformMatrix4fv(bone_loc, 1, True, bone_matrix)

        self.vertex_array.draw(GL.GL_TRIANGLES)
        
        GL.glUseProgram(0)