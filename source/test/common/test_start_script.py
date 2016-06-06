import pytest
from os.path import realpath, dirname
import rafcon
import subprocess
import os
import testing_utils
# /tmp/rafcon/unittests/test_start_script.txt??? /tmp/rafcon_unit_test/test_start_script.txt


def test_start_script_open():
    script = dirname(realpath(rafcon.__file__)) + "/statemachine/start.py"
    start_path = rafcon.__path__[0] + "/../test_scripts/unit_test_state_machines/start_script_test"
    cmd = "python %s -o %s" % (script, start_path)
    subprocess.call(cmd, shell=True)
    tmp_file = open("/tmp/rafcon_unit_tests/test_start_script.txt", "r")
    res = tmp_file.read()
    tmp_file.close()
    assert (res == "start, state, "), "start script failed"
    os.remove("/tmp/rafcon_unit_tests/test_start_script.txt")


def test_start_script_state():
    script = dirname(realpath(rafcon.__file__)) + "/statemachine/start.py"
    start_path = rafcon.__path__[0] + "/../test_scripts/unit_test_state_machines/start_script_test"
    state_path = "UTUOSC/AHWBOG"
    cmd = "python %s -o %s -s %s" % (script, start_path, state_path)
    subprocess.call(cmd, shell=True)
    tmp_file = open("/tmp/rafcon_unit_tests/test_start_script.txt", "r")
    res = tmp_file.read()
    tmp_file.close()
    assert (res == "state, "), "start from state failed"
    os.remove("/tmp/rafcon_unit_tests/test_start_script.txt")


def test_start_script_valid_config():
    # valid config
    script = dirname(realpath(rafcon.__file__)) + "/statemachine/start.py"
    start_path = rafcon.__path__[0] + "/../test_scripts/unit_test_state_machines/start_script_test"
    config = rafcon.__path__[0] + "/../test/common/configs_for_start_script_test/valid_config"
    cmd = "python %s -o %s -c %s" % (script, start_path, config)
    subprocess.call(cmd, shell=True)
    tmp = open("/tmp/rafcon_unit_tests/test_start_script.txt", "r")
    res = tmp.read()
    tmp.close()
    assert (res == "start, state, "), "start with valid config failed"
    os.remove("/tmp/rafcon_unit_tests/test_start_script.txt")


'''
def test_start_script_invalid_config(caplog):
    # invalid config
    script = dirname(realpath(rafcon.__file__)) + "/statemachine/start.py"
    start_path = rafcon.__path__[0] + "/../test_scripts/unit_test_state_machines/start_script_test"
    config = rafcon.__path__[0] + "/../test/common/configs_for_start_script_test/invalid_config"
    cmd = "python %s -o %s -c %s" % (script, start_path, config)
    subprocess.call(cmd, shell=True)
    tmp = open("/tmp/rafcon_unit_tests/test_start_script.txt", "r")
    res = tmp.read()
    tmp.close()
    assert (res == "start, state, "), "start with invalid config failed"
    os.remove("/tmp/rafcon_unit_tests/test_start_script.txt")
    testing_utils.assert_logger_warnings_and_errors(caplog, 0, 0)
'''

if __name__ == '__main__':
    # test_start_script_state(None)
    pytest.main([__file__])


