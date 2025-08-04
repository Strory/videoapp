import cv2
import mediapipe as mp
import json


def video_to_pose(video_name: str, extension: str):
    # Инициализация MediaPipe
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose(static_image_mode=False, model_complexity=1, enable_segmentation=False,
                        min_detection_confidence=0.5)

    # Открытие видео
    cap = cv2.VideoCapture(f"uploaded_videos/{video_name}.{extension}")

    # Получение метаинформации
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Структура для сохранения данных
    video_data = {
        "metadata": {
            "fps": fps,
            "total_frames": total_frames,
            "width": width,
            "height": height
        },
        "frames": []
    }

    frame_index = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)

        frame_data = {
            "frame_index": frame_index,
            "timestamp": frame_index / fps,  # Время в секундах
            "landmarks": []
        }

        if results.pose_landmarks:
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                landmark_data = {
                    "index": idx,
                    "x": landmark.x,
                    "y": landmark.y,
                    "z": landmark.z,
                    "visibility": landmark.visibility if hasattr(landmark, 'visibility') else None
                }
                frame_data["landmarks"].append(landmark_data)

        video_data["frames"].append(frame_data)
        frame_index += 1

    cap.release()

    # Сохранение в JSON файл
    with open(f"temp_poses/{video_name}pose.json", "w", encoding="utf-8") as f:
        json.dump(video_data, f, indent=2, ensure_ascii=False)
