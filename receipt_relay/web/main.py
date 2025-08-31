from fastapi import FastAPI, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from uuid import uuid4
from datetime import datetime
from zoneinfo import ZoneInfo

from .. import config
from ..core.markdown import markdown_to_lines
from ..core.image import process_image
from ..device.printer import EscposUsbPrinter

settings = config.settings

app = FastAPI()
templates = Jinja2Templates(directory="receipt_relay/web/templates")
printer = EscposUsbPrinter()


def _header() -> str:
    tz = ZoneInfo(settings.header_dt_tz)
    return datetime.now(tz).strftime(settings.header_dt_fmt)


def _footer() -> str:
    return settings.footer_char * settings.max_cols


def _check_token(request: Request) -> None:
    token = settings.web_token
    if token:
        supplied = request.headers.get("X-Token")
        if supplied != token:
            raise HTTPException(status_code=401, detail="unauthorized")


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


@app.get("/config", response_class=HTMLResponse)
async def get_config(request: Request):
    _check_token(request)
    return templates.TemplateResponse(
        "config.html", {"request": request, "config": settings}
    )


@app.post("/config", response_class=HTMLResponse)
async def post_config(
    request: Request,
    signal_number: str = Form(None),
    allowed_senders: str = Form(None),
    signal_rest_url: str = Form(None),
):
    _check_token(request)
    data = {
        "signal_number": signal_number or None,
        "allowed_senders": allowed_senders or None,
        "signal_rest_url": signal_rest_url or settings.signal_rest_url,
    }
    new_settings = config.Settings(**data)
    config.save_settings(new_settings.model_dump(exclude_none=True))
    config.reload_settings()
    return templates.TemplateResponse(
        "config.html", {"request": request, "config": settings}
    )


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
