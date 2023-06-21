#!/usr/bin/python3

import sys
import os
from ansi import *
from cliAgent import CLIagent

class GitWrapper(CLIagent):

    def handle_error(self, e):
        os.system("git " + " ".join(self.argv[1:]))

    def command_s(self):
        """
        git status
        """
        GitWrapper(["gitwrapper", "status"])

    def command_status(self):
        """
        git status
        """
        output_stream = os.popen("git status -sb")
        for line in output_stream.readlines():
            if line[:2] == "##":
                try:
                    branch, origin = line.split("...")
                    branch = " " + branch.strip()[2:] + " "
                    origin = str(Container(origin.strip(), "", Container.RED, "", "", formatting=Container.BOLD))
                    origin = origin.replace(" [", " "+Container.ansi_fmt[Container.DIM]).replace("]", Container.ansi_fmt[Container.RESET])
                    branch = str(Container(branch, Container.YELLOW, Container.BLACK))
                except:
                    branch = line
                    branch = " " + branch.strip()[2:] + " "
                    branch = str(Container(branch, Container.YELLOW, Container.BLACK))
                    origin = ""
                print(branch + " " + origin)
                print()

            elif line[1] == "M":
                print(Container("    ", Container.YELLOW, Container.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "M":
                print("\t", end="")
                print(Container("    ", Container.YELLOW, Container.BLACK), end=" ")
                print(line[2:].strip())

            elif line[:2] == "??":
                print(Container("    ", Container.GREEN, Container.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[:2] == "A ":
                print("\t" + str(Container("    ", Container.GREEN, Container.BLACK)), end=" ")
                print(line[2:].strip())

            elif line[1] == "D":
                print(Container("    ", Container.RED, Container.WHITE, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "D":
                print("\t", end="")
                print(Container("    ", Container.RED, Container.WHITE), end=" ")
                print(line[2:].strip())

            # Merge conflict, not currently correct
            elif line[1] == "U":
                print(Container("    ", Container.MAGENTA, Container.WHITE, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "U":
                print("\t", end="")
                print(Container("    ", Container.MAGENTA, Container.WHITE), end=" ")
                print(line[2:].strip())

            else:
                print(line)
        return

    def command_l(self):
        """
        git log
        """
        GitWrapper(["gitwrapper", "log"])
        
    def command_log(self):
        """
        git log
        """
        
        def printCommitMessage(commit_message):
            if commit_message != "":
                print()
                print(formatText("   ", Container.CYAN))
                print(formatText("".ljust(73), Container.GREY, Container.BLACK))
                print(commit_message.strip())
                print(formatText("".ljust(73), Container.GREY, Container.BLACK))
                print()

        output_stream = os.popen("git log --decorate")
        commit_message = ""
        for line in output_stream.readlines():
            if line[:6] == "commit":
                tokens = line[6:].split("(")
                
                # c1 = Container(" commit ", Container.ORANGE, Container.BLACK, start="", end=formatText("", Container.YELLOW, Container.ORANGE))
                print(formatText(" ", "", Container.YELLOW, Container.BOLD), end = "")
                c2 = Container(" " + tokens[0].strip() + " ", Container.YELLOW, Container.BLACK)
                c3 = Container.Empty()
                c4 = Container.Empty()

                if len(tokens) != 1:
                    branch = tokens[1].strip().strip(")")
                    tokens = branch.split("->")
                    if len(tokens) == 1:
                        c3 = Container(" " + tokens[0].strip() + " ", Container.RED, Container.WHITE)
                    else:
                        c3 = Container(" " + tokens[0].strip() + " ", Container.CYAN, Container.WHITE)
                        c4 = Container(" " + tokens[1].strip() + " ", Container.GREEN, Container.WHITE)

                print(Container.join(c2, c3, c4))

            elif line[:6] == "Author":
                print(formatText(" ", "", Container.MAGENTA), end=" ")
                # print(Container(line[8:].strip(), Container.MAGENTA, Container.WHITE))
                print(formatText(line[8:].strip(), formatting=Container.ITALIC))

            elif line[:4] == "Date":
                print(formatText(" ", "", Container.GREEN), end=" ")
                # print(Container(line[6:].strip(), Container.GREEN, Container.BLACK))
                print(formatText(line[6:].strip(), formatting=Container.ITALIC))


            elif line.strip() == "":
                printCommitMessage(commit_message)
                commit_message = ""
            
            else:
                commit_message += (formatText((" " + line.strip()).ljust(73), Container.GREY, Container.BLACK)) + "\n"
        
        printCommitMessage(commit_message)
        return
    
    def command_ll(self):
        """
        Oneline git log
        """

        def printCommitMessage(commit_message):
            if commit_message != "":
                print(commit_message.strip())

        output_stream = os.popen("git log --decorate")
        commit_message = ""
        for line in output_stream.readlines():
            if line[:6] == "commit":
                tokens = line[6:].split("(")
                
                c1 = Container("  ", Container.ORANGE, Container.BLACK, start="")
                c2 = Container(" " + tokens[0].strip()[:7] + " ", Container.YELLOW, Container.BLACK)
                c3 = Container.Empty()
                c4 = Container.Empty()

                if len(tokens) != 1:
                    branch = tokens[1].strip().strip(")")
                    tokens = branch.split("->")
                    if len(tokens) == 1:
                        c3 = Container(" " + tokens[0].strip() + " ", Container.RED, Container.WHITE)
                    else:
                        c3 = Container(" " + tokens[0].strip() + " ", Container.CYAN, Container.WHITE)
                        c4 = Container(" " + tokens[1].strip() + " ", Container.GREEN, Container.WHITE)

                print(Container.join(c1, c2, c3, c4), end="")

            elif line[:6] == "Author":
                print(Container(" " + line[8:].split("<")[0].strip(), Container.MAGENTA, Container.WHITE, start = dividers["CIRCLE"][0], end = dividers["CIRCLE"][1]), end="")

            elif line[:4] == "Date":
                continue

            elif line.strip() == "":
                printCommitMessage(commit_message)
                commit_message = ""

            else:
                commit_message += formatText(" " + line.strip(), formatting=Container.ITALIC)
                
        printCommitMessage(commit_message)
        return


if __name__ == "__main__":
    GitWrapper(sys.argv)
