import sys
import os

class colors:

    # Only for autocomplete lol
    BOLD = "BOLD" 
    DIM = "DIM" 
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

def container(text, back_color, text_color, start="", end="", formatting=""):
    return colors.ansi_fg[back_color] + start + formatText(text, back_color, text_color, formatting) + colors.ansi_fg[back_color] + end + colors.ansi_fmt[colors.RESET]

def formatText(text, back_color = "", text_color = "", formatting = ""):
    return colors.ansi_bg[back_color] + colors.ansi_fg[text_color] + colors.ansi_fmt[formatting] + text + colors.ansi_fmt[colors.RESET]


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
                    origin = container(origin.strip(), "", colors.RED, "", "", formatting=colors.BOLD)
                    origin = origin.replace(" [", " "+colors.ansi_fmt[colors.DIM]).replace("]", colors.ansi_fmt[colors.RESET])
                    branch = container(branch, colors.YELLOW, colors.BLACK)
                except:
                    branch = line
                    branch = " " + branch.strip()[2:] + " "
                    branch = container(branch, colors.YELLOW, colors.BLACK)
                    origin = ""
                print(branch + " " + origin)
                print()

            elif line[1] == "M":
                print(container(" Modified ", colors.YELLOW, colors.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "M":
                print("\t", end="")
                print(container(" Modified ", colors.YELLOW, colors.BLACK), end=" ")
                print(line[2:].strip())

            elif line[:2] == "??":
                print(container(" Added    ", colors.GREEN, colors.BLACK, ""), end=" ")
                print(line[2:].strip())
            elif line[:2] == "A ":
                print("\t" + container(" Added    ", colors.GREEN, colors.BLACK), end=" ")
                print(line[2:].strip())

            elif line[1] == "D":
                print(container(" Deleted  ", colors.RED, colors.WHITE, ""), end=" ")
                print(line[2:].strip())
            elif line[0] == "D":
                print("\t", end="")
                print(container(" Deleted  ", colors.RED, colors.WHITE), end=" ")
                print(line[2:].strip())

            else:
                print(line)
         return
        
    elif argv[1] == "l" or argv[1] == "log":
         output_stream = os.popen("git log --decorate")
         for line in output_stream.readlines():
            if line[:6] == "commit":
                print(container(" commit ", colors.ORANGE, colors.BLACK, start="", end=formatText("", colors.YELLOW, colors.ORANGE)), end="")
                print(container(" " + line[6:].strip() + " ", colors.YELLOW, colors.BLACK, start=""))

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
