# some view / cell helper that could be used from another concept
import re
import xml.etree.ElementTree as etree
from operator import attrgetter

from ekklesia_common.md import MARKDOWN_EXTENSIONS
from ekklesia_common.translation import _
from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from urllib.parse import quote, unquote


def items_for_document_select_widgets(model, departments, proposition_types):
    proposition_type_items = [('', _('not_determined'))] + [(t.id, t.name) for t in proposition_types]
    area_items = [('', _('not_determined'))]

    for department in sorted(departments, key=attrgetter('name')):
        for area in sorted(department.areas, key=attrgetter('name')):
            area_items.append((area.id, f"{department.name} - {area.name}"))

    return {'area': area_items, 'proposition_type': proposition_type_items}


def _handle_double_quote(s, t):
    k, v = t.split('=', 1)
    return k, v.strip('"')


def _handle_single_quote(s, t):
    k, v = t.split('=', 1)
    return k, v.strip("'")


def _handle_key_value(s, t):
    return t.split('=', 1)


def _handle_word(s, t):
    if t.startswith('.'):
        return '.', t[1:]
    if t.startswith('#'):
        return 'id', t[1:]
    return t, t


_scanner = re.Scanner([
    (r'[^ =]+=".*?"', _handle_double_quote),
    (r"[^ =]+='.*?'", _handle_single_quote),
    (r'[^ =]+=[^ =]+', _handle_key_value),
    (r'[^ =]+', _handle_word),
    (r' ', None),
])


def _get_attrs(str):
    """ Parse attribute list and return a list of attribute tuples. """
    return _scanner.scan(str)[0]


class ProposeChangeTreeprocessor(Treeprocessor):

    def __init__(self, md, url_template):
        self.url_template = url_template
        self.levels = []
        self.last_level = 0
        super().__init__(md)

    BASE_RE = r'\{\:?([^\}\n]*)\}'
    HEADER_RE = re.compile(r'[ ]+%s[ ]*$' % BASE_RE)

    def run(self, doc):
        for elem in doc.iter():
            if elem.tag in ['h2', 'h3', 'h4', 'h5', 'h6'] and elem.text:

                level = int(elem.tag[1])
                if level > self.last_level:
                    self.levels.append(0)
                elif level < self.last_level:
                    self.levels = self.levels[:level - 1]

                self.last_level = level
                self.levels[-1] += 1

                m = ProposeChangeTreeprocessor.HEADER_RE.search(elem.text)
                if m:
                    attrs = m.group(1)
                else:
                    attrs = None

                text = elem.text[:m.start()].rstrip('#').rstrip()
                link = self.make_link(text, attrs)
                elem.text = ''
                elem.append(link)

    def make_link(self, header_text, attrs=None):

        def link(section):
            link = etree.Element('a')
            link.set('href', self.url_template.replace('SECTION', quote(section)))
            link.append(etree.Element('i', attrib={'class': 'far fa-edit'}))
            link.text = f'{section} {header_text} '
            return link

        if attrs is not None:
            for k, v in _get_attrs(attrs):
                if k == 'data-section':
                    return link(v)

        section = ".".join(str(l) for l in self.levels)
        return link(section)


class ProposeChangeExtension(Extension):

    def __init__(self, url_template):
        self.url_template = url_template

    def extendMarkdown(self, md):
        md.registerExtension(self)
        tree_processor = ProposeChangeTreeprocessor(md, self.url_template)
        md.treeprocessors.register(tree_processor, 'proposechange', 100)


def markdown_with_propose_change(url_template, text):
    md = Markdown(extensions=MARKDOWN_EXTENSIONS + [ProposeChangeExtension(url_template)])
    return md.convert(text)


def get_section_from_document(document, section_identifier):
    """Returns headline and content of a document section specified by a section identifier.
    Section identifiers look like this: ## heading {data-section=1.1.1}
    """
    level = len(section_identifier.split('.'))
    heading_prefix = "#" * (level + 1) + " "
    heading_re = re.compile("^#{2,%s} " % (level + 1))
    section_start_marker = f' {{data-section="{section_identifier}"}}'
    lines = document.text.splitlines()
    start = None
    for pos, line in enumerate(lines):
        if start is None and line.endswith(section_start_marker):
            start = pos
            headline = line.removeprefix(heading_prefix).removesuffix(section_start_marker)

        elif start is not None and heading_re.search(line):
            break
    else:
        pos += 1

    if not start:
        raise RuntimeError(f"Couldn't find section {section_identifier} in document {document.name}")

    content = "\n".join(lines[start+1:pos]).strip() + "\n"
    return (headline, content)
