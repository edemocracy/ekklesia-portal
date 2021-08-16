import os
import ekklesia_common.logging

if os.environ.get("EKKLESIA_SKIP_LOG_SETUP") is None:
    ekklesia_common.logging.init_logging()
