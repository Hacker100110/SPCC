precedence = {'+': 1, '-': 1, '*': 2, '/': 2, 'uminus': 3}
temp_counter = 1
three_ac = []

def get_temp():
    global temp_counter
    temp = f"t{temp_counter}"
    temp_counter += 1
    return temp

def tokenize(expr):
    tokens, i = [], 0
    while i < len(expr):
        if expr[i].isspace():
            i += 1
        elif expr[i] in '+-*/=()':
            if expr[i] == '-' and (i == 0 or expr[i - 1] in '+-*/=( '):
                tokens.append('uminus')
            else:
                tokens.append(expr[i])
            i += 1
        else:
            start = i
            while i < len(expr) and expr[i].isalnum():
                i += 1
            tokens.append(expr[start:i])
    return tokens

def infix_to_postfix(tokens):
    out, stack = [], []
    for t in tokens:
        if t not in precedence and t not in ('(', ')'):
            out.append(t)
        elif t == '(':
            stack.append(t)
        elif t == ')':
            while stack[-1] != '(':
                out.append(stack.pop())
            stack.pop()
        else:
            while stack and stack[-1] != '(' and precedence[t] <= precedence[stack[-1]]:
                out.append(stack.pop())
            stack.append(t)
    return out + stack[::-1]

def generate_3ac(postfix):
    stack = []
    for token in postfix:
        if token == 'uminus':
            op = stack.pop()
            temp = get_temp()
            three_ac.append((temp, 'minus', op, ''))
            stack.append(temp)
        elif token in precedence:
            op2, op1 = stack.pop(), stack.pop()
            temp = get_temp()
            three_ac.append((temp, op1, token, op2))
            stack.append(temp)
        else:
            stack.append(token)
    return stack.pop()

def generate_quadruples():
    quads = []
    for t in three_ac:
        if t[1] == 'minus':
            quads.append(('minus', t[2], '', t[0]))
        elif t[2] == '=':
            quads.append(('=', t[1], '', t[0]))
        else:
            quads.append((t[2], t[1], t[3], t[0]))
    return quads

def main():
    global temp_counter, three_ac
    expr = input("Enter a statement (e.g. a = b * -c + b * -c): ").strip()
    temp_counter, three_ac = 1, []

    if '=' in expr:
        lhs, rhs = map(str.strip, expr.split('='))
        postfix = infix_to_postfix(tokenize(rhs))
        result = generate_3ac(postfix)
        three_ac.append((lhs, result, '=', ''))
    else:
        postfix = infix_to_postfix(tokenize(expr))
        generate_3ac(postfix)

    print("\n--- Three Address Code ---")
    for t in three_ac:
        if t[1] == 'minus':
            print(f"{t[0]} = minus {t[2]}")
        elif t[2] == '=':
            print(f"{t[0]} = {t[1]}")
        else:
            print(f"{t[0]} = {t[1]} {t[2]} {t[3]}")

    print("\n--- Quadruples ---")
    for i, q in enumerate(generate_quadruples()):
        print(f"{i}: ({q[0]:^7}, {q[1]:^5}, {q[2]:^5}, {q[3]:^5})")

if __name__ == "__main__":
    main()
