# Discrete Radon Transform
This is the raelization of discrete radon transform algorithm for straight lines detection
The `Discrete_Radon_Transform.py` contains class `Discrete_Radon_Transform`, which has input parametrs:
1. `path_to_picture: str`
2. `angle_acc=500` than it is bigger than the angle step less (more accurate)
3. `shift_acc=500` than it is bigger than the shift step less (more accurate)

The result matrix provides method `get_transform`. 
Method `display_result` draws heatmap of the transform result.