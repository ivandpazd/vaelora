"""Master camera, lighting, rendering and manifest helpers for Vaelora v0.3."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable

import bpy
from mathutils import Vector

from vaelora_style import (
    ART_STYLE_ID,
    CAMERA_ELEVATION_DEG,
    CAMERA_FRAME_Z_OFFSET,
    CAMERA_ORTHO_CITY,
    CAMERA_ORTHO_TERRAIN,
    CAMERA_ORTHO_UNIT,
    CAMERA_TARGET_Z,
    CAMERA_YAW_DEG,
    CANVAS,
    GENERATOR_VERSION,
    MANIFEST_SCHEMA_VERSION,
    PRODUCTION_BLENDER_VERSION,
    SUPPORTED_BLENDER_MIN,
)

SCRIPT_DIR = Path(__file__).resolve().parent


def reset_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for datablocks in (bpy.data.meshes, bpy.data.curves, bpy.data.cameras, bpy.data.lights):
        for block in list(datablocks):
            if block.users == 0:
                datablocks.remove(block)


def assert_blender_version(strict: bool = False) -> dict[str, Any]:
    current = tuple(bpy.app.version[:3])
    if current < SUPPORTED_BLENDER_MIN:
        raise RuntimeError(f"Vaelora v0.3.2-r2 requires Blender >= {SUPPORTED_BLENDER_MIN}, got {current}")
    exact = current == PRODUCTION_BLENDER_VERSION
    if strict and not exact:
        raise RuntimeError(
            f"Accepted Vaelora v0.3.2-r2 production renders require Blender {PRODUCTION_BLENDER_VERSION}; got {current}."
        )
    if not exact:
        print(f"[Vaelora] WARNING: review-only render. Production pin is {PRODUCTION_BLENDER_VERSION}; current is {current}.")
    return {"current": current, "production_pin": PRODUCTION_BLENDER_VERSION, "production_exact": exact}


def _look_at(obj: bpy.types.Object, target: Vector) -> None:
    obj.rotation_euler = (target - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup_master_camera(family: str = "terrain") -> bpy.types.Object:
    ortho = {
        "terrain": CAMERA_ORTHO_TERRAIN,
        "overlay": CAMERA_ORTHO_TERRAIN,
        "hero_prop": CAMERA_ORTHO_TERRAIN,
        "city": CAMERA_ORTHO_CITY,
        "unit": CAMERA_ORTHO_UNIT,
    }[family]
    yaw = math.radians(CAMERA_YAW_DEG)
    elevation = math.radians(CAMERA_ELEVATION_DEG)
    distance = 9.0
    horizontal = math.cos(elevation) * distance
    location = Vector((math.cos(yaw) * horizontal, math.sin(yaw) * horizontal, math.sin(elevation) * distance))
    frame_z_offset = CAMERA_FRAME_Z_OFFSET[family]
    location.z += frame_z_offset
    data = bpy.data.cameras.new("VAELORA_MasterCamera")
    data.type = "ORTHO"
    data.ortho_scale = ortho
    camera = bpy.data.objects.new("VAELORA_MasterCamera", data)
    bpy.context.collection.objects.link(camera)
    camera.location = location
    _look_at(camera, Vector((0.0, 0.0, CAMERA_TARGET_Z[family] + frame_z_offset)))
    bpy.context.scene.camera = camera
    return camera


def setup_lighting() -> list[bpy.types.Object]:
    """Create the single canonical luminous-fantasy rig used by sprite renders."""
    result: list[bpy.types.Object] = []

    key_data = bpy.data.lights.new("VAELORA_Key", type="AREA")
    key_data.energy = 890.0
    key_data.shape = "DISK"
    key_data.size = 5.5
    key_data.color = (1.0, 0.83, 0.64)
    key = bpy.data.objects.new("VAELORA_Key", key_data)
    bpy.context.collection.objects.link(key)
    key.location = (4.8, -5.4, 8.4)
    _look_at(key, Vector((0, 0, 0.25)))
    result.append(key)

    fill_data = bpy.data.lights.new("VAELORA_Fill", type="AREA")
    fill_data.energy = 245.0
    fill_data.size = 7.0
    fill_data.color = (0.63, 0.76, 0.88)
    fill = bpy.data.objects.new("VAELORA_Fill", fill_data)
    bpy.context.collection.objects.link(fill)
    fill.location = (-4.5, 4.0, 5.5)
    _look_at(fill, Vector((0, 0, 0.5)))
    result.append(fill)

    rim_data = bpy.data.lights.new("VAELORA_Rim", type="AREA")
    rim_data.energy = 110.0
    rim_data.size = 4.0
    rim_data.color = (0.72, 0.83, 0.93)
    rim = bpy.data.objects.new("VAELORA_Rim", rim_data)
    bpy.context.collection.objects.link(rim)
    rim.location = (-3.2, -4.5, 6.8)
    _look_at(rim, Vector((0, 0, 0.8)))
    result.append(rim)

    world = bpy.context.scene.world or bpy.data.worlds.new("VAELORA_World")
    bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value = (0.30, 0.37, 0.41, 1.0)
        bg.inputs["Strength"].default_value = 0.36
    return result


def configure_render(family: str, output_path: Path, transparent: bool = True) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    work_w, work_h = CANVAS[family]["work"]
    scene.render.resolution_x = work_w
    scene.render.resolution_y = work_h
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = transparent
    # Render supersampled and let host-side Lanczos do the final reduction.
    scene.render.filter_size = 0.90
    scene.render.filepath = str(output_path)
    scene.view_settings.view_transform = "AgX"
    try:
        look_items = {item.identifier for item in scene.view_settings.bl_rna.properties["look"].enum_items}
    except Exception:
        look_items = set()
    for candidate in ("AgX - Medium High Contrast", "Medium High Contrast"):
        if candidate in look_items:
            scene.view_settings.look = candidate
            break
    scene.view_settings.exposure = 0.12
    scene.view_settings.gamma = 1.0


def render_png(family: str, output_path: Path, transparent: bool = True) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    configure_render(family, output_path, transparent)
    bpy.ops.render.render(write_still=True)
    return output_path


def save_blend(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    bpy.ops.wm.save_as_mainfile(filepath=str(path))
    return path


def object_statistics() -> dict[str, int]:
    meshes = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    triangles = 0
    vertices = 0
    for obj in meshes:
        vertices += len(obj.data.vertices)
        triangles += sum(max(1, len(poly.vertices) - 2) for poly in obj.data.polygons)
    return {"objects": len(meshes), "vertices": vertices, "triangles_estimate": triangles}


def world_bounds() -> dict[str, list[float]] | None:
    points: list[Vector] = []
    for obj in bpy.context.scene.objects:
        if obj.type not in {"MESH", "CURVE"}:
            continue
        points.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)
    if not points:
        return None
    return {
        "min": [min(p[i] for p in points) for i in range(3)],
        "max": [max(p[i] for p in points) for i in range(3)],
    }


def _sha256(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def source_hashes(source_script: str, dependencies: Iterable[str] = ()) -> dict[str, str]:
    names = [source_script, "vaelora_style.py", "vaelora_contract.py", "vaelora_composition.py", "vaelora_geometry.py", "vaelora_materials.py", "vaelora_render.py", *dependencies]
    result: dict[str, str] = {}
    for name in dict.fromkeys(names):
        digest = _sha256(SCRIPT_DIR / name)
        if digest:
            result[name] = digest
    return result


def write_manifest(
    path: Path,
    *,
    asset_id: str,
    seed: int,
    family: str,
    source_script: str,
    dependencies: Iterable[str] = (),
    lifecycle_state: str = "benchmark",
    extra: dict[str, Any] | None = None,
) -> Path:
    payload: dict[str, Any] = {
        "manifest_schema": MANIFEST_SCHEMA_VERSION,
        "asset_id": asset_id,
        "art_style_id": ART_STYLE_ID,
        "generator_version": GENERATOR_VERSION,
        "lifecycle_state": lifecycle_state,
        "seed": seed,
        "family": family,
        "source_script": source_script,
        "source_sha256": source_hashes(source_script, dependencies),
        "blender_version": list(bpy.app.version[:3]),
        "production_blender_pin": list(PRODUCTION_BLENDER_VERSION),
        "renderer": "BLENDER_EEVEE",
        "color_management": {"view_transform": "AgX", "exposure": 0.12, "gamma": 1.0},
        "camera": {
            "projection": "orthographic",
            "yaw_deg": CAMERA_YAW_DEG,
            "elevation_deg": CAMERA_ELEVATION_DEG,
            "target_z": CAMERA_TARGET_Z[family],
            "frame_z_offset": CAMERA_FRAME_Z_OFFSET[family],
        },
        "canvas": CANVAS[family],
        "provenance": "internally generated from Vaelora procedural source; no external models or image textures",
        "statistics": object_statistics(),
        "world_bounds": world_bounds(),
        "acceptance_state": "rendered_review_only",
    }
    if extra:
        payload.update(extra)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return path
