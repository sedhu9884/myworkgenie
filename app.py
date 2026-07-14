from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from tools.converter import convert

import os
import uuid
import logging

# -----------------------------
# Logging
# -----------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# -----------------------------
# App
# -----------------------------

app = FastAPI(
    title="MyWorkGeniee",
    version="1.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MAX_FILE_SIZE = 100 * 1024 * 1024

SUPPORTED = {
    "pdf_to_word": [".pdf"],
    "word_to_pdf": [".doc", ".docx"]
}

MEDIA = {
    ".pdf": "application/pdf",
    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
}


# -----------------------------
# Home
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# -----------------------------
# Convert
# -----------------------------

@app.post("/convert")
async def convert_document(

    background_tasks: BackgroundTasks,

    tool: str = Form(...),

    file: UploadFile = File(...)

):

    if tool not in SUPPORTED:

        raise HTTPException(
            400,
            "Unsupported conversion selected."
        )

    if not file.filename:

        raise HTTPException(
            400,
            "No file selected."
        )

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in SUPPORTED[tool]:

        raise HTTPException(
            400,
            f"Only {', '.join(SUPPORTED[tool])} files are supported."
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:

        raise HTTPException(
            400,
            "Maximum upload size is 100 MB."
        )

    unique_name = str(uuid.uuid4()) + extension

    upload_path = os.path.join(
        UPLOAD_FOLDER,
        unique_name
    )

    with open(upload_path, "wb") as f:
        f.write(contents)

    original_name = os.path.splitext(file.filename)[0]

    try:

        output_path = convert(
            tool,
            upload_path,
            original_name
        )

        if tool == "pdf_to_word":

            download_name = original_name + ".docx"

        else:

            download_name = original_name + ".pdf"

        media_type = MEDIA[
            os.path.splitext(download_name)[1]
        ]

        logger.info(
            f"{tool} | {file.filename} | Success"
        )

        background_tasks.add_task(delete_file, upload_path)

        background_tasks.add_task(delete_file, output_path)

        return FileResponse(
            output_path,
            media_type=media_type,
            filename=download_name,
            background=background_tasks
        )

    except Exception as ex:

        logger.exception(ex)

        delete_file(upload_path)

        raise HTTPException(
            500,
            str(ex)
        )


# -----------------------------
# Delete helper
# -----------------------------

def delete_file(path):

    try:

        if os.path.exists(path):

            os.remove(path)

    except:

        pass