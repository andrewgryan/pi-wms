import io


def interpret(code: str) -> str:
    result = 0
    stream = io.StringIO(code)
    operator = "+"
    while True:
        token = peek(stream)
        if token == '':
            break
        elif token == ' ':
            stream.read(1)
            continue
        elif token.isdigit():
            number = parse_number(stream)
            if operator == "+":
                result += number
            elif operator == "-":
                result -= number
            elif operator == "*":
                result *= number
        elif token in ("+", "*", "-"):
            operator = stream.read(1)
        else:
            raise Exception(f"Unknown token: {token}")
    return str(result)


def parse_number(stream):
    number = 0
    while peek(stream).isdigit():
        token = stream.read(1)
        number *= 10
        number += int(token)
    return number


def peek(stream):
    """look ahead by 1 token"""
    cur = stream.tell()
    token = stream.read(1)
    stream.seek(cur)
    return token
