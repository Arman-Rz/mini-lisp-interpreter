import math

from .node import Node, binary_ops, unary_ops


class Evaluator:
    def __init__(self, varTable):
        self._varTable = varTable

    def _run(self, startNode):
        nodeType = startNode._type
        node = startNode._node
        match nodeType:
            case "SET":
                name = self._checkVarName(node._varName)
                if isinstance(node._varValue, Node):
                    value = self._run(node._varValue)
                else:
                    value = self._checkValue(node._varValue)
                if value is None:
                    raise EvaluationError(
                        f"Invalid numeric value {node._varValue} in (SET {name} {node._varValue})"
                    )
                self._varTable.SetVar(name, value)
                return value

            case op if op in binary_ops:

                first = self._resolve(node._inputs[0], node._inputs[1], True, op)
                second = self._resolve(node._inputs[1], node._inputs[0], False, op)

                match op:
                    case "ADD":
                        res = first + second
                    case "MUL":
                        res = first * second
                    case "SUB":
                        res = first - second
                    case "DIV":
                        if second == 0.0:
                            raise EvaluationError(
                                f"Division by zero in (DIV {self._format_value(first)} {self._format_value(second)})"
                            )
                        res = first / second
                    case "LOG":
                        if first == 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Zero value for (LOG {self._format_value(first)} {self._format_value(second)})"
                            )
                        if first < 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Negative value for (LOG {self._format_value(first)} {self._format_value(second)})"
                            )
                        if second < 0:
                            raise EvaluationError(
                                f"LOG base must be a positive value. Negative base value for (LOG {self._format_value(first)} {self._format_value(second)})"
                            )
                        if second == 0:
                            raise EvaluationError(
                                f"LOG base must be a positive value. Zero base value for (LOG {self._format_value(first)} {self._format_value(second)})"
                            )
                        if second == 1:
                            raise EvaluationError(
                                f"LOG base cannot be 1. (LOG {self._format_value(first)} {self._format_value(second)})"
                            )
                        res = math.log(first, second)

            case op if op in unary_ops:
                if isinstance(node._input, Node):
                    value = self._run(node._input)
                else:
                    value = self._checkValue(node._input)
                if value is None:
                    raise EvaluationError(
                        f"Invalid numeric value {node._input} in ({op} {node._input})"
                    )

                match op:
                    case "SQRT":
                        if value < 0.0:
                            raise EvaluationError(
                                f"Negative value for (SQRT {self._format_value(value)})"
                            )
                        res = math.sqrt(value)
                    case "NEG":
                        res = (-1) * value
                    case "ABS":
                        res = abs(value)
                    case "FACT":
                        if value < 0.0:
                            raise EvaluationError(
                                f"Negative value for (FACT {self._format_value(value)})"
                            )
                        if isinstance(value, float) and not value.is_integer():
                            raise EvaluationError(
                                f"FACT requires an integer value: {self._format_value(value)}"
                            )
                        res = math.factorial(int(value))
                    case "EXP":
                        res = math.exp(value)
                    case "LOG2":
                        if value == 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Zero value for (LOG2 {self._format_value(value)})"
                            )
                        if value < 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Negative value for (LOG2 {self._format_value(value)})"
                            )
                        res = math.log2(value)
                    case "LOG10":
                        if value == 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Zero value for (LOG10 {self._format_value(value)})"
                            )
                        if value < 0.0:
                            raise EvaluationError(
                                f"LOG is not defined for non-positive values. Negative value for (LOG10 {self._format_value(value)})"
                            )
                        res = math.log10(value)

        return res

    def _checkVarName(self, varName):
        if (
            varName.isalnum()
            and varName[0].isalpha()
            and varName not in binary_ops
            and varName not in unary_ops
            and varName != "SET"
        ):
            return varName
        raise TypeError(f"The name {varName} is not an acceptable name for a variable.")

    def _checkValue(self, value):
        try:
            res = float(value)
            return res
        except:
            return None

    def _resolve(self, x, y, first, op_repr):
        value = self._checkValue(x)

        if value is not None:
            return value

        if isinstance(x, str):
            if self._varTable.VarExists(x):
                return self._varTable.GetVar(x)
            if first:
                raise EvaluationError(f"Undefined variable {x} in ({op_repr} {x} {y})")
            else:
                raise EvaluationError(f"Undefined variable {x} in ({op_repr} {y} {x})")

        return self._run(x)

    def _format_value(self, value):
        if isinstance(value, float) and value.is_integer():
            return str(int(value))
        return str(value)


class EvaluationError(Exception):
    pass
