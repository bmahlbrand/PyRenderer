import OpenGL.GL as GL
import glfw
from PIL import Image

class Texture:
    def __init__(self, filename):
        self.id = read(self, filename)

    def read(self, filename):
        # PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM
        # and other file types.  We convert into a texture using GL.
        print('trying to load texture from: ', filename)
        try:
            image = Image.open(filename)
        except IOError as ex:
            print('IOError: failed to open texture file')
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            return -1
        print('opened file: size=', image.size, 'format=', image.format)
        imageData = numpy.array(list(image.getdata()), numpy.uint8)

        textureID = glGenTextures(1)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, image.size[0], image.size[1],
            0, GL_RGB, GL_UNSIGNED_BYTE, imageData)

        image.close()
        return textureID
