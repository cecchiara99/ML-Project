import numpy as np
import pandas as pd

class Layer:
    def __init__(self, input_size, output_size, activation='sigmoid',
                 learning_rate=0.01, momentum=0.9, weight_decay=0.001):
        """
        Initialize the neural network layer with specified parameters.

        Args:
            input_size (int): Number of input neurons.
            hidden_size (int): Number of neurons in the hidden layer.
            output_size (int): Number of output neurons.
            activation (str, optional): Activation function ('sigmoid' or 'relu').
            learning_rate (float, optional): Learning rate for gradient descent.
            momentum (float, optional): Momentum term for gradient descent.
            weight_decay (float, optional): Weight decay term for regularization.
        """

        # Initialize the layer with specified parameters
        self.input_size = input_size
        #self.hidden_size = hidden_size
        hidden_size = 3 # prova
        self.output_size = output_size
        self.learning_rate = learning_rate
        self.momentum = momentum
        self.weight_decay = weight_decay

        self.inputs = None
        self.outputs = None
        self.delta = None

        # Initialize weights and biases
        self.weights = np.random.randn(input_size, output_size)
        # Altrimenti c'è un inizializzazione migliore secondo il web - Formula di inizializzazione di He.
        # Questa formula si basa sulla scelta della funzione di attivazione
        # e aiuta a mantenere la varianza stabile attraverso i livelli della rete.
        # self.weights = np.random.randn(input_size, output_size) * np.sqrt(2 / input_size)
        self.bias = np.zeros((1, output_size))
       
        self.weights_input_hidden = np.random.randn(input_size, hidden_size)
        self.bias_hidden = np.zeros((1, hidden_size))
        self.weights_hidden_output = np.random.randn(hidden_size, output_size)
        self.bias_output = np.zeros((1, output_size))

        # Initialize momentum terms
        self.momentum_weights = np.zeros_like(self.weights)
        self.momentum_bias = np.zeros_like(self.bias)
        
        self.momentum_weights_input_hidden = np.zeros_like(self.weights_input_hidden)
        self.momentum_bias_hidden = np.zeros_like(self.bias_hidden)
        self.momentum_weights_hidden_output = np.zeros_like(self.weights_hidden_output)
        self.momentum_bias_output = np.zeros_like(self.bias_output)

        # Set activation functions
        self.activation = self.sigmoid if activation == 'sigmoid' else self.relu
        self.activation_derivative = self.sigmoid_derivative if activation == 'sigmoid' else self.relu_derivative


    def sigmoid(self, x):
        """
        Sigmoid activation function.

        Args:
            x (numpy.ndarray): Input to the sigmoid function.

        Returns:
            numpy.ndarray: Output of the sigmoid function.
        """
        return 1 / (1 + np.exp(-x))

    def sigmoid_derivative(self, x):
        """
        Derivative of the sigmoid activation function.

        Args:
            x (numpy.ndarray): Output of the sigmoid function.

        Returns:
            numpy.ndarray: Derivative of the sigmoid function.
        """
        return x * (1 - x)

    def relu(self, x):
        """
        Rectified Linear Unit (ReLU) activation function.

        Args:
            x (numpy.ndarray): Input to the ReLU function.

        Returns:
            numpy.ndarray: Output of the ReLU function.
        """
        return np.maximum(0, x)

    def relu_derivative(self, x):
        """
        Derivative of the ReLU activation function.

        Args:
            x (numpy.ndarray): Output of the ReLU function.

        Returns:
            numpy.ndarray: Derivative of the ReLU function.
        """
        return np.where(x > 0, 1, 0)
    

    def forward_pass(self, inputs: np.ndarray):
        """
        Compute the forward pass of the layer.

        Args:
            inputs (numpy.ndarray): Inputs to the layer.

        Returns:
            numpy.ndarray: Outputs from the layer.
        """

        self.inputs = inputs
        """
        print("Inputs shape:", inputs.shape)
        print("Weights shape:", self.weights.shape)
        print("Bias shape:", self.bias.shape)
        """
        linear_output = np.dot(inputs, self.weights) + self.bias # Multiply by weights and add bias
        self.outputs = self.activation(linear_output) # Apply activation function

        """
            Gli output sembrano essere valori compresi tra 0 e 1, che è comune quando
                si utilizzano funzioni di attivazione come la sigmoide.
            Tuttavia, per interpretare meglio l'output, potresti voler arrotondarlo o
                utilizzare una soglia per convertire i valori in previsioni binarie,
                soprattutto se stai affrontando un problema di classificazione binaria.

            Ad esempio, se vuoi convertire i valori dell'output in previsioni binarie basate
                su una soglia, potresti fare qualcosa del genere:
            ```python
            threshold = 0.5
            binary_predictions = (output > threshold).astype(int)
            print("Binary predictions:", binary_predictions)
            ```
            In questo esempio, i valori superiori a 0.5 vengono convertiti in 1,
                mentre quelli inferiori o uguali a 0.5 vengono convertiti in 0.
                Tuttavia, la scelta della soglia dipende dal tuo problema specifico
                e dalle tue esigenze.
        """
        return self.outputs
    
    def backward_pass(self, output_gradient, learning_rate):
        """
        Backpropagate the gradient through the layer.

        Args:
            output_gradient (numpy.ndarray): Gradient of the error with respect to the output.
            learning_rate (float): Learning rate for gradient descent.

        Returns:
            numpy.ndarray: Gradient of the error with respect to the input.
        """

        # Compute the gradient respect to the inputs
        delta_inputs = np.dot(output_gradient, self.weights.T)

        # Compute the gradient respect to the weights and bias
        delta_weights = np.dot(self.inputs.T, output_gradient)
        delta_bias = np.sum(output_gradient, axis=0, keepdims=True)


        # Update the weights and bias with momentum
        self.momentum_weights = self.momentum * self.momentum_weights + learning_rate * delta_weights
        self.momentum_bias = self.momentum * self.momentum_bias + learning_rate * delta_bias

        # Update the weights and bias
        self.weights += self.momentum_weights
        self.bias += self.momentum_bias

        # Restituisci il gradiente rispetto agli input per l'uso nelle retropropagazioni successive
        return delta_inputs
