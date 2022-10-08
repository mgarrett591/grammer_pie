import sys
import tokens

def process_file(file_name):
    with open(file_name) as f:
        text_body = f.read()
        token_list = tokens.getTokens(text_body)
        print(text_body)

for x in sys.argv[1:]:
    process_file(x)