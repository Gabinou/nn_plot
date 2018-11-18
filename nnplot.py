# -*- coding: utf-8 -*- #
import numpy as np
import matplotlib.pyplot as plt


class Neuron():
    def __init__(self, x, y, color='k'):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, neuron_radius):
        circle = plt.Circle(
            (self.x, self.y), radius=neuron_radius, color=self.color, fill=False)
        plt.text(self.x-0.3, self.y-0.1, '0.1')
        plt.gca().add_patch(circle)


class Layer():
    def __init__(self, network, number_of_neurons, number_of_neurons_in_widest_layer, neuron_radius, line_weights, line_colors, neuron_color):
        self.vertical_distance_between_layers = 6
        self.horizontal_distance_between_neurons = 2
        self.neuron_radius = neuron_radius
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.previous_layer = self.__get_previous_layer(network)
        self.y = self.__calculate_layer_y_position()
        self.neurons = self.__intialise_neurons(
            number_of_neurons, neuron_color)
        self.line_weights = line_weights
        self.line_colors = line_colors

    def __intialise_neurons(self, number_of_neurons, neuron_color='k'):
        neurons = []
        x = self.__calculate_left_margin_so_layer_is_centered(
            number_of_neurons)
        for iteration in range(number_of_neurons):
            neuron = Neuron(x, self.y, neuron_color)
            neurons.append(neuron)
            x += self.horizontal_distance_between_neurons
        return neurons

    def __calculate_left_margin_so_layer_is_centered(self, number_of_neurons):
        return self.horizontal_distance_between_neurons * (self.number_of_neurons_in_widest_layer - number_of_neurons) / 2

    def __calculate_layer_y_position(self):
        if self.previous_layer:
            return self.previous_layer.y + self.vertical_distance_between_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def __line_between_two_neurons(self, neuron1, neuron2, line_weight=1, linecolor='k'):
        angle = np.arctan((neuron2.x - neuron1.x) /
                          float(neuron2.y - neuron1.y))
        x_adjustment = self.neuron_radius * np.sin(angle)
        y_adjustment = self.neuron_radius * np.cos(angle)
        line = plt.Line2D((neuron1.x - x_adjustment, neuron2.x + x_adjustment),
                          (neuron1.y - y_adjustment, neuron2.y + y_adjustment), alpha=line_weight, color=linecolor)
        plt.gca().add_line(line)

    def draw(self, layerType=0):
        for this_layer_neuron_index in range(len(self.neurons)):
            neuron = self.neurons[this_layer_neuron_index]
            neuron.draw(self.neuron_radius)
            if self.previous_layer:
                for previous_layer_neuron_index in range(len(self.previous_layer.neurons)):
                    previous_layer_neuron = self.previous_layer.neurons[previous_layer_neuron_index]
                    if isinstance(self.previous_layer.line_weights, int):
                        line_weight = self.previous_layer.line_weights
                    else:
                        line_weight = self.previous_layer.line_weights[this_layer_neuron_index,
                                                             previous_layer_neuron_index]
                    if isinstance(self.previous_layer.line_colors, str):
                        linecolor = self.previous_layer.line_colors
                    else:
                        linecolor = self.previous_layer.line_colors[this_layer_neuron_index,
                                                                    previous_layer_neuron_index]
                    self.__line_between_two_neurons(
                        neuron, previous_layer_neuron, line_weight, linecolor)
        # write Text
        x_text = self.number_of_neurons_in_widest_layer * \
            self.horizontal_distance_between_neurons
        if layerType == 0:
            plt.text(x_text, self.y, 'Input Layer', fontsize=12)
        elif layerType == -1:
            plt.text(x_text, self.y, 'Output Layer', fontsize=12)
        else:
            plt.text(x_text, self.y, 'Hidden Layer ' +
                     str(layerType), fontsize=12)


class NeuralNetwork():
    def __init__(self, number_of_neurons_in_widest_layer, neuron_radius=0.5):
        self.number_of_neurons_in_widest_layer = number_of_neurons_in_widest_layer
        self.layers = []
        self.layertype = 0
        self.neuron_radius = neuron_radius

    def add_layer(self, number_of_neurons, neuron_radius=0.5, line_weights=1, line_colors='k', neuron_color='k'):
        layer = Layer(self, number_of_neurons, self.number_of_neurons_in_widest_layer,
                      neuron_radius, line_weights, line_colors, neuron_color)
        self.layers.append(layer)

    def draw(self):
        plt.figure(figsize=(10, 6))
        for i in range(len(self.layers)):
            layer = self.layers[i]
            if i == len(self.layers)-1:
                i = -1
            layer.draw(i)
        plt.axis('scaled')
        plt.axis('off')
        # plt.title( 'Neural Network architecture', fontsize=15 )
        plt.gcf().tight_layout()
        # transform = Affine2D().rotate_deg(270)
        # plot_extents = 0, 10, 0, 10
        # helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
        plt.show()


network = NeuralNetwork(10)
# line_weights to convert from 10 outputs to 4 (decimal digits to their binary representation)
line_weights1 = np.array([[0, 0, 0, 0, 1, 0.3, 0, 0, 1, 1],
                     [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                     [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                     [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])
print(line_weights1.shape)
network.add_layer(10, line_weights=line_weights1, line_colors='b')
network.add_layer(4, neuron_color='b')
network.add_layer(1)
network.draw()
