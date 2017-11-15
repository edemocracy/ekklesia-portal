import morepath

import jinja2
from arguments.helper.templating import PyJadeExtension, select_jinja_autoescape
from werkzeug.datastructures import ImmutableDict
from munch import Munch


class App(morepath.App):
    def __init__(self):
        super().__init__()
        jinja_globals=dict(url_for=lambda *args, **kwargs: "#", 
                           g=Munch(locale="de"),
                           current_user=Munch(is_authenticated=False),
                           _=lambda name, *args: name,
                           get_flashed_messages=lambda *a, **k: []
                           )
        jinja_options = ImmutableDict(
            loader=jinja2.PackageLoader("arguments", "templates"),
            extensions=[PyJadeExtension, "jinja2.ext.autoescape"],
            autoescape=select_jinja_autoescape, 
            )

        self.jinja_env = jinja2.Environment(**jinja_options)
        self.jinja_env.globals.update(jinja_globals)
        
    def render_template(self, template, **context):
        template = self.jinja_env.get_template(template)
        return template.render(**context)
