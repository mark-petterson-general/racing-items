class Ref:
    history = {}


def reward_function(params):
    '''
    Reward only for finishing.
    Give more reward if it finished in fewer steps.

    '''

    # Read input parameters
    progress = params['progress']  # percentage
    nsteps = int(params['steps'])  # 1/15 second

    steepness = 20
    reward_amount = 600

    finish_reward = -1.0
    if progress > 99.99:
        finish_reward = steepness * (313 - nsteps) + reward_amount
    # never negative
    return max(0.001, finish_reward)
