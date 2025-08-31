from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from datetime import datetime
from zoneinfo import ZoneInfo

from ..config import settings
from ..core.markdown import markdown_to_lines
from ..core.image import process_image
from ..device.printer import EscposUsbPrinter

app = FastAPI()
templates = Jinja2Templates(directory="receipt_relay/web/templates")
printer = EscposUsbPrinter()


def _header() -> str:
    tz = ZoneInfo(settings.header_dt_tz)
    return datetime.now(tz).strftime(settings.header_dt_fmt)


def _footer() -> str:
    return settings.footer_char * settings.max_cols


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/print")
async def do_print(request: Request, text: str = Form(None), image: UploadFile | None = File(None)):
    if not text and not image:
        raise HTTPException(status_code=400, detail="text or image required")

    lines = []
    if text:
        if len(text.encode()) > settings.max_msg_bytes:
            raise HTTPException(status_code=400, detail="text too large")
        lines = markdown_to_lines(text, settings.max_cols)

    header = _header()
    footer = _footer()

    printer.print_lines([header, ""])  # header + blank line
    if lines:
        printer.print_lines(lines)
    if image:
        data = await image.read()
        if len(data) > settings.max_img_bytes:
            raise HTTPException(status_code=400, detail="image too large")
        img = process_image(data, settings.printer_max_dots)
        printer.print_image(img)
    printer.print_lines(["", footer])
    printer.cut()

    job_id = str(uuid4())
    accept = request.headers.get("accept", "")
    payload = {"ok": True, "job_id": job_id}
    if "text/html" in accept:
        return templates.TemplateResponse("success.html", {"request": request, **payload})
    return JSONResponse(payload)


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
