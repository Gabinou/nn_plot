# -*- coding: utf-8 -*- #
import numpy as np
import matplotlib.pyplot as plt


class Neuron():
    def __init__(self, x, y, color='k', text=''):
        self.x = x
        self.y = y
        self.color = color
        self.text = text

    def draw(self, neuron_radius=0.5):
        circle = plt.Circle(
            (self.x, self.y), radius=neuron_radius, color=self.color, fill=False)
        plt.text(self.x-0.3, self.y-0.1, self.text)
        plt.gca().add_patch(circle)


class Layer():
    def __init__(self, network, neuron_num, neuron_num_widest, neuron_radius, line_weights, line_colors, neuron_color, neuron_text, distance_layers=6, distance_neurons=2):

        self.distance_layers = distance_layers
        self.distance_neurons = distance_neurons
        self.neuron_radius = neuron_radius
        self.neuron_text = neuron_text
        self.neuron_num_widest = neuron_num_widest
        self.previous_layer = self.__get_previous_layer(network)
        self.direction = network.direction
        if (self.direction == 'bottomtotop') or (self.direction == 'toptobottom'):
            self.y = self.__layer_position()
        elif (self.direction == 'righttoleft') or (self.direction == 'lefttoright'):
            self.x = self.__layer_position()
        self.neurons = self.__intialise_neurons(
            neuron_num, neuron_color, neuron_text)
        self.line_weights = line_weights
        self.line_colors = line_colors

    def __intialise_neurons(self, neuron_num, neuron_color='k', neuron_text=''):
        neurons = []
        if (self.direction == 'bottomtotop') or (self.direction == 'toptobottom'):
            self.x = self.__lmargin_for_centering(neuron_num)
        elif (self.direction == 'righttoleft') or (self.direction == 'lefttoright'):
            self.y = self.__lmargin_for_centering(neuron_num)
        for iteration in range(neuron_num):
            if isinstance(neuron_color, str):
                color = neuron_color
            else:
                color = neuron_color[iteration]
            if isinstance(neuron_text, str):
                text = neuron_text
            else:
                text = neuron_text[iteration]
            neuron = Neuron(self.x, self.y, color, text)
            neurons.append(neuron)
            if (self.direction == 'bottomtotop') or (self.direction == 'toptobottom'):
                self.x += self.distance_neurons
            elif (self.direction == 'righttoleft') or (self.direction == 'lefttoright'):
                self.y += self.distance_neurons
        return neurons

    def __lmargin_for_centering(self, neuron_num):
        return self.distance_neurons * (self.neuron_num_widest - neuron_num) / 2

    def __layer_position(self):
        if self.previous_layer:
            if (self.direction == 'bottomtotop'):
                return self.previous_layer.y + self.distance_layers
            elif (self.direction == 'toptobottom'):
                return self.previous_layer.y - self.distance_layers
            elif (self.direction == 'lefttoright'):
                return self.previous_layer.x + self.distance_layers
            elif (self.direction == 'righttoleft'):
                return self.previous_layer.x - self.distance_layers
        else:
            return 0

    def __get_previous_layer(self, network):
        if len(network.layers) > 0:
            return network.layers[-1]
        else:
            return None

    def __line_two_neurons(self, neuron1, neuron2, line_weight=1, linecolor='k'):
        if (self.direction == 'bottomtotop') or (self.direction == 'toptobottom'):
            angle = np.arctan((neuron2.x - neuron1.x) /
                              float(neuron2.y - neuron1.y))
            x_adjustment = self.neuron_radius * np.sin(angle)
            y_adjustment = self.neuron_radius * np.cos(angle)
        elif (self.direction == 'righttoleft') or (self.direction == 'lefttoright'):
            angle = np.arctan((neuron2.y - neuron1.y) /
                              float(neuron2.x - neuron1.x))
            x_adjustment = self.neuron_radius * np.cos(angle)
            y_adjustment = self.neuron_radius * np.sin(angle)
        if (self.direction == 'bottomtotop'):
            line_x1 = neuron1.x - x_adjustment
            line_x2 = neuron2.x + x_adjustment
            line_y1 = neuron1.y - y_adjustment
            line_y2 = neuron2.y + y_adjustment
        elif (self.direction == 'toptobottom'):
            line_x1 = neuron1.x + x_adjustment
            line_x2 = neuron2.x - x_adjustment
            line_y1 = neuron1.y + y_adjustment
            line_y2 = neuron2.y - y_adjustment
        if (self.direction == 'lefttoright'):
            line_x1 = neuron1.x - x_adjustment
            line_x2 = neuron2.x + x_adjustment
            line_y1 = neuron1.y - y_adjustment
            line_y2 = neuron2.y + y_adjustment
        elif (self.direction == 'righttoleft'):
            line_x1 = neuron1.x + x_adjustment
            line_x2 = neuron2.x - x_adjustment
            line_y1 = neuron1.y + y_adjustment
            line_y2 = neuron2.y - y_adjustment
        line = plt.Line2D((line_x1, line_x2),
                          (line_y1, line_y2),
                          alpha=line_weight, color=linecolor)
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
                    self.__line_two_neurons(
                        neuron, previous_layer_neuron, line_weight, linecolor)
        if (self.direction == 'bottomtotop') or (self.direction == 'toptobottom'):
            x_text = self.neuron_num_widest * self.distance_neurons
            if layerType == 0:
                plt.text(x_text, self.y, 'Input Layer', fontsize=12)
            elif layerType == -1:
                plt.text(x_text, self.y, 'Output Layer', fontsize=12)
            else:
                plt.text(x_text, self.y, 'Hidden Layer ' +
                         str(layerType), fontsize=12)
        elif (self.direction == 'righttoleft') or (self.direction == 'lefttoright'):
            y_text = self.neuron_num_widest * self.distance_neurons
            x_text = self.x - self.distance_neurons
            if layerType == 0:
                plt.text(x_text, y_text, 'Input Layer', fontsize=12)
            elif layerType == -1:
                plt.text(x_text, y_text, 'Output Layer', fontsize=12)
            else:
                plt.text(x_text, y_text, 'Hidden Layer ' +
                         str(layerType), fontsize=12)


class NeuralNetwork():
    def __init__(self, neuron_num_widest, neuron_radius=0.5, direction='lefttoright'):
        self.neuron_num_widest = neuron_num_widest
        self.layers = []
        self.layertype = 0
        self.direction = direction
        self.neuron_radius = neuron_radius

    def add_layer(self, neuron_num, neuron_radius=0.5, line_weights=1, line_colors='k', neuron_color='k', neuron_text=''):
        layer = Layer(self, neuron_num, self.neuron_num_widest, neuron_radius,
                      line_weights, line_colors, neuron_color, neuron_text)
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
        plt.gcf().tight_layout()


network = NeuralNetwork(10)
# line_weights to convert from 10 outputs to 4 (decimal digits to their binary representation)
line_weights1 = np.array([[0, 0, 0, 0, 1, 0.3, 0, 0, 1, 1],
                          [0, 0, 0, 0, 1, 1, 1, 1, 0, 0],
                          [0, 0, 1, 1, 0, 0, 1, 1, 0, 0],
                          [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]])
neuron_text1 = np.array(['0.1', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
print(line_weights1.shape)
network.add_layer(10, line_weights=line_weights1,
                  line_colors='b', neuron_text=neuron_text1)
network.add_layer(4, neuron_color='b', )
network.add_layer(1)
network.draw()
plt.show()
