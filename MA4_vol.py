"""
Solutions to module 4 - A calculator
Student: Alexander Cremer
Mail: alexander.cremer.1041@student.uu.se
"""

# For exercise 10 I implemented the absolute value | |
"""
The program is only working for a very tiny set of operations.
You have to add and/or modify code in ALL functions as well as add some new functions.
Use the syntax charts when you write the functions!
However, the class CalculatorSyntaxError is complete as well as handling in main
of CalculatorSyntaxError and TokenError.
"""




from MA4tokenizer_vol import TokenizeWrapper
import math
from tokenize import TokenError
class CalculatorSyntaxError(Exception):
    pass


class EvaluationError(Exception):
    pass


def fac(n):
    if n < 0 or not float(n).is_integer():
        raise EvaluationError(f"Fac needs positive integers as arg")
    n = int(n)
    if n == 1 or n == 0:
        return 1
    return n*fac(n-1)


def fib(n):  # Looping
    if n < 0 or not float(n).is_integer():
        raise EvaluationError(f"Fib needs positive integer as arg")
    n = int(n)
    if n == 0:
        return 0
    if n == 1:
        return 1

    fib_prev_prev = 0
    fib_prev = 1
    fib_curr = 0
    for i in range(n-1):
        fib_curr = fib_prev + fib_prev_prev
        fib_prev_prev = fib_prev
        fib_prev = fib_curr
    return fib_curr


functions_1 = {"exp": math.exp, "sin": math.sin,
               "cos": math.cos, "log": math.log, "fib": fib, "fac": fac}


def statement(wtok, variables):
    """ See syntax chart for statement"""
    result = assignment(wtok, variables)
    # print(f"wtok.is_at_end()={wtok.is_at_end()}")
    if wtok.is_at_end() == False:
        raise CalculatorSyntaxError(
            f"Probably a syntax error such as '**' or '//' ")

    variables["ans"] = result
    return result


def assignment(wtok, variables):
    """ See syntax chart for assignment"""
    result = expression(wtok, variables)

    while wtok.get_current() == '=':
        wtok.next()
        if wtok.is_name() is False:
            raise CalculatorSyntaxError(f"String name is expected, not number")

        # elif wtok.get_current() in variables:
        #     raise CalculatorSyntaxError(f"The variable already exists")

        variables[str(wtok.get_current())] = result
        wtok.next()

    # wtok.next()

    return result


def expression(wtok, variables):
    """ See syntax chart for expression"""
    result = term(wtok, variables)

    while wtok.get_current() == '+' or wtok.get_current() == '-':
        pm = wtok.get_current()
        wtok.next()
        if pm == '+':
            result = result + term(wtok, variables)
        else:
            result = result - term(wtok, variables)
    return result


def term(wtok, variables):
    """ See syntax chart for term"""
    result = factor(wtok, variables)

    while wtok.get_current() in ('*', '/'):
        md = wtok.get_current()
        wtok.next()
        if md == '*':
            if wtok.get_current() == '*' or wtok.get_current() == '/' or wtok.get_current() == '+':
                raise CalculatorSyntaxError(
                    f"You can't have {wtok.get_current()} after {wtok.get_previous()}")
            result = result * factor(wtok, variables)

        else:
            if wtok.get_current() == '*' or wtok.get_current() == '/' or wtok.get_current() == '+':
                raise CalculatorSyntaxError(
                    f"You can't have {wtok.get_current()} after {wtok.get_previous()}")
            fact = factor(wtok, variables)

            if fact == 0:
                raise EvaluationError(f"Division by 0 is not allowed")

            else:
                result = result / fact

    return result


def factor(wtok, variables):
    """ See syntax chart for factor"""

    if wtok.get_current() == '(':
        wtok.next()
        result = assignment(wtok, variables)
        if wtok.get_current() != ')':
            raise CalculatorSyntaxError("Expected ')'")
        else:
            wtok.next()

    elif wtok.is_number():
        # result = int(wtok.get_current())
        result = float(wtok.get_current())
        wtok.next()

    elif wtok.get_current() == '-':
        wtok.next()
        result = - factor(wtok, variables)

    elif wtok.get_current() == '|':
        wtok.next()
        result = abs(assignment(wtok, variables))
        if wtok.get_current() != '|':
            raise CalculatorSyntaxError("Expected '|'")
        else:
            wtok.next()

    elif wtok.is_name():
        name = wtok.get_current()
        if name in variables:
            wtok.next()
            result = variables[name]
        elif name in functions_1:
            wtok.next()
            if wtok.get_current() != '(':
                raise CalculatorSyntaxError("Expected '(' after function name")
            wtok.next()
            arg = assignment(wtok, variables)

            if name == 'log' and float(arg) <= 0:
                raise EvaluationError(f"Log arg <= 0")

            # if (name == 'fac' and float(arg) < 0) or (name == 'fac' and (arg).is_integer() == False):
            #     raise EvaluationError(f"Fac needs positive integers as arg")

            # if (name == 'fib' and float(arg) < 0) or (name == 'fib' and (arg).is_integer() == False):
            #     raise EvaluationError(f"Fib needs positive integer as arg")

            if wtok.get_current() != ')':
                raise CalculatorSyntaxError("Expected ')' after argument")

            # if name in ('fac', 'fib'):
            #     arg = int(arg)

            wtok.next()

            result = functions_1[name](arg)

        else:
            raise EvaluationError(f"Undefined variable '{name}'")
            # raise CalculatorSyntaxError(f"Undefined variable '{name}'")

    else:
        raise CalculatorSyntaxError(
            "Expected number or '('")
    return result


def main():
    """
    Handles:
       the iteration over input lines,
       commands like 'quit' and 'vars' and
       raised exceptions.
    Starts with reading the init file
    """

    print("Numerical calculator")
    variables = {"ans": 0.0, "PI": math.pi, "E": math.e}

    # Note: The unit test file initiate variables in this way. If your implementation
    # requires another initiation you have to update the test file accordingly.
    init_file = 'MA4init.txt'
    lines_from_file = ''
    try:
        with open(init_file, 'r') as file:
            lines_from_file = file.readlines()
    except FileNotFoundError:
        pass

    while True:
        if lines_from_file:
            line = lines_from_file.pop(0).strip()
            print('init  :', line)
        else:
            line = input('\nInput : ')
        if line == '' or line[0] == '#':
            continue
        wtok = TokenizeWrapper(line)

        if wtok.get_current() == 'quit':
            print('Bye!')
            exit()

        if wtok.get_current() == 'vars':
            w = 8
            for key, value in variables.items():
                print(f"{key: <{w}} : {value}")

        else:
            try:
                result = statement(wtok, variables)
                print('Result:', result)

            except CalculatorSyntaxError as se:
                print("*** Syntax error: ", se)
                print(
                    f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except EvaluationError as ee:
                print("*** Evaluation error: ", ee)
                print(
                    f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

            except TokenError as te:
                print('*** Syntax error: Unbalanced parentheses')


if __name__ == "__main__":
    main()
