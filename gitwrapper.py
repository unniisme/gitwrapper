import sys
import os

class Container:

    # Only for autocomplete lol
    BOLD = "BOLD" 
    DIM = "DIM" 
    ITALIC = "IT"
    RESET = "RESET" 
    UNBOLD = "UNBOLD" 
    UNDIM = "UNDIM"   
    GREY = "GREY"  
    RED = "RED" 
    WHITE = "WHITE" 
    ORANGE = "ORANGE"
    BLACK = "BLACK" 
    BLUE = "BLUE" 
    CYAN = "CYAN" 
    GREEN = "GREEN" 
    YELLOW = "YELLOW" 
    MAGENTA = "MAGENTA" 

    ansi = {
        "" : "",
        "FMT_BOLD" : "\033[01m",
        "FMT_DIM" : "\033[02m",
        "FMT_RESET" : "\033[00m",
        "FMT_UNBOLD" : "\033[22m",
        "FMT_UNDIM" : "\033[22m",
        "FG_BLACK" : "\033[30m",
        "FG_BLUE" : "\033[34m",
        "FG_CYAN" : "\033[36m",
        "FG_GREEN" : "\033[32m",
        "FG_YELLOW" : "\033[33m",
        "FG_GREY" : "\033[37m",
        "FG_MAGENTA" : "\033[35m",
        "FG_RED" : "\033[31m",
        "FG_WHITE" : "\033[97m",
        "FG_ORANGE" : "\033[38;2;255;165;0m",
        "BG_BLACK" : "\033[40m",
        "BG_BLUE" : "\033[44m",
        "BG_CYAN" : "\033[46m",
        "BG_GREEN" : "\033[42m",
        "BG_YELLOW" : "\033[43m",
        "BG_MAGENTA" : "\033[45m"
    }

    ansi_fmt = {
        "" : "",
        "BOLD" : "\033[01m",
        "IT" : "\033[03m",
        "DIM" : "\033[02m",
        "RESET" : "\033[00m"
    }

    ansi_fg = {
        "" : "",
        "BLACK" : "\033[30m",
        "BLUE" : "\033[34m",
        "CYAN" : "\033[36m",
        "GREEN" : "\033[32m",
        "YELLOW" : "\033[33m",
        "GREY" : "\033[37m",
        "MAGENTA" : "\033[35m",
        "RED" : "\033[31m",
        "WHITE" : "\033[97m",
        "ORANGE" : "\033[38;2;255;165;0m"
    }

    ansi_bg = {
        "" : "",
        "BLACK" : "\033[40m",
        "BLUE" : "\033[44m",
        "CYAN" : "\033[46m",
        "GREEN" : "\033[42m",
        "YELLOW" : "\033[43m",
        "MAGENTA" : "\033[45m",
        "RED" : "\033[41m",
        "ORANGE" : "\033[48;2;255;165;0m"
    }

    def __init__(self, text, back_color, text_color, start="", end="", formatting=""):
        self.text = text
        self.back_color = back_color
        self.text_color = text_color
        self.start = start
        self.end = end
        self.formatting = formatting

    def to_string(self):
        return Container.ansi_fg[self.back_color] + self.start + formatText(self.text, self.back_color, self.text_color, self.formatting) + Container.ansi_fg[self.back_color] + self.end + Container.ansi_fmt[Container.RESET]

    def __str__(self):
        return self.to_string()

    def join(*args) -> str:
        # Joins to the right only
        for i in range(len(args)-1):
            args[i].end = formatText(args[i].end, args[i+1].back_color, args[i].back_color)
            args[i+1].start = ""
        return "".join([str(c) for c in args])

    def Empty():
        return Container("", "", "", "", "")

def formatText(text, back_color = "", text_color = "", formatting = "", text_formatting = ""):
    return Container.ansi_bg[back_color] + Container.ansi_fg[text_color] + Container.ansi_fmt[formatting] + text_formatting + text + Container.ansi_fmt[Container.RESET]

def container(text, back_color, text_color, start="", end="", formatting=""):
    return Container(text, back_color, text_color, start, end, formatting).to_string()

def main(argv):
    if len(argv) == 1:
        print("Help")
        return

    if argv[1] == "s" or argv[1] == "status":
         output_stream = os.popen("git status -sb")
         for line in output_stream.readlines():
            if line[:2] == "##":
                try:
                    branch, origin = line.split("...")
                    branch = " " + branch.strip()[2:] + " "
                    origin = container(origin.strip(), "", Container.RED, "", "", formatting=Container.BOLD)
                    origin = origin.replace(" [", " "+Container.ansi_fmt[Container.DIM]).replace("]", Container.ansi_fmt[Container.RESET])
                    branch = container(branch, Container.YELLOW, Container.BLACK)
                except:
                    branch = line
                    branch = " " + branch.strip()[2:] + " "
                    branch = container(branch, Container.YELLOW, Container.BLACK)
                    origin = ""
                print(branch + " " + origin)
                print()

            elif line[1] == "M":
                print(container(" Modified ", Container.YELLOW, Container.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "M":
                print("\t", end="")
                print(container(" Modified ", Container.YELLOW, Container.BLACK), end=" ")
                print(line[2:].strip())

            elif line[:2] == "??":
                print(container(" Added    ", Container.GREEN, Container.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[:2] == "A ":
                print("\t" + container(" Added    ", Container.GREEN, Container.BLACK), end=" ")
                print(line[2:].strip())

            elif line[1] == "D":
                print(container(" Deleted  ", Container.RED, Container.WHITE, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "D":
                print("\t", end="")
                print(container(" Deleted  ", Container.RED, Container.WHITE), end=" ")
                print(line[2:].strip())

            else:
                print(line)
         return
        
    elif argv[1] == "l" or argv[1] == "log":
         output_stream = os.popen("git log --decorate")
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


            else:
                print(line.strip())
         return

    elif argv[1] == "a" or argv[1] == "add":
        os.system("git add " + " ".join(argv[2:]))
        return main(["gw", "s"])
    
    os.system("git " + " ".join(argv[1:]))
    return


if __name__ == "__main__":
    main(sys.argv)
