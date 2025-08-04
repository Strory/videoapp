import json
import math


def angle_to_json(file_name: str, uuid: str):
    with open(f"temp_poses/{file_name}", "r", encoding='utf-8') as f:
        data = json.load(f)
    angles_list = [pose_to_angle(frame['landmarks']) for frame in data['frames']]
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
