from markdown import Markdown
from mdx_gfm import GithubFlavoredMarkdownExtension


MARKDOWN_EXTENSIONS = [GithubFlavoredMarkdownExtension()]

md = Markdown(extensions=MARKDOWN_EXTENSIONS)

convert = md.convert
