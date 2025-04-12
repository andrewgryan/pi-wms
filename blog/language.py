import io


def interpret(code: str) -> str:
    stream = io.StringIO(code)
    return parse_expression(stream)


def parse_expression(stream):
    result = 0
    operator = "+"
    while True:
        token = peek(stream)
        if token == '':
            break
        elif token == '(':
            stream.read(1)
            expr = parse_expression(stream)
            if expr["status"] == "error":
                return expr
            elif peek(stream) != ")":
                return {"status": "error", "message": f"SyntaxError: expected ')' found '{peek(stream)}'"}
            else:
                stream.read(1)
                number = expr["value"]
                try:
                    result = apply_operator(result, number, operator)
                except ZeroDivisionError:
                    return {"status": "error", "message": f"ZeroDivisionError: division by {number}"}
        elif token == ')':
            break
        elif token in ' \n':
            stream.read(1)
            continue
        elif token.isdigit():
            number = parse_number(stream)
            try:
                result = apply_operator(result, number, operator)
            except ZeroDivisionError:
                return {"status": "error", "message": f"ZeroDivisionError: division by {number}"}
        elif token in "+*-/":
            operator = stream.read(1)
        else:
            return {"status": "error", "message": f"Unknown token: '{token}' at position {stream.tell()}"}
    return {"status": "success", "message": str(result), "value": result}


def apply_operator(lhs, rhs, operator):
    if operator == "+":
        return lhs + rhs
    elif operator == "-":
        return lhs - rhs
    elif operator == "*":
        return lhs * rhs
    elif operator == "/":
        return lhs / rhs


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
