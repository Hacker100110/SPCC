def generate_precedence_table():
    t = ['+', '*', 'id', '$']
    rels = {
        ('+', '+'): '>', ('+', '*'): '<', ('+', 'id'): '<', ('+', '$'): '>',
        ('*', '+'): '>', ('*', '*'): '>', ('*', 'id'): '<', ('*', '$'): '>',
        ('id', '+'): '>', ('id', '*'): '>', ('id', 'id'): '-', ('id', '$'): '>',
        ('$', '+'): '<', ('$', '*'): '<', ('$', 'id'): '<', ('$', '$'): 'acc'
    }
    return {r: {c: rels.get((r, c), '-') for c in t} for r in t}

def print_table(table):
    t = list(table.keys())
    print("\nPrecedence Table:")
    print("    | " + " | ".join(f"{x:<4}" for x in t) + " |")
    print("-" * (7 * len(t) + 5))
    for r in t:
        print(f"{r:<3} | " + " | ".join(f"{table[r][c]:<4}" for c in t) + " |")

def find_rightmost_terminal(stack):
    return next((s for s in reversed(stack) if s in ['+', '*', 'id', '$']), '$')

def parse_input(expr, table):
    print("\nParsing Table:")
    stack, expr = ['$',], expr + '$'
    print(f"{'Stack':<30}| {'Input':<20}| Action")
    print("-" * 70)

    tokens, i = [], 0
    while i < len(expr):
        if expr[i:i+2] == 'id':
            tokens.append('id')
            i += 2
        else:
            tokens.append(expr[i])
            i += 1

    def reduce_stack():
        if stack[-1] == 'id':
            stack.pop(); stack.append('E')
            return "Reduce: id -> E"
        elif len(stack) >= 3 and stack[-3] == 'E' and stack[-2] in ['+', '*'] and stack[-1] == 'E':
            op = stack[-2]
            stack[-3:] = ['E']
            return f"Reduce: E {op} E -> E"
        return "Error"

    while tokens:
        top, curr = find_rightmost_terminal(stack), tokens[0]
        if top == '$' and curr == '$':
            print(f"{''.join(stack):<30}| {''.join(tokens):<20}| Accept")
            break

        action = table[top].get(curr, '-')
        print(f"{''.join(stack):<30}| {''.join(tokens):<20}| ", end="")

        if action in ['<', '=']:
            stack.append(tokens.pop(0))
            print("Shift")
        elif action == '>':
            print(reduce_stack())
        else:
            print("Error: Invalid precedence relation")
            return

    print("\nParsing Completed.")

if __name__ == "__main__":
    expr = "id+id*id"
    print("Step 1: Checking the input string...")
    print("Input string:", expr)
    table = generate_precedence_table()
    print_table(table)
    print("\nInput string is valid. Starting parsing...")
    print("\nStep 2: Parsing with operator precedence...")
    parse_input(expr, table)
