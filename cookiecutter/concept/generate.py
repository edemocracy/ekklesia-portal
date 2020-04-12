"""
Generate a basic CRU (Delete is not implemented) concept that provides views for a database model object.

The script must be run from the project's root dir:

    python cookiecutter/concept/generate.py my_concept
"""
import os
import sys
import case_conversion
import inflect
from cookiecutter.main import cookiecutter as run_cookiecutter


OUTPUT_DIR = 'src/ekklesia_portal/concepts/'


def main():
    if len(sys.argv) == 1:
        raise Exception('expected one argument: concept name is missing!')

    if not os.path.isdir(OUTPUT_DIR):
        raise Exception(f'concept dir {OUTPUT_DIR} cannot be found. Did you run the script from the root directory of the project?')

    concept_name = sys.argv[1]
    p = inflect.engine()
    concept_name_plural = p.plural(concept_name)
    concept_name_camelcase_upper = case_conversion.pascalcase(concept_name)
    concept_name_camelcase_upper_plural = case_conversion.pascalcase(concept_name_plural)
    extra_context = {
        'concept_name': concept_name,
        'concept_names': concept_name_plural,
        'ConceptName': concept_name_camelcase_upper,
        'ConceptNames': concept_name_camelcase_upper_plural
    }
    run_cookiecutter('cookiecutter/concept', output_dir=OUTPUT_DIR, no_input=True, extra_context=extra_context)

    concept_location = os.path.join(OUTPUT_DIR, concept_name)
    print(f"generated concept {concept_location}, tests are located at tests/{concept_name}")


if __name__ == "__main__":
    main()
