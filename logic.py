
import pandas as pd

# Boolean expressions for all seven logic gates
expressions = {
    "AND": "Y = A.B",
    "OR": "Y = A + B",
    "NOT": "Y = A'",
    "NAND": "Y = (A.B)'",
    "NOR": "Y = (A+B)'",
    "XOR": "Y = A XOR B",
    "XNOR": "Y = (A XOR B)'"
}

def generate_truth_table(gate):
    gate = gate.upper()

    if gate not in expressions:
        raise ValueError("Unknown logic gate")

    rows = []

    # NOT gate has only one input
    if gate == "NOT":
        for a in [0, 1]:
            y = int(not a)
            rows.append([a, y])

        return pd.DataFrame(rows, columns=["A", "Y"])

    # Other gates have two inputs
    for a in [0, 1]:
        for b in [0, 1]:

            if gate == "AND":
                y = a & b

            elif gate == "OR":
                y = a | b

            elif gate == "NAND":
                y = int(not (a & b))

            elif gate == "NOR":
                y = int(not (a | b))

            elif gate == "XOR":
                y = a ^ b

            elif gate == "XNOR":
                y = int(not (a ^ b))

            rows.append([a, b, y])

    return pd.DataFrame(rows, columns=["A", "B", "Y"])


# Test the program
if __name__ == "__main__":
    gate = "AND"

    print("Logic Gate:", gate)
    print("Boolean Expression:", expressions[gate])
    print("Truth Table:")
    print(generate_truth_table(gate))
