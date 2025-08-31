from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    printer_vendor_id: str = Field('0x04B8', env='PRINTER_VENDOR_ID')
    printer_product_id: Optional[str] = Field(None, env='PRINTER_PRODUCT_ID')
    printer_charset: str = Field('CP437', env='PRINTER_CHARSET')
    printer_max_dots: int = Field(576, env='PRINTER_MAX_DOTS')
    max_cols: int = Field(42, env='MAX_COLS')
    cut_mode: str = Field('full', env='CUT_MODE')
    header_dt_tz: str = Field('America/New_York', env='HEADER_DT_TZ')
    header_dt_fmt: str = Field('EEE MMM d, yyyy HH:mm:ss', env='HEADER_DT_FMT')
    footer_char: str = Field('─', env='FOOTER_CHAR')
    signal_number: Optional[str] = Field(None, env='SIGNAL_NUMBER')
    signal_rest_url: str = Field('http://signal:8080', env='SIGNAL_REST_URL')
    allowed_senders: Optional[str] = Field(None, env='ALLOWED_SENDERS')
    max_msg_bytes: int = Field(16384, env='MAX_MSG_BYTES')
    max_img_bytes: int = Field(2000000, env='MAX_IMG_BYTES')
    rate_limit_per_min: int = Field(10, env='RATE_LIMIT_PER_MIN')
    log_level: str = Field('INFO', env='LOG_LEVEL')
    web_bind: str = Field('0.0.0.0', env='WEB_BIND')
    web_port: int = Field(8081, env='WEB_PORT')
    web_token: Optional[str] = Field(None, env='WEB_TOKEN')

settings = Settings()
