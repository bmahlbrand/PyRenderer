import sys, os

sys.path.insert(0,"E:\workspace\assimp\build\code\Release")

import pyassimp
import pyassimp.postprocess

from Mesh import *
from Transform import *

def computeCenter(vertices):

    centerOfMass = [0., 0., 0.]

    for v in vertices:
        centerOfMass += v

    for comp in v:
        centerOfMass[comp] /= len(vertices)

    return centerOfMass

def translate(vertices, pos):

    ret = vertices

    for v in vertices:
        v += pos
        
        ret.append(v)

    return ret

def scale(vertices, scaleV):

    ret = vertices

    for v in vertices:
        v *= scaleV
        
        ret.append(v)

    return ret

def scaleByCenter(vertices):

    center = computeCenter(vertices)

    vertices = translate([c * -1. for c in center])
    vertices = scale(vertices)
    vertices = translate(center)

    return vertices

def computeAABB(vertices):
    mi = [1000000, 1000000, 1000000]
    ma = [0, 0, 0]

    for v in vertices:
        mi[0] = min(mi[0], v[0])
        mi[1] = min(mi[1], v[1])
        mi[2] = min(mi[2], v[2])

        ma[0] = ma(ma[0], v[0])
        ma[1] = ma(ma[1], v[1])
        ma[2] = ma(ma[2], v[2])

    return mi, ma

def scaleByAABB(vertices):
    mi, ma = computeAABB(vertices)



    ret = []

    for v in vertices:
        v *= ( 1. / np.linalg.norm(ma - mi))
        ret.append(v)

def recur_node(node,level = 0):
    print("  " + "\t" * level + "- " + str(node))
    for child in node.children:
        recur_node(child, level + 1)

def load_mesh(filename):

    meshes = []

    scene = pyassimp.load(filename, processing=pyassimp.postprocess.aiProcess_Triangulate)
    
    #the model we load
    print("MODEL:" + filename)
    print
    
    #write some statistics
    print("SCENE:")
    print("  meshes:" + str(len(scene.meshes)))
    print("  materials:" + str(len(scene.materials)))
    print("  textures:" + str(len(scene.textures)))
    print
    
    print("NODES:")
    recur_node(scene.rootnode)

    print
    print("MESHES:")
    for index, mesh in enumerate(scene.meshes):
        print("  MESH" + str(index+1))
        print("    material id:" + str(mesh.materialindex+1))
        print("    vertices:" + str(len(mesh.vertices)))
        print("    first 3 verts:\n" + str(mesh.vertices[:3]))

        if mesh.normals.any():
                print("    first 3 normals:\n" + str(mesh.normals[:3]))
        else:
                print("    no normals")
        print("    colors:" + str(len(mesh.colors)))
        tcs = mesh.texturecoords
        if tcs.any():
            for index, tc in enumerate(tcs):
                print("    texture-coords "+ str(index) + ":" + str(len(tcs[index])) + "first3:" + str(tcs[index][:3]))

        else:
            print("    no texture coordinates")
        print("    uv-component-count:" + str(len(mesh.numuvcomponents)))
        print("    faces:" + str(len(mesh.faces)) + " -> first:\n" + str(mesh.faces[:3]))
        print("    bones:" + str(len(mesh.bones)) + " -> first:" + str([str(b) for b in mesh.bones[:3]]))
        print

        # colors = np.array([])
        # colors = np.empty((0, 3))

        # for i in range(len(mesh.vertices)):
            # np.append(colors, [1., 0., 1.], axis = 0)

        # print(mesh.vertices)
        # print(colors)

        

        meshes.append(Mesh([mesh.vertices, mesh.vertices]))
    # print("ANIMATIONS:")
    # for animation in enumerate(scene.animations):
    #     for joint in enumerate(animation):
    #         if joint[1]:
    #             print(joint[1])
    #     # ----- load animations
    # def conv(assimp_keys, ticks_per_second):
    #     """ Conversion from assimp key struct to our dict representation """
    #     return {key.time / ticks_per_second: key.value for key in assimp_keys}

    # transform_keyframes = {}
    
    # if scene.animations:
    #     anim = scene.animations[0]
    #     for channel in anim.channels:
    #         print(channel.nodename)
    #         # for each animation bone, store trs dict with {times: transforms}
    #         # (pyassimp name storage bug, bytes instead of str => convert it)
    #         transform_keyframes[channel.nodename.data.decode('utf-8')] = (
    #             conv(channel.positionkeys, anim.tickspersecond),
    #             conv(channel.rotationkeys, anim.tickspersecond),
    #             conv(channel.scalingkeys, anim.tickspersecond)
    #         )
    # print(transform_keyframes)

    print("MATERIALS:")
    for index, material in enumerate(scene.materials):
        print("  MATERIAL (id:" + str(index+1) + ")")
        for key, value in material.properties.items():
            print("    %s: %s" % (key, value))
    print()
    
    print("TEXTURES:")
    for index, texture in enumerate(scene.textures):
        print("  TEXTURE" + str(index+1))
        print("    width:" + str(texture.width))
        print("    height:" + str(texture.height))
        print("    hint:" + str(texture.achformathint))
        print("    data (size):" + str(len(texture.data)))
   
    # Finally release the model
    pyassimp.release(scene)
    # print(meshes)
    
    return meshes