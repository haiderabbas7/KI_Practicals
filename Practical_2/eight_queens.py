

class EightQueens:
    # state wird als string der länge 8 repräsentiert
    # dabei steht jedes zeichen für eine spalte, wo sich queen in der spalte befindet
    def __init__(self, initial_state=None):
        if initial_state and (len(initial_state) != 8 or not all(char.isdigit() and 0 <= int(char) <= 8 for char in initial_state)):
            raise ValueError("Invalid initial state")
        self.state = list(initial_state) if initial_state else ['0'] * 8


    # methode zum bewegen von der queen in Spalte column in die neue Zeile new_row
    def place_queen(self, column, new_row):
        if 0 <= column <= 7 and 0 <= new_row <= 8:
            self.state[column] = str(new_row)
            return True
        return False


    # gibt True zurück, wenn es auf dem Board mindestens eine Kollision gibt. Ansonsten False
    def detect_collision(self):
        for i in range(8):
            if self.state[i] == '0':
                continue
            for j in range(i + 1, 8):
                if self.state[j] == '0':
                    continue
                if self.state[i] == self.state[j] or abs(i - j) == abs(int(self.state[i]) - int(self.state[j])):
                    return True
        return False


    # heuristic und cost function sind das gleiche
    def heuristic(self):
        h = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if self.state[i] == self.state[j]:
                    h += 1
                elif abs(i - j) == abs(int(self.state[i]) - int(self.state[j])):
                    h += 1
        return h


    def visualize(self):
        for i in range(8, 0, -1):
            row = []
            for j in range(8):
                if self.state[j] == str(i):
                    tile = 'Q'
                else:
                    tile = '.'
                row.append(tile)
            print(' '.join(row))
        print("Heuristic value: " + str(self.heuristic()))
