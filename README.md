# Blend My Bot

<div align="center">

**Import your robot in Blender and create a nice render of it!**

https://github.com/ami-iit/blend-my-bot/assets/29798643/c224cd56-1d90-42dd-aec5-960a13690ce7

</div>

## 🐍 Requirements

- [`python3`](<https://wiki.python.org/moin/BeginnersGuide>)
- [`Blender`](<https://www.blender.org/download/>)
- [`iDynTree`](<https://github.com/robotology/idyntree>)
- [`numpy`](<https://numpy.org/>)
- [`bpy`](<https://pypi.org/project/bpy/>)

Note: This library has been tested with the `appimage` version of Blender 3.6. You should use a Python version that matches the one supported by the Blender version.

Note 2: This library does not define the rig of the robot. For this, you can use a library such as [`blender-robotics-utils`](https://github.com/robotology/blender-robotics-utils).

## 💾 Installation

Create a conda environment and install the dependencies:

```bash
conda create -n blender_env python=3.10
conda activate blender_env
```

Create a backup of the python folder in the blender folder:

```bash
mv blender_folder/version/python blender_folder/version/python_backup
```

Run the command below in the blender python folder to create a symbolic link to the conda environment in the blender python folder:

```bash
sudo ln -s ~/mambaforge/envs/blender_env blender_folder/version/python
```

From the root of the repository install the package:

```bash
pip install blend-my-bot
```

If you want to run the scripts from `Visual Studio Code`, you need to install the `vscode python` extension and set the python interpreter to the already created conda environment.

You need an additional vscode extension: `Blender Development` which can be found [here](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).

Once installed, you can run Blender by typing `Ctrl+Shift+P` and then `Blender: Start`. It will ask you to select the blender executable: select the one in the folder where you extracted the blender archive (or the installed version if you installed it). Once Blender is running, you can run the script by typing `Ctrl+Shift+P` and then `Blender: Run Script`.

You can add objects, lights, and cameras as well as play with render parameters directly in Blender.
If you prefer, you can save the Blender project. Everything will be there, including the robot and its motion, so that it does not need to run your script again.

Note that you could also write a script directly in the `Scripting` tab of Blender and run it from there.

For possible issues when running the script see the [Troubleshooting](#troubleshooting) section.

## 🚀 Usage

```python
# import the library
from blend_my_bot import ModelImporter
# import the blender python API
import bpy

# ModelImporter needs 3 arguments:
# - the name you want to give to your robot
# - the path to the urdf file
# - the list of the joints you want to move in the animation

urdf_path = "path/to/urdf"
robot_name = "my_robot"
joints_list = ["joint1", "joint2", "joint3", "etc"]

# build the blender robot model
model = ModelImporter.build_model(robot_name, urdf_path, joints_list)

# you need to set the frame rate and the number of frames of the animation
# length of the animation in seconds
bpy.context.scene.render.fps_base = time_length
# number of frames
bpy.context.scene.render.fps = number_of_frames
# when the animation starts
bpy.context.scene.frame_start = 0
# when the animation ends
bpy.context.scene.frame_end = number_of_frames

# in Blender the effective frame rate is fps / fps_base

# you can now move the base and the joints of the robot
for k in range(number_of_frames):
    # jet the joint trajectory at time k
    s = joint_trajectory[k]
    # get the base pose described by a 4x4 homogeneous matrix at time k
    w_H_b = base_trajectory[k]
    # update the robot model
    model.update(w_H_b, s)
    # set the frame
    bpy.context.scene.frame_set(k)
```

Have a look at the `examples` folder for more examples.

In the `examples/jumping` folder you can find a script that generates a jumping animation of the `iCub` robot. Here the meshes are in a gray, `stl` format.

Having the meshes in an `obj` format, instead, will give a nicer and more colorful render! See the Readme of the following repository, for example!

[Whole-Body Trajectory Optimization for Robot Multimodal Locomotion](<https://github.com/ami-iit/paper_lerario_2022_humanoids_planning-multimodal-locomotion>)

## 🦿 Troubleshooting

If you install a new package in the conda environment but it is not working as you expect when you run the script, try to activate it in a terminal **before** and then open `Visual Studio Code` from the terminal:

```bash
conda activate blender_env
code .
```

For example, when using [`resolve_robotics_uri_py`](https://github.com/ami-iit/resolve-robotics-uri-py) an error like the following one appears:

```
FileNotFoundError: resolve-robotics-uri-py: No file corresponding to uri "package://iCub/robots/iCubGazeboV2_7/model.urdf" found
```

This is due to the fact that environmental variables are not sourced. Activating the conda environment before opening `vscode` solves this issue!

## 🦸‍♂️ Contributing

`blend-my-bot` is an open-source project. Contributions are very welcome!

Open an issue with your feature request or if you spot a bug. Then, you can also proceed with a Pull-requests! 🚀

## 📝 Tips

Some tips to speed up your Cycle render:
<https://www.youtube.com/watch?v=FNiobzflmpA>

Feel free to add your own tips here!
