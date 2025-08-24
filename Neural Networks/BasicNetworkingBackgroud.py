import pickle
import numpy as np
from tensorflow.keras.datasets import mnist

(x_train, y_train), (x_test, y_test) = mnist.load_data()

# This line is coverts the rgb values to their 0-1 range floats
x_train = x_train.astype(np.float32) / 255.0
x_test = x_test.astype(np.float32) / 255.0

# y_train and y_test are just a 1 dimensional array of numbers/answers

x_train = x_train.reshape(-1, 784).T  # shape: (784, 60k)
x_test = x_test.reshape(-1, 784).T  # shape: (784, 10k)
y_train_hot = np.eye(10)[y_train].T  # shape: (10, 60k)
y_test_hot = np.eye(10)[y_test].T  # shape: (10, 10k)


def make_batch(X, Y, batch_size, i):
    return X[:, (i * batch_size):((i + 1) * batch_size)], Y[:, (i * batch_size):((i + 1) * batch_size)]


def activate(X, type='SIGMOID'):
    if type.upper() == 'SIGMOID':
        return 1 / (1 + np.exp(-1 * X))
    if type.upper() == 'SOFTMAX':
        exp_X = np.exp(X - np.max(X, axis=0, keepdims=True))
        return exp_X / np.sum(exp_X, axis=0, keepdims=True)
    return None


def handle_data(data, is_save):
    if is_save:
        with open('parameters.pickle', 'wb') as f:
            pickle.dump(data, f)
    else:
        with open('parameters.pickle', 'rb') as f:
            return pickle.load(f)


class Network:

    def __init__(self, size, params=None):
        self.size = size  # [a, b, c, d]
        self.step_size = 0.4
        self.layers = []
        self.create_net()
        if params != None:
            self.get_net(params)

    def create_net(self):
        for i in range(len(self.size) - 2):
            self.layers.append(self.HiddenLayer(self.size[i + 1], self.size[i]))
        self.layers.append(self.OutputLayer(self.size[-1], self.size[-2]))

    def get_net(self, params):
        for i in range(len(self.layers)):
            self.layers[i].W, self.layers[i].b = params[i]

    def export_params(self):
        params = []
        for layer in self.layers:
            params.append([layer.W, layer.b])
        return params

    def feed_forward(self, X):
        outputs = None
        for i in range(len(self.size) - 1):
            active_layer = self.layers[i]
            if i == 0:
                outputs = active_layer.feed_forward(X)
            else:
                outputs = active_layer.feed_forward(outputs)
        return outputs

    def calculate_gradient(self, X, y):
        for i in range(len(self.layers)):
            active_layer = self.layers[len(self.layers) - i - 1]
            previous_layer = self.layers[len(self.layers) - i - 2]
            results = ()

            if i == 0:  # For the output layer
                results = active_layer.back_propagate(previous_layer.A, y)
            if i == len(self.layers) - 1:  # For input layers
                results = active_layer.back_propagate(X, results[0], results[1])
            else:  # For the other layers
                print("\n\n\n\n\n\nPRINTING RESULTS\n", previous_layer.A,"\n\n\n\n\n\n",results[0],"\n\n\n\n\n\n",results[1])
                results = active_layer.back_propagate(previous_layer.A, results[0], results[1])

    def update_params(self):
        for layer in self.layers:
            layer.update_weights(self.step_size)

    class HiddenLayer:
        def __init__(self, n_l, n_l_1):
            self.n_l = n_l
            self.n_l_1 = n_l_1
            self.generate_rand_data()

        def generate_rand_data(self):
            self.W = np.random.randn(self.n_l, self.n_l_1)
            self.b = np.random.randn(self.n_l, 1)

        def feed_forward(self, A_l_1):
            self.z = self.W @ A_l_1 + self.b
            self.A = activate(self.z)
            return self.A

        def back_propagate(self, A_l_1, W_l_2, Delta_l_2):
            # Calculate the gradients
            m = self.A.shape[1]

            self.Delta_l = (np.transpose(W_l_2) @ Delta_l_2) * (self.A * (1 - self.A))
            self.dC_dW = (1 / m) * (self.Delta_l @ np.transpose(A_l_1))
            self.dC_db = (1 / m) * np.sum(self.Delta_l, axis=1)
            return self.W, self.Delta_l

        def update_weights(self, step_size):
            self.W = self.W - (step_size * self.dC_dW)
            self.b = self.b - (step_size * self.dC_db)

    class OutputLayer:
        def __init__(self, n_l, n_l_1):
            self.n_l = n_l
            self.n_l_1 = n_l_1
            self.generate_rand_data()

        def generate_rand_data(self):
            self.W = np.random.randn(self.n_l, self.n_l_1)
            self.b = np.random.randn(self.n_l, 1)

        def feed_forward(self, A_l_1):
            self.z = self.W @ A_l_1 + self.b
            self.A = activate(self.z)
            return self.A

        def back_propagate(self, A_l_1, y):
            # Calculate the gradients
            m = self.A.shape[1]  # This is the size of the batch we are sending
            self.Delta_l = (self.A - y) * (self.A * (1 - self.A))
            self.dC_dW = (1 / m) * (self.Delta_l @ np.transpose(A_l_1))
            self.dC_db = (1 / m) * np.sum(self.Delta_l, axis=1)

            return self.W, self.Delta_l

        def update_weights(self, step_size):
            self.W = self.W - (step_size * self.dC_dW)
            self.b = self.b - (step_size * self.dC_db)


def train_network(X, y, epoches, batch_size, Network):
    # Here, y is oneHot value. Not the regular value
    for epoch in range(epoches):
        print(f"\n\n\n We are now starting with epoch : {epoch}\n\n\n")

        for batch in range(X.shape[1] // batch_size):
            X, y = make_batch(X, y, batch_size, batch)
            A_out = Network.feed_forward(X)
            Network.calculate_gradient(X, y)
            Network.update_params()

            # Update the user after every 100 batches
            if (batch + 1) % 100 == 0:
                print(f"{batch + 1} / {X.shape[1] // batch_size}")

    params = Network.export_params()
    handle_data(params, True)


def test_network(X, y, Network):
    # Here, y shouldn't be oneHot value. It should be the y_test data recieved from the orginal file

    print("\n\n\n Starting the test phase.")
    output = Network.feed_forward(X)
    print("---Outputs Recieved")
    A = np.argmax(output, axis=0)
    accuracy = (np.sum(A - y) / output.shape[1]) * 100
    print(f"Accuracy of model : {accuracy[0]}%")


# Running the actual code

Neural_Network = Network([784, 24, 24, 24, 10])

train_network(x_train, y_train_hot, 5, 100, Neural_Network)
test_network(x_test, y_test, Neural_Network)
