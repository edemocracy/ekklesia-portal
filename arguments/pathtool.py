import morepath

from arguments.app import App
from more.pathtool import path_tool


def paths():
    morepath.autoscan()
    App.commit()
    path_tool(App)


if __name__ == '__main__':
    paths()
