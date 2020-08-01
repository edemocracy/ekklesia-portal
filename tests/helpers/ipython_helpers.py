import os
import sys

from IPython.core.interactiveshell import InteractiveShell
from IPython.paths import get_ipython_dir
from IPython.terminal.embed import InteractiveShellEmbed
from IPython.terminal.ipapp import TerminalIPythonApp


def load_config_for_embed_ipython(profile_name='debug'):
    """Load the a config file from the default ipython_dir.
    """
    ipython_dir = get_ipython_dir()
    profile_dir = os.path.join(ipython_dir, f'profile_{profile_name}')
    app = TerminalIPythonApp()
    app.config_file_paths.append(profile_dir)
    app.load_config_file()
    config = app.config
    # XXX: setting the profile in config seems to have no effect for InteractiveShellEmbed.
    # TODO: learn more about IPython internals...
    # fix history location with a little workaround
    if 'hist_file' not in config.HistoryAccessor:
        config.HistoryManager.hist_file = os.path.join(profile_dir, 'history.sqlite')
    return config


def embed_ipython():
    """
    Taken from `IPython.terminal.embed()`, see documentation there.
    Call this to embed IPython at the current point in your program with config from profile 'debug'.
    """
    config = load_config_for_embed_ipython()
    config.InteractiveShellEmbed = config.TerminalInteractiveShell
    # save ps1/ps2 if defined
    ps1 = None
    ps2 = None
    try:
        ps1 = sys.ps1
        ps2 = sys.ps2
    except AttributeError:
        pass
    # save previous instance
    saved_shell_instance = InteractiveShell._instance
    if saved_shell_instance is not None:
        cls = type(saved_shell_instance)
        cls.clear_instance()
    frame = sys._getframe(1)
    location = f'{frame.f_code.co_filename}:{frame.f_lineno}'
    shell = InteractiveShellEmbed.instance(_init_location_id=location, config=config)
    shell(header=location, stack_depth=2, _call_location_id=location)
    InteractiveShellEmbed.clear_instance()
    # restore previous instance
    if saved_shell_instance is not None:
        cls = type(saved_shell_instance)
        cls.clear_instance()
        for subclass in cls._walk_mro():
            subclass._instance = saved_shell_instance
    if ps1 is not None:
        sys.ps1 = ps1
        sys.ps2 = ps2
