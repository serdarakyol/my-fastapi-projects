from starlette.requests import Request
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import FileResponse

from api.services.service_extract_data import FileProcess

from pathlib import Path

router_xlsx = APIRouter()
ROOT_DIR = str(Path(__file__).parent.parent.parent.parent)

@router_xlsx.post("/process_xlsx_data", name="Extract and process data")
async def upload_files(
    request: Request,
    files: list[UploadFile] = File(description="Upload files"),
):
    processer = FileProcess(files=files, root_dir=ROOT_DIR)
    await processer.calculate()

    return FileResponse(path=f"{ROOT_DIR}/output.xlsx", filename="output.xlsx")
