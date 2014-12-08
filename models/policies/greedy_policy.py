from models.policies.policy import Policy
import random
import numpy as np


class GreedyPolicy(Policy):
    """
    The greedy policy
    """

    def __init__(self, agent, field, value_init=None, epsilon=.0, gamma=.0, q_value_select=False):
        super(GreedyPolicy, self).__init__(agent, field, value_init)
        self.epsilon = epsilon
        self.gamma = gamma
        self.q_value_select = q_value_select

    def pick_next_action(self, state):
        """
        picks the next action according to a greedy policy:

        In case self.q_value_select is set to True, it picks the highest value
        according to the state and next_action combination.

        In case of a gamma > 0 it picks the next action according to the reward and discounted value
        of the next state

        In case gamma = 0 and q_value_select = False, the highest value given the next state will be picked.

        In case a epsilon of > 0 is given, a random action is chosen with epsilon chance.
        otherwise one of the above happens

        if there are more than 1 choices with equally high values one of them will be picked at random
        :param state: the current state
        :return: the best action for the current state
        """

        if random.random() <= self.epsilon:
            return self.pick_random_action()
        else:
            max_val = -np.inf
            selected_states = []

            for next_action in self.agent.get_actions():
                if self.q_value_select:
                    if max_val < self.value[state, next_action]:
                        selected_states = [(state, next_action)]
                        max_val = self.value[state, next_action]
                    elif max_val == self.value[state, next_action]:
                        selected_states.append((next_state, next_action))

                else:
                    if self.gamma > 0:
                        tmp_val = 0

                    for next_state in self.field.get_next_states(state, next_action):
                        if self.gamma > 0:
                            tmp_prob = self.get_probability(state, next_state, next_action)
                            tmp_rew = self.field.get_reward(next_state) + self.gamma * self.value[next_state]
                            tmp_val += tmp_prob * tmp_rew
                        else:
                            if max_val < self.value[next_state]:
                                selected_states = [(next_state, next_action)]
                                max_val = self.value[next_state]
                            elif max_val == self.value[next_state]:
                                selected_states.append((next_state, next_action))

                    if self.gamma > 0:
                        if max_val < tmp_val:
                            selected_states = [(next_state, next_action)]
                            max_val = self.value[next_state]
                        elif max_val == self.value[next_state]:
                            selected_states.append((next_state, next_action))

                if len(selected_states) == 1:
                    best_state, best_action = selected_states[0]
                elif len(selected_states) > 1:
                    best_state, best_action = random.choice(selected_states)
                else:
                    raise ValueError("no state found")

        if best_action not in self.agent.get_actions():
            raise ValueError("action not in legal actions of agent from State: ", state, ", NextState: ",
                         best_state, ", action: ", best_action)

        return best_action