import csv
from dataclasses import dataclass
import io
from ekklesia_common import md
from ekklesia_portal.datamodel import Proposition
from eliot import log_call, start_task, log_message


@dataclass
class TableRowOptionalFields:
    content: bool = True
    motivation: bool = True
    submitters: bool = False
    tags: bool = True


@log_call
def proposition_to_table_row(proposition: Proposition, origin: str,
        optional_fields: TableRowOptionalFields):

    row = {
        "Identifier": proposition.voting_identifier,
        "Title": proposition.title,
        "Origin": origin,
        "Category": proposition.ballot.proposition_type.name,
        "Motion block": proposition.ballot.name
    }

    if optional_fields.content:
        row["Text"] = md.convert(proposition.content)

    if optional_fields.motivation:
        row["Reason"] = md.convert(proposition.motivation)

    if optional_fields.tags:
        row["Tags"] = ",".join(t.name for t in proposition.tags)

    if optional_fields.submitters:
        submitter_names = [pm.member.name for pm in proposition.propositions_member if pm.submitter]
        row["Submitters"] = ",".join(submitter_names)

    return row


def propositions_to_csv(propositions, origin="", delimiter=";", optional_fields: TableRowOptionalFields=TableRowOptionalFields()):
    proposition_rows = [proposition_to_table_row(p, origin, optional_fields) for p in propositions]
    csv_out = io.StringIO()
    fieldnames = ['Identifier', 'Submitters', 'Title', 'Text', 'Reason', 'Category', 'Tags', 'Motion block', 'Origin']

    writer = csv.DictWriter(csv_out, fieldnames, delimiter=delimiter, quoting=csv.QUOTE_ALL)
    writer.writeheader()
    writer.writerows(proposition_rows)

    return csv_out.getvalue()
