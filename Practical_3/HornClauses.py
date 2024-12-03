from utils import *


class HornKnowledgeBase:
    def __init__(self):
        self.clauses = []

    def reset(self):
        self.clauses = []

    def print_knowledge_base(self):
        for i, clause in enumerate(self.clauses):
            premise, conclusion = clause
            if premise == ["true"]:
                print(f"Clause {i + 1}: {conclusion}")
            else:
                premise_str = " ∧ ".join(premise)
                print(f"Clause {i + 1}: {premise_str} => {conclusion}")

    # Bildet Hornklausel nach Stil true => Literal und fügt der KB hinzu
    def tell_literal(self, literal):
        if not isinstance(literal, str):
            raise ValueError("Literal must be a string.")
        if not is_valid_literal(literal):
            raise ValueError("Invalid literal.")
        if is_negative(literal):
            raise ValueError("Literal must be positive.")
        # Überprüfen, ob das Literal bereits in der Wissensbasis vorhanden ist
        for premise, conclusion in self.clauses:
            if conclusion == literal:
                return
        self.clauses.append((["true"], literal))

    # Bildet Hornklausel (premise => conclusion) und fügt der KB hinzu
    def tell_clause(self, premise, conclusion):
        if not isinstance(premise, list) or not all(isinstance(literal, str) for literal in premise):
            raise ValueError("Premise must be an array of strings.")
        if not isinstance(conclusion, str):
            raise ValueError("Conclusion must be a string.")
        if not all(is_valid_literal(literal) for literal in premise) or not is_valid_literal(conclusion):
            raise ValueError("Invalid literal in premise or conclusion.")
        if any(is_negative(literal) for literal in premise) or is_negative(conclusion):
            raise ValueError("All literals in premise and conclusion must be positive.")
        # Überprüfen, ob die Klausel bereits in der Wissensbasis vorhanden ist
        for existing_premise, existing_conclusion in self.clauses:
            if existing_premise == premise and existing_conclusion == conclusion:
                return
        self.clauses.append((premise, conclusion))

    # Forward Chaining als Inferenzmechanismus
    def ask(self, q):
        clauses = self.clauses.copy()

        # count zählt die Literale/Symbole in den Prämissen
        count = []
        for (premise, conclusion) in clauses:
            count.append(len(premise))

        # inferred gibt für ein Symbol an, ob es aus einem anderen Symbol hervorgeht
        inferred = {}
        for (premise, conclusion) in clauses:
            for literal in premise:
                if literal not in inferred:
                    if literal != "true":
                        inferred[literal] = False
            if conclusion not in inferred:
                inferred[conclusion] = False

        # agenda zum speichern der positiven Literale
        agenda = []
        for (premise, conclusion) in clauses:
            if "true" in premise:
                if conclusion not in agenda:
                    agenda.append(conclusion)

        while agenda:
            p = agenda.pop(0)
            if p == q:
                return True
            if not inferred[p]:
                inferred[p] = True
                for i, (premise, conclusion) in enumerate(clauses):
                    if p in premise:
                        count[i] -= 1
                        if count[i] == 0:
                            agenda.append(conclusion)
        return False


if __name__ == '__main__':
    kb = HornKnowledgeBase()
    #kb.tell_literal("A21")
    #kb.tell_clause(["A21", "B31"], "B21")
    kb.tell_clause(["P11"], "Q11")
    kb.tell_clause(["L11", "M11"], "P11")
    kb.tell_clause(["B11", "L11"], "M11")
    kb.tell_clause(["A11", "P11"], "L11")
    kb.tell_clause(["A11", "B11"], "L11")
    kb.tell_literal("A11")
    kb.tell_literal("B11")
    kb.print_knowledge_base()
    print(kb.ask("Q11"))
