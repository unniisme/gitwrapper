class CLIagent():
    """
    Handler for CLI commands
    Populate with functions prefixed with 'command_' for it to be added as a command.
    Functions starting with 'option_' will be treated as an option (ie. --something).
    'help' command is default and will be automatically populated with docstrings.
    """

    variables = {'test' : 0}

    def HandleCLI(*argv):
        if len(argv) == 1:
            return CLIagent.HandleCLI(*argv, 'help')

        for i,arg in enumerate(argv[1:]):
            # Handle options
            if arg[:2] == "--":
                try:
                    # Fetch argument count of option
                    op_arg_count = getattr(CLIagent, "option_" + arg[2:]).__code__.co_argcount
                    # Call the function with that many arguments following the option
                    op_args = argv[i+2: i+2+op_arg_count]
                    getattr(CLIagent, "option_" + arg[2:])(*op_args)
                    argv = list(argv)
                    argv.pop(i+1)                       # remove option
                    return CLIagent.HandleCLI(*argv)    # Can have multiple options
                except AttributeError as e:
                    # TODO : Handle argument mismatch
                    print("Unknown option : " + arg + ". Use help to get list of options")
                    return -1
                except Exception as e:
                    raise e

        for i,arg in enumerate(argv[1:]):
            try:
                # Fetch argument count of option
                cmd_arg_count = getattr(CLIagent, "command_" + arg).__code__.co_argcount
                # Call the function with that many arguments following the option
                cmd_args = argv[i+2: i+2+cmd_arg_count]
                getattr(CLIagent, "command_" + arg)(*cmd_args)
                return 0    #Only 1 command
            except AttributeError as e:
                # TODO : Handle argument mismatch
                print("Unknown command : " + arg + ". Use help to get list of options")
                return -1
            except Exception as e:
                raise e

    def main(argv = None):
        if argv == None:
            import sys
            argv = sys.argv

        # TODO: save state
        var_backup = CLIagent.variables.copy()

        CLIagent.HandleCLI(*argv)

        CLIagent.variables = var_backup
        
    def __init__(self, argv = None):
        return CLIagent.main(argv)


    def command_help():
        """
        Show help
        """
        for arg in dir(CLIagent):
            if arg[:8] == "command_":
                print(arg[8:], end="\t")
                print(getattr(CLIagent, arg).__doc__.replace("\n", "\t\n"))

        for arg in dir(CLIagent):
            if arg[:7] == "option_":
                print("--" + arg[7:], end="\t")
                print(getattr(CLIagent, arg).__doc__.replace("\n", "\t\n"))

    def command_template(a,b,c):
        """
        A template command.
        Takes 3 inputs and prints them.
        Also prints the instance variable "test"
        """
        print(a,b,c)
        print('test: ',CLIagent.variables['test'])

    def option_template(a, b):
        """
        A template option.
        Takes 2 inputs
        Set the value instance variable "test" to the sum of inputs
        """
        CLIagent.variables['test'] = int(a)+int(b)


if __name__ == '__main__':
    CLIagent()