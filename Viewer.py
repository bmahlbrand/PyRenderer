import sys
from itertools import cycle

from PIL import Image, ImageOps

import glfw
import OpenGL.GL as GL

from Trackball import Trackball
from Shader import Shader
from Texture import Texture

# from shaders.color.glsl import COLOR_VERT, COLOR_FRAG
from shaders.lighting.glsl import PHONG_VERT, PHONG_FRAG

from SkinnedCylinder import SkinnedCylinder

from Transform import *

from loadMesh import load_mesh

from Renderer import *

def obj_centered_camera_pose(rho_in, phi_deg, theta_deg):
    phi, theta = np.radians((phi_deg, theta_deg))
    
    x = (rho_in * np.cos(theta) * np.cos(phi))
    y = (rho_in * np.sin(theta) * np.cos(phi))
    z = (rho_in * np.sin(phi))
    # print(vec(x, y, z))
    # print(quaternion_matrix(quaternion_from_euler(rho_in, phi_deg, theta_deg, None)))
    # raise ValueError("bad")
    return quaternion_matrix(quaternion_from_euler(rho_in, phi_deg, theta_deg, None))
    # return lookat(vec(x, y, z), vec(0., 0., 0.), vec(0., 1., 0.))

class GLFWTrackball(Trackball):
    """ Use in Viewer for interactive viewpoint control """

    def __init__(self, win):
        """ Init needs a GLFW window handler 'win' to register callbacks """
        super().__init__(96., 20., 32.)
        self.mouse = (0, 0)
        glfw.set_cursor_pos_callback(win, self.on_mouse_move)
        glfw.set_scroll_callback(win, self.on_scroll)

    def on_mouse_move(self, win, xpos, ypos):
        """ Rotate on left-click & drag, pan on right-click & drag """
        old = self.mouse
        self.mouse = (xpos, glfw.get_window_size(win)[1] - ypos)
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_LEFT):
            self.drag(old, self.mouse, glfw.get_window_size(win))
        if glfw.get_mouse_button(win, glfw.MOUSE_BUTTON_RIGHT):
            self.pan(old, self.mouse)

    def on_scroll(self, win, _deltax, deltay):
        """ Scroll controls the camera distance to trackball center """
        self.zoom(deltay, glfw.get_window_size(win)[1])

class Viewer:
    """ GLFW viewer window, with classic initialization & graphics loop """

    def __init__(self, width=640, height=480):

        # version hints: create GL window with >= OpenGL 3.3 and core profile
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.RESIZABLE, True)
        self.win = glfw.create_window(width, height, 'Viewer', None, None)

        # make win's OpenGL context current; no OpenGL calls can happen before
        glfw.make_context_current(self.win)

        # register event handlers
        glfw.set_key_callback(self.win, self.on_key)
        glfw.set_window_size_callback(self.win, self.on_resize)
        
        # useful message to check OpenGL renderer characteristics
        print('OpenGL', GL.glGetString(GL.GL_VERSION).decode() + ', GLSL',
              GL.glGetString(GL.GL_SHADING_LANGUAGE_VERSION).decode() +
              ', Renderer', GL.glGetString(GL.GL_RENDERER).decode())

        # initialize GL by setting viewport and default render characteristics
        GL.glClearColor(0.1, 0.1, 0.1, 0.1)
        GL.glEnable(GL.GL_DEPTH_TEST)         # depth test now enabled (TP2)
        GL.glEnable(GL.GL_CULL_FACE)          # backface culling enabled (TP2)

        # compile and initialize shader programs once globally
        # self.color_shader = Shader(COLOR_VERT, COLOR_FRAG)
        # print(COLOR_VERT)
        self.lighting_shader = Shader(PHONG_VERT, PHONG_FRAG)

        # initially empty list of object to draw
        self.drawables = []
        self.trackball = GLFWTrackball(self.win)
        
        # cyclic iterator to easily toggle polygon rendering modes
        self.fill_modes = cycle([GL.GL_LINE, GL.GL_POINT, GL.GL_FILL])
    
    
    def run(self):
        """ Main render loop for this OpenGL window """
        while not glfw.window_should_close(self.win):
            # clear draw buffer and depth buffer (<-TP2)
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            winsize = glfw.get_window_size(self.win)
            view = self.trackball.view_matrix()
            # print(view)
            # view = obj_centered_camera_pose(96., 20., 32.)
            
            projection = self.trackball.projection_matrix(winsize)
            # projection = identity()
            # draw our scene objects
            for drawable in self.drawables:
                drawable.draw(projection, view, identity(), win=self.win,
                              color_shader=self.lighting_shader)
            
            # flush render commands, and swap draw buffers
            glfw.swap_buffers(self.win)

            # Poll for and process events
            glfw.poll_events()

    def screenshot(self, filename):
        GL.glPixelStorei(GL.GL_PACK_ALIGNMENT, 1)
        winsize = glfw.get_window_size(self.win)
        
        data = GL.glReadPixels(0, 0, winsize[0], winsize[1], GL.GL_RGBA, GL.GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (winsize[0], winsize[1]), data)
        image.save(filename, 'PNG')

    def add(self, *drawables):
        """ add objects to draw in this window """
        self.drawables.extend(drawables)

    def on_key(self, _win, key, _scancode, action, _mods):
        """ 'Q' or 'Escape' quits """
        if action == glfw.PRESS or action == glfw.REPEAT:
            if key == glfw.KEY_ESCAPE or key == glfw.KEY_Q:
                glfw.set_window_should_close(self.win, True)
            if key == glfw.KEY_W:
                GL.glPolygonMode(GL.GL_FRONT_AND_BACK, next(self.fill_modes))
            if key == glfw.KEY_SPACE:
                glfw.set_time(0)
            if key == glfw.KEY_S:
                self.screenshot("screenshot.png")

    
    def on_resize(self, window, width, height):
        GL.glViewport(0, 0, width, height)
        # print(width, height)

    def render2image(self, drawables, rho_ins, phi_degs, theta_degs):
        init_theta_deg = 0
        k = 0
        for rho_in in rho_ins:
            for phi_deg in phi_degs:
                for theta_deg in theta_degs:
                    view = obj_centered_camera_pose(rho_in, phi_deg, (theta_deg+init_theta_deg)%360 )
                    fname = 'image_%03d_p%03d_t%03d_r%03d.png'%(k, phi_deg, theta_deg, rho_in)
                    k += 1
                    
                    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
                    for drawable in drawables:
                        drawable.draw(identity(), view, identity(), win=self.win,
                                color_shader=self.color_shader)
                    self.screenshot(fname)
                    
                    # flush render commands, and swap draw buffers
                    glfw.swap_buffers(self.win)

                    # Poll for and process events
                    glfw.poll_events()


def main():
    """ create a window, add scene objects, then run rendering loop """
    viewer = Viewer(256, 256)

    # if len(sys.argv) < 2:
    #     print('Cylinder skinning demo.')
    #     print('Note:\n\t%s [3dfile]*\n\n3dfile\t\t the filename of a model in'
    #           ' format supported by pyassimp.' % sys.argv[0])
    #     viewer.add(SkinnedCylinder())
    # else:
    #     viewer.add(*[m for file in sys.argv[1:] for m in load_skinned(file)])

    viewer.add(*load_mesh('assets/rock.fbx'))
    # viewer.add(*load_mesh('model_normalized.obj'))
    # viewer.add(*load_mesh('model_normalized (2).obj'))
    # viewer.add(*load_mesh('model_normalized (3).obj'))
    # start rendering loop

    # rho_ins = [96]
    # phi_degs = [20, 40]
    # theta_delta_deg = 32
    # theta_degs = np.linspace(0, 360, theta_delta_deg).astype(np.int)
    # total = len(rho_ins)*len(phi_degs)*len(theta_degs)
    # sys.exit()
    viewer.run()
    
    # viewer.render2image(load_mesh('model_normalized.obj'), rho_ins, phi_degs, theta_degs)
    # viewer.render2image(load_mesh('model_normalized (2).obj'), rho_ins, phi_degs, theta_degs)
    # viewer.render2image(load_mesh('model_normalized (3).obj'), rho_ins, phi_degs, theta_degs)



if __name__ == '__main__':
    glfw.init()                # initialize window system glfw
    main()                     # main function keeps variables locally scoped
    glfw.terminate()           # destroy all glfw windows and GL contexts