#!/usr/bin/python3

from itertools import combinations_with_replacement

import numpy as np
import torch
from torch.autograd import Variable


class NN():
    def __init__(self):
        # Tensor type
        self.dtype = torch.FloatTensor
        # Minibatch size
        self.N = 1
        # Input dimension (Position + Orientation)
        self.D_in = 0
        # Output dimension (Rotor Thrusts)
        self.D_out = 0
        # Hidden Layer 1 dimension
        self.H1 = 12
        # Hidden Layer 2 dimension
        self.H2 = 40
        # Hidden Layer 3 dimension
        self.H3 = 12

        # Reinforcement Learning Parameters
        self.learning_rate = 1e-4
        self.discount_factor = 1e-4
        self.reward = 0.0

    def create_model(self):
        # Create model
        self.model = torch.nn.Sequential(
            torch.nn.Linear(self.D_in, self.H1),
            torch.nn.ReLU(),
            torch.nn.Linear(self.H3, self.D_out),
        )
        # Set optimizer
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learning_rate)

        # Loss function
        self.loss_fn = torch.nn.MSELoss(size_average=False)
        return

    def create_in_out_vars(self):
        input = Variable(torch.zeros(self.D_in, 1), requires_grad=True)
        output = Variable(torch.zeros(self.D_out, 1), requires_grad=True)
        return input, output

    def generate_output_combos(self):
        delta_thrusts = np.linspace(-2, +2, 200, dtype=float)
        rotor_combi = list(combinations_with_replacement(delta_thrusts, 4))
        return rotor_combi

    def np_to_torch(self, data):
        return torch.from_numpy(data)

    def torch_to_np(self, data):
        return data.numpy()

    def get_predicted_data(self, state_data):
        pred_data = self.model(state_data)
        return pred_data

    def get_loss(self, pred, curr):
        loss = self.loss_fn(pred, curr)
        return loss

    def do_backprop(self, loss):
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return