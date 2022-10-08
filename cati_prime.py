import sys
import tokens

prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 21, 40, 73, 79, 83, 89, 97]

def under_line_prime(token):
    return
    
def blue_even(token):
    return
    
def validions(token):
    try:
        num = int(token.body)
        if(num in prime_list):
            token.style = tokens.style.underline
        if(num % 2 == 0):
            token.text_color = tokens.color.blue
        else:
            token.text_color = tokens.color.green
    except:
        pass

def process_file(file_name):
    with open(file_name) as f:
        text_body = f.read()
        token_list = tokens.getTokens(text_body)
        for token in token_list:
            validions(token)
        print(tokens.ansi_joinTokens(token_list))

for x in sys.argv[1:]:
    process_file(x)