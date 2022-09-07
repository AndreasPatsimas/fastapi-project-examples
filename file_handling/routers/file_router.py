from io import BytesIO
import os
from typing import List

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse
import shutil
import zipfile

from starlette.responses import StreamingResponse

# from pathlib import Path
# print(Path.cwd())
PATH = "/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/"

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
    path = PATH + file.filename
    with open(path, "w+b") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file name": path,
        "type": file.content_type
    }


@router.post("/zip-files/{zip_file_name}", response_class=FileResponse)
async def zip_file(zip_file_name: str, files: List[UploadFile] = File(...)):

    file_list = []
    for file in files:
        file_name = PATH + file.filename
        with open(file_name, "w+b") as buffer:
            shutil.copyfileobj(file.file, buffer)
        file_list.append(file_name)

    zipped_file = zipfiles(file_list, zip_file_name)
    for file_name in file_list:
        os.remove(file_name)

    return zipped_file


@router.get("/download/{name}", response_class=FileResponse)
async def download_file(name: str):
    path = PATH + name
    return path


def zipfiles(file_list, zip_file_name: str):
    io = BytesIO()
    zip_sub_dir = zip_file_name
    zip_filename = "%s.zip" % zip_sub_dir
    with zipfile.ZipFile(io, mode='w', compression=zipfile.ZIP_DEFLATED) as zip:
        for fpath in file_list:
            zip.write(fpath)
        # close zip
        zip.close()
    return StreamingResponse(
        iter([io.getvalue()]),
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment;filename=%s" % zip_filename}
    )
