class Ref:
    history = {}


def reward_function(params):
    '''
    Reward for staying close to centre line. Centreline reward
    to have an s-shaped curve based on logistic function.

    Reward for making more progress, for example by cutting corners.
    For this, the term effective speed has been devised which is computed
    based on the progress percentage and the track length. The effective
    speed is the speed that it would have been expected to travel at to have
    progressed that far around the track. This is compared to the actual
    average of all the speeds over the last 10 steps.

    The progress reward is then computed as the effective speed divided
    by the actual average speed, but don't reward if any wheels go
    off-track at any time during the previous 10 steps.

    Reward for greater speed, but apply a non-linear curve to adjust
    how much effect speed has on the reward.

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
        'all_wheels_on_track': all_wheels_on_track,
        'speed': speed
    }

    # Overall scaling
    scaling_wt = 2.0

    # Raise progress to this exponent
    progress_power = 1.2

    # Raise speed to this exponent
    speed_power = 0.8

    # Timestep assumed for progress computations
    steps_per_sec = 6

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

    # progress reward is effective speed / actual average speed
    # where effective speed is computed by converting the
    # progress into a metres per second value based on the track length
    # initialize a default progress reward of 1.0
    progress_reward = 1.0  # default
    steps_in_history = [i for i in range(nsteps - 10, nsteps)
                        if i in history]
    if any(not history[i]['all_wheels_on_track'] for i in steps_in_history):
        # went off the track
        progress_reward = 0.001
    else:
        if len(steps_in_history) > 0:
            avg_speed = sum(history[i]['speed'] for i in steps_in_history) \
                    / len(steps_in_history)
            i = steps_in_history[0]
            effective_speed = (
                progress - history[i]['progress']
            ) * track_length / 100 * steps_per_sec / (nsteps - i)
            progress_reward = effective_speed / avg_speed
    # never zero
    progress_reward = max(0.001, progress_reward)

    # Non-linear so more progress is rewarded
    return scaling_wt * centreline_reward \
        * progress_reward ** progress_power \
        * (speed / 3.5) ** speed_power
