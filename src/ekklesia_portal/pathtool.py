import morepath

from ekklesia_portal.app import App


def paths():
    morepath.autoscan()
    App.commit()
    path_tool(App)


if __name__ == '__main__':
    from more.pathtool import path_tool
    paths()
