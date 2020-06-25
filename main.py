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


sc_name = 'lamp_pole_1'

scene = camera_parameters.scene[sc_name]
cam = scene['cam']

intrinsic = cam['mtx']
dist = cam['dist']
img_res = cam['base_res']

angle = scene['angle']
height = scene['height']
image_path = scene['img_path']

fl_mm = 2.2
fx_px, fy_px = intrinsic[0][0], intrinsic[1][1]
sens_dim = calc_sens_dim((fx_px, fy_px), fl_mm, img_res)
intrinsic_local = (np.asarray(img_res), fl_mm, np.asarray(sens_dim))

x = 1
y = height
vertices_bottom = np.array(list(itertools.product([x], [y], np.arange(2, 12, 1), [1])))
vertices_bottom1 = np.array(list(itertools.product([x + 0.5], [y], np.arange(2, 12, 1), [1])))
vertices_bottom2 = np.array(list(itertools.product([x - 0.5], [y], np.arange(2, 12, 1), [1])))
vertices_up = np.array(list(itertools.product([x + 0.1], [y + 1.83], np.arange(2, 12, 1), [1])))

vertices = np.vstack((vertices_bottom, vertices_up, vertices_bottom1, vertices_bottom2))

rw_system = t3d.Handler3D(vertices, operations=['rx'], k=intrinsic_local)
rw_system.transform(np.deg2rad(angle))

image = cv2.imread(image_path, 0)
ud_image = cv2.undistort(image, intrinsic, dist)

plt.imshow(ud_image, cmap='gray', vmin=0, vmax=255)
plt.scatter(rw_system.img_points[:, 0], rw_system.img_points[:, 1], s=1, color='red')
plt.show()
