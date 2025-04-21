def parse_3ac(statement):
    # Supports format: result = arg1 op arg2
    parts = statement.split('=')
    result = parts[0].strip()
    expr = parts[1].strip()

    tokens = expr.split()
    if len(tokens) == 3:
        arg1, op, arg2 = tokens
    else:
        # Fallback if expression is not in expected format
        arg1 = tokens[0]
        op = '='
        arg2 = ''
    
    return {
        'op': op,
        'arg1': arg1,
        'arg2': arg2,
        'result': result
    }

def main():
    n = int(input("Enter number of 3AC statements: "))
    statements = []
    
    for i in range(n):
        stmt = input(f"Enter 3AC statement #{i+1} (e.g., t1 = a + b): ")
        statements.append(parse_3ac(stmt))

    print("\n--- Quadruples ---")
    print(f"{'Op':<7}{'Arg1':<10}{'Arg2':<10}{'Result':<10}")
    for q in statements:
        print(f"{q['op']:<7}{q['arg1']:<10}{q['arg2']:<10}{q['result']:<10}")

if __name__ == "__main__":
    main()
