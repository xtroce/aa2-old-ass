from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.policies.random_predator_policy import RandomPredatorPolicy
from models.policies.random_prey_policy import RandomPreyPolicy

def run_iterative_policy_evaluation(verbose=True):
    if verbose:
        print "=== ITERATIVE POLICY EVALUATION ==="
    field = Field(11, 11)
    predator = Predator((0, 0))
    predator.policy = RandomPredatorPolicy(predator, field)
    chip = Prey((5, 5))
    chip.policy = RandomPreyPolicy(chip, field)
    field.add_player(predator)
    field.add_player(chip)

    change_epsilon = 0.001
    discount_factor = 0.8

    all_states = field.get_all_states()

    iterations = iterative_policy_evaluation(field, discount_factor, all_states, change_epsilon)

    value = field.get_predator().policy.value

    print "IPE Iterations: ", iterations
    print "Predator(0,0), Prey(5,5): ", value[((0, 0), (5, 5))]
    print "Predator(2,3), Prey(5,4): ", value[((2, 3), (5, 4))]
    print "Predator(2,10), Prey(10,0): ", value[((2, 10), (10, 0))]
    print "Predator(10,10), Prey(0,0): ", value[((10, 10), (0, 0))]

def iterative_policy_evaluation(field, discount_factor, all_states, change_epsilon = 0.001):
    # Initialise value array and temp array:
    policy = field.get_predator().policy

    iterations = 0
    go_on = True
    while go_on:
        delta_value = 0
        iterations += 1
        for state in all_states:
            temp_value = policy.value[state]
            policy.value[state] = calculate_value(state, field, policy, discount_factor)
            delta_value = max(delta_value, abs(temp_value - policy.value[state]))
        if delta_value < change_epsilon:
            go_on = False
    return iterations

def calculate_value(state, field, policy, discount_factor):
    new_value = 0
    for prob, action in policy.get_probability_mapping(state):
        tmp_v = 0
        for next_state in field.get_next_states(state, action):
            # for next_state in all_states:
            tmp_prob = policy.get_probability(state, next_state, action)
            tmp_rew = field.get_reward(next_state) + discount_factor * policy.value[next_state]
            tmp_v += tmp_prob * tmp_rew
        new_value += prob * tmp_v
    return new_value


if __name__ == '__main__':
    run_iterative_policy_evaluation(verbose=False)
