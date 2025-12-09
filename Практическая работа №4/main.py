import io
from typing import List, Optional, Union
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from bson import ObjectId

# user id 693844b05b6eff4365f9e78d
# survey id 693845575b6eff4365f9e78e
# file id 693846c55b6eff4365f9e78f

# Настройки
MONGO_URL = "mongodb://127.0.0.1:27017"
DB_NAME = "survey_db"

app = FastAPI(title="Практическая работа №4: Опросы + GridFS")

# Глобальные переменные для БД (будут инициализированы при старте)
client: AsyncIOMotorClient = None
db = None
fs = None


# --- Инициализация БД при запуске сервера ---
@app.on_event("startup")
async def startup_db_client():
    global client, db, fs
    # Создаем подключение ВНУТРИ цикла событий
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    fs = AsyncIOMotorGridFSBucket(db)
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_db_client():
    global client
    if client:
        client.close()
    print("Disconnected from MongoDB")


# --- Модели данных (Pydantic) ---
class Question(BaseModel):
    q_id: int
    text: str
    type: str


class UserCreate(BaseModel):
    username: str
    email: str


class User(UserCreate):
    id: str = Field(alias="_id")


class SurveyCreate(BaseModel):
    title: str
    description: str
    owner_id: str
    questions: List[Question]


class Survey(SurveyCreate):
    id: str = Field(alias="_id")
    banner_image_id: Optional[str] = None


class Answer(BaseModel):
    q_id: int
    value: Union[str, int]


class SubmissionCreate(BaseModel):
    survey_id: str
    respondent_email: str
    answers: List[Answer]


# --- API Методы ---

# 1. USERS
@app.post("/users/", response_model=User, tags=["Users"])
async def create_user(user: UserCreate):
    # Исправлено .dict() -> .model_dump()
    new_user = await db.users.insert_one(user.model_dump())
    created_user = await db.users.find_one({"_id": new_user.inserted_id})
    created_user["_id"] = str(created_user["_id"])
    return created_user


@app.get("/users/", response_model=List[User], tags=["Users"])
async def get_users():
    users = []
    async for user in db.users.find():
        user["_id"] = str(user["_id"])
        users.append(user)
    return users


# 2. SURVEYS (CRUD)
@app.post("/surveys/", response_model=Survey, tags=["Surveys"])
async def create_survey(survey: SurveyCreate):
    # Исправлено .dict() -> .model_dump()
    survey_dict = survey.model_dump()

    # Проверка юзера
    user_exists = await db.users.find_one({"_id": ObjectId(survey.owner_id)})
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")

    survey_dict["banner_image_id"] = None
    new_survey = await db.surveys.insert_one(survey_dict)
    created_survey = await db.surveys.find_one({"_id": new_survey.inserted_id})
    created_survey["_id"] = str(created_survey["_id"])
    return created_survey


@app.get("/surveys/", response_model=List[Survey], tags=["Surveys"])
async def get_surveys():
    surveys = []
    async for s in db.surveys.find():
        s["_id"] = str(s["_id"])
        if s.get("banner_image_id"):
            s["banner_image_id"] = str(s["banner_image_id"])
        surveys.append(s)
    return surveys


# 3. GridFS: Загрузка файла
@app.post("/surveys/{survey_id}/upload-banner", tags=["GridFS"])
async def upload_banner(survey_id: str, file: UploadFile = File(...)):
    file_content = await file.read()

    # GridFS bucket (fs) уже инициализирован в startup
    grid_in = fs.open_upload_stream(
        file.filename,
        metadata={"content_type": file.content_type}
    )
    await grid_in.write(file_content)
    await grid_in.close()

    await db.surveys.update_one(
        {"_id": ObjectId(survey_id)},
        {"$set": {"banner_image_id": grid_in._id}}
    )
    return {"status": "uploaded", "file_id": str(grid_in._id)}


# 3. GridFS: Скачивание файла
@app.get("/surveys/{survey_id}/banner", tags=["GridFS"])
async def get_banner(survey_id: str):
    survey = await db.surveys.find_one({"_id": ObjectId(survey_id)})
    if not survey or not survey.get("banner_image_id"):
        raise HTTPException(status_code=404, detail="No banner")

    grid_out = await fs.open_download_stream(survey["banner_image_id"])

    return StreamingResponse(
        io.BytesIO(await grid_out.read()),
        media_type=grid_out.metadata.get("content_type")
    )

# 4. SUBMISSIONS (Ответы на опрос)
@app.post("/submissions/", tags=["Submissions"])
async def submit_survey(sub: SubmissionCreate):
    # Исправлено .dict() -> .model_dump()
    await db.submissions.insert_one(sub.model_dump())
    return {"message": "Saved"}


if __name__ == "__main__":
    import uvicorn

    # Оставляем порт 8001, чтобы не конфликтовать
    uvicorn.run(app, host="127.0.0.1", port=8001)