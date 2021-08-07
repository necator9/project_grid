# Created by Ivan Matveev at 25.06.20
# E-mail: ivan.matveev@hs-anhalt.de

import numpy as np

cam_param = {'rpi': {'mtx': np.array([[602.17434328, 0., 511.32476428],  # Optical center was corrected manually
                                      [0., 601.27444228, 334.8572872],
                                      [0., 0., 1.]]),
                     'base_res': (1024, 768),
                     'dist': np.array([[-0.321267, 0.11775163, 0.00091285, 0.0007689, -0.02101163]]),
                     'fl_mm': 2.2},

             'rpi_opt': {'mtx': np.array([[464.4719696, 0., 517.5116402],  # alpha = 0.5
                                          [0., 462.89021301, 365.84214009],
                                          [0., 0., 1., ]]),
                         'base_res': (1024, 768),
                         'dist': np.array([[0, 0, 0, 0, 0]]),
                         'fl_mm': 2.2},

             'hd_3000_sc1': {'mtx': np.array([[693.38863768, 0., 339.53274061],
                                              [0., 790.71040995, 236.18033069],
                                              [0., 0., 1.]]),
                             'base_res': (640, 480),
                             'dist': np.array([[0.21584076, -1.58033256, -0.00369491, 0.00366677, 2.94284061]]),
                             'fl_mm': 2.2},
             'hd_3000_sc2': {'mtx': np.array([[693.38863768, 0., 339.53274061],
                                              [0., 690.71040995, 236.18033069],
                                              [0., 0., 1.]]),
                             'base_res': (640, 480),
                             'dist': np.array([[0.21584076, -1.58033256, -0.00369491, 0.00366677, 2.94284061]]),
                             'fl_mm': 2.2},
             'cctv': {'mtx': np.array([[1.33528711e+03, 0.00000000e+00, 5.95825150e+02],
                                       [0.00000000e+00, 1.33790643e+03, 3.57672066e+02],
                                       [0.00000000e+00, 0.00000000e+00, 1.00000000e+00]]),
                      'base_res': (1280, 720),
                      'dist': np.array([[-3.99390135e-01, -2.87038173e-01, -1.87622642e-03, 2.57836298e-03,
                                         1.95568750e+00]]),
                      'fl_mm': 3.6}
             }

scene = {'lamp_pole_1': {'angle': -43, 'height': -3.325, 'cam': cam_param['rpi'],
                         'img_path': 'scenes/lamp_pole_1_4.jpg',
                         'distorted': True,
                         'img_res_cap': (1024, 768)},
         'lamp_pole_opt': {'angle': -39, 'height': -3.325, 'cam': cam_param['rpi_opt'],
                           'img_path': 'scenes/lamp_pole_opt_mtx_2.png',
                           'distorted': False,
                           'img_res_cap': (1024, 768)},
         'scene_1_TZK': {'angle': -13, 'height': -3.1, 'cam': cam_param['hd_3000_sc1'],
                         'img_path': 'scenes/29.jpg',
                         'distorted': True,
                         'img_res_cap': (320, 240)},
         'scene_2_TZK': {'angle': -22, 'height': -3, 'cam': cam_param['hd_3000_sc2'],
                         'img_path': 'scenes/scene_2_1.png',
                         'distorted': True,
                         'img_res_cap': (320, 240)},
         'synth_1': {'angle': -30, 'height': -10, 'cam': None,
                     'img_path': 'scenes/synth_3.png',
                     'distorted': None,
                     'img_res_cap': (640, 480)},
         'scene_3_sasha': {'angle': -16.4, 'height': -4.9, 'cam': cam_param['cctv'],
                           'img_path': 'scenes/scene_3_0.jpg',
                           'distorted': False,
                           'img_res_cap': (320, 240)}
         }
