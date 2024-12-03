def is_valid_literal(literal):
    if literal.startswith("-"):
        literal = literal[1:]
    if len(literal) == 3:
        return literal[0].isalpha() and literal[1:].isdigit()
    elif len(literal) == 4:
        return literal[0].isalpha() and literal[1].isalpha() and literal[2:].isdigit()
    else:
        return False


def print_clauses(clauses):
    for i, clause in enumerate(clauses):
        literals = ', '.join(clause)
        print(f"Clause {i + 1}: {literals}")


def is_complement(literal_a, literal_b):
    if literal_a.startswith("-") and literal_a[1:] == literal_b:
        return True
    elif literal_b.startswith("-") and literal_b[1:] == literal_a:
        return True
    else:
        return False


def is_negative(literal):
    return literal.startswith("-")


def array_union(clauses_a, clauses_b):
    union = clauses_a
    for clause_b in clauses_b:
        if clause_b not in union:
            union.append(clause_b)
    return union


def array_contains(small, big):
    con = True
    for elem in small:
        if elem not in big:
            con = False
    return con


if __name__ == '__main__':
    print(is_valid_literal("AB21"))
    #print(array_union([[1],[2],[3],[4]],[[2,5,7]]))
    #print(array_contains([1,2,4],[1,2,5]))
