# -*- coding: utf-8 -*-
"""Lab_Task_2_(2021_3_60_288)Trading Agent for Smartphone Inventory Management.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1xszGdLBZfySgf_NfuVz5l2v6jVa9UQK-
"""

 import random
 import math
 import matplotlib.pyplot as plt


def argmaxall(gen):

    maxv = -math.inf
    maxvals = []
    for (e, v) in gen:
        if v > maxv:
            maxvals, maxv = [e], v
        elif v == maxv:
            maxvals.append(e)
    return maxvals

def argmaxe(gen):

    return random.choice(argmaxall(gen))

def flip(prob):

    return random.random() < prob

def select_from_dist(item_prob_dist):

    ranreal = random.random()
    for it, prob in item_prob_dist.items():
        if ranreal < prob:
            return it
        ranreal -= prob
    raise RuntimeError(f"{item_prob_dist} is not a valid probability distribution")


class Displayable:
    max_display_level = 1

    def display(self, level, *args, **nargs):

        if level <= self.max_display_level:
            print(*args, **nargs)


class Environment(Displayable):
    def initial_percept(self):

        raise NotImplementedError("initial_percept")

    def do(self, action):

        raise NotImplementedError("Environment.do")


class Simulate(Displayable):
    def __init__(self, agent, environment):
        self.agent = agent
        self.env = environment
        self.percept = self.env.initial_percept()
        self.percept_history = [self.percept]
        self.action_history = []

    def go(self, steps):

        for step in range(steps):
            action = self.agent.select_action(self.percept)
            self.action_history.append(action)
            print(f"Step {step}, Action: {action}")
            self.percept = self.env.do(action, step)
            self.percept_history.append(self.percept)
            print(f"Step {step}, Percept: {self.percept}")


class TP_env(Environment):
    price_delta = [0, 20, -15, 10, -25, 30, -10, 5, 0, -20]
    sd = 5

    def __init__(self):
        self.time = 0
        self.stock = 20
        self.stock_history = []
        self.price_history = []

    def initial_percept(self):

        self.stock_history.append(self.stock)
        self.price = round(200 + self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}

    def do(self, action, time_unit):

        used = select_from_dist({6: 0.1, 5: 0.2, 4: 0.3, 3: 0.2, 2: 0.1, 1: 0.1})
        bought = action['buy']
        self.stock = self.stock + bought - used
        self.stock_history.append(self.stock)

        self.time += 1
        self.price = round(self.price + self.price_delta[self.time % len(self.price_delta)] +
                           self.sd * random.gauss(0, 1))
        self.price_history.append(self.price)
        return {'price': self.price, 'instock': self.stock}


class TP_agent(Displayable):
    def __init__(self, environment):
        self.spent = 0
        percept = environment.initial_percept()
        self.ave = percept['price']
        self.last_price = percept['price']
        self.instock = percept['instock']
        self.buy_history = []

    def select_action(self, percept):

        self.last_price = percept['price']
        self.ave = self.ave + (self.last_price - self.ave) * 0.05
        self.instock = percept['instock']

        if self.last_price < 0.9 * self.ave and self.instock < 60:
            tobuy = 48
        elif self.instock < 12:
            tobuy = 12
        else:
            tobuy = 0

        self.spent += tobuy * self.last_price
        self.buy_history.append(tobuy)
        return {'buy': tobuy}


class Plot_history:
    def __init__(self, environment, agent):
        self.env = environment
        self.agent = agent

    def plot(self):

        plt.figure(figsize=(12, 6))


        plt.subplot(2, 1, 1)
        plt.plot(self.env.price_history, label="Price")
        plt.plot(self.env.stock_history, label="Stock")
        plt.xlabel("Time")
        plt.ylabel("Value")
        plt.legend()
        plt.grid()


        plt.subplot(2, 1, 2)
        plt.bar(range(len(self.agent.buy_history)), self.agent.buy_history, label="Bought")
        plt.xlabel("Time")
        plt.ylabel("Units Bought")
        plt.legend()
        plt.grid()

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    env = TP_env()
    agent = TP_agent(env)
    sim = Simulate(agent, env)

    sim.go(30)


    plot = Plot_history(env, agent)
    plot.plot()
