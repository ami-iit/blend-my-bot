from dataclasses import dataclass

import bpy
import idyntree.bindings as idyntree


@dataclass
class Link:
    name: str
    mesh: bpy.types.Object
    link_H_geometry: idyntree.Transform
