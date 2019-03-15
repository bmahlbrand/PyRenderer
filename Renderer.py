from shaders.color import *

from Mesh import *

from Transform import *

class ImageRenderer():
    def __init__(self, rho_ins, phi_degs, theta_degs):
        self.rho_ins = rho_ins
        self.phi_degs = phi_degs
        self.theta_degs = theta_degs
    
    def obj_centered_camera_pose(rho_in, phi_deg, theta_deg):
        phi, theta = np.radians((phi_deg, theta_deg))
        
        x = (rho_in * np.cos(theta) * np.cos(phi))
        y = (rho_in * np.sin(theta) * np.cos(phi))
        z = (rho_in * np.sin(phi))
        # print(vec(x, y, z))
        print(quaternion_matrix(quaternion_from_euler(rho_in, phi_deg, theta_deg, None)))
        # raise ValueError("bad")
        return quaternion_matrix(quaternion_from_euler(rho_in, phi_deg, theta_deg, None))
        # return lookat(vec(x, y, z), vec(0., 0., 0.), vec(0., 1., 0.))

    def render2folder(dirname, callback):
        k = 0
        for rho_in in self.rho_ins:
            for phi_deg in self.phi_degs:
                for theta_deg in self.theta_degs:
                    view = obj_centered_camera_pose(rho_in, phi_deg, (theta_deg+init_theta_deg)%360 )
                    fname = dirname/('image_%03d_p%03d_t%03d_r%03d.png'%(k, phi_deg, theta_deg, rho_in))
                    k += 1
                    callback(view)

def drawMesh(mesh, rho_in, phi_deg, theta_deg):
    pass

def drawSkinnedMesh():
    pass

if __name__ == '__main__':
    print(obj_centered_camera_pose(96., 32., 24.))