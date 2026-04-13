binary_ops = ["ADD", "SUB", "MUL", "DIV", "LOG"]
unary_ops = ["SQRT", "NEG", "ABS", "FACT", "EXP", "LOG2", "LOG10"]

class VarNode():
    def __init__(self, varName, varValue:any):
        self._varName = varName
        self._varValue = varValue

    def setValue(self, value):
        self._varValue = value

class BinaryOpNode():
    def __init__(self, typeOf, inputs):
        self._typeOf = typeOf
        self._inputs = inputs

class UnaryOpNode():
    def __init__(self, typeOf, input):
        self._typeOf = typeOf
        self._input = input

class Node():
    def __init__(self, type:str, params, next=None):
        self._type = type
        self.node = None
        self._exist = False
        if type == "SET":
            self._node = VarNode(params[0], params[1])

        elif type in binary_ops:
            self._node = BinaryOpNode(type, params)
        
        elif type in unary_ops:
            self._node = UnaryOpNode(type, params)

        self._next = next

    def showLisp(self):
        match self._type:
            case "SET":
                varName = self._node._varName
                varValue = self._node._varValue
                print(f"(SET {varName} ", end='')
                if isinstance(varValue, str):
                    print(f"{varValue})", end='')
                else:
                    varValue.showLisp()
                    print(")", end='')
            case op if op in binary_ops:
                first = self._node._inputs[0]
                second = self._node._inputs[1]
                print(f"({self._type} ", end='')
                if isinstance(first, str):
                    print(f"{first}", end='')
                else:
                    first.showLisp()
                
                print(" ", end='')
                
                if isinstance(second, str):
                    print(f"{second})", end='')
                else:
                    second.showLisp()
                    print(")", end='')
            case op if op in unary_ops:
                value = self._node._input
                print(f"({self._type} ", end='')
                if isinstance(value, str):
                    print(f"{value})", end='')
                else:
                    value.showLisp()
                    print(")", end='')
    
    
    def showTree(self, prefix="", is_last=False):
        # Print current node
        connector = "└── " if is_last else "├── "

        if self._type == "SET":
            label = f"SET {self._node._varName}"
        else:
            label = self._type

        print(prefix + connector + label)

        # Prepare children
        children = []

        if self._type == "SET":
            val = self._node._varValue
            if isinstance(val, str):
                children.append(val)
            else:
                children.append(val)

        elif self._type in binary_ops:
            children.extend(self._node._inputs)

        elif self._type in unary_ops:
            children.append(self._node._input)

        # New prefix for children
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Print children
        for i, child in enumerate(children):
            last_child = (i == len(children) - 1)

            if isinstance(child, str):
                connector = "└── " if last_child else "├── "
                print(new_prefix + connector + child)
            else:
                child.showTree(new_prefix, last_child)