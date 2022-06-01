
from loguru import logger as log

from .application import run_application

version = (1,0,0,0)

log.remove(0)
log.add(
    '.\log\Brevix_sync_server\{time:DD-MM-YYYY}.log', 
    format='{time:HH:mm:ss.SSSZ} | [{level}] | {name}:{function}({line}) | {message}', 
    rotation="00:01", 
    retention="7 days", 
    compression="zip"
)


def run():
    try:
        log.info(("="*25)+"serat_phrases_generator v"+".".join(str(x) for x in version) + ("="*25))
        run_application()
    except KeyboardInterrupt:
        log.info("Приложение завершилось в штатном режиме.")
        return
    except Exception as e:
        log.error(f"Приложение завершилось с ошибкой ({e.__class__.__name__}): {str(e)}")
        