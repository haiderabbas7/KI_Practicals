from eight_queens import *
from utils import *


# kombiniert die eight_queens links und rechts zusammen abhängig vom Index i
# i=0 => nur right, i=8, nur left
def crossover(left: EightQueens, right: EightQueens, i):
    if not (0 <= i <= 8):
        return False
    new_state = left.state[:i] + right.state[i:]
    return EightQueens(''.join(new_state))


# mutiert zufällig eine spalte mit einem zufälligen wert (kann auch der gleiche bleiben)
def mutate(eight_queens: EightQueens):
    column = random.randint(0, 7)
    new_row = random.randint(1, 8)
    eight_queens.place_queen(column, new_row)
    return eight_queens


def fitness_function(eight_queens: EightQueens):
    heuristic = eight_queens.heuristic()
    fitness = 28 - heuristic
    return fitness


def genetic_algorithm(population_size=100, num_iterations=100, dump_threshold=14, threshold=22, mutation_chance=0.01,
                      threshold_multiplier: (float, int) = 3):
    # Anfangspopulation wird mit zufälligen Werten befüllt
    population = [EightQueens(''.join(str(random_number(1, 8)) for _ in range(8))) for _ in range(population_size)]

    # Zum Speichern des besten Individuums über alle Iterationen; wird anfangs mit dem schlechst-möglichen Wert befüllt
    best_individual_all_time = EightQueens("12345678")
    found_in_iteration = 0

    for i in range(num_iterations):
        # berechnet die fitness werte für jedes individuum der population
        fitnesses = [fitness_function(individual) for individual in population]
        new_population = []

        # für jedes individuum in der population
        for j in range(population_size):
            # SELECTION: Wahrscheinlichkeiten der Weiterverwendung von Individuen wird abhängig ihrer Fitness berechnet
            # Individuen mit Fitness <= dumpthreshold werden verworfen
            # Individuen mit Fitness im Intervall [dump_threshold+1;threshold] werden mit einfacher W'keit benutzt
            # und Individuen mit Fitness größer als threshold werden mit einem Multiplikator der W'keit benutzt
            total_fitness = sum(fitnesses)
            probabilities = []
            for fitness in fitnesses:
                if fitness <= dump_threshold:
                    probabilities.append(0)
                elif dump_threshold < fitness <= threshold:
                    probabilities.append(fitness / total_fitness)
                else:
                    probabilities.append(threshold_multiplier * (fitness / total_fitness))

            # Wählt nun aus der Population normalverteilt (mit dem W'keiten aus probabilites) zwei Individuen
            # Individuen können mehrfach vorkommen
            x = random.choices(population, weights=probabilities, k=1)[0]
            y = random.choices(population, weights=probabilities, k=1)[0]

            # CROSSOVER: kombiniert die zufällig ausgewählten Individuen ab einem zufälligen Index und erstellt ein
            # neues Individuum
            child = crossover(x, y, random_number(0, 8))

            # MUTATION: Mit einer Wahrscheinlichkeit verändert eine der Spalten des neuen Individuums
            if random.random() < mutation_chance:
                child = mutate(child)

            new_population.append(child)

        population = new_population

        # Findet und speichert das beste Individuum der Iteration und gibt es aus
        final_fitnesses = [fitness_function(individual) for individual in population]
        best_individual = population[final_fitnesses.index(max(final_fitnesses))]
        print(f"\nBest individual after iteration {i + 1}:")
        best_individual.visualize()

        # prüft, ob ein neues individuum mit rekordhohen fitness finden konnte. wenn ja dann speichert er es
        if fitness_function(best_individual) > fitness_function(best_individual_all_time):
            best_individual_all_time = best_individual
            found_in_iteration = i
    print(f"\nBest individual across all iterations, found in iteration {found_in_iteration + 1}: ")
    best_individual_all_time.visualize()


if __name__ == '__main__':
    genetic_algorithm()

    # SEHR GUT
    # genetic_algorithm(population_size=500, num_iterations=50, dump_threshold=20, threshold=26, mutation_chance=0.5, threshold_multiplier=5)
