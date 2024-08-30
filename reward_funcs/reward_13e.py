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

    Previous trainings used to compute a decent speed for every waypoint
    so that car can be rewarded for exceeding that speed.

    '''

    reinvent_cw_speeds = {
        "0": 2.0673798018,
        "1": 2.0665704141,
        "2": 2.0800774282,
        "3": 2.0813796084,
        "4": 2.105497588,
        "5": 2.1159897725,
        "6": 2.1299968841,
        "7": 2.1088985027,
        "8": 2.094928791,
        "9": 2.0751947523,
        "10": 2.0823476524,
        "11": 2.0679623069,
        "12": 2.048997604,
        "13": 2.0118434512,
        "14": 1.9732402434,
        "15": 1.9585288158,
        "16": 1.932193012,
        "17": 1.9044962526,
        "18": 1.8424894418,
        "19": 1.7970009611,
        "20": 1.7541250706,
        "21": 1.7044646143,
        "22": 1.6243863138,
        "23": 1.528640055,
        "24": 1.4377747104,
        "25": 1.362353992,
        "26": 1.2929660592,
        "27": 1.2607515191,
        "28": 1.2707430801,
        "29": 1.2991688087,
        "30": 1.3499392569,
        "31": 1.4046758785,
        "32": 1.4554443437,
        "33": 1.4909130545,
        "34": 1.4855915824,
        "35": 1.479675682,
        "36": 1.4815912802,
        "37": 1.4538183188,
        "38": 1.4048416789,
        "39": 1.3193760838,
        "40": 1.253229254,
        "41": 1.2132779684,
        "42": 1.2116162403,
        "43": 1.2620163537,
        "44": 1.3369215397,
        "45": 1.405222388,
        "46": 1.4676750943,
        "47": 1.5237483126,
        "48": 1.5554607051,
        "49": 1.549597376,
        "50": 1.5112279411,
        "51": 1.4601459451,
        "52": 1.4340970595,
        "53": 1.4078808829,
        "54": 1.3934851759,
        "55": 1.4034775628,
        "56": 1.41489778,
        "57": 1.438235262,
        "58": 1.4800163141,
        "59": 1.5323372475,
        "60": 1.5736509585,
        "61": 1.6000317261,
        "62": 1.5851355343,
        "63": 1.560854716,
        "64": 1.5238217605,
        "65": 1.4659507293,
        "66": 1.3782547227,
        "67": 1.2926481761,
        "68": 1.2677318578,
        "69": 1.2814339045,
        "70": 1.3208229356,
        "71": 1.3731487153,
        "72": 1.4314721103,
        "73": 1.4878195656,
        "74": 1.5517164264,
        "75": 1.6290064686,
        "76": 1.7065176033,
        "77": 1.7702394881,
        "78": 1.8363400834,
        "79": 1.8675279036,
        "80": 1.9044989718,
        "81": 1.93087994,
        "82": 1.9484194112,
        "83": 1.9314510622,
        "84": 1.8769943831,
        "85": 1.8181813089,
        "86": 1.725393494,
        "87": 1.5902010671,
        "88": 1.5150348708,
        "89": 1.5011527293,
        "90": 1.524885218,
        "91": 1.5205585469,
        "92": 1.5087888688,
        "93": 1.5151417158,
        "94": 1.5224783507,
        "95": 1.4809213842,
        "96": 1.4234756775,
        "97": 1.3841117855,
        "98": 1.3587211768,
        "99": 1.3494687787,
        "100": 1.3609044126,
        "101": 1.3946503652,
        "102": 1.4497783741,
        "103": 1.5147025569,
        "104": 1.5926264025,
        "105": 1.6751583531,
        "106": 1.7519498909,
        "107": 1.8115947298,
        "108": 1.885019204,
        "109": 1.9547701629,
        "110": 2.0172009672,
        "111": 2.0529650354,
        "112": 2.0549078252
    }

    waypoint_speeds = reinvent_cw_speeds
    # Read input parameters
    progress = params['progress']  # percentage
    nsteps = int(params['steps'])  # 1/10 second
    track_length = params['track_length']  # metres
    all_wheels_on_track = params['all_wheels_on_track']
    waypoint = params['closest_waypoints'][1]  # w[0] behind, w[1] in-front

    # Setup history
    history = Ref.history
    if nsteps <= 1:
        history.clear()
    history[nsteps] = {
        'progress': progress,
        'all_wheels_on_track': all_wheels_on_track,
    }

    # Scaling factor for effective speed
    scale_fact = 4.0

    # If the effective speed is below that from the waypoint list
    # by this margin then reward is zero
    margin = 0.25

    # Timestep assumed for progress computations
    steps_per_sec = 15

    # effective speed is computed by converting the
    # progress into a metres per second value based on the track length
    # initialize a default progress reward of 1.0
    progress_reward = 1.0  # default
    steps_in_history = [i for i in range(nsteps - 20, nsteps)
                        if i in history]
    if any(not history[i]['all_wheels_on_track'] for i in steps_in_history):
        # went off the track
        progress_reward = 0.001
    else:
        if len(steps_in_history) > 18:
            waypoint_speed = waypoint_speeds[str(waypoint)]
            i = steps_in_history[0]
            effective_speed = (
                progress - history[i]['progress']
            ) * track_length / 100 * steps_per_sec / (nsteps - i)
            # Scale the reward to be zero when the effective speed
            # is slower than the waypoint speed by more than the margin.
            # The scale_fact determines the steepness of the slope.
            progress_reward = scale_fact * (
                effective_speed - waypoint_speed + margin)
            # never negative
            progress_reward = max(0.001, progress_reward)

    return progress_reward
