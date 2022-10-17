class ExpEvaluator:
    OPERATORS = {'+': (1, lambda x, y: x + y), '-': (1, lambda x, y: x - y),
                 '*': (2, lambda x, y: x * y), '/': (2, lambda x, y: x / y)}

    def parse(self, formula_string):
        number = ''
        for s in formula_string:
            if s in '1234567890.':
                number += s
            elif number:
                yield float(number)
                number = ''
            if s in self.OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(self, parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in self.OPERATORS:
                while stack and stack[-1] != "(" and self.OPERATORS[token][0] <= self.OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(self, polish):
        stack = []
        for token in polish:
            if token in self.OPERATORS:
                if len(stack) == 0:
                    raise Exception("No numbers found")
                elif len(stack) == 1:
                    if token == "-":
                        stack.append(-stack.pop())
                    elif token == "+":
                        stack.append(stack.pop())
                    else:
                        raise Exception("Only unary +/- are supported")
                else:
                    y, x = stack.pop(), stack.pop()
                    if token == '/' and y == 0:
                        raise TypeError('Division by zero')
                    stack.append(self.OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    def eval_(self, formula):
        return self.calc(self.shunting_yard(self.parse(formula)))


expression = input('> ')
evaluator = ExpEvaluator()
print(evaluator.eval_(expression))
