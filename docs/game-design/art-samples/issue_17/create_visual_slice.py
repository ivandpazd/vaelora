"""Build a faceted, painterly 2.5D Vaelora visual-direction study in Blender.

The scene uses shallow dimetric terrain relief and deliberately simplified
low-poly forms with restrained pigment texture. It is an original style study,
not a recreation of another game's assets. All outputs remain unaccepted
candidates under documentation samples, outside the runtime asset directory.
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import bpy
from mathutils import Vector


OUTPUT = Path(__file__).resolve().parent
PALETTE = {
    "meadow": "#87966B", "meadow_light": "#A7A67A", "plains": "#77845C",
    "plains_light": "#9D9970", "forest": "#435A45", "forest_mid": "#62764F",
    "forest_light": "#87906A", "hill": "#8D8060", "hill_light": "#B0A078",
    "mountain": "#707A78", "mountain_light": "#A0A196", "mountain_dark": "#4F5C5B",
    "snow": "#E2DFD2", "snow_shadow": "#C1C5B9", "coast": "#C3AA7A",
    "wet_sand": "#9C9D7D", "shallow": "#71958F", "sea": "#426E7D",
    "foam": "#B6C2AC", "soil": "#62503E", "stone": "#C8B99A",
    "stone_shadow": "#918876", "slate": "#45586A", "gold": "#D5A447",
    "ivory": "#E8DFC9", "blue": "#345C78", "blue_light": "#7190A0",
    "timber": "#76543D", "timber_light": "#A77B51", "iron": "#4B5353",
    "iron_light": "#A2A193", "ember": "#A8493E", "copper": "#BC7947",
    "moss": "#68775B", "hide": "#88684F", "skin": "#A87556",
    "skin_orc": "#75816A", "paper": "#D8D3C3", "shadow": "#303B36",
}
MATERIALS: dict[str, bpy.types.Material] = {}


def color(hex_value: str) -> tuple[float, float, float, float]:
    values = [int(hex_value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in values]
    return linear[0], linear[1], linear[2], 1


def material(name: str, swatch: str, texture: float = .0) -> bpy.types.Material:
    key = f"{name}:{swatch}:{texture}"
    if key in MATERIALS:
        return MATERIALS[key]
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = color(swatch)
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    shader = nodes.new("ShaderNodeBsdfPrincipled")
    shader.inputs["Roughness"].default_value = .88
    shader.inputs["Metallic"].default_value = 0
    base = color(swatch)
    if texture:
        texcoord = nodes.new("ShaderNodeTexCoord")
        noise = nodes.new("ShaderNodeTexNoise")
        noise.inputs["Scale"].default_value = 5.5
        noise.inputs["Detail"].default_value = 2.0
        noise.inputs["Roughness"].default_value = .72
        ramp = nodes.new("ShaderNodeValToRGB")
        ramp.color_ramp.elements[0].position = .28
        ramp.color_ramp.elements[0].color = (base[0] * (1-texture), base[1] * (1-texture), base[2] * (1-texture), 1)
        ramp.color_ramp.elements[1].position = .72
        ramp.color_ramp.elements[1].color = (min(1, base[0] * (1+texture)), min(1, base[1] * (1+texture)), min(1, base[2] * (1+texture)), 1)
        links.new(texcoord.outputs["Generated"], noise.inputs["Vector"])
        links.new(noise.outputs["Fac"], ramp.inputs["Fac"])
        links.new(ramp.outputs["Color"], shader.inputs["Base Color"])
        bump = nodes.new("ShaderNodeBump")
        bump.inputs["Strength"].default_value = .12
        bump.inputs["Distance"].default_value = .035
        links.new(noise.outputs["Fac"], bump.inputs["Height"])
        links.new(bump.outputs["Normal"], shader.inputs["Normal"])
    else:
        shader.inputs["Base Color"].default_value = base
    links.new(shader.outputs["BSDF"], output.inputs["Surface"])
    MATERIALS[key] = mat
    return mat


def mesh_object(name: str, vertices: list[tuple[float, float, float]],
                faces: list[tuple[int, ...]], swatch: str, texture: float = .0,
                smooth: bool = False) -> bpy.types.Object:
    mesh = bpy.data.meshes.new(f"{name} mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.materials.append(material(name, swatch, texture))
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    if not smooth:
        for face in mesh.polygons:
            face.use_smooth = False
    return obj


def prism(name: str, outline: list[tuple[float, float]], z: float,
          depth: float, swatch: str, texture: float = .0) -> bpy.types.Object:
    count = len(outline)
    vertices = [(x, y, z) for x, y in outline] + [(x, y, z-depth) for x, y in outline]
    faces: list[tuple[int, ...]] = [tuple(range(count)), tuple(range(count, count*2))]
    faces += [(i, (i+1) % count, (i+1) % count + count, i+count) for i in range(count)]
    return mesh_object(name, vertices, faces, swatch, texture)


def ico(name: str, location: tuple[float, float, float], scale: tuple[float, float, float],
        swatch: str, subdivisions: int = 1, texture: float = .0) -> bpy.types.Object:
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=subdivisions, radius=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale = scale
    obj.data.materials.append(material(name, swatch, texture))
    for face in obj.data.polygons:
        face.use_smooth = False
    return obj


def cone(name: str, location: tuple[float, float, float], radius: float, depth: float,
         swatch: str, vertices: int = 7) -> bpy.types.Object:
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=0, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material(name, swatch, .035))
    for face in obj.data.polygons:
        face.use_smooth = False
    return obj


def beam(name: str, start: tuple[float, float, float], end: tuple[float, float, float],
         radius: float, swatch: str, vertices: int = 5) -> bpy.types.Object:
    delta = Vector(end) - Vector(start)
    middle = (Vector(start) + Vector(end)) / 2
    bpy.ops.mesh.primitive_cone_add(vertices=vertices, radius1=radius, radius2=radius*.82,
                                    depth=delta.length, location=middle)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler = delta.to_track_quat("Z", "Y").to_euler()
    obj.data.materials.append(material(name, swatch, .025))
    for face in obj.data.polygons:
        face.use_smooth = False
    return obj


def clear_scene() -> None:
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    MATERIALS.clear()


def aim(obj: bpy.types.Object, point: tuple[float, float, float]) -> None:
    obj.rotation_euler = (Vector(point) - obj.location).to_track_quat("-Z", "Y").to_euler()


def setup(width: int, height: int, transparent: bool, ortho: float,
          target: tuple[float, float, float] = (0, 0, 0)) -> None:
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x, scene.render.resolution_y = width, height
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA" if transparent else "RGB"
    scene.render.image_settings.color_depth = "8"
    scene.render.film_transparent = transparent
    scene.render.image_settings.color_management = "FOLLOW_SCENE"
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.camera = None
    camera_data = bpy.data.cameras.new("Fixed 2:1 dimetric camera")
    camera_data.type = "ORTHO"
    camera_data.ortho_scale = ortho
    camera = bpy.data.objects.new("Fixed dimetric camera", camera_data)
    bpy.context.collection.objects.link(camera)
    # A deliberately low dimetric angle keeps top faces readable without the
    # steep tabletop/minature-diorama perspective of the earlier study.
    camera.location = (8, -8, 8)
    aim(camera, target)
    scene.camera = camera
    scene.world.color = color("#A9A595")[:3]
    scene.render.image_settings.file_format = "PNG"
    key_data = bpy.data.lights.new("Large soft painterly key", "AREA")
    key_data.energy = 1750
    key_data.shape = "DISK"
    key_data.size = 9
    key = bpy.data.objects.new("Large soft painterly key", key_data)
    bpy.context.collection.objects.link(key)
    key.location = (-5, -7, 12)
    aim(key, target)
    fill_data = bpy.data.lights.new("Soft sky fill", "AREA")
    fill_data.energy = 650
    fill_data.size = 10
    fill = bpy.data.objects.new("Soft sky fill", fill_data)
    bpy.context.collection.objects.link(fill)
    fill.location = (5, 4, 9)
    aim(fill, target)
    scene.render.filepath = str(OUTPUT / "render.png")


def render(path: Path) -> None:
    bpy.context.scene.render.filepath = str(path)
    bpy.ops.render.render(write_still=True)


def tile_base(kind: str, origin: tuple[float, float], seed: int) -> None:
    rng = random.Random(seed)
    ground = {
        "meadow": PALETTE["meadow"], "plains": PALETTE["plains"], "forest": PALETTE["forest"],
        "hills": PALETTE["hill"], "mountain": PALETTE["mountain"], "peak": PALETTE["mountain_dark"],
        "coast": PALETTE["shallow"], "shallow_sea": PALETTE["shallow"], "open_sea": PALETTE["sea"],
    }[kind]
    x, y = origin
    # Thin flat-top hex cell: shallow sides read as terrain, not a display plinth.
    outline = [(x-1,y,0),(x-.5,y+.866,0),(x+.5,y+.866,0),
               (x+1,y,0),(x+.5,y-.866,0),(x-.5,y-.866,0)]
    verts = outline + [(px,py,-.045) for px,py,_ in outline]
    faces = [(0,1,2,3,4,5),(6,11,10,9,8,7)] + [(i,(i+1)%6,(i+1)%6+6,i+6) for i in range(6)]
    mesh_object(f"{kind.title()} thin terrain tile", verts, faces, ground, .07)
    accents = {
        "meadow": ["#9EAA75", "#AAA77B"], "plains": ["#89916A", "#A39C72"],
        "forest": ["#536A4B", "#66764F"], "hills": ["#A2966F", "#9C8A66"],
        "mountain": ["#8B928B", "#808A82"], "peak": ["#64716E", "#78817A"],
        "coast": ["#8CA49A", "#9AAB9E"], "shallow_sea": ["#85A49A", "#789C97"],
        "open_sea": ["#527D86", "#4B7480"],
    }[kind]
    for index in range(14):
        px, py = x+rng.uniform(-.72,.72), y+rng.uniform(-.34,.34)
        if abs(px-x) + 2*abs(py-y) > .96:
            continue
        dab = ico(f"{kind.title()} painterly ground dab {index}", (px,py,.025+index*.001),
                  (rng.uniform(.05,.18),rng.uniform(.025,.07),.012), rng.choice(accents), 1, .02)
        dab.rotation_euler[2] = rng.uniform(-.5,.5)


def tree(origin: tuple[float, float], x: float, y: float, size: float,
         rng: random.Random, index: int) -> None:
    ox, oy = origin
    beam(f"Tree {index} faceted trunk", (ox+x,oy+y,.02), (ox+x+.02,oy+y,size*.48), size*.065, "#67523D")
    for layer, (height, radius, swatch) in enumerate(((.42,.34,PALETTE["forest"]),(.65,.29,PALETTE["forest_mid"]),(.87,.22,PALETTE["forest_light"]))):
        crown = cone(f"Tree {index} angular canopy tier {layer}", (ox+x,oy+y,size*height), size*radius, size*.48, swatch, 7)
        crown.rotation_euler[2] = rng.uniform(-.4,.4)
        for facet in range(2):
            fleck = ico(f"Tree {index} leaf pigment facet {layer}-{facet}",
                        (ox+x+rng.uniform(-.12,.12),oy+y+rng.uniform(-.1,.1),size*(height+.08)),
                        (size*.13,size*.09,size*.045), rng.choice(("#9A9A6E", "#A4A477")), 1, .03)


def mountain_form(kind: str, origin: tuple[float, float], height: float, index: int) -> None:
    x,y = origin
    footprint = .43 if kind == "peak" else .32
    base = [(x-footprint,y-.22,0),(x-.12,y-.42,0),(x+.3,y-.25,0),(x+footprint,y+.04,0),(x+.16,y+.37,0),(x-.32,y+.28,0)]
    verts = base + [(x-.12,y-.04,height*.62),(x+.08,y+.02,height),(x+.23,y+.12,height*.55)]
    faces = [(0,1,6),(1,2,6),(2,3,8,6),(3,4,8),(4,5,7,8),(5,0,6,7),(0,6,7,5),(6,8,7)]
    mesh_object(f"{kind.title()} faceted summit {index}", verts, faces,
                PALETTE["mountain_dark"], .055)
    # Hand-placed light plane and snow patch keep the faceting graphic and readable.
    mesh_object(f"{kind.title()} broad sunlit plane {index}",
                [(x-footprint,y-.22,.01),(x-.12,y-.04,height*.62),(x+.08,y+.02,height),
                 (x-.06,y+.12,height*.25),(x-.32,y+.28,0)], [(0,1,2,3,4)], PALETTE["mountain_light"], .04)
    if kind == "peak" or height > .85:
        mesh_object(f"{kind.title()} snowcap {index}",
                    [(x-.12,y-.04,height*.62),(x+.08,y+.02,height),(x+.20,y+.09,height*.72),(x+.04,y+.13,height*.66)],
                    [(0,1,2,3)], PALETTE["snow"], .025)


def terrain(kind: str, origin: tuple[float, float] = (0,0), seed: int = 17) -> None:
    rng = random.Random(seed)
    x,y = origin
    tile_base(kind, origin, seed)
    if kind == "forest":
        for index, (dx,dy,size) in enumerate(((-.54,-.08,.66),(-.24,.16,.76),(.07,-.02,.83),(.40,.12,.70),(-.37,-.31,.58),(.10,-.30,.68),(.48,-.22,.56))):
            tree(origin, dx,dy,size,rng,index+1)
    elif kind in ("meadow","plains"):
        for index in range(23 if kind == "meadow" else 30):
            px,py=x+rng.uniform(-.72,.72),y+rng.uniform(-.3,.3)
            if abs(px-x)+2*abs(py-y)>.9: continue
            beam(f"{kind.title()} painterly grass stroke {index}",(px,py,.035),(px+rng.uniform(-.04,.04),py+.09,.06),.012,
                 rng.choice(("#6F8058","#A5A276","#829064")),4)
            if kind == "meadow" and index%4==0:
                ico(f"Meadow flower pigment dab {index}",(px,py+.09,.075),(.025,.018,.012),"#D8C18A",1)
    elif kind == "hills":
        for index,(dx,dy,sx,sy,sz) in enumerate(((-.35,-.10,.56,.34,.28),(.18,.09,.63,.40,.34),(.49,-.22,.38,.28,.22))):
            hill=ico(f"Hill soft faceted rise {index}",(x+dx,y+dy,sz*.28),(sx,sy,sz),PALETTE["hill_light"],2,.055)
            hill.rotation_euler[2]=rng.uniform(-.3,.3)
    elif kind in ("mountain","peak"):
        peaks=[(-.38,-.04,.92),(.03,.12,1.12),(.43,-.15,.78)] if kind=="mountain" else [(0,0,1.55)]
        for index,(dx,dy,height) in enumerate(peaks): mountain_form(kind,(x+dx,y+dy),height,index)
    elif kind == "coast":
        # A low, irregular sandy spit meets shallow water on the tile surface.
        vertices=[(x-.86,y-.12,.035),(x-.55,y-.28,.04),(x-.18,y-.25,.045),(x+.14,y-.13,.04),(x+.48,y-.20,.04),(x+.84,y-.08,.035),(x+.57,y+.12,.04),(x+.22,y+.07,.045), (x-.12,y+.18,.04),(x-.48,y+.13,.04)]
        mesh_object("Coast sculpted sand shoreline",vertices,[tuple(range(len(vertices)))],PALETTE["coast"],.045)
        for index in range(7):
            px=x+rng.uniform(-.65,.65); py=y+rng.uniform(.16,.34)
            beam(f"Coast broken foam brush {index}",(px,py,.045),(px+.13,py+.015,.05),.012,PALETTE["foam"],4)
    elif kind in ("shallow_sea","open_sea"):
        for index in range(12):
            px=x+rng.uniform(-.7,.7); py=y+rng.uniform(-.3,.3)
            beam(f"{kind.title()} hand-painted wave {index}",(px,py,.035),(px+rng.uniform(.08,.2),py+.025,.045),.009,
                 rng.choice((PALETTE["foam"],"#91AAA0")),4)


def house(faction: str, origin: tuple[float,float], size: float, index: int) -> None:
    x,y=origin
    wall,roof = ((PALETTE["stone"],PALETTE["slate"]) if faction=="auren" else (PALETTE["timber"],PALETTE["iron"]))
    # Compact faceted cottage: a shallow block, pitched roof and painted roof plane.
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x,y,size*.29))
    body=bpy.context.object; body.name=f"{faction.title()} cottage {index} stone/timber mass"; body.scale=(size*.36,size*.29,size*.27); bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    body.data.materials.append(material(body.name,wall,.045))
    for face in body.data.polygons: face.use_smooth=False
    verts=[(x-size*.43,y-size*.34,size*.48),(x,y-size*.34,size*.84),(x+size*.43,y-size*.34,size*.48),
           (x-size*.43,y+size*.34,size*.48),(x,y+size*.34,size*.84),(x+size*.43,y+size*.34,size*.48)]
    mesh_object(f"{faction.title()} cottage {index} angular pitched roof",verts,[(0,1,2),(3,5,4),(0,3,4,1),(1,4,5,2),(2,5,3,0)],roof,.04)
    beam(f"{faction.title()} cottage {index} chimney",(x+size*.20,y+size*.10,size*.62),(x+size*.20,y+size*.10,size*.96),size*.055,PALETTE["stone_shadow"] if faction=="auren" else PALETTE["copper"],5)
    door=PALETTE["soil"]
    prism(f"{faction.title()} cottage {index} inset door",[(x-size*.06,y-size*.294),(x+size*.06,y-size*.294),(x+size*.06,y-size*.294+size*.22),(x-size*.06,y-size*.294+size*.22)],size*.02,.01,door)


def city(faction: str, center: tuple[float,float]=(0,0)) -> None:
    x,y=center
    for index,(dx,dy,size) in enumerate(((-.55,.05,.72),(0,.10,1),(.53,-.04,.68))): house(faction,(x+dx,y+dy),size,index+1)
    if faction=="auren":
        beam("Auren civic Trama arch left",(x-.12,y,.02),(x-.12,y,.60),.035,PALETTE["stone"],5)
        beam("Auren civic Trama arch right",(x+.12,y,.02),(x+.12,y,.60),.035,PALETTE["stone"],5)
        beam("Auren civic Trama lintel",(x-.13,y,.58),(x+.13,y,.58),.035,PALETTE["gold"],5)
        banner=PALETTE["blue"]
    else:
        prism("Brasal dark forge",[(x+.62,y-.2),(x+.9,y-.2),(x+.9,y+.15),(x+.62,y+.15)],.08,.04,PALETTE["iron"])
        banner=PALETTE["ember"]
    beam(f"{faction.title()} banner pole",(x-.88,y,.02),(x-.88,y,.82),.018,PALETTE["soil"],5)
    mesh_object(f"{faction.title()} faction banner",
                [(x-.87,y,.72),(x-.57,y,.68),(x-.66,y,.49),(x-.87,y,.53)],[(0,1,2,3)],banner)


def soldier(faction: str, center: tuple[float,float]=(0,0)) -> None:
    x,y=center
    skin,cloth,armor = ((PALETTE["skin"],PALETTE["blue"],PALETTE["ivory"]) if faction=="auren" else (PALETTE["skin_orc"],PALETTE["hide"],PALETTE["iron_light"]))
    # Small low-poly figure with an intentional readable head/torso/limb silhouette.
    for dx in (-.10,.10):
        beam(f"{faction.title()} soldier leg",(x+dx,y,.02),(x+dx*1.2,y,.38),.055,cloth,5)
    ico(f"{faction.title()} soldier torso",(x,y,.58),(.20,.14,.29),cloth,1,.025)
    ico(f"{faction.title()} soldier breastplate",(x,y-.09,.62),(.16,.07,.20),armor,1,.02)
    ico(f"{faction.title()} soldier head",(x,y,.94),(.13,.12,.16),skin,1)
    cone(f"{faction.title()} soldier faceted helm",(x,y,1.10),.17,.19,armor,6)
    beam(f"{faction.title()} soldier left arm",(x-.15,y,.70),(x-.27,y-.02,.43),.045,cloth,5)
    beam(f"{faction.title()} soldier right arm",(x+.15,y,.70),(x+.25,y-.02,.47),.045,cloth,5)
    if faction=="auren":
        beam("Auren soldier spear shaft",(x+.31,y,.04),(x+.31,y,1.35),.018,PALETTE["soil"],5)
        cone("Auren soldier spear point",(x+.31,y,1.44),.07,.20,armor,5)
        for dx in (-.045,0,.045): beam("Auren Trama breast insignia",(x+dx,y-.16,.70),(x+dx+.02,y-.16,.65),.009,PALETTE["gold"],4)
    else:
        ico("Brasal broad shoulder mantle",(x,y,.78),(.27,.15,.12),PALETTE["moss"],1,.025)
        beam("Brasal soldier axe haft",(x+.31,y,.35),(x+.31,y,1.28),.025,PALETTE["timber"],5)
        ico("Brasal soldier axe blade",(x+.31,y,1.25),(.16,.08,.14),armor,1)
        for side in (-1,1): cone(f"Brasal tusk {side}",(x+side*.07,y-.08,.88),.035,.13,PALETTE["ivory"],5)


def save_render(path: Path, width: int, height: int) -> None:
    bpy.context.scene.render.resolution_x=width
    bpy.context.scene.render.resolution_y=height
    render(path)


def review_sheet(zoom: float) -> None:
    clear_scene(); setup(720,540,False,8.7/zoom,(0,0,.25))
    # Painted-paper field is a backdrop; terrain objects stay as separate shallow 3D assets.
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0,0,-.35))
    paper=bpy.context.object; paper.name="Warm paper review backdrop"; paper.data.materials.append(material("Warm paper",PALETTE["paper"],.018))
    kinds=("mountain","peak","hills","forest","forest","plains","meadow","forest",
           "coast","hills","plains","coast","open_sea","shallow_sea","coast","plains")
    for index,kind in enumerate(kinds):
        row,col=divmod(index,4)
        pos=((col-1.5)*1.5,(1.5-row)*math.sqrt(3)+(col%2)*math.sqrt(3)/2)
        terrain(kind,pos,171+index)
    city("auren",(-.75,math.sqrt(3)/2)); soldier("auren",(.75,math.sqrt(3)))
    city("brasal",(2.25,-math.sqrt(3))); soldier("brasal",(-.75,-math.sqrt(3)/2))
    render(OUTPUT/f"review_slice_{int(zoom*100)}.png")


def main() -> None:
    OUTPUT.mkdir(parents=True,exist_ok=True)
    terrain_kinds=("meadow","plains","forest","hills","mountain","coast","shallow_sea","open_sea","peak")
    for index,kind in enumerate(terrain_kinds):
        clear_scene(); setup(256,128,True,3.2)
        terrain(kind,(0,0),17+index)
        render(OUTPUT/f"terrain_{kind}_2x.png")
    for faction in ("auren","brasal"):
        clear_scene(); setup(512,256,True,4.6)
        tile_base("plains",(0,0),17); city(faction)
        render(OUTPUT/f"city_{faction}_level_3_4_2x.png")
        clear_scene(); setup(256,128,True,3.6)
        tile_base("plains",(0,0),17); soldier(faction)
        render(OUTPUT/f"unit_{faction}_basic_soldier_2x.png")
    for zoom in (.75,1.0,1.25): review_sheet(zoom)
    bpy.ops.wm.save_as_mainfile(filepath=str(OUTPUT/"issue_17_visual_slice.blend"))
    print(f"Rendered faceted painterly 2.5D issue #17 study to {OUTPUT}")


if __name__=="__main__":
    main()
