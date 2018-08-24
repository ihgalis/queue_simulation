import unittest

from core.controller import Caller
from core.controller import Simulation


class TestQueueSimulation(unittest.TestCase):
    """
    tests the entire construct
    """

    def setUp(self):
        """
        sets up the test object (Simulation class) and some variables

        :return:
        """

        self.number_of_agents = 2
        self.number_of_callers = 5
        self.test_sim = Simulation(number_of_agents=self.number_of_agents, number_of_callers=self.number_of_callers)

    def testSimulationObject(self):
        """
        tests some basic settings in simulation

        :return:
        """

        # correct class type
        self.assertEqual(str(type(self.test_sim)), "<class 'core.controller.Simulation'>")

        # should be empty
        self.assertEqual(len(self.test_sim.agent_list), 0)
        self.assertEqual(self.test_sim.caller_queue.qsize(), 0)

    def testAgentCreation(self):
        """
        tests the agent creation

        :return:
        """
        agent_list = self.test_sim.create_agents()
        self.assertEqual(len(agent_list), 2)
        self.assertEqual(str(type(agent_list)), "<class 'list'>")

    def testCallerAdd(self):
        """
        tests caller add method

        :return:
        """

        caller_queue = self.test_sim.add_easy_callers()
        self.assertEqual(caller_queue.qsize(), 5)
        self.assertEqual(str(type(caller_queue)), "<class 'queue.Queue'>")

    def testCheckAgents(self):
        """
        tests whether there is a free agent

        :return:
        """

        agent_list = self.test_sim.create_agents()
        agent = self.test_sim.check_agents(agent_list)

        self.assertEqual(str(type(agent)), "<class 'core.agent.Agent'>")
        self.assertTrue(agent.free)

    def testAddCallersToWorklist(self):
        """
        test adding callers to worklist

        :return:
        """

        temp_caller = self.test_sim.add_callers_to_worklist()
        self.assertEqual(str(type(temp_caller)), "test")
        self.assertIn(temp_caller, self.test_sim.work_list)

    def testWorkOnNewCaller(self):
        """
        a more complex test where the work on a new caller is done

        :return:
        """
        agent_list = self.test_sim.create_agents()
        free_agent = self.test_sim.check_agents(agent_list=agent_list)

        self.assertNotEqual(free_agent, None)
        self.test_sim.work_on_new_caller(free_agent=free_agent, caller=self.test_sim.work_list[0])

    def testJump(self):
        """
        test the caller jump (increasing waiting time etc.)

        :return:
        """

        first_waiting_time = self.test_sim.work_list[0].waiting_time
        self.test_sim.jump(caller=self.test_sim.work_list[0])
        self.assertEqual(self.test_sim.work_list[0].waiting_time, first_waiting_time+1)

    def testWorkOnCaller(self):
        """
        some actions should be tested which are done within the work_on_caller method

        :return:
        """
        caller = Caller.factory(caller_type="easy_caller", minutes=5, in_process=0, waiting_time=0, serve_time=0,
                                agent_id=False)

        new_caller = self.test_sim.work_on_caller(caller=caller, hash=caller.hash)
        self.assertEqual(new_caller.minutes, caller.minutes+1)

        caller2 = Caller.factory(caller_type="easy_caller", minutes=0, in_process=0, waiting_time=0, serve_time=0,
                                 agent_id=False)

        new_caller2 = self.test_sim.work_on_caller(caller=caller2, hash=caller2.hash)

        # should have increased by 1
        self.assertEqual(self.test_sim.current_callers_worked_on, 1)

        # should be False
        self.assertFalse(new_caller2.in_process)

    def testCalcAverageTimes(self):
        """
        test the algorithm for average times. waiting and serve time.

        :return:
        """

        # waiting time
        self.test_sim.total_waiting_time = 489387
        self.test_sim.current_callers_worked_on = 876
        test_average_wait = self.test_sim.total_waiting_time / self.test_sim.current_callers_worked_on

        # serve time
        self.test_sim.total_serve_time = 892634
        test_serve_average = self.test_sim.total_serve_time / self.test_sim.current_callers_worked_on

        self.test_sim.calc_average_times()
        self.assertEqual(self.test_sim.average_waiting_time, test_average_wait)
        self.assertEqual(self.test_sim.average_serve_time, test_serve_average)
