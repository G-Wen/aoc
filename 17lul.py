from itertools import accumulate

"""
Part 1: 
Verify that there is an initial horizontal velocity that will stop within the target's x-range.
Search to see if any triangle number lies within the horizontal range of the target component. 
The smallest triangle number is also our lowest possible initial velocity in the x-component.
For my case this was 22. 

Since we did find a case where this is true we now need to find a the maximum vertical velocity
such that the shuttle will at some point land within the y-component of the target space. 

Notice that for each positive initial velocity V we will be at y-position 0 after 2V+1 steps. 
Thus after 2V+2 steps the y-position will be -(V+1), and each further step will be lower. 

For cases where the target is below the horizontal, the largest V we can select that will fall 
into the target's y-range, [lower_y, upper_y], is V=(lower_y+1).

From there calculate the peak reached by the shuttle: T(V = lower_y+1) = (V^2 + V) / 2

Part 2:
Brute force search.
We have found the minimum horizontal velocity, and the maximum vertical velocities in part 1. 
The maximum horizontal velocity is the farthest end of the target's x-range.
Likewise the minimum vertical velocity is the lowest end of the target's y-range.
The maximum number of steps taken is from the path that has the maximum vertical velocity.
This path takes 2V+2 steps as we have calculated before. 

Use these bounds to do a brute force search. 
"""

target_min_x, target_max_x, target_min_y, target_max_y, trajectories = 248, 285, -85, -56, 0
for x in range(22, 285+1):
    for y in range(-85, 84+1):
        trajectory = list(accumulate(((max(x-i, 0), y-i) for i in range(170)), lambda a, b: (a[0] + b[0], a[1] + b[1])))
        if list(filter(lambda pos: target_min_x <= pos[0] <= target_max_x and target_min_y <= pos[1] <= target_max_y, trajectory)):
            trajectories += 1

print(f"Maximum y-position reached: {int(((target_min_y+1)**2 + target_min_y+1)/2)}")
print(f"Number of unique trajectories: {trajectories}")
