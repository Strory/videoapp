from fastapi import FastAPI, Request, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import threading
from processing_service.video_to_json import video_to_pose
from processing_service.pose_to_angles import angle_to_json
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
        if tg_id != 'null':
            thread = threading.Thread(
                target=video_processing_request,
                args=(unique_filename, file_extension, int(tg_id))
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


def video_processing_request(video_name: str, extension: str, tg_id: int):
    video_to_pose(video_name, extension)
    angle_to_json(f"{video_name}pose.json", video_name)
    video_data = {'video_path': f"uploaded_videos/{video_name}.{extension}",
                  'pose_path': f"temp_poses/{video_name}pose.json",
                  'angle_path': f"{video_name}angles.json", 'description': "description"}
    add_video_data(video_data, tg_id)
