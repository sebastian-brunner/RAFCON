"""
.. module:: state
   :platform: Unix, Windows
   :synopsis: A module to represent a state in the statemachine

.. moduleauthor:: Sebastian Brunner


"""

import threading
from gtkmvc import Observable
from mercurial.discovery import outgoing

from utils import log
logger = log.get_logger(__name__)
from outcome import Outcome
from script import Script
from statemachine_status import StateMachineStatus
from config import *
from utils.id_generator import *


class State(threading.Thread, Observable):

    """A class for representing a state in the state machine

    It inherits from Observable to make a change of its fields observable.

    :ivar _state_id: the id of the state
    :ivar _name: the name of the state
    :ivar _input_keys: holds the input data keys of the state
    :ivar _output_keys: holds the output data keys of the state
    :ivar _outcomes: holds the state outcomes, which are the connection points for transitions
    :ivar _is_start: indicates if this state is a start state of a hierarchy
    :ivar _is_final: indicates if this state is a end state of a hierarchy
    :ivar _sm_status: reference to the status of the statemachine
    :ivar _state_status: holds the status of the state
    :ivar _script: a script file that holds the definitions of the custom state functions (entry, execute, exit)

    """

    def __init__(self, state_id=None, name=None, input_keys=None, output_keys=None, outcomes=None, sm_status=None):
        Observable.__init__(self)
        threading.Thread.__init__(self)

        if state_id is None:
            self._state_id = generate_state_id()
        else:
            self._state_id = state_id
        self._name = name

        if not input_keys is None and not isinstance(input_keys, dict):
            raise TypeError("input_keys must be of type list or tuple")
        self._input_keys = input_keys

        if not output_keys is None and not isinstance(output_keys, dict):
            raise TypeError("output_keys must be of type list or tuple")
        self._output_keys = output_keys

        if not outcomes is None and not isinstance(outcomes, dict):
            raise TypeError("outcomes must be of type list or tuple")
        self._outcomes = outcomes

        self._is_start = None
        self._is_final = None
        self._sm_status = sm_status
        self._state_status = None
        self._script = None

        logger.debug("State with id %s initialized" % self._state_id)

    def add_input_key(self, name):
        """Add a new input key to the state

        """
        self._input_keys[name] = 0

    def add_output_key(self, name):
        """Add a new output key to the state

        """
        self._output_keys[name] = 0

    def add_outcome(self, name, outcome_id=None):
        """Add a new outcome to the state

        """
        if outcome_id is None:
            outcome_id = generate_outcome_id()
        outcome = Outcome(outcome_id, name)
        self._outcomes[outcome_id] = outcome
        return outcome_id

    def run(self):
        """Implementation of the abstract run() method of the :class:`threading.Thread`

        TODO: Should be filled with code, that should be executed for each state derivative
        """
        logger.debug("Starting state with id %s" % self._state_id)

#########################################################################
# Properties for all class fields that must be observed by gtkmvc
#########################################################################

    @property
    def state_id(self):
        """Property for the _state_id field

        """
        return self._state_id

    @state_id.setter
    @Observable.observed
    def state_id(self, state_id):
        """Setter function for the _id property

        :param state_id: The new id of the state. The type of the id has to be a string
        :type state_id: str
        """
        if not isinstance(state_id, str):
            raise TypeError("ID must be of type str")
        if len(state_id) < 1:
            raise ValueError("ID must have at least one character")

        self._state_id = state_id

    @property
    def name(self):
        """Property for the _name field

        """
        return self._name

    @name.setter
    @Observable.observed
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("Name must be of type str")
        if len(name) < 1:
            raise ValueError("Name must have at least one character")

        self._name = name

    @property
    def input_keys(self):
        """Property for the _input_keys field

        """
        return self._input_keys

    @input_keys.setter
    @Observable.observed
    def input_keys(self, input_keys):
        if not isinstance(input_keys, dict):
            raise TypeError("input_keys must be of type list or tuple")
        for key in input_keys:
            if not isinstance(key, str):
                raise TypeError("element of input_keys must be of type str")
        self._input_keys = input_keys

    @property
    def output_keys(self):
        """Property for the _output_keys field

        """
        return self._output_keys

    @output_keys.setter
    @Observable.observed
    def output_keys(self, output_keys):
        if not isinstance(output_keys, dict):
            raise TypeError("output_keys must be of type list or tuple")
        for key in output_keys:
            if not isinstance(key, str):
                raise TypeError("element of output_keys must be of type str")
        self._output_keys = output_keys

    @property
    def outcomes(self):
        """Property for the _outcomes field

        """
        return self._outcomes

    @outcomes.setter
    @Observable.observed
    def outcomes(self, outcomes):
        if not isinstance(outcomes, (list, tuple)):
            raise TypeError("outcomes must be of type list or tuple")
        for o in outcomes:
            if not isinstance(o, Outcome):
                raise TypeError("element of outcomes must be of type list or tuple")
        self._outcomes = outcomes

    @property
    def is_start(self):
        """Property for the _is_start field

        """
        return self._is_start

    @is_start.setter
    @Observable.observed
    def is_start(self, is_start):
        if not isinstance(is_start, bool):
            raise TypeError("is_start must be of type bool")
        self._is_start = is_start

    @property
    def is_final(self):
        """Property for the _is_final field

        """
        return self._is_final

    @is_final.setter
    @Observable.observed
    def is_final(self, is_final):
        if not isinstance(is_final, bool):
            raise TypeError("is_final must be of type bool")
        self._is_final = is_final

    @property
    def sm_status(self):
        """Property for the _sm_status field

        """
        return self._sm_status

    @sm_status.setter
    @Observable.observed
    def sm_status(self, sm_status):
        if not isinstance(sm_status, int):
            raise TypeError("sm_status must be of type int")
        self._sm_status = sm_status

    @property
    def state_status(self):
        """Property for the _state_status field

        """
        return self._state_status

    @state_status.setter
    @Observable.observed
    def state_status(self, state_status):
        if not isinstance(state_status, StateMachineStatus):
            raise TypeError("state_status must be of type StatemachineStatus")
        self._state_status = state_status

    @property
    def script(self):
        """Property for the _script field

        """
        return self._script

    @script.setter
    @Observable.observed
    def script(self, script):
        if not isinstance(script, Script):
            raise TypeError("script must be of type Script")
        self._script = script