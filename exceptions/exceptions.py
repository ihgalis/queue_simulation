class WeirdException(Exception):
    """
    exception will be used everytime something weird happens, which should not happen.
    """

    def __init__(self, message):
        """
        call the parent class

        :param message:
        """
        self.message = message
        super(Exception, self).__init__(message)

    def __str__(self):
        """
        make it printable in any case someone needs it
        
        :return:
        """
        return self.message
