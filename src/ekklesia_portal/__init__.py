import eliot
import logging
import sys
from eliot.stdlib import EliotHandler

logging.getLogger().addHandler(EliotHandler())
logging.getLogger().setLevel(logging.DEBUG)
eliot.to_file(sys.stdout)
logging.captureWarnings(True)

logg = logging.getLogger(__name__)

logging.getLogger("parso").setLevel(logging.WARN)

logg.info("init")
