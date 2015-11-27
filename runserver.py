import argparse
import datetime
import os.path
from arguments import make_app
import tempfile

tmpdir = tempfile.gettempdir()

parser = argparse.ArgumentParser("Arguments runserver.py")

parser.add_argument("-b", "--bind", default="127.0.0.1", help="hostname / IP to bind to, default 127.0.0.1")
parser.add_argument("-p", "--http_port", default=5000, help="HTTP port to use, default 5000")
parser.add_argument("-d", "--debug", action="store_true", help="enable Flask debugging (+ reloader)")
parser.add_argument("-s", "--stackdump", action="store_true", help="write stackdumps to temp dir {} on SIGQUIT".format(tmpdir))
        
args = parser.parse_args()

print("cmdline args:", args)

flask_app = make_app(args.debug)


def stackdump_setup():
    import codecs
    import logging
    import sys
    logg = logging.getLogger(__name__)
    import threading
    import traceback
    try:
        import IPython.core.ultratb as ultratb
    except:
        ultratb = None

    if ultratb is None:
        logg.warn("IPython not installed, stack dumps not available!")
    else:
        logg.info("IPython installed, write stack dumps to tmpdir with: `kill -QUIT <arguments_pid>`")

        def dumpstacks(signal, frame):
            print("dumping stack")
            filepath = os.path.join(tmpdir, "arguments_threadstatus")
            id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
            full = ["-" * 80]
            tb_formatter = ultratb.ListTB(color_scheme="Linux")
            for thread_id, stack in sys._current_frames().items():
                thread_name = id2name.get(thread_id, "")
                stacktrace = traceback.extract_stack(stack)
                stb = tb_formatter.structured_traceback(Exception, Exception(), stacktrace)[8:-1]
                if stb:
                    formatted_trace = tb_formatter.stb2text(stb).strip()
                    with codecs.open("{}.{}".format(filepath, thread_id), "w", encoding='utf8') as wf:
                        wf.write("\n{}".format(formatted_trace))
                    if len(stb) > 4:
                        short_stb = stb[:2] + ["..."] + stb[-2:]
                    else:
                        short_stb = stb
                    formatted_trace_short = tb_formatter.stb2text(short_stb).strip()
                    full.append("# Thread: %s(%d)" % (thread_name, thread_id))
                    full.append(formatted_trace_short)
                    full.append("-" * 80)

            with codecs.open(filepath, "w", encoding='utf8') as wf:
                wf.write("\n".join(full))

        import signal
        signal.signal(signal.SIGQUIT, dumpstacks)


if args.stackdump:
    stackdump_setup()


with open(os.path.join(tmpdir, "arguments.started"), "w") as wf:
    wf.write(datetime.datetime.now().isoformat())
    wf.write("\n")


flask_app.run(host=args.bind, port=int(args.http_port), debug=args.debug, extra_files=[os.path.join(os.path.dirname(__file__), ".babelcompiled")])
