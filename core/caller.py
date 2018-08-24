import hashlib


class Caller(object):
    """
    generates different caller objects
    """

    def factory(caller_type, minutes, in_process, waiting_time, serve_time, agent_id):
        if caller_type == "easy_caller":
            return EasyCaller(minutes, in_process, waiting_time, serve_time, agent_id)
        elif caller_type == "hard_caller":
            return HardCaller(minutes, in_process, waiting_time, serve_time, agent_id)

    factory = staticmethod(factory)

    def chat(self):
        pass


class EasyCaller(Caller):
    """
    easy_caller object reprsents caller who do not talk
    that much.
    """

    def __init__(self, minutes, in_process, waiting_time, serve_time, agent_id=False):
        """
        standard constructor sets a couple of variables

        :param minutes: integer telling how many minutes the caller needs
        :param in_process: boolean value which tells you whether the caller is within a talk to the agent
        :param agent_id: integer saves the id of the agent
        """
        self.minutes = minutes
        self.in_process = in_process
        self.agent_id = agent_id
        self.waiting_time = waiting_time
        self.serve_time = serve_time

        m = hashlib.sha256()
        hash_string = self.minutes + self.in_process + self.agent_id + self.waiting_time + self.serve_time
        m.update(str(hash_string).encode('utf-8'))
        self.hash = m.hexdigest()

    @staticmethod
    def chat():
        """
        standard chat method

        :return:
        """
        return "bla bla bla!"


class HardCaller(Caller):
    """
    hard_caller object reprsents caller who do not talk
    that much.
    """

    def __init__(self, minutes, in_process, waiting_time, serve_time, agent_id=False):
        """
        standard constructor sets a couple of variables

        :param minutes: integer telling how many minutes the caller needs
        :param in_process: boolean value which tells you whether the caller is within a talk to the agent
        :param agent_id: integer saves the id of the agent
        """
        self.minutes = minutes
        self.in_process = in_process
        self.agent_id = agent_id
        self.waiting_time = waiting_time
        self.serve_time = serve_time

    @staticmethod
    def chat():
        """
        stanard chat method

        :return:
        """
        return "bla bla bla bla bla bla!!"
