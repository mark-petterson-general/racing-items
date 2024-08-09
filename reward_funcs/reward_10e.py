class Ref:
    history = {}


def reward_function(params):
    '''
    Reward for staying close to centre line. Centreline reward
    to have an s-shaped curve based on logistic function.

    Reward for making more progress per step, for example
    by cutting corners, as compared to its progress 10 steps ago,
    but don't reward if it goes off track. Reward per step increases
    in a non-linear upward curve, so that if the track is completed
    faster, and thus uses fewer steps, the reward is greater.

    Reward for greater speed.

    The centre, progress and speed are multiplied together.

    '''

    const_e = 2.718281828

    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    progress = params['progress']  # percentage
    nsteps = int(params['steps'])  # 1/10 second
    track_length = params['track_length']  # metres
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']  # metres per second

    # Setup history
    history = Ref.history
    if nsteps <= 1:
        history.clear()
    history[nsteps] = {
        'progress': progress,
        'all_wheels_on_track': all_wheels_on_track
    }

    # Overall scaling
    scaling_wt = 1.5

    # Raise progress to this exponent
    progress_power = 2.0

    # Raise speed to this exponent
    speed_power = 0.3

    # Logistic function parameters
    # https://en.wikipedia.org/wiki/Logistic_function
    # for following center
    k = 8  # steepness
    zone_width = 0.7  # normalized to track_width so 1.0 is at edge of track

    # logistic function for centerline
    x0 = zone_width * track_width / 2
    centreline_reward = 1 - 1 / (
        1 + const_e ** (k * (x0 - distance_from_center)))
    # never zero
    centreline_reward = max(0.001, centreline_reward)

    # progress in metres per step
    metres_per_step = 0.1 * speed  # default
    steps_in_history = [i for i in range(nsteps - 10, nsteps)
                        if i in history]
    if any(not history[i]['all_wheels_on_track'] for i in steps_in_history):
        # went off the track
        metres_per_step = 0.001
    else:
        for i in steps_in_history:
            metres_per_step = (
                progress - history[i]['progress']
            ) * track_length / 100 / (nsteps - i)
            break
    # never zero
    metres_per_step = max(0.001, metres_per_step)
    # approx reward = 1 at speed of 4 m/s
    progress_per_step_reward = 2.5 * metres_per_step

    # Non-linear so more progress is rewarded
    return scaling_wt * centreline_reward \
        * progress_per_step_reward ** progress_power \
        * speed ** speed_power
