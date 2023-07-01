class CLIagent():
    """
    Handler for CLI commands
    Populate with functions prefixed with 'command_' for it to be added as a command.
        function arguments are command arguments. *args is all the next arguments
    Functions starting with 'option_' will be treated as an option (ie. --something).
    'help' command is default and will be automatically populated with docstrings.
    """

    variables = {'test' : 0}

    def HandleCLI(self, *argv):
        if len(argv) == 1:
            return self.HandleCLI(*argv, 'help')

        for i,arg in enumerate(argv[1:]):
            # Handle options
            if arg[:2] == "--":
                try:
                    # Fetch argument count of option
                    op_arg_count = getattr(self, "option_" + arg[2:]).__code__.co_argcount - 1
                    # Call the function with that many arguments following the option
                    op_args = argv[i+2: i+2+op_arg_count]
                    getattr(self, "option_" + arg[2:])(*op_args)
                    argv = list(argv)
                    argv.pop(i+1)                       # remove option
                    return self.HandleCLI(*argv)    # Can have multiple options
                except AttributeError as e:
                    # TODO : Handle argument mismatch
                    print("Unknown option : " + arg + ". Use help to get list of options")
                    return -1
                except Exception as e:
                    raise e

        for i,arg in enumerate(argv[1:]):
            try:
                command_function = getattr(self, "command_" + arg)
                
                # See if it takes all the next arguments
                if command_function.__code__.co_flags & 0x04:
                    cmd_args = argv[i+2:]
                    command_function(*cmd_args)
                    return 0

                # Fetch argument count of command
                cmd_arg_count = command_function.__code__.co_argcount - 1
                # Call the function with that many arguments following the command
                cmd_args = argv[i+2: i+2+cmd_arg_count]
                command_function(*cmd_args)
                return 0    #Only 1 command
            except AttributeError as e:
                self.handle_error(e)
                return -1
            except Exception as e:
                raise e

    def main(self, argv = None):
        if argv == None:
            import sys
            argv = sys.argv

        self.argv = argv
        self.HandleCLI(*argv)

    def handle_error(self, e : Exception):
        # TODO : Handle argument mismatch
        print("Unknown command : " + arg + ". Use help to get list of options")



        
    def __init__(self, argv = None):
        # TODO: save state
        self.variables = CLIagent.variables.copy()
        self.main(argv)


    def command_help(self):
        """
        Show help
        """
        for arg in dir(self):
            if arg[:8] == "command_":
                print(arg[8:], end="\t")
                print(getattr(self, arg).__doc__.replace("\n", "\t\n"))

        for arg in dir(self):
            if arg[:7] == "option_":
                print("--" + arg[7:], end="\t")
                print(getattr(self, arg).__doc__.replace("\n", "\t\n"))

    # def command_template(self, a,b,c):
    #     """
    #     A template command.
    #     Takes 3 inputs and prints them.
    #     Also prints the instance variable "test"
    #     """
    #     print(a,b,c)
    #     print('test: ',self.variables['test'])

    # def option_template(self, a, b):
    #     """
    #     A template option.
    #     Takes 2 inputs
    #     Set the value instance variable "test" to the sum of inputs
    #     """
    #     self.variables['test'] = int(a)+int(b)


if __name__ == '__main__':
    CLIagent()