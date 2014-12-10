__author__ = 'Fritjof'


class Plearner(object):
    """
    Planning/Learning object. Contains the policy and models the update step for planning/learning
    """
    def __init__(self, policy, field, agent):
        self.policy = policy
        self.field = field
        self.agent = agent
        policy.agent = agent
        policy.field = field

    def update(self, old_state, new_state, action, reward):
        pass

    def pick_next_action(self, state):
        return self.policy.pick_next_action(state)