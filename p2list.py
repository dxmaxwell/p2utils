#!/usr/bin/python2

import sys, os, os.path, re, time, subprocess
from StringIO import StringIO


if "ECLIPSE_BIN" not in os.environ:
    sys.stderr.write("Eclipse application not found, set ECLIPSE_BIN environment variable\n")
    sys.exit(1)

eclipse = os.environ["ECLIPSE_BIN"]

if not os.path.isfile(eclipse):
    sys.stderr.write("Eclipse application not found, file not found: " + eclipse + "\n");
    sys.exit(1)


def p2list(repo, query=None):

    iu_pattern = re.compile(r"{id=(.*),version=(.*)}")

    cmd_args = [ eclipse, "-nosplash", "-application", "org.eclipse.equinox.p2.director", "-repository", repo, "-lf", '{id=${id},version=${version}}', "-list" ]

    if query is not None:
        cmd_args.append(query)

    sys.stderr.write("Querying repository: " + repo + ": ")
    start = time.time()
    try:
        output = subprocess.check_output(cmd_args)
    except subprocess.CalledProcessError as e:
        sys.stderr.write("Error ("  + e.returncode + ")\n")
        sys.exit(1)

    sys.stderr.write("Done (%.2fs)\n" % ((time.time() - start),))

    ius = []
    for line in StringIO(output):
        result = iu_pattern.match(line)
        if result is not None:
            ius.append(result.group(1,2))

    return ius


if __name__ == '__main__':
    if len(sys.argv) > 2:
        ius = p2list(sys.argv[1], sys.argv[2])

    elif len(sys.argv) > 1:
        ius = p2list(sys.argv[1])

    else:
        sys.stderr.write("Usage: p2list.py repoitory [ query ]\n")
        sys.exit(1)

    for iu in ius:
        sys.stdout.write(iu[0]+'/'+iu[1]+'\n')
