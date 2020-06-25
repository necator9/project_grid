# Created by Ivan Matveev at 25.06.20
# E-mail: ivan.matveev@hs-anhalt.de

import numpy as np

cam_param = {'rpi': {'mtx': np.array([[613, 0., 512],
                                      [0., 613, 354.82125218],
                                      [0., 0., 1.]]),
                     'base_res': (1024, 768),
                     'dist': np.array([[-0.33212234, 0.13364714, 0.0004479, -0.00159172, -0.02811601]])}}


scene = {'lamp_pole_1': {'angle': -39, 'height': -3.325, 'cam': cam_param['rpi'], 'img_path': 'scenes/lamp_pole_1_2.png'}}
