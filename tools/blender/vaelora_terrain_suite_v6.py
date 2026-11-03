"""Vaelora Terrain Suite v6.0-rc1.

This is a parallel visual candidate built from the approved v5 technical baseline.
Its purpose is to approach the approved 9-10 art references without sacrificing
hex registration, deterministic seeds, clip safety or strategy readability.
"""
from __future__ import annotations

import math
import random
from pathlib import Path
from typing import Callable

import bpy
from mathutils import Vector

import vaelora_geometry as geo
import vaelora_render as render
from vaelora_contract import coast_asset_seed, derive_seed
from vaelora_materials import create_flat_material, create_terrain_v3_material, world_materials
from vaelora_style import COAST_VARIANT_COUNT, HEX_AXIAL_X_STEP, HEX_AXIAL_Y_STEP, HEX_RADIUS
from vaelora_terrain_suite_v6_spec import BENCHMARK36_V6, SUITE_V6_FAMILIES, SUITE_V6_VARIANTS

TAU = math.tau
SEA_KINDS = {"shallow_sea", "open_sea"}
AXIAL_EDGE = {(0, 1): 0, (-1, 1): 1, (-1, 0): 2, (0, -1): 3, (1, -1): 4, (1, 0): 5}
FLOWER7 = ((0, 0), (1, 0), (1, -1), (0, -1), (-1, 0), (-1, 1), (0, 1))


def _world_pos(q: int, r: int) -> tuple[float, float]:
    return HEX_AXIAL_X_STEP * (q + r / 2.0), HEX_AXIAL_Y_STEP * r


def _translate_new(before: set[bpy.types.Object], q: int, r: int, center=(0.0, 0.0)) -> None:
    x, y = _world_pos(q, r)
    x -= center[0]; y -= center[1]
    for obj in [o for o in bpy.context.scene.objects if o not in before]:
        obj.location.x += x; obj.location.y += y


def _materials() -> dict[str, bpy.types.Material]:
    """Brighter v6 palette tuned to the approved reference renders."""
    return {
        "plains": create_terrain_v3_material("VAE_V6_Plains", "#526C38", "#88A850", "#C6CC70", broad_scale=1.08, micro_scale=6.0, roughness=0.89, bump_strength=0.060),
        "hills": create_terrain_v3_material("VAE_V6_Hills", "#486A38", "#7FA84A", "#D0CF6C", broad_scale=1.06, micro_scale=5.7, roughness=0.89, bump_strength=0.064),
        "mountain_ground": create_terrain_v3_material("VAE_V6_MountainGround", "#53613E", "#74884A", "#AAB65E", broad_scale=1.08, micro_scale=5.1, roughness=0.91, bump_strength=0.066),
        "desert": create_terrain_v3_material("VAE_V6_Desert", "#9B673A", "#D3A05C", "#F0CC7C", broad_scale=1.02, micro_scale=6.8, roughness=0.93, bump_strength=0.052),
        "snow": create_terrain_v3_material("VAE_V6_Snow", "#9FB5C4", "#D7E2E7", "#F6F4EA", broad_scale=1.04, micro_scale=7.0, roughness=0.80, bump_strength=0.036),
        "forest_ground": create_terrain_v3_material("VAE_V6_ForestGround", "#365B3D", "#659049", "#A6BB5D", broad_scale=1.07, micro_scale=5.7, roughness=0.91, bump_strength=0.057),
        "rock": create_flat_material("VAE_V6_Rock", "#69727A", roughness=0.91),
        "rock_light": create_flat_material("VAE_V6_RockLight", "#A5A39A", roughness=0.90),
        "rock_warm": create_flat_material("VAE_V6_RockWarm", "#94816D", roughness=0.91),
        "rock_shadow": create_flat_material("VAE_V6_RockShadow", "#49535D", roughness=0.92),
        "leaf_warm": create_flat_material("VAE_V6_LeafWarm", "#81A94B", roughness=0.88),
        "leaf_light": create_flat_material("VAE_V6_LeafLight", "#A8C45E", roughness=0.88),
        "leaf_deep": create_flat_material("VAE_V6_LeafDeep", "#426D49", roughness=0.90),
        "conifer": create_flat_material("VAE_V6_Conifer", "#557C62", roughness=0.90),
        "snow_leaf": create_flat_material("VAE_V6_SnowLeaf", "#E8F0EF", roughness=0.84),
        "snow_leaf_shadow": create_flat_material("VAE_V6_SnowLeafShadow", "#B9CDD5", roughness=0.86),
        "palm": create_flat_material("VAE_V6_Palm", "#668A3C", roughness=0.89),
        "palm_light": create_flat_material("VAE_V6_PalmLight", "#9BAA45", roughness=0.89),
    }


def _hex_perimeter(samples_per_side: int = 7) -> list[Vector]:
    corners = [Vector((math.cos(math.radians(30 + 60*i))*HEX_RADIUS, math.sin(math.radians(30+60*i))*HEX_RADIUS, 0.0)) for i in range(6)]
    out=[]
    for i in range(6):
        a,b=corners[i],corners[(i+1)%6]
        for j in range(samples_per_side): out.append(a.lerp(b,j/samples_per_side))
    return out


def _elliptic(x,y,cx,cy,rx,ry,angle,height,power=1.48):
    ca,sa=math.cos(angle),math.sin(angle); dx,dy=x-cx,y-cy
    u,v=dx*ca+dy*sa,-dx*sa+dy*ca
    d2=(u/max(rx,0.001))**2+(v/max(ry,0.001))**2
    return height*math.exp(-(d2**power)*1.30)


def _shape_params(kind: str, seed: int, variant: int):
    rng=random.Random(derive_seed(seed,"suite-v6-shape",kind,variant)); a=rng.uniform(0,TAU); m=-1 if rng.random()<0.5 else 1; v=variant%4
    A={
      "plains":(
        [(-.60,.30,1.30,.52,.20),(.56,-.48,.92,.38,.11),(.04,-.02,.76,.64,-.055)],
        [(-.70,-.10,1.00,.44,.16),(.38,.52,1.08,.46,.18),(.56,-.52,.72,.34,.08)],
        [(-.08,.56,1.42,.38,.19),(.18,-.52,1.18,.36,.13),(-.70,-.22,.66,.44,-.035)],
        [(.56,.24,1.22,.52,.20),(-.56,-.50,.78,.36,.11),(-.52,.50,.68,.38,.08)],),
      "hills":(
        [(-.64,.30,1.02,.58,.46),(.50,-.24,.92,.54,.39),(.48,.62,.64,.38,.20),(-.04,.02,.62,.50,-.10)],
        [(-.58,-.48,.86,.56,.41),(.08,.42,1.10,.56,.47),(.70,-.18,.66,.42,.23),(.06,-.06,.60,.50,-.09)],
        [(-.08,.58,1.18,.46,.44),(-.28,-.54,1.02,.46,.39),(.70,.06,.58,.38,.22),(-.02,.02,.60,.50,-.10)],
        [(.52,.40,.94,.54,.43),(-.58,.04,.86,.52,.37),(.32,-.58,.88,.46,.35),(-.04,-.04,.62,.50,-.09)],),
      "mountain":(
        [(0,.08,1.42,.90,.54),(-.72,-.34,.78,.50,.20),(.66,.42,.66,.44,.16)],
        [(-.30,.26,1.30,.84,.50),(.58,-.34,.94,.58,.29),(.10,-.08,.68,.50,-.035)],
        [(.20,.40,1.46,.78,.52),(-.42,-.44,.90,.56,.24),(.66,-.18,.58,.40,.12)],
        [(-.28,-.08,1.36,.88,.51),(.62,.38,.76,.48,.20),(-.60,.46,.66,.44,.15)],),
      "peak":(
        [(0,.06,1.42,.90,.58),(.50,-.46,.70,.46,.16)],
        [(-.18,.22,1.34,.84,.56),(.54,-.18,.76,.48,.18)],
        [(.16,-.04,1.42,.82,.58),(-.54,.50,.66,.44,.15)],
        [(-.16,-.12,1.36,.86,.56),(.48,.44,.70,.46,.17),(-.50,-.44,.56,.38,.11)],),
      "desert":(
        [(-.56,.30,1.42,.42,.26),(.58,-.34,1.24,.38,.21),(0,.02,.80,.66,-.07)],
        [(-.12,.56,1.46,.38,.24),(-.20,-.48,1.34,.36,.21),(.68,.02,.62,.42,-.04)],
        [(-.66,-.18,1.18,.40,.22),(.18,.40,1.42,.42,.26),(.58,-.54,.80,.38,.14)],
        [(.56,.34,1.34,.42,.25),(-.56,-.40,1.26,.38,.20),(-.50,.52,.68,.34,.12)],),
      "snow":(
        [(-.44,.34,1.20,.58,.26),(.58,-.40,.94,.48,.16),(.08,-.02,.78,.62,-.05)],
        [(-.10,.56,1.28,.50,.25),(-.54,-.42,.84,.44,.15),(.60,-.24,.74,.42,.12)],
        [(.46,.32,1.20,.56,.25),(-.52,.02,.84,.46,.15),(.26,-.58,.78,.42,.13)],
        [(-.34,-.36,1.18,.54,.23),(.48,.46,.98,.48,.18),(-.62,.52,.64,.36,.10)],),
      "forest":(
        [(-.36,.32,1.08,.60,.17),(.56,-.42,.84,.46,.09),(0,0,.76,.64,-.035)],
        [(.42,.42,1.02,.58,.16),(-.58,-.34,.84,.46,.10),(-.10,.02,.74,.60,-.035)],
        [(-.52,.04,.98,.56,.16),(.38,-.52,.90,.48,.11),(.48,.56,.60,.36,.08)],
        [(.18,.50,1.08,.56,.17),(-.44,-.48,.80,.44,.10),(.62,-.18,.66,.38,.08)],),
    }
    src=A.get(kind, A["plains"])[v]
    forms=[]
    for cx,cy,rx,ry,h in src:
        forms.append((cx*m+rng.uniform(-.04,.04), cy+rng.uniform(-.03,.03), rx*rng.uniform(.97,1.03), ry*rng.uniform(.97,1.03), h*rng.uniform(.97,1.03)))
    return a,forms


def _height_limit(kind: str) -> tuple[float,float]:
    return {
        "plains":(-.05,.34), "hills":(-.06,.66), "mountain":(-.05,.78), "peak":(-.05,.86),
        "desert":(-.05,.38), "snow":(-.05,.38), "forest":(-.05,.32),
    }.get(kind,(-.05,.34))


def _create_surface(kind: str, seed: int, variant: int, material) -> bpy.types.Object:
    outer=_hex_perimeter(7); rings=13 if kind in {"mountain","peak","hills"} else 11; inner_scale=.12
    angle,forms=_shape_params(kind,seed,variant); jitter=random.Random(derive_seed(seed,"suite-v6-jitter",kind,variant)); lo,hi=_height_limit(kind)
    verts=[]
    for ring in range(rings):
        t=ring/max(1,rings-1); scale=1+(inner_scale-1)*t; edge_t=min(1,max(0,(1-scale)/.28)); weight=edge_t*edge_t*(3-2*edge_t)
        for p in outer:
            x,y=p.x*scale,p.y*scale
            if ring==0: z=0.0
            else:
                z=.012+sum(_elliptic(x,y,cx,cy,rx,ry,angle+i*.31,h,1.40+i*.07) for i,(cx,cy,rx,ry,h) in enumerate(forms))
                if kind=="desert":
                    axis=x*math.cos(angle)+y*math.sin(angle)
                    z += math.sin(axis*1.42+variant*.8)*.030 + math.sin(axis*.70+1.1)*.012
                elif kind=="snow": z += math.sin(x*.94-y*.62+variant*.7)*.018
                elif kind=="plains": z += math.sin(x*.70+y*.28+variant)*.012
                z=(z+jitter.uniform(-.0025,.0025))*weight; z=max(lo,min(hi,z))
            verts.append((x,y,z))
    center=.012+sum(_elliptic(0,0,cx,cy,rx,ry,angle+i*.31,h,1.40+i*.07) for i,(cx,cy,rx,ry,h) in enumerate(forms)); center=max(lo,min(hi,center))
    ci=len(verts); verts.append((0,0,center)); sec=len(outer); faces=[]
    for ring in range(rings-1):
        a0,a1=ring*sec,(ring+1)*sec
        for i in range(sec): j=(i+1)%sec; faces.append((a0+i,a0+j,a1+j,a1+i))
    inner=(rings-1)*sec
    for i in range(sec): j=(i+1)%sec; faces.append((inner+i,inner+j,ci))
    obj=geo.make_mesh(f"VAE_V6_{kind}_Surface",verts,faces); geo.set_material(obj,material)
    for poly in obj.data.polygons: poly.use_smooth=True
    return obj


def _create_land_base(kind: str, seed: int, variant: int, material):
    mats=world_materials(); geo.create_hex_prism("VAE_V6_GeologyDark",-.22,-.63,mats["earth"]); geo.create_hex_prism("VAE_V6_GeologyWarm",-.11,-.24,mats["clay"]); geo.create_hex_prism("VAE_V6_Topsoil",-.035,-.12,mats["earth"]); geo.create_hex_side_band("VAE_V6_SurfaceRim",0,-.040,material)
    return _create_surface(kind,seed,variant,material)


def _ground(surface,x,y,lift=.012): return geo.surface_z_at(surface,x,y,0.0)+lift


def _safe_point(rng,ring,clearance,occupied,spacing=.18):
    for _ in range(240):
        p=geo.random_hex_ring_point(rng,ring,clearance=clearance)
        if p is None: return None
        x,y=p
        if all(math.hypot(x-ox,y-oy)>=spacing+orad for ox,oy,orad in occupied): return x,y
    return None


def _add_rock(rng,surface,occupied,ring="mid",scale=.72,warm=True):
    p=_safe_point(rng,ring,.34*scale+.05,occupied,.14)
    if not p:return
    x,y=p; occupied.append((x,y,.28*scale)); geo.create_terrain_rock_cluster(rng,(x,y,_ground(surface,x,y,.012)),scale,warm=warm)


def _add_grass(rng,surface,occupied,ring="mid",scale=.65,dry=False,flowers=False):
    p=_safe_point(rng,ring,.18*scale+.04,occupied,.08)
    if not p:return
    x,y=p; occupied.append((x,y,.13*scale))
    if dry: geo.create_grass_clump(rng,(x,y,_ground(surface,x,y,.006)),scale=scale,dry=True)
    else: geo.create_terrain_ground_clump_v41(rng,(x,y,_ground(surface,x,y,.006)),scale)
    if flowers and rng.random()<.45: geo.create_flower_cluster(rng,(x+rng.uniform(-.08,.08),y+rng.uniform(-.08,.08),_ground(surface,x,y,.020)),scale=.48)


def _blob(rng,name,center,radii,material):
    cx,cy,cz=center; rx,ry,rz=radii; pts=[]
    for _ in range(16):
        th=rng.uniform(0,TAU); ph=math.acos(rng.uniform(-1,1)); w=rng.uniform(.78,1.15)
        pts.append((cx+math.sin(ph)*math.cos(th)*rx*w, cy+math.sin(ph)*math.sin(th)*ry*w, cz+math.cos(ph)*rz*w))
    return geo.create_convex_hull(name,pts,material,min(rx,ry,rz)*.024)


def _create_v6_tree(rng,location,scale=1.0,conifer=False,snow=False):
    m=_materials(); wm=world_materials(); x,y,z=location; h=rng.uniform(1.02,1.30)*scale
    leanx=rng.uniform(-.07,.07)*scale; leany=rng.uniform(-.05,.05)*scale
    root=Vector((x,y,z)); top=Vector((x+leanx,y+leany,z+h*.66)); geo.create_branch("VAE_V6_TreeTrunk",root,top,.10*scale,.045*scale,wm["trunk"],8)
    if conifer:
        mats=(m["snow_leaf_shadow"],m["snow_leaf"],m["snow_leaf"]) if snow else (m["conifer"],m["conifer"],m["leaf_deep"])
        for i,w in enumerate((.42,.34,.25)):
            _blob(rng,"VAE_V6_ConiferMass",(top.x,top.y,z+h*(.50+i*.17)),(w*scale,w*.84*scale,.22*scale),mats[i])
    else:
        leafset=(m["leaf_warm"],m["leaf_light"],m["leaf_deep"])
        for i in range(4):
            a=TAU*i/4+rng.uniform(-.25,.25); rr=rng.uniform(.16,.30)*scale
            c=(top.x+math.cos(a)*rr,top.y+math.sin(a)*rr,top.z+rng.uniform(.02,.18)*scale)
            _blob(rng,"VAE_V6_BroadleafMass",c,(.34*scale,.31*scale,.30*scale),leafset[i%3])


def _create_palm_leaf(name,base,direction,length,width,material):
    f=Vector((math.cos(direction),math.sin(direction),0)); s=Vector((-math.sin(direction),math.cos(direction),0)); b=Vector(base); verts=[]
    for t,wf in zip((0,.30,.66,1.0),(1,.86,.46,.05)):
        c=b+f*(length*t)+Vector((0,0,.08*math.sin(math.pi*t)-.16*(t**1.8)))
        ww=width*wf; verts.extend([tuple(c-s*ww),tuple(c+s*ww)])
    obj=geo.make_mesh(name,verts,[(0,1,3,2),(2,3,5,4),(4,5,7,6)]); geo.set_material(obj,material); return obj


def _create_palm(rng,location,scale=1.0):
    m=_materials(); wm=world_materials(); x,y,z=location; h=rng.uniform(.95,1.15)*scale
    p0=Vector((x,y,z)); p1=Vector((x+rng.uniform(-.05,.05)*scale,y+rng.uniform(-.04,.04)*scale,z+h*.48)); p2=Vector((p1.x+rng.uniform(-.06,.06)*scale,p1.y+rng.uniform(-.05,.05)*scale,z+h))
    geo.create_branch("VAE_V6_PalmLower",p0,p1,.11*scale,.085*scale,wm["trunk"],8); geo.create_branch("VAE_V6_PalmUpper",p1,p2,.085*scale,.045*scale,wm["trunk"],8)
    for i in range(7):
        a=TAU*i/7+rng.uniform(-.16,.16); _create_palm_leaf("VAE_V6_PalmLeaf",p2,a,rng.uniform(.45,.62)*scale,.08*scale,m["palm_light"] if i%3==0 else m["palm"])


def _create_spire(rng,location,scale=1.0):
    m=_materials(); x,y,z=location; n=8; verts=[]
    for i in range(n):
        a=TAU*i/n; rr=(.52 if i%2==0 else .46)*scale*rng.uniform(.94,1.06); verts.append((x+math.cos(a)*rr,y+math.sin(a)*rr,z))
    for i in range(n):
        a=TAU*i/n+.08; rr=(.28 if i%2==0 else .23)*scale*rng.uniform(.94,1.06); verts.append((x+math.cos(a)*rr,y+math.sin(a)*rr,z+1.00*scale))
    apex=len(verts); verts.append((x+rng.uniform(-.06,.06)*scale,y+rng.uniform(-.05,.05)*scale,z+1.78*scale))
    faces=[]
    for i in range(n): j=(i+1)%n; faces.append((i,j,n+j,n+i)); faces.append((n+i,n+j,apex))
    obj=geo.make_mesh("VAE_V6_HeroSpire",verts,faces); geo.set_material(obj,m["rock"]); geo.shade_flat(obj); geo.bevel(obj,.018*scale,1)
    # small pale/snow crest, integrated rather than a separate cap.
    if rng.random()<.72:
        geo.create_ridge_mass(rng,"VAE_V6_SpireSnow",(x,y,z+1.10*scale),length=.58*scale,width=.22*scale,height=.34*scale,sections=4,material=world_materials()["snow"],direction_rad=rng.uniform(0,TAU),asymmetry=.16)


def _build_plains(seed,variant):
    m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-plains",variant)); s=_create_land_base("plains",seed,variant,m["plains"]); occ=[]
    for ring in ("mid","outer"): _add_rock(rng,s,occ,ring,rng.uniform(.48,.68),True)
    for ring in ("outer","mid","inner","outer"): _add_grass(rng,s,occ,ring,rng.uniform(.54,.72),False,flowers=True)


def _build_hills(seed,variant):
    m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-hills",variant)); s=_create_land_base("hills",seed,variant,m["hills"]); occ=[]
    # v6 hills rely on the sculpted surface itself, avoiding obvious object-on-top ridges.
    for ring in ("outer","mid"): _add_rock(rng,s,occ,ring,rng.uniform(.45,.62),True)
    for ring in ("outer","mid","inner","outer"): _add_grass(rng,s,occ,ring,rng.uniform(.50,.68),False,flowers=True)
    if variant%2==1:
        p=_safe_point(rng,"mid",.34,occ,.18)
        if p: geo.create_ridge_mass(rng,"VAE_V6_HillStoneShelf",(p[0],p[1],_ground(s,*p,.004)),length=.68,width=.20,height=.14,sections=4,material=m["rock_warm"],direction_rad=rng.uniform(0,TAU),asymmetry=.18)


def _mountain_mass(rng,surface,peak=False,variant=0):
    m=_materials(); direction=rng.uniform(0,TAU)
    # Broad mountain foundation: terrain + wide stone ridges together occupy most of the hex.
    base_len=rng.uniform(2.55,2.90); base_w=rng.uniform(.92,1.08); base_h=rng.uniform(.72,.92)
    geo.create_ridge_mass(rng,"VAE_V6_MountainFoundation",(0,0,_ground(surface,0,0,.002)),length=base_len,width=base_w,height=base_h,sections=8,material=m["rock"],direction_rad=direction,asymmetry=.25)
    side=direction+rng.choice((-1,1))*rng.uniform(.62,.82)
    geo.create_ridge_mass(rng,"VAE_V6_MountainShoulder",(math.cos(direction)*-.16,math.sin(direction)*-.16,_ground(surface,0,0,.002)),length=rng.uniform(1.60,2.00),width=rng.uniform(.56,.72),height=base_h*.56,sections=6,material=m["rock_warm"],direction_rad=side,asymmetry=.28)
    if peak:
        _create_spire(rng,(rng.uniform(-.08,.08),rng.uniform(-.05,.08),_ground(surface,0,0,.34)),scale=rng.uniform(.90,1.04))
    elif variant%2==0:
        geo.create_ridge_mass(rng,"VAE_V6_MountainLitRib",(.10,-.06,_ground(surface,.10,-.06,.20)),length=1.12,width=.30,height=.36,sections=5,material=m["rock_light"],direction_rad=direction+.12,asymmetry=.16)


def _build_mountain(seed,variant,peak=False):
    kind="peak" if peak else "mountain"; m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-"+kind,variant)); s=_create_land_base(kind,seed,variant,m["mountain_ground"]); occ=[]
    _mountain_mass(rng,s,peak,variant)
    for ring in (("outer",) if peak else ("outer","mid")): _add_rock(rng,s,occ,ring,rng.uniform(.42,.58),False)
    if not peak:
        for ring in ("outer","outer","mid"): _add_grass(rng,s,occ,ring,rng.uniform(.38,.54),False,flowers=(ring=="outer"))


def _build_desert(seed,variant):
    m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-desert",variant)); s=_create_land_base("desert",seed,variant,m["desert"]); occ=[]
    for ring in ("mid","outer"): _add_rock(rng,s,occ,ring,rng.uniform(.45,.66),True)
    for ring in rng.sample(["outer","mid","inner"],2): _add_grass(rng,s,occ,ring,rng.uniform(.42,.58),True,False)
    # Only palms are allowed as desert trees; only some variants receive one.
    if variant in (1,3):
        p=_safe_point(rng,"mid",.72,occ,.24)
        if p: occ.append((p[0],p[1],.38)); _create_palm(rng,(p[0],p[1],_ground(s,*p,.006)),scale=rng.uniform(.78,.94))


def _build_snow(seed,variant):
    m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-snow",variant)); s=_create_land_base("snow",seed,variant,m["snow"]); occ=[]
    for ring in ("mid","outer"): _add_rock(rng,s,occ,ring,rng.uniform(.44,.62),False)
    # Snow trees deliberately use white/snow-covered foliage, never green foliage.
    if variant in (1,3):
        count=1 if variant==1 else 2
        for _ in range(count):
            p=_safe_point(rng,rng.choice(("mid","outer")),.46,occ,.24)
            if p: occ.append((p[0],p[1],.36)); _create_v6_tree(rng,(p[0],p[1],_ground(s,*p,.006)),scale=rng.uniform(.64,.78),conifer=True,snow=True)


def _build_forest(seed,variant):
    m=_materials(); rng=random.Random(derive_seed(seed,"suite-v6-forest",variant)); s=_create_land_base("forest",seed,variant,m["forest_ground"]); occ=[]
    plans=((4,3),(3,3,2),(4,2),(3,2,2)); centres=[]
    for ci,count in enumerate(plans[variant%4]):
        ring=("mid" if ci==0 else "outer") if ci<2 else "mid"; p=_safe_point(rng,ring,.52,occ,.28)
        if not p: continue
        occ.append((p[0],p[1],.38)); centres.append((p,count))
    for ci,(p,count) in enumerate(centres):
        cx,cy=p
        for i in range(count):
            a=TAU*i/count+rng.uniform(-.26,.26); rr=rng.uniform(.10,.30); x,y=cx+math.cos(a)*rr,cy+math.sin(a)*rr
            if geo.hex_contains_disc(x,y,.38): _create_v6_tree(rng,(x,y,_ground(s,x,y,.006)),scale=rng.uniform(.72,.90),conifer=((i+variant+ci)%4==0),snow=False)
    for ring in ("outer","mid"): _add_rock(rng,s,occ,ring,rng.uniform(.40,.56),True)
    for ring in ("outer","mid"): _add_grass(rng,s,occ,ring,rng.uniform(.42,.58),False,flowers=True)


def _build_water(seed,variant):
    rng=random.Random(derive_seed(seed,"suite-v6-water",variant)); open_sea=variant%2==1; kind="open_sea" if open_sea else "shallow_sea"
    geo.create_hex_base(kind,rng,variant=variant%4,terrain_seed=seed)
    geo.create_water_highlights(rng,open_sea=open_sea,count=4 if open_sea else 6)


def build_candidate_tile(kind,variant,seed,core_builder):
    if kind=="meadow": core_builder("meadow",variant%4,seed)
    elif kind=="plains": _build_plains(seed,variant)
    elif kind=="forest": _build_forest(seed,variant)
    elif kind=="hills": _build_hills(seed,variant)
    elif kind=="mountain": _build_mountain(seed,variant,False)
    elif kind=="peak": _build_mountain(seed,variant,True)
    elif kind=="desert": _build_desert(seed,variant)
    elif kind=="snow": _build_snow(seed,variant)
    elif kind=="water": _build_water(seed,variant)
    elif kind in SEA_KINDS: _build_water(seed,1 if kind=="open_sea" else 0)
    else: raise ValueError(f"unknown Terrain Suite v6 kind: {kind}")


def _render(path,blend,ortho,strict,resolution=(1920,1080)):
    render.assert_blender_version(strict); cam=render.setup_master_camera("terrain"); cam.data.ortho_scale=ortho; render.setup_lighting(); path.parent.mkdir(parents=True,exist_ok=True); render.configure_render("terrain",path,transparent=False); sc=bpy.context.scene; sc.render.resolution_x=resolution[0]; sc.render.resolution_y=resolution[1]; sc.render.resolution_percentage=100; bpy.ops.render.render(write_still=True); render.save_blend(blend)


def generate_family_review(family,seed,output,strict,core_builder):
    if family not in SUITE_V6_FAMILIES: raise ValueError(family)
    if family=="coast": generate_coast_review(seed,output,strict,core_builder); return
    render.reset_scene()
    for idx,(q,r) in enumerate(FLOWER7):
        variant=idx%SUITE_V6_VARIANTS[family]; local=derive_seed(seed,"suite-v6-family",family,idx,variant); before=set(bpy.context.scene.objects); build_candidate_tile(family,variant,local,core_builder); _translate_new(before,q,r)
    ortho=12.2 if family in {"mountain","peak"} else 11.4
    _render(output/"review"/f"terrain_suite_v6_{family}_1920x1080.png",output/"review"/f"terrain_suite_v6_{family}.blend",ortho,strict)


def generate_coast_review(seed,output,strict,core_builder):
    render.reset_scene(); layout={(-1,0):"meadow",(-1,1):"meadow",(0,1):"plains",(0,0):"meadow",(1,0):"shallow_sea",(1,-1):"shallow_sea",(0,-1):"open_sea"}; positions=[_world_pos(q,r) for q,r in layout]; centre=(sum(x for x,_ in positions)/len(positions),sum(y for _,y in positions)/len(positions)); forced=(0,1,2,3,4); cc=0
    for idx,((q,r),kind) in enumerate(layout.items()):
        before=set(bpy.context.scene.objects); build_candidate_tile(kind,idx%4,derive_seed(seed,"suite-v6-coast-base",q,r),core_builder)
        if kind not in SEA_KINDS:
            for (dq,dr),edge in AXIAL_EDGE.items():
                if layout.get((q+dq,r+dr)) in SEA_KINDS:
                    cv=forced[cc%len(forced)]%COAST_VARIANT_COUNT; cc+=1; geo.create_coast_edge(edge,random.Random(coast_asset_seed(seed,cv,edge)),morphology=cv)
        _translate_new(before,q,r,centre)
    _render(output/"review"/"terrain_suite_v6_coast_1920x1080.png",output/"review"/"terrain_suite_v6_coast.blend",10.6,strict)


def generate_all_family_reviews(seed,output,strict,core_builder):
    for family in SUITE_V6_FAMILIES: generate_family_review(family,derive_seed(seed,"suite-v6-family-root",family),output,strict,core_builder)


def generate_benchmark36(seed,output,strict,core_builder):
    render.reset_scene(); layout={}
    for r,row in enumerate(BENCHMARK36_V6):
        for q,kind in enumerate(row): layout[(q,r)]=kind
    positions=[_world_pos(q,r) for q,r in layout]; centre=(sum(x for x,_ in positions)/len(positions),sum(y for _,y in positions)/len(positions))
    for idx,((q,r),kind) in enumerate(layout.items()):
        local="water" if kind in SEA_KINDS else kind; variant=idx%SUITE_V6_VARIANTS.get(local,4); local_seed=derive_seed(seed,"suite-v6-benchmark36",q,r,kind,variant); before=set(bpy.context.scene.objects); build_candidate_tile(kind,variant,local_seed,core_builder)
        if kind not in SEA_KINDS:
            for (dq,dr),edge in AXIAL_EDGE.items():
                if layout.get((q+dq,r+dr)) in SEA_KINDS:
                    cv=derive_seed(seed,"suite-v6-coast",q,r)%COAST_VARIANT_COUNT; geo.create_coast_edge(edge,random.Random(coast_asset_seed(seed,cv,edge)),morphology=cv)
        _translate_new(before,q,r,centre)
    _render(output/"review"/"terrain_suite_v6_benchmark36_1920x1080.png",output/"review"/"terrain_suite_v6_benchmark36.blend",24.4,strict)
