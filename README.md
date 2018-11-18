# nnplot: Neural network visualization with Matplotlib

New classes are introduced that enable the plotting of neurons, any number of connexions, with weights represented by transparency.

This code was created using code originally published on StackOverflow by users Milo and DenisFlash at the following url: [https://stackoverflow.com/questions/29888233/how-to-visualize-a-neural-network]

The code was intended to print neuron networks vertically, from the input layer (IL) at the bottom to the output layer (OL) at the top.

It has been pruned and modified to accomodate printing text in neurons, rotating the neuron stack, etc.

Some features listed here are not implemented yet, and the codebase is still quite messy and prone to change.


# Classes
### `NeuralNetwork`

Main class meant to be interacted with to easily plot neural networks. For now, on instance initialization the number of neurons in the wides layer must be specified. Then, the `add_layer` method can be used to create any number of layers. By default, the IL, hidden layers (HLs) and OL are automatically labelled. 

In the `add_layer` method,
-the `line_color` and `neuron_color` can be specified using a string or an numpy.array of strings/floats between 0 and 1 (of shape (current layer neurons, next layer neurons)) if the individual object color needs to be specified.
-the `line_weigths` and `neuron_weights` (NOT YET IMPLEMENTED) can be specified similarly, with floats or a np.array of floats between 0 and 1.

### `Layer`
Layer object class. Not meant to be interacted with by the user.

A great number of parameters must be specified on initialization.

## `Neuron`
Neuron object class. Not meant to be interacted with by the user.

Specifiy its position and color on initialization. `draw` method used to draw it on a previously initialized figure.

