from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import models
from exceptions import AddressException
from database import engine
from routers import auth, todos, users, address, transaction_functionality
from pagination_api_example.routers import pagination, populate_db
from file_handling.routers import file_router
from ocr import ocr_router
from company import companyapis, dependencies

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(companyapis.router, prefix="/companyapis", tags=["companyapis"],
                   dependencies=[Depends(dependencies.get_token_header)],
                   responses={418: {"description": "Internal Use Only"}})
app.include_router(users.router)
app.include_router(address.router)
app.include_router(pagination.router)
app.include_router(populate_db.router)
app.include_router(transaction_functionality.router)
app.include_router(file_router.router)
app.include_router(ocr_router.router)


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(AddressException)
def address_exception(request: Request, ex: AddressException):
    return JSONResponse(status_code=406, content={"response": ex.name})


app.mount("/files",
          StaticFiles(directory="/home/andreas/PycharmProjects/fastApiProject/file_handling/uploaded_files/"),
          name="files")










