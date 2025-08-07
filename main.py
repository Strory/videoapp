from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Form, Header
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import threading
from processing_service.video_to_json import video_to_pose
from processing_service.pose_to_angles import angle_to_json
from processing_service.video_cropping import cropping_video
from processing_service.angles_to_videos import build_movie
from database_app.requests_bd import add_video_data

app = FastAPI()

# Разрешаем все запросы со всех источников (для разработки)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/endpoint")
async def receive_data(request: Request):
    data = await request.json()  # Получаем JSON из запроса
    print("Получены данные:", data)
    return JSONResponse(content={"status": "ok it is server", "received": "ok it is server"})


@app.get("/api/e2")
async def test():
    return "Hello world"


@app.post("/upload4")
async def upload_request(request: Request):
    body = await request.body()

    # 🔽 Сохраняем "как есть" в файл
    with open("debug_request.bin", "wb") as f:
        f.write(body)

    print(f"💾 Тело запроса сохранено в debug_request.bin ({len(body)} байт)")
    print("Заголовки:")
    for k, v in request.headers.items():
        print(f"  {k}: {v}")

    return {"status": "success"}


@app.get("/api/video1")
async def send_video1(authorization: str = Header(...)):

    return FileResponse(
        path='cropping_videos/4ebfc8fb-a96b-481f-adbb-7e52663a9dc2.mp4',
        media_type="video/mp4",
        filename=f"video1.mp4"
    )


@app.get("/api/video2")
async def send_video2(authorization: str = Header(...)):

    return FileResponse(
        path='temp_movie/4ebfc8fb-a96b-481f-adbb-7e52663a9dc2movie.mp4',
        media_type="video/mp4",
        filename=f"video2.mp4"
    )


@app.post("/upload")
async def upload_video(video: UploadFile = File(...),
                       tg_id: str = File(...),
                       first_name: str = File(...),
                       last_name: str = File(...),
                       user_name: str = File(...),
                       language_code: str = File(...),
                       is_premium: bool = File(...),
                       start_time: float = File(...),
                       end_time: float = File(...),
                       description: str = File(...)):
    """
    Загружает видео и сохраняет с уникальным именем
    """
    print(f"📹 Видео: {video.filename}")
    # print(f"\n👤 Пользователь Telegram:")
    print(f"   ID: {tg_id}")
    print(f"   Имя: {first_name}")
    print(f"   Фамилия: {last_name}")
    print(f"   Username: @{user_name}")
    print(f"   LanguageCode: {language_code}")
    print(f"   is Premium?: {is_premium}")
    print(f"   Начало: {start_time} сек")
    print(f"   Конец: {end_time} сек")
    print(f"   Описание: {description}")

    try:
        # Генерируем уникальное имя файла
        file_extension = video.filename.split('.')[-1] if '.' in video.filename else 'mp4'

        unique_filename = f"{uuid.uuid4()}"
        full_filename = f"{unique_filename}.{file_extension}"
        file_location = f"uploaded_videos/{full_filename}"

        # Сохраняем файл
        with open(file_location, "wb") as f:
            content = await video.read()
            f.write(content)

        print(f"Видео сохранено: {file_location}")
        # if tg_id != 'null':
        #     thread = threading.Thread(
        #         target=video_processing_request,
        #         args=(unique_filename, file_extension, int(tg_id), start_time, end_time)
        #     )
        #     thread.start()

        thread = threading.Thread(
            target=video_processing_request,
            args=(unique_filename, file_extension, 123, start_time, end_time)
        )
        thread.start()

        return JSONResponse(content={
            "status": "success",
            "message": "Видео успешно загружено",
            "filename": unique_filename,
            "file_path": file_location
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка загрузки: {str(e)}")


def video_processing_request(video_name: str, extension: str, tg_id: int, start_time: str, end_time: str):
    if cropping_video(video_name, extension, start_time, end_time):
        video_to_pose(video_name, extension)
        angle_to_json(f"{video_name}pose.json", video_name)
        build_movie(video_name, f"{video_name}angles.json")
        video_data = {'video_path': f"cropping_videos/{video_name}.{extension}",
                      'pose_path': f"temp_poses/{video_name}pose.json",
                      'angle_path': f"{video_name}angles.json", 'description': "description"}
        add_video_data(video_data, tg_id)



