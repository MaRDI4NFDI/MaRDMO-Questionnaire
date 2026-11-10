'''Check the catalog files of the MaRDMO questionnaire.

    python ci/check_catalog.py [catalog directory]

Reports, and exits with 1 on

- a file that is not well-formed XML;
- a reference to an element that no file defines (attribute, option set,
  option, question, question set, page, section, catalog, condition);
- an element defined twice in one file, or differently in two files (RDMO
  imports one element per URI: the file imported last would win);
- a widget type the released RDMO does not know (rdmo.questions.constants);
- a text given in English or German only (title, text, help, ...).

Needs RDMO installed (pip install rdmo) for its widget types.
'''
import sys
import xml.etree.ElementTree as ET
from collections import defaultdict
from pathlib import Path

DC = '{http://purl.org/dc/elements/1.1/}uri'
LANGUAGES = {'en', 'de'}

# References that point to an element of another tag than their own:
# <parent> to one of its element's tag, a condition's <source> to an
# attribute and its <target_option> to an option
REFERENCE_TAGS = {'source': 'attribute', 'target_option': 'option'}


def widget_types():
    '''The widget types of the installed (released) RDMO.'''
    from rdmo.questions.constants import WIDGET_TYPE_CHOICES
    return {widget for widget, _ in WIDGET_TYPE_CHOICES}


def check(catalog):
    problems = []
    roots = {}
    for path in sorted(catalog.glob('*.xml')):
        try:
            roots[path.name] = ET.parse(path).getroot()
        except ET.ParseError as error:
            problems.append(f'{path.name}: not well-formed: {error}')

    # Elements: {(tag, URI): {file: XML}}
    elements = defaultdict(dict)
    for name, root in roots.items():
        for element in root:
            key = (element.tag, element.get(DC))
            if name in elements[key]:
                problems.append(f'{name}: {element.tag} {key[1]} defined twice')
            elements[key][name] = ET.tostring(element, encoding='unicode').strip()
    for (tag, uri), files in sorted(elements.items()):
        if len(set(files.values())) > 1:
            problems.append(f'{tag} {uri} differs between {", ".join(sorted(files))}')

    widgets = widget_types()
    for name, root in roots.items():
        for element in root:
            for child in element.iter():
                if child is not element and child.get(DC):
                    tag = element.tag if child.tag == 'parent' else REFERENCE_TAGS.get(child.tag, child.tag)
                    if (tag, child.get(DC)) not in elements:
                        problems.append(f'{name}: {element.tag} {element.get(DC)} refers to the missing '
                                        f'{tag} {child.get(DC)}')
            widget = element.findtext('widget_type')
            if element.tag == 'question' and widget not in widgets:
                problems.append(f'{name}: question {element.get(DC)} has the widget type {widget!r}, '
                                f'which RDMO does not know')
            texts = defaultdict(set)
            for child in element:
                if child.get('lang') and (child.text or '').strip():
                    texts[child.tag].add(child.get('lang'))
            for field, languages in sorted(texts.items()):
                if languages != LANGUAGES:
                    problems.append(f'{name}: {element.tag} {element.get(DC)} has its {field} only in '
                                    f'{", ".join(sorted(languages))}')
    return problems


if __name__ == '__main__':
    catalog = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parents[1] / 'catalog')
    problems = check(catalog)
    for problem in problems:
        print(problem)
    print(f'{len(problems)} problems in {catalog}')
    sys.exit(1 if problems else 0)
