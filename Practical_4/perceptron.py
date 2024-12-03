import numpy as np
from utils import *


class Perceptron:
    def __init__(self):
        self.synaptic_weights = np.random.random(3) - 1

    def think(self, inputs):
        # numpy vektor wird erstellt
        input_matrix = np.array(inputs)
        return sigmoid(np.dot(input_matrix, self.synaptic_weights))

    def train(self, inputs, targets, iterations):
        # numpy vektoren werden erstellt
        input_vector = np.array(inputs)
        target_vector = np.array(targets)

        # inital wird output einmal berechnet
        output_vector = self.think(inputs)

        for i in range(iterations):
            print("Synaptic weights before iteration", i)
            print(self.synaptic_weights, "\n")

            # abweichung des berechneten ergebnis von dem gewollten wird berechnet
            error_vector = target_vector - output_vector

            # delta w zur anpassung der gewichtungen der eingaben werden berechnet
            delta_w = input_vector.T @ (error_vector * sigmoid_derivative(output_vector))

            # gewichtung der eingaben werden angepasst
            self.synaptic_weights = self.synaptic_weights + delta_w

            # outputs werden neu berechnet
            output_vector = self.think(inputs)

if __name__ == "__main__":
    input_data = [[0, 0, 1], [1, 1, 1], [1, 0, 0], [0, 1, 1]]
    target_data = [0, 1, 1, 0]
    p = Perceptron()
    p.train(input_data, target_data, 10000)
    print(p.think([1, 1, 0]))

