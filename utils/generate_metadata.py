import json

speeds = [
    0.8,
    1.2,
    1.5,
    2.0,
    2.5,
    3.0,
    3.5,
    4.0,
]

# (angle, max_speed) + allow for floating point precision
angle_speeds = {
    0: 4.01,
    2: 4.01,
    4: 4.01,
    6: 4.01,
    8: 4.01,
    10: 3.01,
    20: 2.01,
    30: 1.51,
}
angle_vals = list(sorted(angle_speeds))
angles = [-x for x in reversed(angle_vals)]
angles.extend(angle_vals[1:])

print(speeds)
print(angles)
print('------')

actions = []

for angle in angles:
    for speed in speeds:
        if speed < angle_speeds[abs(angle)]:
            actions.append({
                'steering_angle': angle,
                'speed': speed,
            })

meta = {'action_space': actions}

out = json.dumps(meta, indent=4)
print(out)
