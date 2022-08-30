from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil

from pathlib import Path
print(Path.cwd())

router = APIRouter(prefix="/files", tags=["files"], responses={
    200: {"description": "Completed Action"},
    406: {"description": "Unacceptable Action"}
})


@router.post("/file")  # small file: for example a local small txt
async def get_file(file: bytes = File(...)):
    content = file.decode("utf-8")
    lines = content.split('\n')
    return {"lines": lines}


@router.post("/upload")  # larges files: stored in memory up to a certain size, then on disk
async def upload_file(file: UploadFile = File(...)):
    path = f"/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/{file.filename}"
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file name": path,
        "type": file.content_type
    }


@router.get("/download/{name}", response_class=FileResponse)
async def download_file(name: str):
    path = f"/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/{name}"
    return path
