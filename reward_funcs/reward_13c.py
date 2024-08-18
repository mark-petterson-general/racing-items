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

    ross_raceway_speeds = {
        "0": 2.6364984179,
        "1": 2.637161077,
        "2": 2.6422737611,
        "3": 2.6550014155,
        "4": 2.6756871042,
        "5": 2.6877075652,
        "6": 2.6903692998,
        "7": 2.6901927863,
        "8": 2.6857186725,
        "9": 2.6399676473,
        "10": 2.6264947993,
        "11": 2.6140688005,
        "12": 2.6025159588,
        "13": 2.5744549686,
        "14": 2.5210759743,
        "15": 2.4492826921,
        "16": 2.3699961472,
        "17": 2.2873976423,
        "18": 2.2334689107,
        "19": 2.1892515899,
        "20": 2.1684425905,
        "21": 2.1671728872,
        "22": 2.1733192677,
        "23": 2.1902990623,
        "24": 2.2210844232,
        "25": 2.2630566854,
        "26": 2.3160506834,
        "27": 2.3774298703,
        "28": 2.4378139788,
        "29": 2.4961431734,
        "30": 2.5460333813,
        "31": 2.5785936171,
        "32": 2.5928352498,
        "33": 2.598671694,
        "34": 2.6435354866,
        "35": 2.6553840031,
        "36": 2.6733589428,
        "37": 2.6890327744,
        "38": 2.6769048225,
        "39": 2.6482025158,
        "40": 2.6247075556,
        "41": 2.597968289,
        "42": 2.582996555,
        "43": 2.5692669217,
        "44": 2.5605585314,
        "45": 2.5327414913,
        "46": 2.4793284219,
        "47": 2.4220035562,
        "48": 2.3525475385,
        "49": 2.2823062757,
        "50": 2.1959780186,
        "51": 2.0987909234,
        "52": 2.0000627519,
        "53": 1.9124304054,
        "54": 1.8459456028,
        "55": 1.8101168387,
        "56": 1.8133117169,
        "57": 1.8540347524,
        "58": 1.9022886052,
        "59": 1.9736484113,
        "60": 2.05088696,
        "61": 2.113266846,
        "62": 2.1766026303,
        "63": 2.2292015913,
        "64": 2.2853654057,
        "65": 2.3351315374,
        "66": 2.3528116887,
        "67": 2.3390526226,
        "68": 2.2899134041,
        "69": 2.2022567131,
        "70": 2.095336872,
        "71": 1.9950653266,
        "72": 1.9053955982,
        "73": 1.7982642599,
        "74": 1.7177458077,
        "75": 1.6586223256,
        "76": 1.6377434736,
        "77": 1.6505303693,
        "78": 1.6698798819,
        "79": 1.7049443505,
        "80": 1.7570649924,
        "81": 1.8039671966,
        "82": 1.8613648873,
        "83": 1.9265088797,
        "84": 1.9745952675,
        "85": 2.030023433,
        "86": 2.093920043,
        "87": 2.1521307062,
        "88": 2.2269623747,
        "89": 2.2896575127,
        "90": 2.3446004534,
        "91": 2.3872549547,
        "92": 2.4100329784,
        "93": 2.4134370625,
        "94": 2.4360778764,
        "95": 2.4341951346,
        "96": 2.4158433856,
        "97": 2.3673528283,
        "98": 2.2809770983,
        "99": 2.1694560451,
        "100": 2.0578144622,
        "101": 1.9727977071,
        "102": 1.8991134873,
        "103": 1.8424257852,
        "104": 1.8142064344,
        "105": 1.8051292782,
        "106": 1.8216641107,
        "107": 1.8439531421,
        "108": 1.8613888915,
        "109": 1.9020264689,
        "110": 1.9534327978,
        "111": 2.0215534498,
        "112": 2.0827327652,
        "113": 2.1456553799,
        "114": 2.2116404792,
        "115": 2.2717606195,
        "116": 2.3254728013,
        "117": 2.3723904757,
        "118": 2.4427129773,
        "119": 2.4988441838,
        "120": 2.5516248666,
        "121": 2.601547805,
        "122": 2.6335788533,
        "123": 2.6596399697,
        "124": 2.6633207201,
        "125": 2.6774159167,
        "126": 2.6803200634,
        "127": 2.7142991784,
        "128": 2.7236504773,
        "129": 2.7220678666,
        "130": 2.7047774461,
        "131": 2.6685297932,
        "132": 2.6447420412,
        "133": 2.624419124,
        "134": 2.5927544432,
        "135": 2.5598146036,
        "136": 2.5001886286,
        "137": 2.4194867727,
        "138": 2.3183745182,
        "139": 2.2332466371,
        "140": 2.1653388818,
        "141": 2.1317085032,
        "142": 2.1042897648,
        "143": 2.1101667114,
        "144": 2.1313706092,
        "145": 2.1602076656,
        "146": 2.2081076259,
        "147": 2.2489812259,
        "148": 2.2999655701,
        "149": 2.3753784471,
        "150": 2.4475057923,
        "151": 2.5130539643,
        "152": 2.5677369158,
        "153": 2.6133822371,
        "154": 2.6320725526,
        "155": 2.6506730139
    }

    waypoint_speeds = ross_raceway_speeds
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
        if len(steps_in_history) > 0:
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
