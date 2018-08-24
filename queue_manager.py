import argparse
import logging

from core.controller import Simulation


def start_simulation():
    """
    starts the simulation by handling the arguments, generating all objects and running through all for loops

    :return:
    """

    # handle arguments
    parser = argparse.ArgumentParser(description="starts a queue simulation with callers and agents.")
    parser.add_argument("--agents", type=int, help="defines the number of agents you want to use", required=True)
    parser.add_argument("--callers", type=int, help="defines the number of callers in queue", required=True)

    args = parser.parse_args()

    # create simulation object
    sim = Simulation(number_of_agents=args.agents, number_of_callers=args.callers)

    # generate agent list
    agent_list = sim.create_agents()

    # fill caller queue with start elements
    caller_queue = sim.add_easy_callers()

    # go into simulation (standard is 120 minutes)
    for minute in range(sim.time_simulation):

        logging.debug("minute: " + str(minute))

        # add callers to worklist if agents are available
        if caller_queue.qsize() > 0 and sim.agents_not_full:
            sim.add_callers_to_worklist()

        # go through all callers which agents work on
        for hash, caller in list(sim.work_list.items()):
            logging.debug("working on caller: " + str(caller.hash))

            # is the current caller processed?
            if not caller.in_process:
                logging.debug("caller not in process")

                # look for an free agent
                free_agent = sim.check_agents(agent_list)
                logging.debug("looking for free agents")

                # agent works on caller
                if free_agent is not None:
                    sim.work_on_new_caller(free_agent=free_agent, caller=caller)

                # no agent available
                else:
                    sim.jump(caller=caller)

            # if current caller is in process?
            else:
                sim.work_on_caller(caller=caller, hash=hash)

            # add up to total values of watiting and serve time
            sim.total_waiting_time += caller.waiting_time
            sim.total_serve_time += caller.serve_time

        sim.calc_average_times()


if __name__ == "__main__":
    start_simulation()
