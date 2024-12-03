import gym
import fh_ac_ai_gym
from CNF import *
from HornClauses import *
from utils import *


def perceptions_to_cnf(knowledge_base, step_results):
    perceptions = step_results[0]
    x = perceptions['x']
    y = perceptions['y']
    position = f"{x}{y}"
    abbreviations = {'stench': 'ST', 'breeze': 'BR', 'glitter': 'GL', 'bump': 'BU', 'scream': 'SC'}

    for perception, value in perceptions.items():
        if perception in abbreviations:
            literal = abbreviations[perception] + position
            if not value:
                literal = "-" + literal
            knowledge_base.tell(literal)


def perceptions_to_horn(knowledge_base, step_results):
    perceptions = step_results[0]
    x = perceptions['x']
    y = perceptions['y']
    position = f"{x}{y}"
    abbreviations = {'stench': 'ST', 'breeze': 'BR', 'glitter': 'GL', 'bump': 'BU', 'scream': 'SC'}

    for observation, value in perceptions.items():
        if observation in abbreviations and value:
            literal = abbreviations[observation] + position
            knowledge_base.tell_literal(literal)


def perceptions_to_both_knowledge_bases(cnf_knowledge_base, horn_knowledge_base, step_results):
    perceptions_to_cnf(cnf_knowledge_base, step_results)
    perceptions_to_horn(horn_knowledge_base, step_results)


def reset_knowledge_bases(cnf_knowledge_base, horn_knowledge_base):
    cnf_knowledge_base.reset()
    horn_knowledge_base.reset()


if __name__ == '__main__':
    kb_c = CNFKnowledgeBase()
    kb_h = HornKnowledgeBase()

    wumpus_env = gym.make('Wumpus-v0', disable_env_checker=True)
    wumpus_env.reset()
    wumpus_env.render()

    # Wumpus Implikationen
    kb_c.tell("-W00")
    kb_c.tell("-ST00, W10, W01")
    kb_c.tell("ST00, -W10")
    kb_c.tell("ST00, -W01")
    kb_c.tell("-ST11, W10, W21, W12, W01")
    kb_c.tell("ST11, -W10")
    kb_c.tell("ST11, -W21")
    kb_c.tell("ST11, -W12")
    kb_c.tell("ST11, -W01")
    kb_h.tell_clause(["ST00", "ST11"], "W10")

    # Mach eine Aktion, um Perceptions zu erhalten
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(1))

    # Check 1: Wumpus links
    print("Check 1: Wumpus links: Ask CNF: ", kb_c.ask("W10"))
    print("Check 1: Wumpus links: Ask horn: ", kb_h.ask("W10"))

    # Geh zum Feld über dem Wumpus
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(2))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    wumpus_env.render()

    # Check 2: Wumpus oben
    print("Check 2: Wumpus oben: Ask CNF: ",  kb_c.ask("W10"))
    print("Check 2: Wumpus oben: Ask horn: ", kb_h.ask("W10"))

    # ENV UND KB RESET: Wir wollen für die Pit-Checks erstmal nicht die Perceptions von Feld (1;1)
    wumpus_env.reset()
    reset_knowledge_bases(kb_c, kb_h)

    # Pit Implikationen
    kb_c.tell("-P00")
    kb_c.tell("-BR02, P03, P12, P01")
    kb_c.tell("-P03, BR02")
    kb_c.tell("-P12, BR02")
    kb_c.tell("-P01, BR02")
    kb_c.tell("-BR23, P03, P12, P23")
    kb_c.tell("-P03, BR23")
    kb_c.tell("-P12, BR23")
    kb_c.tell("-P23, BR23")
    kb_c.tell("-BR22, P12, P23, P32, P21")
    kb_c.tell("-P12, BR22")
    kb_c.tell("-P23, BR22")
    kb_c.tell("-P32, BR22")
    kb_c.tell("-P21, BR22")
    kb_c.tell("-BR11, P01, P10, P21, P12")
    kb_c.tell("-P01, BR11")
    kb_c.tell("-P10, BR11")
    kb_c.tell("-P21, BR11")
    kb_c.tell("-P12, BR11")
    kb_h.tell_clause(["BR02", "BR13", "BR22", "BR11"], "P12")

    # Geh zum Feld links neben der Pit
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(1))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    wumpus_env.render()

    # Check 3: Pit links
    print("Check 3: Pit links: Ask CNF: ", kb_h.ask("P12"))
    print("Check 3: Pit links: Ask horn: ", kb_h.ask("P12"))

    # Geh einmal um die Pit herum bis du wieder auf dem Feld links landest
    print("\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(2))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(2))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(2))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(2))
    perceptions_to_both_knowledge_bases(kb_c, kb_h, wumpus_env.step(0))
    wumpus_env.render()

    # Check 4: Pit links nach dem Loop
    print("Check 4: Pit links nach dem Loop: Ask CNF: ", kb_h.ask("P12"))
    print("Check 4: Pit links nach dem Loop: Ask horn: ", kb_h.ask("P12"))

