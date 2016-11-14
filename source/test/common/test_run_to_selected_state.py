# singleton elements
import rafcon.statemachine.singleton
from rafcon.statemachine.storage import storage


# test environment elements
import testing_utils
from rafcon.statemachine.enums import StateExecutionState
from rafcon.utils.constants import RAFCON_TEMP_PATH_BASE
from rafcon.utils import log

import time
import pytest

logger = log.get_logger(__name__)


def test_run_to_selected_state(caplog):

    rafcon.statemachine.singleton.state_machine_manager.delete_all_state_machines()
    testing_utils.test_multithrading_lock.acquire()

    sm = storage.load_state_machine_from_path(testing_utils.get_test_sm_path("unit_test_state_machines/"
                                                                             "run_to_selected_state_test"))
    # select state machine for this purpose
    rafcon.statemachine.singleton.state_machine_manager.add_state_machine(sm)
    rafcon.statemachine.singleton.state_machine_execution_engine.run_to_selected_state("VVBPOY/AOZXRY",
                                                                                       sm.state_machine_id)
    # run the statemachine to the state before AOYXRY, this is an asynchronous task
    timeout = time.time()
    while not sm.get_state_by_path("VVBPOY/ABNQFK").state_execution_status is StateExecutionState.WAIT_FOR_NEXT_STATE:
        time.sleep(.05)
        if time.time()-timeout > 2:
            raise RuntimeError("execution_state ABNQFK not reached --> timeout")
    # wait until the statemachine is executed until ABNQFK the state before AOZXRY, so it doesnt check for the file
    # before its even written

    with open(RAFCON_TEMP_PATH_BASE + '/test_file', 'r') as test_file:
        lines = test_file.readlines()

    # the state machines waits at ABNQFK with state WAIT_FOR_NEXT_STATE, so it needs to be stopped manually
    rafcon.statemachine.singleton.state_machine_execution_engine.stop()
    rafcon.statemachine.singleton.state_machine_execution_engine.join()

    assert len(lines) < 3

    # read all lines of the file and check if not more than 2 states have written to it
    testing_utils.test_multithrading_lock.release()
    testing_utils.assert_logger_warnings_and_errors(caplog)


if __name__ == '__main__':
    # test_run_to_selected_state(None)
    pytest.main([__file__])