# Receipt Relay

Containerized Python service that listens for Signal messages and provides a small web UI for printing text or images to an Epson TM-T20III receipt printer.

## Features

* FastAPI web interface with form at `/` and print endpoint at `/print`.
* Prints a header with the current date/time and a footer rule.
* Basic Markdown wrapping.
* Image processing with Pillow for scaling and dithering.
* ESC/POS output using `python-escpos` over USB.
* Dockerfile and docker-compose setup including `signal-cli` sidecar.

## Development

```bash
pip install -r requirements.txt
uvicorn receipt_relay.web.main:app --reload
```

Visit `http://localhost:8081/` to access the form.

## Testing

```bash
pytest
```

## Docker

The included `docker-compose.yml` runs the web service and the Signal sidecar. Set the required `SIGNAL_NUMBER` and `ALLOWED_SENDERS` environment variables before starting.

```bash
docker compose up --build
```
