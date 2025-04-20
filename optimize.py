import os

def is_constant(expr):
    try:
        eval(expr)
        return True
    except:
        return False

def evaluate(expr):
    try:
        return str(eval(expr))
    except:
        return expr

def optimize_code(lines):
    optimized, constants, copies, expressions = [], {}, {}, {}

    for line in lines:
        if "=" not in line:
            optimized.append(line)
            continue

        lhs, rhs = map(str.strip, line.split("="))

        # 1. Constant folding
        if is_constant(rhs):
            constants[lhs] = evaluate(rhs)
            optimized.append(f"{lhs} = {constants[lhs]}")
            continue

        # 2. Copy propagation
        rhs = copies.get(rhs, rhs)

        # 3. Replace variables in rhs using copies
        new_rhs = ''.join(copies.get(token, token) if token.isidentifier() else token for token in rhs.split())

        # 4. Common Subexpression Elimination (CSE)
        for expr, var in expressions.items():
            new_rhs = new_rhs.replace(expr, var)

        optimized.append(f"{lhs} = {new_rhs}")
        copies[lhs] = lhs
        expressions[new_rhs] = lhs

    return optimized

def main():
    print("Working directory:", os.getcwd())

    try:
        with open("C:/Users/deep/OneDrive/Desktop/deep/exp9/input.txt", "r") as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("Error: 'input.txt' not found.")
        return

    print("\n--- Input Code (Before Optimization) ---")
    print('\n'.join(lines))

    optimized = optimize_code(lines)

    print("\n--- Output Code (After Optimization) ---")
    print('\n'.join(optimized))

if __name__ == "__main__":
    main()
