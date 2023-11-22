# blend-my-bot

<div align="center">

**Import your robot in Blender and create a nice render of it!**

https://github.com/ami-iit/blend-my-bot/assets/29798643/aa7b130f-0fa4-44cc-844b-eeb1e762af18

</div>

## 🐍 Requirements

- `python3`(<https://wiki.python.org/moin/BeginnersGuide>)
- [Blender](<https://www.blender.org/download/>)
- `iDynTree`(<https://github.com/robotology/idyntree>)
- `numpy`(<https://numpy.org/>)
- `bpy`(<https://pypi.org/project/bpy/>)

Note: This library has been tested with the `appimage` version of Blender 3.6.

## 💾 Installation

Create a conda environment and install the dependencies:

```bash
conda create -n blender_env python=3.10
conda activate blender
```

Create a backup of the python folder in the blender folder

```bash
mv blender_folder/version/python blender_folder/version/python_backup
```

Run the command below in the blender python folder to create a symbolic link to the conda environment in the blender python folder

```bash
sudo ln -s ~/mambaforge/envs/blender blender_folder/version/python
```

From the root of the repository install the package

```bash
pip install -e .
```

If you want to run the scripts from `Visual Studio Code`, you need to install the `vscode python` extension and set the python interpreter to the already created conda environment.

You need an additional vscode extension: `Blender Development` which can be found [here](https://marketplace.visualstudio.com/items?itemName=JacquesLucke.blender-development).

Once installed, you can run Blender by typing `Ctrl+Shift+P` and then `Blender: Start`. It will ask you to select the blender executable. Select the one in the folder where you extracted the blender archive (or the installed version if you installed it). Once Blender is running, you can run the script by typing `Ctrl+Shift+P` and then `Blender: Run Script`.

## 🚀 Usage

TODO

## 🦿 Troubleshooting

If you install a new package in the conda environment but it is not available when you run the script, try to activate it in a terminal **before** and then open `Visual Studio Code` from the terminal:

```bash
conda activate blender_env
code .
```

## 🦸‍♂️ Contributing

`blend-my-bot` is an open-source project. Contributions are very welcome!

Open an issue with your feature request or if you spot a bug. Then, you can also proceed with a Pull-requests! 🚀

## 📝 Tips

Some tips to speed up your Cycle render:
<https://www.youtube.com/watch?v=FNiobzflmpA>

Feel free to add your own tips here!
