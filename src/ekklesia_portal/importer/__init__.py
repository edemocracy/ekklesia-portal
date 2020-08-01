from .discourse import import_discourse_post_as_proposition

# import handlers are functions with the following signature:
# def import_handler(base_url: str, from_data: str)
# this assumes that we want to import data from some url with some ID, but from_data can be anything
PROPOSITION_IMPORT_HANDLERS = {"discourse_post": import_discourse_post_as_proposition}
