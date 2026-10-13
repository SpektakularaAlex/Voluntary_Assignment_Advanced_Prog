from fastapi import FastAPI
from pydantic import BaseModel
from MA4_vol import fac, fib, statement, assignment, expression, term, factor, factor
from MA4tokenizer_vol import TokenizeWrapper

app = FastAPI()

class StatementRequest(BaseModel):
    data: str
    vars: dict[str, float] = {}


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None


@app.get("/")
def read_root():
    return {"Numerical Calculator"}

@app.post("/multiply/{number}")
def multiply_numb(number: int):
    return {"result": 3*number}


# @app.post("/statement/{data, variables}")
# def state(data: str, variables: str):
#     return {statement(data, variables)}



@app.post("/statement")
def state(req: StatementRequest):
    wtok = TokenizeWrapper(req.data)
    return {statement(wtok, req.vars)}
    # return {"data": req.data, "vars": req.vars}



@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}





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