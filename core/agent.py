class Agent(object):
    """
    represents the agent who takes the calls from the queue

    """

    def __init__(self, id, free, minutes_till_ready=0):
        """
        constructor just sets the id

        :param name: string
        """
        self.id = id
        self.free = free
        self.minutes_till_ready = minutes_till_ready

    @staticmethod
    def consume(caller_list):
        """
        consumes callers from the queue and chats with the
        caller.

        :param caller_list:
        :return:
        """
        temp_caller = caller_list.consume_caller()
        print("agent consumes - " + str(temp_caller.chat()))
