import os
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter()


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):  # noqa: B008
    suffix = Path(file.filename).suffix.lower()  # 转为小写
    if suffix not in [".txt", ".pdf"]:  # 校验扩展名
        raise HTTPException(status_code=400, detail="只允许 txt 和 pdf 文件")
    os.makedirs("uploads", exist_ok=True)  # 确认目录存在
    file_path = f"uploads/{file.filename}"
    content = await file.read()
    with open(file_path, "wb") as f:  # noqa: ASYNC230
        f.write(content)

    file_size = os.path.getsize(file_path)
    return {"filename": file.filename, "size": file_size}
