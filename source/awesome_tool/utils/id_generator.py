"""
.. module:: id_generator
   :platform: Unix, Windows
   :synopsis: A module to generate different kinds of state machine ids

.. moduleauthor:: TODO


"""

import string
import random


transition_id_counter = 0
data_flow_id_counter = 0
state_id_counter = 0
outcome_id_counter = 0


def generate_transition_id():
    global transition_id_counter
    transition_id_counter += 1
    return transition_id_counter


def generate_data_flow_id():
    global data_flow_id_counter
    data_flow_id_counter += 1
    return data_flow_id_counter


def generate_state_id():
    global state_id_counter
    state_id_counter += 1
    return state_id_counter

def generate_outcome_id():
    global outcome_id_counter
    outcome_id_counter += 1
    return outcome_id_counter


def state_id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))