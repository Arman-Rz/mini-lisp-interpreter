from src.vartable import VarTable

from src.node import Node, binary_ops, unary_ops
from src.evaluator import Evaluator


class Program:
    def __init__(self):
        self._varTable = VarTable()
        self._front = None
        self._end = None
        self._numChildren = 0
        self._evaluator = Evaluator(self._varTable)

    def Execute(self, code: str):
        if self._check_lisp(code):
            tokens = self._tokenizer(code)
            tokens = self._divide(tokens)
            if len(tokens) > 1:
                raise ValueError(
                    "Execute() accepts only a single expression. "
                    "Use Add() for multi-line programs."
                )

            newNode = self._parser(tokens[0])
            res = self._evaluator._run(newNode)
            if newNode._type != "SET":
                if res is not None:
                    return self._format_value(res)

    def Run(self):
        if self._isEmpty():
            return "The Program is empty."

        results = []
        current = self._front
        while current != None:
            res = self._evaluator._run(current)
            if current._type != "SET":
                results.append(self._format_value(res))
            current = current._next
        return results

    def Add(self, code: str):
        if self._check_lisp(code):
            tokens = self._tokenizer(code)
            tokens = self._divide(tokens)
            for token in tokens:
                newNode = self._parser(token)

                if self._isEmpty():
                    self._front = newNode
                    self._end = newNode
                    self._numChildren += 1
                else:
                    if type == "SET" and not newNode._exist:
                        self._end._next = newNode
                        self._end = newNode
                        newNode._next = None
                        self._numChildren += 1
                    else:
                        self._end._next = newNode
                        self._end = newNode
                        newNode._next = None
                        self._numChildren += 1

    def Show(self, mode: str = None):
        if self._front is not None:
            print("(PROGRAM)")
            current = self._front
            if mode == None or mode == "lisp":
                while current is not None:
                    print("    ", end="")
                    current.showLisp()
                    print()
                    current = current._next
            elif mode == "tree":
                print("│")
                while True:
                    if current == self._end:
                        current.showTree(is_last=True)
                    else:
                        current.showTree(is_last=False)

                    current = current._next
                    if current == None:
                        break
                    print("│")
        else:
            print("The structure is empty.")

    def Variable(self, variable: str = None):
        if variable is None:
            return self._varTable.GetAll()
        else:
            value = self._varTable.GetVar(variable)
            if value is None:
                raise TypeError(f"Variable {variable} is not defined.")
            else:
                return self._format_value(value)

    def Clear(self, variables=False, verbose=False):
        self._front = None
        self._end = None
        self._numChildren = 0

        if variables:
            self._varTable = VarTable()
            self._evaluator = Evaluator(self._varTable)

        if verbose:
            print("Program cleared.")

    # ---------------------------------------------------------#
    # -------------------- Private Methods --------------------#
    # ---------------------------------------------------------#

    def _parser(self, token):
        iterator = iter(range(1, len(token)))
        for i in iterator:
            args = self._getArgs(token)
            match token[i]:
                case "SET":
                    if len(args) != 2:
                        raise SyntaxError(f"SET expects 2 arguments, got {len(args)}")

                    if len(args[0]) != 1 or args[0][0] == "(":
                        raise SyntaxError(
                            "SET: First argument must be a variable name."
                        )

                    varName = args[0][0]
                    varValue = (
                        args[1][0] if len(args[1]) == 1 else self._parser(args[1])
                    )

                    return Node(type="SET", params=[varName, varValue])

                case op if op in binary_ops:
                    if len(args) != 2:
                        raise SyntaxError(f"{op} expects 2 arguments, got {len(args)}")

                    first = args[0][0] if len(args[0]) == 1 else self._parser(args[0])
                    second = args[1][0] if len(args[1]) == 1 else self._parser(args[1])

                    return Node(type=op, params=[first, second])

                case op if op in unary_ops:
                    if len(args) != 1:
                        raise SyntaxError(f"{op} expects 1 arguments, got {len(args)}")

                    val = args[0][0] if len(args[0]) == 1 else self._parser(args[0])

                    return Node(type=op, params=val)

    def _findEnd(self, token):
        curr = -1
        for index in range(len(token)):
            if token[index] == ")":
                if curr == 0:
                    return token[: index + 1]
                curr -= 1
            elif token[index] == "(":
                curr += 1

    def _divide(self, tokens):
        nodes = []
        j = 0
        Counts = 0

        for i in range(len(tokens)):
            if tokens[i] == "(":
                Counts += 1
            if tokens[i] == ")":
                Counts -= 1
            if Counts == 0:
                nodes.append(tokens[j : i + 1])
                j = i + 1
        return nodes

    def _check_lisp(self, lisp):
        if len(lisp) < 3:
            raise ValueError(
                "Lisp must have at least one characters surrounded by a '(' and ')'."
            )

        if not (lisp.startswith("(") or lisp.startswith("\n(")) and not (
            lisp.endswith(")") or lisp.endswith(")\n")
        ):
            raise ValueError("Lisp must start with '(' and end with ')'.")

        if lisp.count("(") != lisp.count(")"):
            raise ValueError("Parentheses are unbalance.")

        for i in range(len(lisp) - 1):
            if lisp[i] == "(" and lisp[i + 1] == "(":
                raise ValueError("Lisp string cannot have two '(' next to each other.")
            if lisp[i] == "(" and lisp[i + 1] == ")":
                raise ValueError("Lisp string cannot have empty '()' with no child.")

        return True

    def _getArgs(self, tokens: list):
        depth = 0
        currArgs = []
        resArgs = []
        i = 2
        while i < len(tokens) - 1:
            if tokens[i] == "(":
                depth += 1

            elif tokens[i] == ")":
                depth -= 1

            currArgs.append(tokens[i])

            if depth == 0:
                resArgs.append(currArgs)
                currArgs = []
            i += 1

        return resArgs

    def _isEmpty(self):
        return self._front == None

    def _tokenizer(self, code):
        code = code.replace("(", " ( ").replace(")", " ) ")
        return code.split()

    def _format_value(self, value):
        if isinstance(value, float) and value.is_integer():
            return int(value)
        return value
