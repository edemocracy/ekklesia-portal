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


logging.getLogger().addHandler(EliotHandler())
logging.getLogger().setLevel(logging.DEBUG)

eliot.to_file(sys.stdout, encoder=MyEncoder)

logging.captureWarnings(True)

logg = logging.getLogger(__name__)

logging.getLogger("parso").setLevel(logging.WARN)
