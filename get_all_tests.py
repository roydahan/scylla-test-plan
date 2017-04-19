import json
import re
import requests
import subprocess
from optparse import OptionParser

ISSUES_FOR_SCYLLA_URL = 'https://github.com/scylladb/scylla/issues/%s'
ISSUES_FOR_SCYLLA_TOOLS_JAVA_URL = 'https://github.com/scylladb/scylla-tools-java/issues/%s'

ISSUES_FOR_C_URL = 'https://issues.apache.org/jira/rest/api/2/issue/CASSANDRA-%s?fields=status'
REPORT_ISSUES_FOR_C_URL = 'https://issues.apache.org/jira/browse/CASSANDRA-%s'

header_report = """<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>list of tests in scylla-dtest</title>
    </head>
    <body>
      <style>
         div {
         margin: 0px 0px 0px 70px;
         background-color: transparent;}
         p {
         text-indent: 30px;
         }
         summary {
         text-indent: 30px;
         }
      </style>"""


def get_comma_separated_args(option, opt, value, parser):
    setattr(parser.values, option.dest, value.split(','))


def optional_arg(arg_default):
    def func(option, opt_str, value, parser):
        if parser.rargs and not parser.rargs[0].startswith('-'):
            val = parser.rargs[0]
            parser.rargs.pop(0)
        else:
            val = arg_default
        setattr(parser.values, option.dest, val)

    return func


def parse_args():
    parser = OptionParser()
    parser.add_option('-i', '--include-decorators',
                      type='string',
                      action='callback',
                      callback=get_comma_separated_args,
                      dest='include_decorators',
                      help="a list of decorators to include in report\n"
                           "(comma separated values)")
    parser.add_option('-e', '--exclude-decorators',
                      type='string',
                      action='callback',
                      callback=get_comma_separated_args,
                      dest='exclude_decorators',
                      help="a list of decorators to exclude from report\n"
                           "(comma separated values)")
    parser.add_option("-s", "--skip_decorators", dest="skip_decorators",
                      action="store_true", default=False,
                      help="don't show decorators in report")
    parser.add_option("-b", "--track_bugs", dest="track_bugs",
                      action="store_true", default=False,
                      help="handle issues in decorator 'require'.\n"
                           "The best option: -i require -b -r")
    parser.add_option("-r", "--report", dest="html_report",
                      action='callback', callback=optional_arg('all_tests.html'),
                      help="generate html report into file")
    parser.add_option("-t", "--tests-file", dest="tests_file",
                      action='callback', callback=optional_arg('scylla_tests'),
                      help="file with the tests to include in report\n"
                           "('scylla_tests' by default")

    parser.set_usage("Usage: python get_all_tests.py [options].\n"
                     "For example:\n"
                     "  python get_all_tests.py -i freshCluster,require -e skipIf -s -t -r")
    (options, args) = parser.parse_args()
    return options.skip_decorators, options.include_decorators, \
           options.exclude_decorators, options.html_report, options.tests_file, options.track_bugs


def parse_nosetests_output(lines):
    tests = {}
    for l in lines:
        if "..." in l and 'Failure:' not in l:
            spl = l.split()
            test_name = spl[0]
            class_path = spl[1][1:-1]
            if class_path in tests:
                if test_name in tests[class_path]:
                    print "error!"
                else:
                    tests[class_path].append(test_name)
            else:
                tests[class_path] = [test_name]
    return tests


def parse_test_file(tests_file):
    tests = {}
    with open(tests_file) as f:
        for line in f:
            if line.strip()[-3:] == ".py":
                tests[line.strip()[:-3]] = {}
            elif ".py:" in line:
                module = line.strip().split(".py:")[0]
                if module not in tests:
                    tests[module] = {}
                path_class = line.strip().split(".py:")[1]
                test = path_class.split(".")[-1]
                cl = path_class.replace("." + test, "")
                if cl in tests[module]:
                    tests[module][cl].append(test)
                else:
                    tests[module][cl] = [test]
    result = {}
    for m, c_t in tests.iteritems():
        if not c_t:
            result[m] = []
        for c, t in c_t.iteritems():
            result[m + "." + c] = t
    # return dict of tests as : module_name.class_name : [list_of_tests]
    return result


def exists_in_tests_file(including_tests, p, t):
    # check if test test p.t exists in tests_file
    for path, tests in sorted(including_tests.iteritems()):
        if not tests and (p + "." + t).startswith(path):
            return True
        for test in tests:
            if path + "." + test in p + "." + t:
                return True
    return False


def main():
    skip_decorators, include_decorators, exclude_decorators, report_file, tests_file, track_bugs = parse_args()
    track_tests = {}
    if tests_file:
        track_tests = parse_test_file(tests_file)

    # get a list of tests via 'nosetests -v --collect-only'
    # nosetests loads all modules, so all external modules should be installed
    p = subprocess.Popen('nosetests -v --collect-only', shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    lines = []
    for line in p.stdout.readlines():
        lines.append(line.strip())
    p.wait()

    tests = parse_nosetests_output(lines)

    class_counter = tests_counter = 0

    if report_file:
        file = open(report_file, "w")
        file.write(header_report)

        if include_decorators:
            file.write("<p><font color=\"gray\">track file with tests: %s</font></p>" % tests_file)
        if include_decorators:
            file.write("<p><font color=\"green\">included decorators: %s</font></p>" % include_decorators)
        if exclude_decorators:
            file.write("<p><font color=\"#00008b\">excluded decorators: %s</font></p>" % exclude_decorators)
        if skip_decorators:
            file.write("<p>decorators skipped in report: %s</p>" % skip_decorators)

    # obtain all decorators for the tests
    for p, ts in sorted(tests.iteritems()):
        to_print = []
        for t in ts:
            module_name = p.rsplit('.', 1)[0]
            # verify if test exists in test file
            if track_tests and not exists_in_tests_file(track_tests, p, t):
                continue
            try:
                # read module with class
                with open(module_name.replace('.', '/') + ".py") as fr:
                    module_src = fr.readlines()
                if module_name == 'sstabledump_test':
                    # for sstabledump_test all tests locates in cqlsh_copy_test.py
                    with open('cqlsh_tests/cqlsh_copy_tests.py') as fr:
                        module_src.extend(fr.readlines())
                if module_name == 'sstableloader_test':
                    # for sstableloader_test all tests locates in migration_test.py
                    with open('migration_test.py') as fr:
                        module_src.extend(fr.readlines())
                test_line = ''
                for src_line in module_src:
                    if ("def " + t) in src_line:
                        test_line = src_line
                        break
                test_line_number = module_src.index(test_line)
                decorators = []
                # get only decorators for the test methods if they are
                for i in xrange(1, 5, 1):
                    if "@" in module_src[test_line_number - i]:
                        decorators.append(module_src[test_line_number - i].strip())
                    else:
                        break
                show = True
                if include_decorators:
                    show = False
                    for decorator in decorators:
                        for incl in include_decorators:
                            if decorator.split("(")[0] in "@" + incl:
                                show = True
                if exclude_decorators:
                    for decorator in decorators:
                        for excl in exclude_decorators:
                            if decorator.split("(")[0] in "@" + excl:
                                show = False
                if decorators and show and not skip_decorators:
                    prefix = "   %s      %s" % (t, decorators)
                    found = False
                    for decorator in decorators:
                        if track_bugs and ('require' in decorator or
                                          ("@skip" in decorator and 'scylladb/scylla' in decorator) or
                                          ("@skip" in decorator and re.findall(r'\d+', decorator) and len(re.findall(r'\d+', decorator)[0])>2)):
                            issue_id = re.findall(r'\d+', decorator)
                            if not len(issue_id):
                                to_print.append('%s <a>unable to parse decorator</a>' % prefix)
                            else:
                                issue_id = issue_id[0]
                                if 'scylla-tools-java' in decorator:
                                    issue_url = ISSUES_FOR_SCYLLA_TOOLS_JAVA_URL % issue_id
                                else:
                                    issue_url = ISSUES_FOR_SCYLLA_URL % issue_id
                                r = requests.get(issue_url)
                                if r.status_code in [404, 403]:
                                    issue_url = ISSUES_FOR_C_URL % issue_id
                                    r = requests.get(issue_url)
                                    status = json.loads(r.content)['fields']['status']['name']
                                    issue_url = REPORT_ISSUES_FOR_C_URL % issue_id
                                    if 'Resolved' == status:
                                        to_print.append('%s <a href="%s"><font color="FF5500"> C* Resolved</font></a>' % (prefix, issue_url))
                                        found = True
                                        break
                                    elif 'Closed' == status:
                                        to_print.append('%s <a href="%s"><font color="FF5500"> C* Closed</font></a>' % (prefix, issue_url))
                                        found = True
                                        break
                                    elif 'Patch Available' == status:
                                        to_print.append('%s <a href="%s"><font color="ADFF2F"> C* Patch Available</font></a>' % (prefix, issue_url))
                                        found = True
                                        break
                                    elif 'IN PROGRESS' == status:
                                        to_print.append('%s <a href="%s"><font color="808000"> C* IN PROGRESS</font></a>' % (prefix, issue_url))
                                        found = True
                                        break
                                    elif 'Open' == status:
                                        to_print.append('%s <a href="%s"><font color="#3CBC3C"> C* OPEN</font></a>' % (prefix, issue_url))
                                        found = True
                                        break
                                    else:
                                        to_print.append('not able to define status')
                                else:
                                    for line in r.content.split('\n'):
                                        if 'state state-closed' in line:
                                            found = True
                                            to_print.append('%s<a href="%s"><font color="FF00CC"> Scylla closed</font></a>' % (prefix, issue_url))
                                            break
                                        if 'state state-open' in line:
                                            found = True
                                            to_print.append('%s<a href="%s"><font color="008000"> Scylla open</font></a>' % (prefix, issue_url))
                                            break
                                    if not found:
                                        to_print.append("Status not found for  %s" % (issue_url))
                    if not found:
                        to_print.append("   %s      %s" % (t, decorators))
                elif show:
                    to_print.append("   %s" % t)
            except Exception as e:
                print e
        if to_print:
            class_counter += 1
            if report_file:
                file.write(
                    "<details><summary>%s         <font color=\"blue\">%s tests</font></summary>" %
                    (p, len(to_print)))
            print "%s         %s tests" % (p, len(to_print))
            for p in to_print:
                if report_file:
                    file.write("<div>%s</div>" % p)
                print p
                tests_counter += 1
            if report_file:
                file.write("</details>")

    print "\n     Total: %s tests in %s test classes" % \
          (tests_counter, class_counter)

    if report_file:
        print "\n     Html report file has been generated: %s\n" % report_file
        file.write("</body></html>")
        file.close()


if __name__ == "__main__":
    main()
