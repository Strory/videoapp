from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

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


@app.post("/upload")
async def upload_video(video: UploadFile = File(...)):
    # Сохраняем файл на диск (можно поменять на любую директорию)
    file_location = f"uploaded_videos/{video.filename}"

    # Читаем содержимое файла и записываем его
    with open(file_location, "wb") as f:
        content = await video.read()
        f.write(content)

    print(f"Файл {video.filename} успешно сохранён по адресу {file_location}")

    return JSONResponse(content={"status": "success", "filename": video.filename})


