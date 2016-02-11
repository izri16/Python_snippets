def is_well_enclosed_single(expression):
    stack = []
    brackets = {
        '(': 'start',
        ')': 'end'
    }

    for item in expression:
        if (item in brackets):
            if (brackets[item] == 'start'):
                stack.append("1")
            else:
                if (len(stack)):
                    stack.pop()
                else:
                    return False
    if (len(stack)):
        return False
    return True


def is_well_enclosed_multiple(expression):
    stack = []
    starting_brackets = ['(', '{', '[']
    closing_brackets = [')', '}', ']']

    for item in expression:
        if (item in starting_brackets):
            stack.append(starting_brackets.index(item))
        elif (item in closing_brackets):
            if (len(stack)):
                last = stack.pop()
                if (last != closing_brackets.index(item)):
                    return False
            else:
                return False

    if (len(stack)):
        return False
    return True


expression_1 = '(a + (b * c) - (a + (c * 9)))'
expression_2 = '(a + {b * c} - [a + (c * 9)])'

print(is_well_enclosed_single(expression_1))
print(is_well_enclosed_multiple(expression_2))
