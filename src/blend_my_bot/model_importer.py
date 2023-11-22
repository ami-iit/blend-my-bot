from dataclasses import dataclass
from typing import List
import bpy
import idyntree.bindings as idyntree
import numpy as np

from blend_my_bot import Link, BlenderModel


@dataclass
class ModelImporter:
    @staticmethod
    def build_model(
        model_name: str, urdf_path: str, joints_list: List = None
    ) -> BlenderModel:
        """Build the model of the robot in blender

        Args:
            model_name (str): Name of the model
            urdf_path (str): Path to the urdf file
            joints_list (List, optional): List of joints to import. Defaults to None.

        Returns:
            BlenderModel: Model of the robot in blender
        """

        kindyn = ModelImporter.build_kindyn(urdf_path, joints_list)
        model_loader_geometry = idyntree.ModelLoader()
        model_loader_geometry.loadModelFromFile(urdf_path)
        model_geometry = model_loader_geometry.model().copy()
        links = ModelImporter.import_links(model_name, model_geometry, kindyn)
        return BlenderModel(
            name=model_name, links=links, kindyn=kindyn, model_geometry=model_geometry
        )

    @staticmethod
    def build_kindyn(urdf_path: str, joints_list: List = None):
        """Build the kindyn model

        Args:
            urdf_path (str): Path to the urdf file
            joints_list (List, optional): List of joints to import. Defaults to None.

        Returns:
            idyntree.KinDynComputations: Kindyn model
        """

        model_loader = idyntree.ModelLoader()
        if joints_list is None:
            model_loader.loadModelFromFile(urdf_path)
        else:
            model_loader.loadReducedModelFromFile(urdf_path, joints_list)
        model = model_loader.model()
        kindyn = idyntree.KinDynComputations()
        kindyn.loadRobotModel(model)
        return kindyn

    @staticmethod
    def import_links(
        model_name: str,
        model_geometry: idyntree.Model,
        kindyn: idyntree.KinDynComputations,
    ) -> List[Link]:
        """Import the links of the robot in blender

        Args:
            model_name (str): Name of the model
            model_geometry (idyntree.Model): Model of the robot
            kindyn (idyntree.KinDynComputations): Kindyn model

        Returns:
            List[Link]: List of links
        """

        visuals = model_geometry.visualSolidShapes().getLinkSolidShapes()
        links = {}
        existing_objects = bpy.context.scene.objects.keys()
        # set zero position
        kindyn.setRobotState(
            np.eye(4),
            np.zeros(kindyn.getNrOfDegreesOfFreedom()),
            np.zeros(6),
            np.zeros(kindyn.getNrOfDegreesOfFreedom()),
            np.zeros(3),
        )
        for link_id in range(model_geometry.getNrOfLinks()):
            link_name = model_geometry.getLinkName(link_id)
            link_visual = visuals[link_id][0]
            if link_visual.isExternalMesh():
                mesh_path = (
                    link_visual.asExternalMesh().getFileLocationOnLocalFileSystem()
                )
                print(f"mesh_path {mesh_path}")
                mesh_name = f"{model_name}_{link_name}_mesh"
                if mesh_name in existing_objects:
                    print(f"Using existing mesh {mesh_name}")
                    mesh = bpy.data.objects[mesh_name]
                elif mesh_path.endswith(".obj"):
                    print(f"Importing {mesh_path}")
                    bpy.ops.import_scene.obj(filepath=mesh_path)
                    mesh = bpy.context.selected_objects[0]
                elif mesh_path.endswith(".stl"):
                    print(f"Importing {mesh_path}")
                    bpy.ops.import_mesh.stl(filepath=mesh_path)
                    mesh = bpy.context.selected_objects[0]
                else:
                    raise ValueError(
                        f"Extension {mesh_path.split('.')[-1]} not supported"
                    )
                mesh.name = mesh_name
                mesh.scale = link_visual.asExternalMesh().getScale().toNumPy().flatten()
                mesh.rotation_mode = "QUATERNION"
                l_H_g = link_visual.getLink_H_geometry()
                # set link pose to rest position
                w_H_l = kindyn.getWorldTransform(link_name)
                w_H_g = w_H_l * l_H_g
                mesh.location = w_H_g.getPosition()
                mesh.rotation_quaternion = w_H_g.getRotation().asQuaternion()
                links[link_name] = Link(link_name, mesh, l_H_g)
        return links
