# Three Address Code (3AC) expressions
three_ac = [
    ("f", "c", "+", "d"),
    ("e", "a", "-", "f"),
    ("g", "b", "*", "e")
]

def generate_triples():
    triples = []
    # Process each instruction in the three address code
    for instr in three_ac:
        if instr[2] == "=":
            triples.append(('=', instr[1], instr[3]))
        else:
            triples.append((instr[2], instr[1], instr[3]))
    return triples

def display_triples():
    triples = generate_triples()
    print("\n--- Triples ---")
    for i, triple in enumerate(triples):
        print(f"{i}: ({triple[0]:^7}, {triple[1]:^5}, {triple[2]:^5})")

# Display the Triples
display_triples()
