# Operator precedence
precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'uminus': 3}
temp_counter = 1
three_ac = []

# Helper function to generate temporary variables
def get_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

# Tokenize input expression
def tokenize(expr):
    tokens = []
    i = 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
            continue
        if expr[i] in '+-*/=()':
            if expr[i] == '-' and (i == 0 or expr[i-1] in '+-*/=('):
                tokens.append('uminus')  # Negative sign as unary minus
            else:
                tokens.append(expr[i])
            i += 1
        elif expr[i].isalnum():
            var = ''
            while i < len(expr) and expr[i].isalnum():
                var += expr[i]
                i += 1
            tokens.append(var)
        else:
            i += 1
    return tokens

# Convert infix expression to postfix
def infix_to_postfix(tokens):
    output = []
    stack = []
    for token in tokens:
        if token not in precedence and token not in ('(', ')'):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence[stack[-1]]:
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

# Generate Three Address Code (3AC) from postfix expression
def generate_3ac_from_postfix(postfix):
    stack = []
    for token in postfix:
        if token == 'uminus':
            op = stack.pop()
            temp = get_temp()
            three_ac.append((temp, 'minus', op, ''))
            stack.append(temp)
        elif token in precedence:
            op2 = stack.pop()
            op1 = stack.pop()
            temp = get_temp()
            three_ac.append((temp, op1, token, op2))
            stack.append(temp)
        else:
            stack.append(token)
    return stack.pop()

# Main function to process the expression
def main():
    global temp_counter, three_ac
    expr = input("Enter a statement (e.g. x = (a + b) * (c - d)): ").strip()

    temp_counter = 1
    three_ac = []

    if '=' in expr:
        lhs, rhs = expr.split('=')
        lhs = lhs.strip()
        rhs = rhs.strip()
        tokens = tokenize(rhs)
        postfix = infix_to_postfix(tokens)
        result = generate_3ac_from_postfix(postfix)
        three_ac.append((lhs, result, '=', ''))
    else:
        tokens = tokenize(expr)
        postfix = infix_to_postfix(tokens)
        generate_3ac_from_postfix(postfix)

    print("\n--- Three Address Code ---")
    for instr in three_ac:
        if instr[1] == 'minus':
            print(f"{instr[0]} = minus {instr[2]}")
        elif instr[2] == '=':
            print(f"{instr[0]} = {instr[1]}")
        else:
            print(f"{instr[0]} = {instr[1]} {instr[2]} {instr[3]}")

if __name__ == "__main__":
    main()
