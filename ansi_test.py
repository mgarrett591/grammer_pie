import tokens

tb = tb = "  1 2 3 4 5 6 7  12"
tt = tokens.getTokens(tb)
tt[1].text_color = tokens.color.red
tt[2].text_color = tokens.color.red
tt[6].text_color = tokens.color.red
print("|",tb,"|")
tokens.printTokens(tt)