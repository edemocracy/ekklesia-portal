from .discourse import import_discourse_post_as_proposition, import_discourse_topic_as_proposition

# import handlers are functions with the following signature:
# def import_handler(config: dict, from_data: str)
# this assumes that we want to import data from some url with some ID, but from_data can be anything
PROPOSITION_IMPORT_HANDLERS = {
    "discourse_post": import_discourse_post_as_proposition,
    "discourse_topic": import_discourse_topic_as_proposition,
}
