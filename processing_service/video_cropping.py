from moviepy import VideoFileClip


def cropping_video(file_name: str, extension: str, start_time: str, end_time: str) -> bool:
    try:
        start, end = float(start_time), float(end_time)
        if start < 0 or end < 0 or start >= end:
            raise ValueError("Invalid time range")
        clip = VideoFileClip(f"uploaded_videos/{file_name}.{extension}").subclipped(start, end)
        clip.write_videofile(f"cropping_videos/{file_name}.{extension}", codec="libx264")
        clip.close()
        return True
    except ValueError as e:
        print(f"Error cropping video: {e}")
        return False
