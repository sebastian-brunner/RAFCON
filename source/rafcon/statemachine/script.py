"""
.. module:: script
   :platform: Unix, Windows
   :synopsis: A module to represent the script file for each state in a state machine

.. moduleauthor:: Sebastian Brunner


"""

import os
import imp
import sys
import yaml
from gtkmvc import Observable
from enum import Enum

from rafcon.statemachine.id_generator import *
import rafcon.statemachine.singleton
from rafcon.utils import log
logger = log.get_logger(__name__)
from rafcon.statemachine.enums import DEFAULT_SCRIPT_PATH


ScriptType = Enum('SCRIPT_TYPE', 'EXECUTION CONTAINER LIBRARY')

class Script(Observable, yaml.YAMLObject):

    """A class for representing the script file for each state in a state machine

    It inherits from Observable to make a change of its fields observable.

    :ivar path: the path where the script resides
    :ivar filename: the full name of the script file
    :ivar _compiled_module: the compiled module
    :ivar _script_id: the id of the script
    :ivar script_type: the type of the script i.e. Execution or Container
    :ivar check_path: a flag to indicate if the path should be checked for existence

    """

    DEFAULT_SCRIPT_EXECUTION = """

def execute(self, inputs, outputs, gvm):
    self.logger.debug("Hello world")
    return 0

"""

    DEFAULT_SCRIPT_CONTAINER = """

###########################################################
# Container States do not have a script
###########################################################

"""

    DEFAULT_SCRIPT_LIBRARY = """

###########################################################
# Do not add anything here, as it won't be executed anyway!
# For further information please refer to the API.
###########################################################

"""

    yaml_tag = u'!Script'

    def __init__(self, path=None, filename=None, script_type=None, check_path=True, state=None):

        Observable.__init__(self)

        self._path = path
        self._filename = filename
        self._compiled_module = None
        self._script_id = generate_script_id()
        self._state = state
        if script_type == ScriptType.EXECUTION:
            self.script = Script.DEFAULT_SCRIPT_EXECUTION
        elif script_type == ScriptType.LIBRARY:
            self.script = Script.DEFAULT_SCRIPT_LIBRARY
        else:
            self.script = Script.DEFAULT_SCRIPT_CONTAINER
        if path is None:
            self._path = os.path.join(DEFAULT_SCRIPT_PATH, state.get_path())
            if not os.path.exists(self._path):
                os.makedirs(self._path)
            if not filename:
                self._filename = "Script_%s.file" % str(self._script_id)
            script_file = open(os.path.join(self._path, self._filename), "w")
            script_file.write(self.script)
            script_file.close()

        if check_path:
            if not os.path.exists(self._path):
                raise RuntimeError("Path %s does not exist" % self._path)
            if not os.path.exists(os.path.join(self._path, self._filename)):
                raise RuntimeError("Path %s does not exist" % os.path.join(self._path, self._filename))

            # load and build the module per default else the default scripts will be loaded in self.script
            self.load_script()
            self.build_module()

    def reload_path(self, filename=None):
        self._path = self._state.get_file_system_path()
        if filename:
            self._filename = filename

    def execute(self, state, inputs={}, outputs={}, backward_execution=False):
        """
        Execute the custom "execute" function specified in the script.
        :param state: the state to which runs the execute function
        :param inputs: the input data of the script
        :param outputs: the output data of the script
        :return:
        """
        if backward_execution:
            if hasattr(self._compiled_module, "backward_execute"):
                return self._compiled_module.backward_execute(
                    state, inputs, outputs, rafcon.statemachine.singleton.global_variable_manager
                )
            else:
                logger.debug("No backward execution method found for state %s" % state.name)
                return None
        else:
            return self._compiled_module.execute(state, inputs, outputs,
                                                 rafcon.statemachine.singleton.global_variable_manager)

    def load_script(self):
        """Loads and builds the module given by the path and the filename
        """
        script_path = os.path.join(self._path, self._filename)

        try:
            script_file = open(script_path, 'r')
        except:
            logger.error("The script file could not be opened (path: %s)" % str(script_path))
            raise IOError("Script file could not be opened!")

        # reset script
        self.script = None
        self.script = script_file.read()
        script_file.close()

    def build_module(self):
        """Loads and builds the module given by the path and the filename
        """

        module_name = os.path.splitext(self._filename)[0] + str(self._script_id)

        # load module
        tmp_module = imp.new_module(module_name)
        sys.modules[module_name] = tmp_module

        code = compile(self.script, '%s (%s)' % (self._filename, self._script_id), 'exec')

        try:
            exec code in tmp_module.__dict__
        except RuntimeError, e:
            raise IOError("The compilation of the script module failed - error message: %s" % str(e))

        # return the module
        self._compiled_module = tmp_module

    # def get_path(self):
    #     """
    #     Returns the path of the script.
    #     Note: Normally you should use the get_filesystem_path of the state class.
    #     :return: the path where this script resides
    #     """
    #     return self._path

    @classmethod
    def to_yaml(cls, dumper, data):
        #TODO:implement
        dict_representation={}
        node = dumper.represent_mapping(u'!Script', dict_representation)
        return node

    @classmethod
    def from_yaml(cls, loader, node):
        #TODO:implement
        return None

#########################################################################
# Properties for all class fields that must be observed by gtkmvc
#########################################################################

    @property
    def filename(self):
        """Property for the _filename field

        """
        return self._filename

    @property
    def compiled_module(self):
        """Property for the _compiled_module field

        """
        return self._compiled_module

    # this setter should actually never be called as the module will be compiled by the build_module() function
    @compiled_module.setter
    @Observable.observed
    def compiled_module(self, compiled_module):
        self._compiled_module = compiled_module