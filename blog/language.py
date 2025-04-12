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
            elif operator == "/":
                try:
                    result /= number
                except ZeroDivisionError:
                    return {"status": "error", "message": f"ZeroDivisionError: division by {number}"}
        elif token in ("+", "*", "-", "/"):
            operator = stream.read(1)
        else:
            return {"status": "error", "message": f"Unknown token: '{token}' at position {stream.tell()}"}
    return {"status": "success", "message": str(result)}


def parse_number(stream):
    whole = parse_int(stream)
    if peek(stream) == ".":
        stream.read(1)
        decimals = parse_decimals(stream)
        return whole + decimals
    else:
        return whole


def parse_int(stream):
    number = 0
    while peek(stream).isdigit():
        token = stream.read(1)
        number *= 10
        number += int(token)
    return number

def parse_decimals(stream):
    number = 0.0
    factor = 0.1
    while peek(stream).isdigit():
        token = stream.read(1)
        number += int(token) * factor
        factor *= 0.1
    return number


def peek(stream):
    """look ahead by 1 token"""
    cur = stream.tell()
    token = stream.read(1)
    stream.seek(cur)
    return token
