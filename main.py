from fastapi import FastAPI, Cookie, Response, HTTPException
from pydantic import BaseModel
from MA4_vol import statement, CalculatorSyntaxError, EvaluationError
from tokenize import TokenError
# from MA4_vol import statement, assignment, expression, term, factor, factor, fac, fib
from MA4tokenizer_vol import TokenizeWrapper
import uuid #Makes random ids
import math

app = FastAPI()

sessions = {}

class StatementRequest(BaseModel):
    data: str
    # vars: dict[str, float] = {"ans": 0.0, "PI": math.pi, "E": math.e}

#Response is used to reach the header of the reply from the server. Return usually just gives back the body of the reply and Response allows us to acess the header. 
    


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Numerical Calculator"}

# @app.post("/multiply/{number}")
# def multiply_numb(number: int):
#     return {"result": 3*number}

def get_variables(session_id, response):
    if session_id is None or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"ans": 0.0, "PI": math.pi, "E": math.e}
        response.set_cookie(key="session_id", value=session_id)
    return sessions[session_id]


@app.post("/statement")
def post_statements(req: StatementRequest, response: Response, session_id: str | None = Cookie(default=None)):
    variables = get_variables(session_id, response)
    try:
        wtok = TokenizeWrapper(req.data)
        result = statement(wtok, variables)
    except CalculatorSyntaxError as se:
        raise HTTPException(status_code=400, detail=(
            f"Syntax error: {se}. Error occurred at '{wtok.get_current()}' "
            f"just after '{wtok.get_previous()}'"))
    except EvaluationError as ee:
        raise HTTPException(status_code=400, detail=(
            f"Evaluation error: {ee}. Error occurred at '{wtok.get_current()}' "
            f"just after '{wtok.get_previous()}'"))
    except TokenError:
        raise HTTPException(status_code=400,
                            detail="Syntax error: Unbalanced parentheses")
    # wtok = TokenizeWrapper(req.data)
    # # variables.update(req.vars)
    # result = statement(wtok, variables)
    return {"value": result}
    # return {"value": result, "vars": variables}


@app.get("/vars")
def get_vars(response: Response, session_id: str | None = Cookie(default=None)):
    return get_variables(session_id, response)


# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: str | None = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}





# def main():
#     """
#     Handles:
#        the iteration over input lines,
#        commands like 'quit' and 'vars' and
#        raised exceptions.
#     Starts with reading the init file
#     """

#     print("Numerical calculator")
#     variables = {"ans": 0.0, "PI": math.pi, "E": math.e}

#     # Note: The unit test file initiate variables in this way. If your implementation
#     # requires another initiation you have to update the test file accordingly.
#     init_file = 'MA4init.txt'
#     lines_from_file = ''
#     try:
#         with open(init_file, 'r') as file:
#             lines_from_file = file.readlines()
#     except FileNotFoundError:
#         pass

#     while True:
#         if lines_from_file:
#             line = lines_from_file.pop(0).strip()
#             print('init  :', line)
#         else:
#             line = input('\nInput : ')
#         if line == '' or line[0] == '#':
#             continue
#         wtok = TokenizeWrapper(line)

#         if wtok.get_current() == 'quit':
#             print('Bye!')
#             exit()

#         if wtok.get_current() == 'vars':
#             w = 8
#             for key, value in variables.items():
#                 print(f"{key: <{w}} : {value}")

#         else:
#             try:
#                 result = statement(wtok, variables)
#                 print('Result:', result)

#             except CalculatorSyntaxError as se:
#                 print("*** Syntax error: ", se)
#                 print(
#                     f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

#             except EvaluationError as ee:
#                 print("*** Evaluation error: ", ee)
#                 print(
#                     f"Error occurred at '{wtok.get_current()}' just after '{wtok.get_previous()}'")

#             except TokenError as te:
#                 print('*** Syntax error: Unbalanced parentheses')