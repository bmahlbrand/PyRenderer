from Shader import *
from VertexArrayObject import *

from shaders.color.glsl import COLOR_VERT, COLOR_FRAG

class Mesh:
    def __init__(self, attributes, index=None):

        self.vertex_array = VertexArrayObject(attributes, index)
        self.shader = Shader(COLOR_VERT, COLOR_FRAG)
    
    def draw(self, projection, view, _model, **_kwargs):
        """ object draw method """

        shader = _kwargs.get('color_shader', self.shader)

        shid = shader.glid
        GL.glUseProgram(shid)

        loc = GL.glGetUniformLocation(shid, 'projection')
        GL.glUniformMatrix4fv(loc, 1, True, projection)
        loc = GL.glGetUniformLocation(shid, 'view')
        GL.glUniformMatrix4fv(loc, 1, True, view)

        self.vertex_array.draw(GL.GL_TRIANGLES)
        
        GL.glUseProgram(0)

        # print('...')

        # code = GL.glGetError()

        # if code == GL.GL_NO_ERROR:
        #     print('no error')