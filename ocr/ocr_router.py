from fastapi import APIRouter, File, UploadFile
import shutil
import pytesseract

router = APIRouter(prefix="/ocr", tags=["ocr"], responses={406: {"description": "Unacceptable"}})


@router.post("/")
def ocr(image: UploadFile = File(...)):
    ocr_file_path = "ocr_file"
    # path = f"/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/{image.filename}"
    with open(ocr_file_path, "w+b") as buffer:
        shutil.copyfileobj(image.file, buffer)
        # langauge --> https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html
    return pytesseract.image_to_string(ocr_file_path, lang="eng")
