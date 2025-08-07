import json
import math

import numpy as np


def angle_to_json(file_name: str, uuid: str):
    with open(f"temp_poses/{file_name}", "r", encoding='utf-8') as f:
        data = json.load(f)
    angles_list = [pose_to_angle2(frame['landmarks']) for frame in data['frames'] if frame['landmarks']]
    with open(f"temp_angles/{uuid}angles.json", "w", encoding="utf-8") as f:
        json.dump(angles_list, f, indent=2, ensure_ascii=False)


def pose_to_angle(pose: list) -> dict:
    RIGHT_SHOULDER = pose[12]
    RIGHT_ELBOW = pose[14]
    a = RIGHT_ELBOW['y'] - RIGHT_SHOULDER['y']
    b = RIGHT_ELBOW['x'] - RIGHT_SHOULDER['x']
    c = math.sqrt(a ** 2 + b ** 2)
    sin_alpha = b / c
    alpha = math.asin(sin_alpha)

    res = {'Shoulder pitch': 0, 'Shoulder roll': alpha, 'Shoulder yaw': 0, 'Elbow pitch': 0,
           'Wrist yaw': 0, 'Wrist roll': 0, 'Wrist pitch': 0}
    return res


def pose_to_angle2(pose: list) -> dict:
    RIGHT_SHOULDER = pose[12]
    RIGHT_ELBOW = pose[14]
    RIGHT_WRIST = pose[16]
    LEFT_SHOULDER = pose[11]
    LEFT_ELBOW = pose[13]
    LEFT_WRIST = pose[15]

    vec1 = np.array([RIGHT_ELBOW['x'] - RIGHT_SHOULDER['x'], -1 * (RIGHT_ELBOW['y'] - RIGHT_SHOULDER['y'])])
    vec2 = np.array([RIGHT_WRIST['x'] - RIGHT_ELBOW['x'], -1 * (RIGHT_WRIST['y'] - RIGHT_ELBOW['y'])])
    vec3 = np.array([LEFT_ELBOW['x'] - LEFT_SHOULDER['x'], -1 * (LEFT_ELBOW['y'] - LEFT_SHOULDER['y'])])
    vec4 = np.array([LEFT_WRIST['x'] - LEFT_ELBOW['x'], -1 * (LEFT_WRIST['y'] - LEFT_ELBOW['y'])])

    res = {'right_arm': {'Shoulder roll': angle_with_x_axis(vec1), 'Elbow pitch': directed_angle(vec1, vec2)},
           'left_arm': {'Shoulder roll': angle_with_x_axis(vec3), 'Elbow pitch': directed_angle(vec3, vec4)}}
    return res


def directed_angle(a, b):
    dot = np.dot(a, b)
    det = a[0] * b[1] - a[1] * b[0]
    return np.arctan2(det, dot)


def angle_with_x_axis(v):
    return np.arctan2(v[1], v[0])
