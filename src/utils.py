import logging
import asyncio
import functools
import os
import time
from logging.handlers import RotatingFileHandler

def setup_logger(name, log_file='logs/bot_errors.log'):
    """
    Configura un logger que escribe tanto en consola como en archivo rotativo.
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        file_handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5, encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
    return logger

def retry_operation(max_retries=3, delay=2, logger=None):
    """
    Decorador para reintentar operaciones fallidas.
    """
    def decorator(func):
        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def async_wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return await func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        msg = f"⚠️ Error en {func.__name__} (Intento {attempt}/{max_retries}): {e}"
                        if logger: logger.warning(msg)
                        else: print(msg)
                        if attempt < max_retries: await asyncio.sleep(delay)
                raise last_exception
            return async_wrapper
        else:
            @functools.wraps(func)
            def sync_wrapper(*args, **kwargs):
                last_exception = None
                for attempt in range(1, max_retries + 1):
                    try:
                        return func(*args, **kwargs)
                    except Exception as e:
                        last_exception = e
                        msg = f"⚠️ Error en {func.__name__} (Intento {attempt}/{max_retries}): {e}"
                        if logger: logger.warning(msg)
                        else: print(msg)
                        if attempt < max_retries: time.sleep(delay)
                raise last_exception
            return sync_wrapper
    return decorator

def convert_svg_to_png(svg_path, png_path):
    """
    Convierte un archivo SVG a PNG usando svglib y reportlab.
    """
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        drawing = svg2rlg(svg_path)
        renderPM.drawToFile(drawing, png_path, fmt="PNG")
        return True
    except Exception:
        return False
