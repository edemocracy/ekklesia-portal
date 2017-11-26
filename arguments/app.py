from datetime import datetime
import morepath

import jinja2
from arguments.helper.templating import PyJadeExtension, select_jinja_autoescape
from werkzeug.datastructures import ImmutableDict
from munch import Munch

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')



class App(morepath.App):
    def __init__(self):
        super().__init__()
        jinja_globals=dict(url_for=lambda *a, **k: "#", 
                           g=Munch(locale="de"),
                           current_user=Munch(is_authenticated=False),
                           _=lambda name, *a, **k: name,
                           ngettext=lambda name, *a, **k: name,
                           get_flashed_messages=lambda *a, **k: [],
                           
                           )
        jinja_options = ImmutableDict(
            loader=jinja2.PackageLoader("arguments", "templates"),
            extensions=[PyJadeExtension, "jinja2.ext.autoescape"],
            autoescape=select_jinja_autoescape, 
            )

        self.jinja_env = jinja2.Environment(**jinja_options)
        self.jinja_env.globals.update(jinja_globals)
        self.jinja_env.filters['datetimeformat'] = format_datetime
        self.jinja_env.filters['markdown'] = lambda t: t 
        
    def render_template(self, template, **context):
        template = self.jinja_env.get_template(template)
        return template.render(**context)
