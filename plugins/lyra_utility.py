""" Template for a lyra python utility  """

ERROR_CODES = {
    "1": "Improper plugin inputs supplied. ",
    "2": "Runtime error: "

}


class lyra_utility(object):
    def __init__(self, inputs):
        """ Initializes the plugin and registers it's inputs """
        self.output_log = []
        self.register_inputs(inputs)
        self.register_commands()

    def register_inputs(self, inputs):
        """
            Validate and initialize inputs necessary for this plugin to run.
            If required inputs are not supplied, plugin cannot will return an error code

        """
        pass

    def register_commands(self, commands):
        """ Register possible commands """
        pass

    def run_function(self, cmd, params):
        self.possible_commands[cmd](params)

    def log(self, message):
        self.output_log.append(message)
