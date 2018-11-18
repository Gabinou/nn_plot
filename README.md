# nnplot: Neural network visualization with Matplotlib

New classes are introduced that enable the plotting of neurons, any number of connexions, with weights represented by transparency.

This was created using code originally published on StackOverflow by users Milo, OliBlum and DenisFlash at: [https://stackoverflow.com/questions/29888233/how-to-visualize-a-neural-network].

The code was intended to print neuron networks vertically, from the input layer (IL) at the bottom to the output layer (OL) at the top. It has been pruned and modified to accomodate printing text in neurons, stacking neurons vertically or horizontally, etc.

Some features listed here are not implemented yet, and the code is still quite messy and prone to change.

# Classes
### `NeuralNetwork`

Main class meant to be interacted with, to plot neural networks. For now, on instance initialization the number of neurons in the wides layer must be specified. Then, the `add_layer` method can be used to create any number of layers, with the number of neurons in this new line the only necessary input. The first added layer using this method is the IL, and the last the OL. By default, the IL, hidden layers (HLs) and OL are automatically labelled, and the HLs numbered. The drawn NN orientation can be specified with the `direction` keyword argument. Starting from the IL, `direction`  = `bottomtotop`, `toptobottom`, `righttoleft`, `lefttoright`.

In the `add_layer` method,
- the `line_color` (of lines that go from the current neuron layer to the next) can be specified using a string or an numpy.array of strings of shape (current layer neuron number, next layer neuron number).
- `neuron_color` (NOT YET IMPLEMENTED)  ibid. `line-color`.
- the `line_weigths` (of lines that go from the current layer to the next) can be specified using a float or an numpy.array of strings/floats between 0 and 1 of shape (current layer neuron number, next layer neuron number), if needed.
- `neuron_weights` (NOT YET IMPLEMENTED) ibid. `line_weigths`.

### `Layer`
Layer object class. Not meant to be interacted with by the user.

A great number of parameters must be specified on initialization. Quite messy. Will probably be pruned somehow in the future.

## `Neuron`
Neuron object class. Not meant to be interacted with by the user.

Specifiy its position and color on initialization. `draw` method used to draw it on a previously initialized figure.

