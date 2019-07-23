import pytest

from tests import utils

from rafcon.utils.gui_functions import call_gui_callback


class GUITester(object):

    def __init__(self):
        import rafcon.core.singleton as core_singletons
        import rafcon.gui.singleton as gui_singletons

        self.post_test = None

        self.expected_warnings = 0
        self.expected_errors = 0

        self.singletons = gui_singletons
        self.core_singletons = core_singletons

    def __call__(self, *args, **kwargs):
        return call_gui_callback(*args, **kwargs)



@pytest.fixture
def gui(request, caplog):
    utils.dummy_gui(caplog)

    parameters = {} if not hasattr(request, "param") else request.param
    utils.run_gui(core_config=parameters.get("core_config"),
                  gui_config=parameters.get("gui_config"),
                  runtime_config=parameters.get("runtime_config"),
                  libraries=parameters.get("libraries"))

    gui_tester = GUITester()
    yield gui_tester

    utils.close_gui()
    utils.shutdown_environment(caplog=caplog, expected_warnings=gui_tester.expected_warnings, expected_errors=gui_tester.expected_errors)

    gui_tester.post_test and gui_tester.post_test()

