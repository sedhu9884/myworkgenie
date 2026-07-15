from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from tools.converter import convert

import os
import uuid
import shutil
import logging

# --------------------------------------------------
# Logging
# --------------------------------------------------

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# --------------------------------------------------
# App
# --------------------------------------------------

app = FastAPI(
    title="MyWorkGenie",
    version="2.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MAX_SIZE = 100 * 1024 * 1024

SUPPORTED = {

    "pdf_to_word": [".pdf"],

    "word_to_pdf": [".docx", ".doc"]

}

MEDIA = {

    ".pdf": "application/pdf",

    ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

}


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/")

async def home(request: Request):

    return templates.TemplateResponse(

        "index.html",

        {

            "request": request

        }

    )


# --------------------------------------------------
# Convert
# --------------------------------------------------

@app.post("/convert")

async def convert_document(

    tool: str = Form(...),

    file: UploadFile = File(...)

):

    if tool not in SUPPORTED:

        raise HTTPException(

            400,

            "Unsupported conversion."

        )

    if file.filename == "":

        raise HTTPException(

            400,

            "Please choose a file."

        )

    extension = os.path.splitext(

        file.filename

    )[1].lower()

    if extension not in SUPPORTED[tool]:

        raise HTTPException(

            400,

            "Invalid file type."

        )

    data = await file.read()

    if len(data) > MAX_SIZE:

        raise HTTPException(

            400,

            "Maximum size is 100 MB."

        )

    unique = str(uuid.uuid4()) + extension

    upload_path = os.path.join(

        UPLOAD_FOLDER,

        unique

    )

    with open(upload_path, "wb") as f:

        f.write(data)

    original = os.path.splitext(

        file.filename

    )[0]

    try:

        output_path = convert(

            tool,

            upload_path,

            original

        )

        if tool == "pdf_to_word":

            download = original + ".docx"

        else:

            download = original + ".pdf"

        media = MEDIA[

            os.path.splitext(download)[1]

        ]

        logger.info(

            f"{tool} : {file.filename}"

        )

        return FileResponse(

            output_path,

            filename=download,

            media_type=media

        )

    except Exception as ex:

        logger.exception(ex)

        raise HTTPException(

            500,

            str(ex)

        )

    finally:

        try:

            if os.path.exists(upload_path):

                os.remove(upload_path)

        except:

            pass