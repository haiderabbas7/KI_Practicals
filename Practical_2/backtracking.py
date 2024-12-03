from eight_queens import *


def backtracking_algorithm(max_iterations):
    board = EightQueens()
    solutions = []
    placement = [0, 0, 0, 0, 0, 0, 0, 0]
    queen = 0

    # Interne Funktion zum Backtracking: Placements werden resetted, bis eine Queen gefunden wurde, die noch bewegt
    # werden kann
    def backtrack():
        nonlocal queen
        while placement[queen] == 8:
            board.place_queen(queen, 0)
            placement[queen] = 0
            queen -= 1
        placement[queen] += 1

    for iteration in range(max_iterations):
        # Falls eine neue Queen gesetzt wird => Fang mit der ersten Zeile an
        board.place_queen(queen, placement[queen] if placement[queen] != 0 else 1)
        placement[queen] = int(board.state[queen])

        # Falls keine Kollisionen gefunden wurden
        if not board.detect_collision():
            if queen == 7:
                # Prüft, ob diese Lösung schon mal gefunden wurde. Ansonsten wird gespeichert und auf Konsole ausgegeben
                if board.state not in solutions:
                    solutions.append(list(board.state))
                    print(f"\nNew solution found in iteration {iteration}:")
                    print(''.join(board.state))
                # Backtracken damit man weitere Lösungen finden kann
                backtrack()
            else:
                queen += 1
        else:
            # Es gibt ne Kollision => Queen auf diesem Platz macht Probleme => Platz resetten
            board.place_queen(queen, 0)
            # Fall es gibt noch mögliche Plätze für die Queen
            if placement[queen] < 8:
                placement[queen] += 1
            # Fall es gibt keine möglichen Plätze mehr => backtracken zur vorherigen Queen!
            else:
                backtrack()

    if len(solutions) == 0:
        print("No solutions found.")
    else:
        print(f"\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n"
              f"  Total amount of solutions found: {len(solutions)}/92\n"
              f"XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


if __name__ == '__main__':
    backtracking_algorithm(10000)
    # in iteration 14851 wird die letzte Lösung 84136275 gefunden
