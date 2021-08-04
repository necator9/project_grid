# Created by Ivan Matveev at 25.06.20
# E-mail: ivan.matveev@hs-anhalt.de
import camera_parameters
import lib_transform_3d as t3d
import matplotlib.pyplot as plt
import cv2
import numpy as np
import itertools


def calc_sens_dim(f_px, fmm, img_res):
    def calc(fmm, res, fpx):
        return fmm * res / fpx

    fxpx, fypx = f_px
    return calc(fmm, img_res[0], fxpx), calc(fmm, img_res[1], fypx)


def scale_intrinsic(new_res, base_res, intrinsic):
    scale_f = np.asarray(base_res) / np.asarray(new_res)
    if scale_f[0] != scale_f[1]:
        print('WARNING! The scaling is not proportional', scale_f)

    intrinsic[0, :] /= scale_f[0]
    intrinsic[1, :] /= scale_f[1]

    return intrinsic


def parse_3d_obj_file(path):
    """
    Convert vertices to np.array([N, 4]) in homogeneous form.
    Faces are converted to np.array([M, 3]), therefore faces must be preliminary triangulated
    :param path: path to wavefront.obj file
    :return: np.array(vertices), np.array(faces)
    """
    def parse_string(string):
        spl = [el.split('//') for el in string.split()]
        res = [el[0] for i, el in enumerate(spl) if i != 0]
        return res

    with open(path, "r") as fi:
        lines = fi.readlines()

    vertices = np.array([parse_string(ln) for ln in lines if ln.startswith("v")], dtype='float')
    faces = [parse_string(ln) for ln in lines if ln.startswith("f")]
    faces = np.asarray([[int(el) for el in ln] for ln in faces]) - 1

    vertices = np.hstack((vertices, np.ones((vertices.shape[0], 1))))  # Bring to homogeneous form

    return vertices, faces


# sc_name = 'lamp_pole_1'
sc_name = 'synth_1'
# sc_name = 'scene_1_TZK'
# sc_name = 'scene_2_TZK'

scene = camera_parameters.scene[sc_name]
img_res = scene['img_res_cap']


angle = scene['angle']
height = scene['height']
image_path = scene['img_path']

fl_mm = 3.67
cx, cy = img_res[0] / 2, img_res[1] / 2
sens_dim = (4.8, 3.6)
intrinsic_local = (np.asarray(img_res), fl_mm, np.asarray(sens_dim), (cx, cy))

x = 0
y = height
dist_range = np.arange(1, 12, 1)
grid_bottom = np.array(list(itertools.product([x], [y], dist_range, [1])))
grid_bottom_r = np.array(list(itertools.product([x + 0.5], [y], dist_range, [1])))
grid_bottom_l = np.array(list(itertools.product([x - 0.5], [y], dist_range, [1])))
grid_up = np.array(list(itertools.product([x + 0.1], [y + 1.8], dist_range, [1])))

grid = np.vstack((grid_bottom, grid_bottom_r, grid_bottom_l, grid_up))
rw_system_grid = t3d.Handler3D(grid, operations=['rx'], k=intrinsic_local)
rw_system_grid.transform(np.deg2rad(angle))

object_distance = 12.27
vertices_ob, faces = parse_3d_obj_file('scenes/test-obj.obj')
rw_system = t3d.Handler3D(vertices_ob, operations=['s', 'ry', 't', 'rx'], k=intrinsic_local)
rw_system.transform((True, np.asarray([0, 1.8, 0])), np.deg2rad(90), np.asarray([x, height, object_distance]),
                    np.deg2rad(angle))  # Transform object in 3D space and project to image plane

image = cv2.imread(image_path, 0)

clahe_adjust = cv2.createCLAHE(clipLimit=8, tileGridSize=(8, 8))
image = clahe_adjust.apply(image)

plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.scatter(rw_system.img_points[:, 0], rw_system.img_points[:, 1], s=0.5, color='red')
plt.scatter(rw_system_grid.img_points[:, 0], rw_system_grid.img_points[:, 1], s=1, color='red')
plt.show()
