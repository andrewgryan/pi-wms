import io


def interpret(code: str) -> str:
    stream = io.StringIO(code)
    return parse_expression(stream)


def parse_expression(stream):
    stack = []
    while peek(stream) != '':
        token = peek(stream)
        if token in " \n":
            token = stream.read(1)
            continue
        elif token.isdigit() or token == "(":
            atom = parse_atom(stream)
            if is_error(atom):
                return atom
            stack.append(unwrap(atom))
        elif token == ")":
            break
        elif token in "+*-/":
            operator =parse_operator(stream)
            if is_error(operator):
                return operator
            stack.append(unwrap(operator))
        else:
            return error(f"Unknown token: '{token}' at position {stream.tell()}")

        # Evaluate top of stack
        if len(stack) > 2:
            rhs = stack.pop()
            op = stack.pop()
            lhs = stack.pop()
            try:
                stack.append(apply_operator(lhs, rhs, op))
            except ZeroDivisionError:
                return error(f"ZeroDivisionError: division by {rhs}")
            except TypeError:
                return error(f"SyntaxError: expected digit found '{rhs}'")

    return success(stack.pop())


def is_error(result):
    return result["status"] == "error"


def error(message: str):
    return {"status": "error", "message": message}


def success(value):
    return {"status": "success", "message": str(value), "value": value}


def unwrap(result):
    return result["value"]


def parse_atom(stream):
    token = peek(stream)
    if token.isdigit():
        return success(parse_number(stream))
    elif token == "(":
        stream.read(1)  # (
        expr = parse_expression(stream)
        if expr["status"] == "error":
            return expr
        elif peek(stream) != ")":
            return error(f"SyntaxError: expected ')' found '{peek(stream)}'")
        stream.read(1)  # )
        return expr
    else:
        return error(f"Unexpected token: '{token}'")


def parse_operator(stream):
    token = peek(stream)
    symbols = "+*-/"
    if token in symbols:
        operator = stream.read(1)
        return success(operator)
    else:
        return error(f"SyntaxError: expected one of '{symbols}' found '{token}'")


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
