import eliot
import logging
import sys
from eliot.stdlib import EliotHandler
from eliot.json import EliotJSONEncoder


class MyEncoder(EliotJSONEncoder):
    def default(self, obj):

        try:
            return EliotJSONEncoder.default(self, obj)
        except TypeError:
            return repr(obj)


root_logger = logging.getLogger()
root_logger.addHandler(EliotHandler())
root_logger.setLevel(logging.DEBUG)
logging.getLogger("morepath.directive").setLevel(logging.INFO)
logging.getLogger("passlib.registry").setLevel(logging.INFO)
logging.getLogger("passlib.utils.compat").setLevel(logging.INFO)

eliot.to_file(sys.stdout, encoder=MyEncoder)

logging.captureWarnings(True)

logg = logging.getLogger(__name__)

logging.getLogger("parso").setLevel(logging.WARN)
