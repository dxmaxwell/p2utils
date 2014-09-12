#!/usr/bin/python2

import sys, p2list

from argparse import FileType
from argparse import ArgumentParser

from xml.etree import ElementTree

parser = ArgumentParser("")
parser.add_argument("baseTarget", type=FileType('r'), help="Base target definition")
parser.add_argument("destTarget", type=FileType('w'), help="Destination target definition", nargs='?', default=sys.stdout)

args = parser.parse_args(sys.argv[1:])


tree = ElementTree.parse(args.baseTarget)
if tree is None:
    sys.stderr.write("Error parsing file: invalid XML file: " + str(baseTarget) + "\n")
    sys.exit(1)

locations = tree.getroot().find("locations")
if locations is None:
    sys.stderr.write("Error parsing file: missing 'locations' element\n")
    sys.exit(1)

for location in locations.findall("location"):
    repository = location.find("repository")
    if repository is None:
        sys.stderr.write("Error parsing file: missing 'repository' element\n")
        sys.exit(1)
    url = repository.get("location")
    if url is None:
        sys.stderr.write("Error parsing file: missing 'location' attribute\n")
        sys.exit(1)

    units = location.findall("unit")
    if len(units) == 0:
        for iu in p2list.p2list(url, "Q:group"):
            elm = ElementTree.Element("unit")
            elm.set('id', iu[0])
            elm.set('version', iu[1])
            elm.tail = '\n'
            location.append(elm)
    else:
        ius = p2list.p2list(url)
        for unit in units:
            id = unit.get('id')
            if id is None:
                sys.stderr.write("Error parsing file: 'unit' element missing 'id' attribute\n")
                sys.exit(1)
            ver = unit.get('version')
            if ver is None:
                location.remove(unit)
                for iu in ius:
                    if iu[0] == id:
                        elm = ElementTree.Element("unit")
                        elm.set('id', iu[0])
                        elm.set('version', iu[1])
                        elm.tail = '\n'
                        location.append(elm)
            else:
                for iu in ius:
                    if iu[0] == id and iu[1] == ver:
                        break
                else:
                    location.remove(unit)
                    sys.stderr.write("Warning verifying file: " + str(id+'/'+ver) + " not found in repository\n")
    
tree.write(args.destTarget, encoding="UTF-8", xml_declaration=True)
