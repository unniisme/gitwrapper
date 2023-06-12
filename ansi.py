
dividers = {
    "TRIANGLE"  : ("", ""),
    "CIRCLE"    : ("", ""),
    "LOWER_TRIANGLE" : ("", ""),
    "UPPER_TRIANGLE" : ("", ""),
    "FLAME"     : ("", ""),
    "WAVE"      : ("", ""),
    "PIXELS"    : ("", ""),
    "PIXELS_MORE" : ("", ""),
    "TRAPEZOID" : ("", "")
}

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
        "GREY" : "\033[47m",
        "YELLOW" : "\033[43m",
        "MAGENTA" : "\033[45m",
        "RED" : "\033[41m",
        "ORANGE" : "\033[48;2;255;165;0m"
    }

    def __init__(self, text, back_color, text_color, start=dividers["TRIANGLE"][0], end=dividers["TRIANGLE"][1], formatting=""):
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