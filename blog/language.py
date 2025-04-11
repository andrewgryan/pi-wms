import io


def interpret(code: str) -> str:
    result = 0
    stream = io.StringIO(code)
    operator = "+"
    while True:
        token = stream.read(1)
        if token == '':
            break
        elif token == ' ':
            continue
        elif token.isdigit():
            number = 0
            while token.isdigit():
                number *= 10
                number += int(token)
                token = stream.read(1)
            if operator == "+":
                result += number
            elif operator == "*":
                result *= number
        elif token == "+":
            operator = "+"
        elif token == "*":
            operator = "*"
    return str(result)
