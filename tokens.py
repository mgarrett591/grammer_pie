import enum

class style(enum.Enum):
    default = -1
    normal = 0
    bold = 1
    light = 2
    italicized = 3
    underline = 4
    blink = 5
    
class color(enum.Enum):
    default = -1
    black = 0
    red = 1
    green = 2
    yellow = 3
    blue = 4
    purple = 5
    cyan = 6
    white = 7

class partOfSpeech(enum.Enum):
    unknown = 0
    noun = 1
    pronoun = 2
    adjective = 3
    verb = 4
    adverb = 5
    particle = 6
    article = 7
    
class errorState(enum.Enum):
    okay = 0
    miss_spelled = 1
    grammer_error = 2

class span():
    def __init__(self, text, style=style.default, text_color=color.default, background_color=color.default):

        self.raw_text = text
    
    def css_format():
        return self.raw_text
    
class Token():
    def __init__(self,style=style.default, text_color=color.default, background_color=color.default):
        self.leading_whitespace = ""
        self.body = ""
        self.trailing_whitespace = ""
        self.style = style
        self.text_color = text_color
        self.background_color = background_color
        self.partOfSpeech = partOfSpeech.unknown
        self.errorState = errorState.okay
    def _add_letter(self,letter):
        if(self._whiteSpaceLetter(letter)):
            if(self.body == ""):
                self.leading_whitespace += letter
                return True
            else:
                self.trailing_whitespace += letter
                return True
        elif(self.trailing_whitespace == ""):
            self.body += letter
            return True
        return False
    def _whiteSpaceLetter(self,letter):
        return (len(letter) == 1 and ord(letter) <= 32)
    def ansi_format(self):
        code_list = []
        if(self.style != style.default):
            code_list.append(str(self.style.value))
        if(self.text_color != color.default):
            code_list.append("3" + str(self.text_color.value))
        if(self.background_color != color.default):
            code_list.append("4" + str(self.background_color.value))
        if(len(code_list) == 0):
            return self.leading_whitespace + self.body + self.trailing_whitespace
        return self.leading_whitespace + "\u001b[" + ";".join(code_list) + "m" + self.body + "\u001b[0;0m" + self.trailing_whitespace

def getTokens(text_body):
    if(len(text_body) == 0):
        return []
    token_list = []
    current_token = Token()
    for letter in text_body:
        if(not current_token._add_letter(letter)):
            token_list.append(current_token)
            current_token = Token()
            current_token._add_letter(letter)
    token_list.append(current_token)
    return token_list

def ansi_joinTokens(token_list):
    text_body = ""
    for x in token_list:
        text_body += x.ansi_format()
    return text_body

def printTokens(token_list):
    for x in token_list:
        print("|",x.ansi_format(),"|",sep="")