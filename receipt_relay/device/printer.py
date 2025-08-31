from typing import Iterable

try:
    from escpos.printer import Usb, Dummy
    from escpos.printer.usb import is_usable as usb_usable
except Exception:  # pyusb not installed
    Usb = None
    usb_usable = lambda: False
    from escpos.printer import Dummy

from escpos import exceptions
from ..config import settings


class EscposUsbPrinter:
    def __init__(self) -> None:
        vid = int(settings.printer_vendor_id, 16)
        pid = int(settings.printer_product_id, 16) if settings.printer_product_id else None
        if Usb and usb_usable():
            try:
                self.printer = Usb(vid, pid or 0)
                return
            except Exception:
                pass
        self.printer = Dummy()

    def print_lines(self, lines: Iterable[str]) -> None:
        for line in lines:
            try:
                self.printer.text(line + "\n")
            except Exception:
                pass

    def print_image(self, image) -> None:
        try:
            self.printer.image(image)
        except Exception:
            pass

    def cut(self) -> None:
        try:
            self.printer.cut()
        except exceptions.Error:
            pass
