def simulate_code_generation(statements):
    reg_desc, addr_desc, output = {'R0': '', 'R1': ''}, {}, []

    for stmt in statements:
        lhs, expr = map(str.strip, stmt.split('='))
        code, reg = [], 'R0' if not reg_desc['R0'] else 'R1'

        parts = expr.split()
        if len(parts) == 3 and parts[1] in '+-':
            op1, op, op2 = parts
            code += [f"MOV {op1}, {reg}", f"{'ADD' if op == '+' else 'SUB'} {op2}, {reg}"]
        else:
            code.append(f"MOV {expr}, {reg}")

        reg_desc[reg], addr_desc[lhs] = lhs, f"{lhs} in {reg}"
        if lhs in ['d', 'result']:
            code.append(f"MOV {reg}, {lhs}")
            addr_desc[lhs] = f"{lhs} in {reg} and memory"

        reg_state = ', '.join(f"{k} contains {v}" if v else f"{k} empty" for k, v in reg_desc.items())
        addr_state = ', '.join(f"{k} in {v.split()[-1]}" for k, v in addr_desc.items())
        output.append((stmt, code, reg_state, addr_state))

    return output

def display_table(table):
    print(f"{'Statements':<15} | {'Code Generated':<30} | {'Register Descriptor':<40} | {'Address Descriptor'}")
    print("-" * 120)
    for stmt, code, reg_desc, addr_desc in table:
        print(f"{stmt:<15} | {'\n                  '.join(code):<30} | {reg_desc:<40} | {addr_desc}")

def main():
    print("Enter the 3-address code statements line by line. Type 'end' to finish:\n")
    statements = iter(input, 'end')
    result = simulate_code_generation(list(statements))
    print("\n--- Code Generation Output ---\n")
    display_table(result)

if __name__ == "__main__":
    main()
