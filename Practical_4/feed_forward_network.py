import numpy as np
import matplotlib.pyplot as plt
from utils import *
import time


class NeuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        self.learning_rate = learning_rate
        # gewichtsmatrizen werden mit den parametern erstellt und zufällig befüllt
        self.W_ih = np.random.rand(hiddennodes, inputnodes) - 0.5
        self.W_ho = np.random.rand(outputnodes, hiddennodes) - 0.5

    def think(self, inputs):
        # numpy vektoren werden erstellt
        input_matrix = np.array(inputs).T

        # outputs werden nach formeln in aufgabenstellung berechnet
        hidden_outputs = sigmoid(np.dot(self.W_ih, input_matrix))
        final_outputs = sigmoid(np.dot(self.W_ho, hidden_outputs))
        return hidden_outputs, final_outputs

    def train(self, inputs, targets, iterations):
        # numpy vektoren werden erstellt
        input_vector = np.array(inputs)
        target_vector = np.array(targets)
        for _ in range(iterations):
            hidden_outputs, final_outputs = self.think(inputs)
            output_errors = target_vector.T - final_outputs
            hidden_errors = np.dot(self.W_ho.T, output_errors)
            delta_w_ho = (output_errors * sigmoid_derivative(final_outputs)) @ hidden_outputs.T
            self.W_ho = self.W_ho + self.learning_rate * delta_w_ho
            delta_w_ih = (hidden_errors * sigmoid_derivative(hidden_outputs)) @ input_vector
            self.W_ih = self.W_ih + self.learning_rate * delta_w_ih

if __name__ == "__main__":
    input_nodes = 784  # 28*28 pixel
    hidden_nodes = 200  # voodoo magic number
    output_nodes = 10  # numbers from [0:9]
    learning_rate = 0.1  # feel free to play around with
    iterations = 1000

    # Dateien werden geöffnet
    mnist_test_10_file = open("misc/mnist_test_10.csv")
    mnist_test_10 = mnist_test_10_file.readlines()
    mnist_test_10_file.close()

    mnist_test_full_file = open("misc/mnist_test_full.csv")
    mnist_test_full = mnist_test_full_file.readlines()
    mnist_test_full_file.close()

    mnist_train_100_file = open("misc/mnist_train_100.csv")
    mnist_train_100 = mnist_train_100_file.readlines()
    mnist_train_100_file.close()

    mnist_train_full_file = open("misc/mnist_train_full.csv")
    mnist_train_full = mnist_train_full_file.readlines()
    mnist_train_full_file.close()

    inputs = []
    targets = []

    # daten aus der trainings datei werden ausgelesen und entsprechend inputs und targets befüllt
    for data in mnist_train_100:  # mnist_train_full
        values = data.split(',')
        correct_label = int(values[0])
        grayscale_values = list(map(float, values[1:]))

        # werte werden normalisiert
        normalized_values = np.array(grayscale_values) / 255.0 * 0.99 + 0.01

        target_array = np.full(10, 0.01)
        target_array[correct_label] = 0.99
        inputs.append(normalized_values)
        targets.append(target_array)

    # Netzwerk wird erstellt und mit den inputs und targets trainiert
    n = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)
    n.train(inputs, targets, iterations)

    # scorecard wird erstellt zum Tracken der korrekt erkannten Bilder
    scorecard = []

    for i, data in enumerate(mnist_test_10):
        values = data.split(',')
        correct_label = int(values[0])
        grayscale_values = list(map(float, values[1:]))
        normalized_values = np.array(grayscale_values) / 255.0 * 0.99 + 0.01

        # print("Plotting image for label: ", correct_label)
        # image_array = normalized_values.reshape((28,28))
        # plt.imshow(image_array, cmap='Greys', interpolation='None')
        # plt.show(block=False)
        # time.sleep(0.5)

        # netzwerk abfragen mit den pixel-daten des bildes
        _, final_outputs = n.think([normalized_values])
        print("Bild ", i, "mit Value", correct_label)
        print(final_outputs)

        # die Vorhersage des Netzwerks ist der Index des größten Werts in den finalen Ausgaben
        network_label = np.argmax(final_outputs)

        # wenn vorhersage korrekt ist, wird eine 1 angehängt. ansonsten eine 0
        if network_label == correct_label:
            scorecard.append(1)
        else:
            scorecard.append(0)

    # performance ist der durchschnitt an korrekt vorhersagten bildern
    performance = np.mean(scorecard)
    print("Performance = ", performance)
