class Ref:
    history = {}


def reward_function(params):
    '''
    Reward for making more progress, for example by cutting corners.
    For this, the term effective speed has been devised which is computed
    based on the progress percentage and the track length. The effective
    speed is the speed that it would have been expected to travel at to have
    progressed that far around the track.

    The progress reward is then computed as the effective speed, but
    don't reward if any wheels go off-track at any time during
    the previous 20 steps.

    '''

    # Read input parameters
    progress = params['progress']  # percentage
    nsteps = int(params['steps'])  # 1/10 second
    track_length = params['track_length']  # metres
    all_wheels_on_track = params['all_wheels_on_track']

    # Setup history
    history = Ref.history
    if nsteps <= 1:
        history.clear()
    history[nsteps] = {
        'progress': progress,
        'all_wheels_on_track': all_wheels_on_track,
    }

    # Overall scaling
    scaling_wt = 2.0

    # Raise progress to this exponent
    progress_power = 2.0

    # Timestep assumed for progress computations
    steps_per_sec = 15

    # progress reward is effective speed
    # where effective speed is computed by converting the
    # progress into a metres per second value based on the track length
    # initialize a default progress reward of 1.0
    progress_reward = 1.0  # default
    steps_in_history = [i for i in range(nsteps - 20, nsteps)
                        if i in history]
    if any(not history[i]['all_wheels_on_track'] for i in steps_in_history):
        # went off the track
        progress_reward = 0.001
    else:
        if len(steps_in_history) > 16:
            i = steps_in_history[0]
            effective_speed = (
                progress - history[i]['progress']
            ) * track_length / 100 * steps_per_sec / (nsteps - i)
            # normalize so reward is 1.0 for speed of 2.8 m/s
            progress_reward = effective_speed / 2.8
    # never negative
    progress_reward = max(0.001, progress_reward)

    # Non-linear so more progress is rewarded
    return scaling_wt \
        * progress_reward ** progress_power
