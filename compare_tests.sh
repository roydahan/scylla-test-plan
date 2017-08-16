#!/bin/bash
python get_all_tests.py -e skip,require,since -t | grep -v 'No such file or directory' > temp_scylla_tests
python get_all_tests.py -e skip,require,since | grep -v 'No such file or directory' > temp_all_tests
echo '<span class="f6"><font color="808000">all tests from scylla_tests file (excluding skip, require, since):'>  compare_tests.html
for i in `seq 10`; do echo '&nbsp;' >> compare_tests.html;done
#echo '|' >> compare_tests.html
for i in `seq 4`; do echo '&nbsp;' >> compare_tests.html;done
echo 'all tests that we have in repository (excluding skip, require, since)</font></span>' >> compare_tests.html


echo '<p><span class="f6"><font color="808000">python get_all_tests.py -e skip,require,since -t'>>  compare_tests.html
for i in `seq 22`; do echo '&nbsp;' >> compare_tests.html;done
#echo '|' >> compare_tests.html
for i in `seq 4`; do echo '&nbsp;' >> compare_tests.html;done
echo 'python get_all_tests.py -e skip,require,since</font></span></p>' >> compare_tests.html


sdiff temp_scylla_tests temp_all_tests |  colordiff | ./ansi2html.sh --bg=dark --palette=xterm >> compare_tests.html

rm -rf temp_scylla_tests temp_all_tests


if [ "$(uname)" == "Darwin" ]; then
    open compare_tests.html
else
    xdg-open compare_tests.html &
fi

