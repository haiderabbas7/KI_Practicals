from utils import *


class CNFKnowledgeBase:
    def __init__(self):
        self.clauses = []

    def reset(self):
        self.clauses = []

    def print_knowledge_base(self):
        print_clauses(self.clauses)

    def tell(self, clause):
        literals = clause.split(", ")
        for literal in literals:
            if not is_valid_literal(literal):
                raise ValueError(f"Invalid literal: {literal}")
        if literals not in self.clauses:
            self.clauses.append(literals)

    def pl_resolve(self, clause_a, clause_b):
        clause_a = clause_a.copy()
        clause_b = clause_b.copy()

        for literal_a in clause_a:
            for literal_b in clause_b:
                if is_complement(literal_a, literal_b):
                    clause_a.remove(literal_a)
                    clause_b.remove(literal_b)
                    break
        return array_union(clause_a, clause_b)

    # Logical resolution algorithmus
    def ask(self, query):
        clauses = self.clauses.copy()

        clauses.append(["-" + query] if not query.startswith("-") else [query[1:]])

        new = []
        while True:
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    resolvent = self.pl_resolve(clauses[i], clauses[j])
                    if resolvent == []:
                        return True

                    new = array_union(new, [resolvent])

            if array_contains(new, clauses):
                return False
            clauses = array_union(clauses, new)


if __name__ == '__main__':
    kb = CNFKnowledgeBase()
    # kb.tell("-A21, A21")
    # kb.print_clauses()
    # print(kb.is_negative("-A21", "-A21"))
    # print(kb.pl_resolve(["A21", "A22"], ["-A21", "A23"]))
    kb.tell("-P21, B11")
    kb.tell("-B11, P12, P21")
    kb.tell("-P12, B11")
    kb.tell("-B11")
    print(kb.ask("P12"))
