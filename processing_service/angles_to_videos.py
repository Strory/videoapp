import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import json
from PIL import Image
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip


def build_movie(name: str, angles_name: str):
    images = angles_to_movie(angles_name)
    fps = 25
    output_video = f'temp_movie/{name}movie.mp4'
    # Создаем видео
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_video, codec='libx264')

    print("Видео создано!")


def angles_to_movie(angles: str):
    with open(f"temp_angles/{angles}", "r", encoding='utf-8') as f:
        data = json.load(f)

    frames = []
    for angles in data:
        frames.append(generate_frame(4, angles['right_arm']['Shoulder roll'],
                                     angles['right_arm']['Elbow pitch'],
                                     angles['left_arm']['Shoulder roll'],
                                     angles['left_arm']['Elbow pitch']))
    return frames


def generate_frame(L, angle1_rad, angle2_rad, angle4_rad, angle5_rad):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-L * 2.3, L * 4)
    ax.set_ylim(-L * 2, L * 2)
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(True)

    x1_end = L * np.cos(angle1_rad)
    y1_end = L * np.sin(angle1_rad)
    ax.plot([0, x1_end], [0, y1_end], 'orange', linewidth=3, label=f'Line 1: {np.degrees(angle1_rad):.1f}°')

    angle2_abs = angle1_rad + angle2_rad
    x2_end = x1_end + L * np.cos(angle2_abs)
    y2_end = y1_end + L * np.sin(angle2_abs)
    ax.plot([x1_end, x2_end], [y1_end, y2_end], 'purple', linewidth=3, label=f'Line 2: Δ={np.degrees(angle2_rad):.1f}°')

    x3_end = 1.7 * L
    y3_end = 0
    ax.plot([0, x3_end], [0, y3_end], 'g-', linewidth=3, label='Line 3: 0°')

    x4_end = x3_end + L * np.cos(angle4_rad)
    y4_end = y3_end + L * np.sin(angle4_rad)
    ax.plot([x3_end, x4_end], [y3_end, y4_end], 'orange', linewidth=3, label=f'Line 4: {np.degrees(angle4_rad):.1f}°')

    angle5_abs = angle4_rad + angle5_rad
    x5_end = x4_end + L * np.cos(angle5_abs)
    y5_end = y4_end + L * np.sin(angle5_abs)
    ax.plot([x4_end, x5_end], [y4_end, y5_end], 'purple', linewidth=3, label=f'Line 5: Δ={np.degrees(angle5_rad):.1f}°')

    buf = BytesIO()
    plt.savefig(buf, format='png', dpi=100, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    img = Image.open(buf)
    return np.array(img)
