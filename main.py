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


# sc_name = 'lamp_pole_1'
sc_name = 'lamp_pole_opt'
# sc_name = 'scene_1_TZK'
# sc_name = 'scene_2_TZK'

scene = camera_parameters.scene[sc_name]
cam = scene['cam']
img_res = scene['img_res_cap']

intrinsic = scale_intrinsic(scene['img_res_cap'], cam['base_res'], cam['mtx'])
dist = cam['dist']


angle = scene['angle']
height = scene['height']
image_path = scene['img_path']

fl_mm = 2.2
fx_px, fy_px = intrinsic[0][0], intrinsic[1][1]
cx, cy = intrinsic[0][2], intrinsic[1][2]
sens_dim = calc_sens_dim((fx_px, fy_px), fl_mm, img_res)
intrinsic_local = (np.asarray(img_res), fl_mm, np.asarray(sens_dim), (cx, cy))

x = 1
y = height
dist_range = np.arange(1, 12, 1)
vertices_bottom = np.array(list(itertools.product([x], [y], dist_range, [1])))
vertices_bottom1 = np.array(list(itertools.product([x + 0.5], [y], dist_range, [1])))
vertices_bottom2 = np.array(list(itertools.product([x - 0.5], [y], dist_range, [1])))
vertices_up = np.array(list(itertools.product([x + 0.1], [y + 1.8], dist_range, [1])))

vertices = np.vstack((vertices_bottom, vertices_up, vertices_bottom1, vertices_bottom2))

rw_system = t3d.Handler3D(vertices, operations=['rx'], k=intrinsic_local)
rw_system.transform(np.deg2rad(angle))

image = cv2.imread(image_path, 0)
ud_image = cv2.undistort(image, intrinsic, dist)
clahe_adjust = cv2.createCLAHE(clipLimit=8, tileGridSize=(8, 8))
ud_image = clahe_adjust.apply(ud_image)

plt.imshow(ud_image, cmap='gray', vmin=0, vmax=255)
plt.scatter(rw_system.img_points[:, 0], rw_system.img_points[:, 1], s=1, color='red')
plt.show()
