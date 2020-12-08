import requests
from eliot import start_task
from ekklesia_portal.enums import PropositionVisibility

from ekklesia_portal.lib.discourse import DiscourseConfig, DiscourseTopic, create_discourse_topic


def push_draft_to_discourse(
    exporter_config, external_content_template, portal_content_template, proposition, proposition_url
):

    editing_remarks = proposition.external_fields['external_draft']['editing_remarks']

    content = external_content_template.format(
        draft_link=proposition_url,
        editing_remarks=editing_remarks,
        abstract=proposition.abstract,
        content=proposition.content,
        motivation=proposition.motivation
    )

    importer_name = exporter_config.pop("importer")

    topic = DiscourseTopic(content, proposition.title, [t.name for t in proposition.tags])
    discourse_config = DiscourseConfig(**exporter_config)
    resp_json = create_discourse_topic(discourse_config, topic).json()
    topic_id = resp_json["topic_id"]
    topic_slug = resp_json["topic_slug"]
    discourse_topic_url = f'{discourse_config.base_url}/t/{topic_slug}/{topic_id}'
    proposition.external_discussion_url = discourse_topic_url
    external_draft = proposition.external_fields["external_draft"]
    external_draft['import_info'] = {'topic_id': topic_id}
    external_draft['importer'] = importer_name
    proposition.external_fields['external_draft'] = external_draft
    proposition.content = portal_content_template.format(topic_url=discourse_topic_url)
    proposition.motivation = ''
    proposition.abstract = ''
    proposition.visibility = PropositionVisibility.PUBLIC
