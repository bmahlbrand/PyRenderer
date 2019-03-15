from Transform import *

class Trackball:
    """Virtual trackball for 3D scene viewing. Independent of window system."""

    def __init__(self, yaw=0., roll=0., pitch=0., distance=6., radians=None):
        """ Build a new trackball with specified view, angles in degrees """
        self.rotation = quaternion_from_euler(yaw, roll, pitch, radians)
        self.distance = max(distance, 0.001)
        self.pos2d = vec(0.0, 0.0)

    def drag(self, old, new, winsize):
        """ Move trackball from old to new 2d normalized window position """
        old, new = ((2*vec(pos) - winsize) / winsize for pos in (old, new))
        self.rotation = quaternion_mul(self._rotate(old, new), self.rotation)

    def zoom(self, delta, size):
        """ Zoom trackball by a factor delta normalized by window size """
        self.distance = max(0.001, self.distance * (1 - 50*delta/size))

    def pan(self, old, new):
        """ Pan in camera's reference by a 2d vector factor of (new - old) """
        self.pos2d += (vec(new) - old) * 0.001 * self.distance

    def view_matrix(self):
        """ View matrix transformation, including distance to target point """
        return translate(*self.pos2d, -self.distance) @ self.matrix()

    def projection_matrix(self, winsize):
        """ Projection matrix with z-clipping range adaptive to distance """
        z_range = vec(0.1, 100) * self.distance  # proportion to dist
        return perspective(35, winsize[0] / winsize[1], *z_range)

    def matrix(self):
        """ Rotational component of trackball position """
        return quaternion_matrix(self.rotation)

    def _project3d(self, position2d, radius=0.8):
        """ Project x,y on sphere OR hyperbolic sheet if away from center """
        p2, r2 = sum(position2d*position2d), radius*radius
        zcoord = math.sqrt(r2 - p2) if 2*p2 < r2 else r2 / (2*math.sqrt(p2))
        return vec(*position2d, zcoord)

    def _rotate(self, old, new):
        """ Rotation of axis orthogonal to old & new's 3D ball projections """
        old, new = (normalized(self._project3d(pos)) for pos in (old, new))
        phi = 2 * math.acos(np.clip(np.dot(old, new), -1, 1))
        return quaternion_from_axis_angle(np.cross(old, new), radians=phi)