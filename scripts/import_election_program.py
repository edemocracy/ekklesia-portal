import argparse
import csv
import re

from eliot import log_call, Message, start_action
import transaction
import sqlalchemy.orm

from ekklesia_portal.database.datamodel import Department, Ballot, Proposition, Tag, PropositionType, Policy,\
                                               VotingPhase, VotingType, PropositionStatus
from ekklesia_portal.database import Session


@log_call
def prepare_regex():

    # First capture group: The header text (Detect if line starts with correct number of # signs)
    # Second capture group: The header number (e.g. {data-section="6.10.2.2"}, attribute name doesn't matter)
    # Third capture group: The chapter content (Until another header is detected)
    # Fourth capture group: Sub chapters (Until another level one header is detected)
    res = [None]
    for layer in range(1, 10):
        res.append(re.compile(
            r'^#{' + str(layer + 1) + '} (.+) '            # Match header text (x+1 # signs)
            r'{.+="([\d.]+)"}'                             # Match header number
            r'\n+([^#]+)'                                  # Match chapter content
            r'\n*((?:[^#]|#{' + str(layer + 2) + ',})+)',  # Match subchapters
            re.MULTILINE
        ))

    return res


@log_call
def parse_layer(content, level, regex_list, parent_chapters, layer_depth):

    results = []

    for layer_chapter in regex_list[level].finditer(content):
        # Extract capture groups
        (chapter_name, chapter_number, chapter_content, sub_chapters) = layer_chapter.group(1, 2, 3, 4)

        # Append data to result list
        cur_chapter = {"name": chapter_name, "level": level, "parent_chapters": parent_chapters, "content": chapter_content,
                       "number": chapter_number, "sub_chapters": []}

        results.append(cur_chapter)

        # Skip chapters of deeper layers
        if level == layer_depth:
            cur_chapter["content"] += "\n" + sub_chapters
            continue

        # Copy and append to parent chapter list
        new_parent_chapters = parent_chapters.copy()
        new_parent_chapters.append({"name": chapter_name, "number": chapter_number})

        # Parse sub chapters
        sub_chapters = parse_layer(sub_chapters, level + 1, regex_list, new_parent_chapters, layer_depth)

        # Create sub chapter list for current chapter
        for sub_chapter in sub_chapters:
            cur_chapter["sub_chapters"].append({"name": sub_chapter["name"], "number": sub_chapter["number"]})

        results += sub_chapters

    return results


@log_call
def load_election_program(filepath, layer_depth):
    with open(filepath) as program_file:
        with start_action(log_level="INFO", action_type="load_file"):
            content = program_file.read()

    # Compile regex patterns
    regex_list = prepare_regex()

    # Start recursive parsing of layers
    return parse_layer(content, 1, regex_list, [], layer_depth)


@log_call
def insert_proposition(subject_area, proposition_type, voting_phase, proposition, identifier, data_tag_regex):

    # Make title
    title = "Streichung: " + proposition["number"] + " " + proposition["name"]

    chapters = ""
    for parent in proposition["parent_chapters"]:
        chapters += "**" + parent["number"] + "** " + parent["name"] + "\n"

    chapters += "**" + proposition["number"] + " " + proposition["name"] + "**\n"

    for child in proposition["sub_chapters"]:
        chapters += "**" + child["number"] + "** " + child["name"] + "\n"

    abstract = "Streichung von Kapitel " + proposition["number"] + " des Wahlprogramms zur Bundestagswahl 2021"

    content = "Der Bundesparteitag möge beschließen, im Wahlprogramm zur Bundestagswahl \nKapitel **"
    content += proposition["number"] + " " + proposition["name"] + "** zu streichen\n\n"

    motivation = "Der Bundesparteitag 2019.2 hat beschlossen, dass alle Teile des Programms zur Bundestagswahl 2017 " \
                 "zur Streichung angemeldet werden um eine Überarbeitung des Programms zur Bundestagswahl 2021 sicherzustellen."

    motivation += "\n#### Einordnung\n"
    motivation += chapters

    motivation += "\n#### Kapitelinhalt\n"
    text = proposition["content"]

    # Remove data-section tags
    text = data_tag_regex.sub("", text)

    if text is None or len(text) == 0 or text.isspace():
        motivation += "*Dieses Kapitel enthält keinen Text. Es beinhaltet nur die oben genannten Unterkapitel.*"
    else:
        motivation += text

    voting_identifier = "WP" + str(identifier).zfill(3)

    ballot = Ballot(area=subject_area, name=voting_identifier, voting_type=VotingType.ASSEMBLY,
                    voting=voting_phase, proposition_type=proposition_type)

    proposition_obj = Proposition(title=title, abstract=abstract, content=content, motivation=motivation,
                                  voting_identifier=voting_identifier, ballot=ballot, status=PropositionStatus.SCHEDULED)

    # Add tags, some defaults + chapter name + parent chapter names (tags can only have a maximum length of 64 characters)
    tags = ["wahlprogrammantrag", "bundestagswahl", "streichung"]
    for parent in proposition["parent_chapters"]:
        tags.append((parent["name"][:61] + "...") if len(parent["name"]) > 64 else parent["name"])

    name_tag = proposition["name"]
    tags.append((name_tag[:61] + "...") if len(name_tag) > 64 else name_tag)

    for tag_name in tags:
        tag = session.query(Tag).filter_by(name=tag_name).scalar()
        if tag is None:
            tag = Tag(name=tag_name)
        proposition_obj.tags.append(tag)


@log_call
def insert_election_program(department_name, subject_area_name, voting_phase_name, propositions, number_start):

    # Load department
    department = session.query(Department).filter_by(name=department_name).scalar()
    if department is None:
        raise ValueError("Department " + department_name + " not found!")

    # Load subject area
    maybe_subject_area = [area for area in department.areas if area.name == subject_area_name]
    if not maybe_subject_area:
        raise ValueError("Subject area " + subject_area_name + " not found! Please create it!")

    subject_area = maybe_subject_area[0]

    # Load proposition type
    proposition_type = session.query(PropositionType).filter_by(abbreviation="WP").scalar()
    if proposition_type is None:
        raise ValueError("Proposition type WP not found!")

    # Load voting phase
    voting_phase = None
    if voting_phase_name is not None:
        voting_phase = session.query(VotingPhase).filter_by(name=voting_phase_name).scalar()

    data_tag_regex = re.compile(r'{data-section="[\d.]+"}')

    # Insert propositions into database
    id = number_start

    for proposition in propositions:
        insert_proposition(subject_area, proposition_type, voting_phase, proposition, id, data_tag_regex)
        id += 1


parser = argparse.ArgumentParser("Ekklesia Portal import_election_program.py")
parser.add_argument("-c", "--config-file", help=f"Path to config file in YAML / JSON format")
parser.add_argument("-d", "--department", help=f"Choose the department to import to.", required=True)
parser.add_argument("-s", "--subject-area", help=f"The subject area for the propositions.", required=True)
parser.add_argument("-f", "--filepath", help=f"Choose the filepath to import from.", required=True)
parser.add_argument("-v", "--voting-phase", help=f"The voting phase to add the propositions to.", default=None)
parser.add_argument("-l", "--layer-depth", help=f"Defines layer depth to create new propositions for", default=10)
parser.add_argument("-n", "--number-start", help=f"The number where WPXXX should start", default=1)

if __name__ == "__main__":
    args = parser.parse_args()

    from ekklesia_portal.app import make_wsgi_app

    app = make_wsgi_app(args.config_file)

    session = Session()
    session.autoflush = True

    sqlalchemy.orm.configure_mappers()

    result = load_election_program(args.filepath, int(args.layer_depth))

    insert_election_program(args.department, args.subject_area, args.voting_phase, result, int(args.number_start))

    input("Press Enter to commit changes to the database, or CTRL-C to abort...")

    transaction.commit()
