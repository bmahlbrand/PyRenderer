import OpenGL.GL as GL
import glfw

from Transform import translate, scale, identity, sincos
from Transform import (lerp, quaternion_slerp, quaternion_matrix, quaternion,
                       quaternion_from_euler)

import numpy as np

class Node:
    """ Scene graph transform and parameter broadcast node """

    def __init__(self, name='', children=(), transform=identity(), **param):
        self.transform, self.param, self.name = transform, param, name
        self.children = list(iter(children))

    def add(self, *drawables):
        """ Add drawables to this node, simply updating children list """
        self.children.extend(drawables)

    def draw(self, projection, view, model, **param):
        """ Recursive draw, passing down named parameters & model matrix. """
        # merge named parameters given at initialization with those given here
        param = dict(param, **self.param)
        # model = model @ self.transform
        model = np.matmul(model, self.transform)
        for child in self.children:
            child.draw(projection, view, model, **param)


# -------------- Keyframing Utilities TP6 ------------------------------------
class KeyFrames:
    """ Stores keyframe pairs for any value type with interpolation_function"""
    def __init__(self, time_value_pairs, interpolation_function=lerp):
        if isinstance(time_value_pairs, dict):  # convert to list of pairs
            time_value_pairs = time_value_pairs.items()
        keyframes = sorted(((key[0], key[1]) for key in time_value_pairs))
        self.times, self.values = zip(*keyframes)  # pairs list -> 2 lists
        self.interpolate = interpolation_function

    def value(self, time):
        """ Computes interpolated value from keyframes, for a given time """

        # 1. ensure time is within bounds else return boundary keyframe
        ...  # TODO: insert your code from TP6 here

        # 2. search for closest index entry in self.times, using bisect_left
        ...  # TODO: insert your code from TP6 here

        # 3. using the retrieved index, interpolate between the two neighboring
        # values in self.values, using the stored self.interpolate function
        ...
        return ...  # TODO: insert your code from TP6 here


class TransformKeyFrames:
    """ KeyFrames-like object dedicated to 3D transforms """
    def __init__(self, translate_keys, rotate_keys, scale_keys):
        """ stores 3 keyframe sets for translation, rotation, scale """
        ...  # TODO: insert your code from TP6 here

    def value(self, time):
        """ Compute each component's interpolation and compose TRS matrix """
        ...  # TODO: insert your code from TP6 here
        return ...


class KeyFrameControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, trans_keys, rotat_keys, scale_keys, **kwargs):
        super().__init__(**kwargs)
        self.keyframes = TransformKeyFrames(trans_keys, rotat_keys, scale_keys)

    def draw(self, projection, view, model, **param):
        """ When redraw requested, interpolate our node transform from keys """
        self.transform = self.keyframes.value(glfw.get_time())
        super().draw(projection, view, model, **param)


class SkinningControlNode(Node):
    """ Place node with transform keys above a controlled subtree """
    def __init__(self, *keys, **kwargs):
        super().__init__(**kwargs)
        self.keyframes = TransformKeyFrames(*keys) if keys[0] else None
        self.world_transform = identity()

    def draw(self, projection, view, model, **param):
        """ When redraw requested, interpolate our node transform from keys """
        # if self.keyframes:  # no keyframe update should happens if no keyframes
        #     self.transform = self.keyframes.value(glfw.get_time())
        # else:
        self.transform = identity()
        # print(self.keyframes)
        # print(model)
        # store world transform for skinned meshes using this node as bone
        # self.world_transform = np.matmul(model, self.transform)
        self.world_transform = model
        # default node behaviour (call children's draw method)
        super().draw(projection, view, model, **param)