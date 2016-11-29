from copy import copy, deepcopy
from gtkmvc import ModelMT

from rafcon.gui.models.state_element import StateElementModel
from rafcon.core.state_elements.data_port import DataPort
from rafcon.utils import log

logger = log.get_logger(__name__)


class DataPortModel(StateElementModel):
    """This model class manages a DataPort

    :param rafcon.core.data_port.DataPort data_port: The input/output data port to be wrapped
    :param rafcon.gui.models.abstract_state.AbstractStateModel parent: The state model of the state element
    :param rafcon.utils.vividict.Vividict meta: The meta data of the state element model
     """

    data_port = None

    __observables__ = ("data_port",)

    def __init__(self, data_port, parent, meta=None):
        """Constructor
        """
        super(DataPortModel, self).__init__(parent, meta)

        assert isinstance(data_port, DataPort)
        self.data_port = data_port

    def __str__(self):
        return "Model of DataPort: {0}".format(self.data_port)

    def __eq__(self, other):
        # logger.info("compare method")
        if isinstance(other, DataPortModel):
            return self.data_port == other.data_port and self.meta == other.meta
        else:
            return False

    def __copy__(self):
        data_port = copy(self.data_port)
        data_port_m = self.__class__(data_port, parent=None, meta=None)
        data_port_m.meta = deepcopy(self.meta)
        return data_port_m

    def __deepcopy__(self, memo=None, _nil=[]):
        return self.__copy__()

    @property
    def core_element(self):
        return self.data_port

    @ModelMT.observe("data_port", before=True, after=True)
    def model_changed(self, model, prop_name, info):
        super(DataPortModel, self).model_changed(model, prop_name, info)