import random
import logging

from queue import Queue
from core.agent import Agent
from core.caller import Caller
from exceptions.exceptions import WeirdException


class Simulation(object):
    """
    manages the entire simulation
    """

    def __init__(self, number_of_agents, number_of_callers, time_simulation=120):
        """
        constructor creates the queue und different variables needed for the correct
        implementation

        :param number_of_agents: selfexplanatory
        :param number_of_callers: selfexplanatory
        """

        self.number_of_agents = number_of_agents
        self.number_of_callers = number_of_callers

        self.agent_list = list()

        logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        self.caller_queue = Queue(maxsize=self.number_of_callers)
        logging.debug("queue generated")

        self.time_simulation = time_simulation
        self.average_waiting_time = 0
        self.average_serve_time = 0

        self.total_waiting_time = 0
        self.total_serve_time = 0

        # used as divisor - should increase with every finished caller
        self.current_callers_worked_on = 0

        # list of callers which is worked on
        self.work_list = dict()

        # agent steering variable
        self.agents_not_full = True

    def create_agents(self):
        """
        create agent list

        :return: list containing all generated agents
        """

        # create agenets
        for count in range(self.number_of_agents):
            self.agent_list.append(Agent(count, True))

        logging.debug("agent list created with " + str(len(self.agent_list)) + " agents")
        return self.agent_list

    def add_easy_callers(self):
        """
        add callers to the queue

        :return: queue including all generated callers
        """

        # add the first callers!
        for count in range(self.number_of_callers):
            self.caller_queue.put(
                Caller.factory(caller_type="easy_caller", minutes=random.randint(2, 20), in_process=0, waiting_time=0,
                               serve_time=0, agent_id=False))

        logging.debug("callers generated: " + str(self.caller_queue.qsize()))

        return self.caller_queue

    @staticmethod
    def check_agents(agent_list):
        """
        return the first free agent

        :param agent_list: defines the list which should be used to find the free agent
        :return: agent|None
        """

        agent_list_length = len(agent_list)

        for count, agent in enumerate(agent_list):
            # free agent and not the end of list?
            if agent.free and count != agent_list_length:
                return agent

            # end of loop without free agent?
            elif count == agent_list_length:
                return None

    def add_callers_to_worklist(self):
        """
        get one element from queue and add it to worklist to keep track of all

        :return:
        """

        temp_caller = self.caller_queue.get()

        logging.debug("got caller from queue " + temp_caller.hash + " into worklist")

        self.work_list[temp_caller.hash] = temp_caller
        return temp_caller

    def work_on_new_caller(self, free_agent, caller):
        """
        performs the work on the caller

        :param free_agent: the agent which should work on the caller
        :param caller: the caller which should be worked on
        :return:
        """

        self.agents_not_full = True
        free_agent.free = False

        logging.debug("agent " + str(free_agent.id) + " works on caller " + caller.hash + " for " + str(
            caller.minutes) + " minutes")
        caller.in_process = True

    def jump(self, caller):
        """
        jump the caller and increase it's waiting time

        :param caller: the caller which should be jumped
        :return:
        """

        logging.debug("no free agents available")
        self.agents_not_full = False
        caller.waiting_time += 1
        logging.debug("caller " + str(caller.hash) + " waits now " + str(caller.waiting_time) + " minutes")

    def work_on_caller(self, caller, hash):
        """
        works on the caller, like decreasing the servetime etc.

        :param caller: the caller to be worked on
        :param hash: the hash needed for identification
        :return:
        """

        logging.debug("caller in process")

        # callers where it needs to be worked on
        if caller.minutes > 0:
            logging.debug("serve time for caller " + str(caller.hash) + " is now " + str(caller.serve_time))

            # decrease the caller time
            caller.minutes -= 1
            logging.debug(
                "for caller " + str(caller.hash) + " there is still work open: " + str(caller.minutes) + " minutes")

        # work on a caller finished
        elif caller.minutes == 0:

            # increment because we need a divisor for the avarage serve time
            self.current_callers_worked_on += 1

            # callers which are ready
            current_agent = self.agent_list[caller.agent_id]
            current_agent.free = True
            logging.debug("agent is free now")

            # set caller on offline
            caller.in_process = False
            logging.debug("caller " + str(caller.hash) + " is not in process anymore")

            # delete caller from dict
            del self.work_list[hash]
        else:
            raise WeirdException("Something weird happend :-(")

        return caller

    def calc_average_times(self):
        """
        calculate the average time (divison by zero possible)

        :return:
        """

        try:
            self.average_waiting_time = self.total_waiting_time / self.current_callers_worked_on
            self.average_serve_time = self.total_serve_time / self.current_callers_worked_on
        except ZeroDivisionError:
            # no need to worry
            pass

        logging.debug("average waiting time: " + str(self.average_waiting_time))
        logging.debug("average serve time: " + str(self.average_serve_time))
