"""
Blender script: tea gift box with separated lid and base.

Model intent:
- Overall assembled size: 260 x 180 x 80 mm
- Plan corner radius: 3 mm
- Lid and base are separate objects
- Lid is slightly larger, base is sized to fit inside with clearance

Run in Blender:
  blender --python tea_tiandi_gift_box.py

Or paste/run from Blender's Text Editor.
"""

from pathlib import Path
import math

import bpy


# -----------------------------
# Key dimensions, in millimeters
# -----------------------------
OUTER_LENGTH_MM = 260.0
OUTER_WIDTH_MM = 180.0
ASSEMBLED_HEIGHT_MM = 80.0
CORNER_RADIUS_MM = 3.0

WALL_THICKNESS_MM = 3.0
BOARD_THICKNESS_MM = 2.0
LID_HEIGHT_MM = 24.0
BODY_HEIGHT_MM = 72.0
LID_CLEARANCE_MM = 1.0

CORNER_SEGMENTS = 28
DISPLAY_GAP_MM = 70.0
SAVE_BLEND = False

DETAIL_OFFSET_MM = 0.35
FOIL_LINE_MM = 1.2
TOP_PANEL_INSET_MM = 13.0
INNER_TRAY_INSET_MM = 18.0


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete()


def configure_units():
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.scale_length = 0.001
    scene.unit_settings.length_unit = "MILLIMETERS"


def make_material(name, color, roughness=0.55, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = color

    bsdf = next((node for node in mat.node_tree.nodes if node.type == "BSDF_PRINCIPLED"), None)
    if bsdf is None:
        bsdf = mat.node_tree.nodes.new(type="ShaderNodeBsdfPrincipled")

    bsdf.inputs["Base Color"].default_value = color
    if "Roughness" in bsdf.inputs:
        bsdf.inputs["Roughness"].default_value = roughness
    if "Metallic" in bsdf.inputs:
        bsdf.inputs["Metallic"].default_value = metallic
    if "Alpha" in bsdf.inputs:
        bsdf.inputs["Alpha"].default_value = color[3]
    if color[3] < 1.0:
        mat.blend_method = "BLEND"
        if hasattr(mat, "use_screen_refraction"):
            mat.use_screen_refraction = True
    return mat


def rounded_rect_points(length, width, radius, segments):
    """Return counter-clockwise points for a rounded rectangle in the XY plane."""
    half_l = length / 2.0
    half_w = width / 2.0
    radius = min(radius, half_l - 0.01, half_w - 0.01)

    corners = [
        (half_l - radius, half_w - radius, 0.0, 90.0),
        (-half_l + radius, half_w - radius, 90.0, 180.0),
        (-half_l + radius, -half_w + radius, 180.0, 270.0),
        (half_l - radius, -half_w + radius, 270.0, 360.0),
    ]

    points = []
    for cx, cy, start, end in corners:
        for i in range(segments + 1):
            if points and i == 0:
                continue
            angle = math.radians(start + (end - start) * i / segments)
            points.append((cx + math.cos(angle) * radius, cy + math.sin(angle) * radius))

    return points


def add_loop(vertices, points, z):
    start = len(vertices)
    for x, y in points:
        vertices.append((x, y, z))
    return list(range(start, start + len(points)))


def add_strip(faces, loop_a, loop_b, reverse=False):
    count = len(loop_a)
    for i in range(count):
        j = (i + 1) % count
        face = [loop_a[i], loop_a[j], loop_b[j], loop_b[i]]
        faces.append(list(reversed(face)) if reverse else face)


def add_ring(faces, outer_loop, inner_loop, reverse=False):
    count = len(outer_loop)
    for i in range(count):
        j = (i + 1) % count
        face = [outer_loop[i], outer_loop[j], inner_loop[j], inner_loop[i]]
        faces.append(list(reversed(face)) if reverse else face)


def create_open_body(name, length, width, height, wall, floor, radius, material):
    inner_length = length - 2.0 * wall
    inner_width = width - 2.0 * wall
    inner_radius = max(radius - wall, 0.6)

    outer_pts = rounded_rect_points(length, width, radius, CORNER_SEGMENTS)
    inner_pts = rounded_rect_points(inner_length, inner_width, inner_radius, CORNER_SEGMENTS)

    vertices = []
    faces = []

    outer_bottom = add_loop(vertices, outer_pts, 0.0)
    outer_floor = add_loop(vertices, outer_pts, floor)
    outer_top = add_loop(vertices, outer_pts, height)
    inner_floor = add_loop(vertices, inner_pts, floor)
    inner_top = add_loop(vertices, inner_pts, height)

    add_strip(faces, outer_bottom, outer_top)
    add_strip(faces, inner_floor, inner_top, reverse=True)
    add_ring(faces, outer_top, inner_top, reverse=True)
    add_ring(faces, outer_floor, inner_floor, reverse=True)
    faces.append(list(reversed(outer_bottom)))
    faces.append(inner_floor)

    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    add_small_edge_softening(obj)
    return obj


def create_inverted_lid(name, length, width, height, wall, top, radius, material):
    inner_length = length - 2.0 * wall
    inner_width = width - 2.0 * wall
    inner_radius = max(radius - wall, 0.6)
    ceiling_z = height - top

    outer_pts = rounded_rect_points(length, width, radius, CORNER_SEGMENTS)
    inner_pts = rounded_rect_points(inner_length, inner_width, inner_radius, CORNER_SEGMENTS)

    vertices = []
    faces = []

    outer_bottom = add_loop(vertices, outer_pts, 0.0)
    outer_ceiling = add_loop(vertices, outer_pts, ceiling_z)
    outer_top = add_loop(vertices, outer_pts, height)
    inner_bottom = add_loop(vertices, inner_pts, 0.0)
    inner_ceiling = add_loop(vertices, inner_pts, ceiling_z)

    add_strip(faces, outer_bottom, outer_top)
    add_strip(faces, inner_bottom, inner_ceiling, reverse=True)
    add_ring(faces, outer_bottom, inner_bottom)
    add_ring(faces, outer_ceiling, inner_ceiling, reverse=True)
    faces.append(outer_top)
    faces.append(list(reversed(inner_ceiling)))

    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    add_small_edge_softening(obj)
    return obj


def add_small_edge_softening(obj, width=0.65, segments=4):
    bevel = obj.modifiers.new(f"{width:.2f}mm soft paper edge", "BEVEL")
    bevel.width = width
    bevel.segments = segments
    try:
        bevel.affect = "EDGES"
    except TypeError:
        pass

    weighted_normals = obj.modifiers.new("weighted paper normals", "WEIGHTED_NORMAL")
    weighted_normals.keep_sharp = True


def add_label(text, location, size=8.0):
    curve = bpy.data.curves.new(text, type="FONT")
    curve.body = text
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = size
    curve.extrude = 0.05

    obj = bpy.data.objects.new(text, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.rotation_euler[0] = math.radians(70.0)
    return obj


def add_dimension_box(name, length, width, height, material):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, height / 2.0))
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = (length, width, height)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.display_type = "WIRE"
    obj.hide_render = True
    obj.data.materials.append(material)
    return obj


def create_rounded_slab(name, length, width, thickness, radius, material, location):
    pts = rounded_rect_points(length, width, radius, CORNER_SEGMENTS)
    vertices = []
    faces = []

    bottom = add_loop(vertices, pts, 0.0)
    top = add_loop(vertices, pts, thickness)
    faces.append(list(reversed(bottom)))
    faces.append(top)
    add_strip(faces, bottom, top)

    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    add_small_edge_softening(obj, width=0.18, segments=2)
    return obj


def create_rounded_ring_slab(name, length, width, ring_width, thickness, radius, material, location):
    inner_length = length - 2.0 * ring_width
    inner_width = width - 2.0 * ring_width
    outer_pts = rounded_rect_points(length, width, radius, CORNER_SEGMENTS)
    inner_pts = rounded_rect_points(inner_length, inner_width, max(radius - ring_width, 0.4), CORNER_SEGMENTS)

    vertices = []
    faces = []

    outer_bottom = add_loop(vertices, outer_pts, 0.0)
    outer_top = add_loop(vertices, outer_pts, thickness)
    inner_bottom = add_loop(vertices, inner_pts, 0.0)
    inner_top = add_loop(vertices, inner_pts, thickness)

    add_ring(faces, outer_top, inner_top)
    add_ring(faces, outer_bottom, inner_bottom, reverse=True)
    add_strip(faces, outer_bottom, outer_top)
    add_strip(faces, inner_bottom, inner_top, reverse=True)

    mesh = bpy.data.meshes.new(f"{name}Mesh")
    mesh.from_pydata(vertices, [], faces)
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    add_small_edge_softening(obj, width=0.12, segments=2)
    return obj


def add_rect_detail(name, location, dimensions, material, bevel_width=0.15):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    obj.data.materials.append(material)
    if bevel_width > 0.0:
        add_small_edge_softening(obj, width=bevel_width, segments=2)
    return obj


def add_cylinder_detail(name, location, radius, depth, material, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    add_small_edge_softening(obj, width=0.12, segments=2)
    return obj


def add_torus_detail(name, location, radius, tube_radius, material):
    bpy.ops.mesh.primitive_torus_add(
        major_segments=128,
        minor_segments=12,
        major_radius=radius,
        minor_radius=tube_radius,
        location=location,
    )
    obj = bpy.context.object
    obj.name = name
    obj.data.materials.append(material)
    return obj


def add_top_text(text, location, material, size=12.0, extrude=0.08):
    curve = bpy.data.curves.new(text, type="FONT")
    curve.body = text
    curve.align_x = "CENTER"
    curve.align_y = "CENTER"
    curve.size = size
    curve.extrude = extrude
    curve.resolution_u = 24

    obj = bpy.data.objects.new(text, curve)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    obj.data.materials.append(material)
    return obj


def add_side_foil_bands(prefix, center_x, length, width, z, material):
    front_y = -width / 2.0 - 0.32
    back_y = width / 2.0 + 0.32
    left_x = center_x - length / 2.0 - 0.32
    right_x = center_x + length / 2.0 + 0.32

    add_rect_detail(f"{prefix} front foil waist line", (center_x, front_y, z), (length - 14.0, 0.55, 1.1), material)
    add_rect_detail(f"{prefix} back foil waist line", (center_x, back_y, z), (length - 14.0, 0.55, 1.1), material)
    add_rect_detail(f"{prefix} left foil waist line", (left_x, 0.0, z), (0.55, width - 14.0, 1.1), material)
    add_rect_detail(f"{prefix} right foil waist line", (right_x, 0.0, z), (0.55, width - 14.0, 1.1), material)


def add_lid_details(center_x, materials):
    top_z = LID_HEIGHT_MM + DETAIL_OFFSET_MM
    lid_panel_l = OUTER_LENGTH_MM - 2.0 * TOP_PANEL_INSET_MM
    lid_panel_w = OUTER_WIDTH_MM - 2.0 * TOP_PANEL_INSET_MM

    create_rounded_slab(
        "slightly raised wrapped-paper top panel",
        lid_panel_l,
        lid_panel_w,
        0.45,
        CORNER_RADIUS_MM,
        materials["lid_panel"],
        (center_x, 0.0, top_z),
    )
    create_rounded_ring_slab(
        "outer gold foil line on lid top",
        OUTER_LENGTH_MM - 18.0,
        OUTER_WIDTH_MM - 18.0,
        FOIL_LINE_MM,
        0.35,
        CORNER_RADIUS_MM,
        materials["gold"],
        (center_x, 0.0, top_z + 0.55),
    )
    create_rounded_ring_slab(
        "inner gold foil line on lid top",
        OUTER_LENGTH_MM - 58.0,
        OUTER_WIDTH_MM - 58.0,
        0.85,
        0.3,
        CORNER_RADIUS_MM,
        materials["gold"],
        (center_x, 0.0, top_z + 0.78),
    )

    create_rounded_slab(
        "raised ivory tea plaque",
        86.0,
        52.0,
        0.75,
        4.0,
        materials["plaque"],
        (center_x, 0.0, top_z + 0.95),
    )
    add_top_text("TEA", (center_x, 7.5, top_z + 1.95), materials["gold"], size=17.0, extrude=0.12)
    add_top_text("PREMIUM GIFT BOX", (center_x, -12.0, top_z + 1.9), materials["deep_green"], size=5.2, extrude=0.06)

    for dx, dy in [(-95.0, -55.0), (95.0, -55.0), (-95.0, 55.0), (95.0, 55.0)]:
        add_cylinder_detail(
            "small gold registration dot",
            (center_x + dx, dy, top_z + 1.05),
            2.2,
            0.32,
            materials["gold"],
            vertices=40,
        )

    add_side_foil_bands("lid upper", center_x, OUTER_LENGTH_MM, OUTER_WIDTH_MM, LID_HEIGHT_MM - 5.0, materials["gold"])
    add_side_foil_bands("lid lower", center_x, OUTER_LENGTH_MM, OUTER_WIDTH_MM, 6.2, materials["shadow_green"])


def add_body_details(center_x, body_length, body_width, materials):
    create_rounded_ring_slab(
        "visible body top rim thickness",
        body_length,
        body_width,
        WALL_THICKNESS_MM + 1.2,
        0.75,
        CORNER_RADIUS_MM,
        materials["body_rim"],
        (center_x, 0.0, BODY_HEIGHT_MM + DETAIL_OFFSET_MM),
    )

    tray_l = body_length - 2.0 * INNER_TRAY_INSET_MM
    tray_w = body_width - 2.0 * INNER_TRAY_INSET_MM
    tray_z = BOARD_THICKNESS_MM + 0.6
    tray = create_open_body(
        "removable molded paper tea insert",
        tray_l,
        tray_w,
        8.0,
        2.0,
        1.0,
        4.0,
        materials["tray"],
    )
    tray.location = (center_x, 0.0, tray_z)

    well_z = tray_z + 8.4
    for dx in (-42.0, 42.0):
        add_cylinder_detail(
            "dark circular tea-can recess",
            (center_x + dx, 0.0, well_z),
            27.0,
            0.45,
            materials["recess"],
            vertices=128,
        )
        add_torus_detail(
            "thin gold rim around tea-can recess",
            (center_x + dx, 0.0, well_z + 0.32),
            27.0,
            0.45,
            materials["gold"],
        )

    add_rect_detail(
        "raised divider between tea recesses",
        (center_x, 0.0, well_z + 1.0),
        (3.0, tray_w - 18.0, 2.0),
        materials["body_rim"],
        bevel_width=0.25,
    )

    add_side_foil_bands("body", center_x, body_length, body_width, BODY_HEIGHT_MM - 12.0, materials["shadow_green"])
    add_side_foil_bands("body lower", center_x, body_length, body_width, 13.0, materials["gold"])


def setup_lighting_and_camera():
    bpy.ops.object.light_add(type="AREA", location=(0.0, -260.0, 260.0))
    key = bpy.context.object
    key.name = "large softbox"
    key.data.energy = 500.0
    key.data.size = 340.0

    bpy.ops.object.camera_add(location=(230.0, -380.0, 210.0), rotation=(math.radians(62), 0.0, math.radians(36)))
    camera = bpy.context.object
    bpy.context.scene.camera = camera
    camera.data.lens = 50.0
    camera.data.dof.use_dof = True
    camera.data.dof.focus_distance = 460.0
    camera.data.dof.aperture_fstop = 7.0

    bpy.context.scene.render.engine = "CYCLES"
    bpy.context.scene.cycles.samples = 96
    bpy.context.scene.view_settings.view_transform = "Filmic"
    bpy.context.scene.view_settings.look = "Medium High Contrast"


def main():
    clear_scene()
    configure_units()

    lid_mat = make_material("tea green wrapped lid", (0.03, 0.21, 0.16, 1.0), 0.62)
    lid_panel_mat = make_material("subtle darker green top paper panel", (0.02, 0.16, 0.12, 1.0), 0.68)
    body_mat = make_material("warm ivory paper body", (0.86, 0.80, 0.68, 1.0), 0.58)
    body_rim_mat = make_material("compressed ivory board edges", (0.72, 0.66, 0.52, 1.0), 0.64)
    tray_mat = make_material("molded cream paper insert", (0.79, 0.74, 0.62, 1.0), 0.72)
    plaque_mat = make_material("matte ivory label plaque", (0.90, 0.84, 0.68, 1.0), 0.52)
    gold_mat = make_material("satin gold foil stamping", (1.0, 0.72, 0.24, 1.0), 0.28, metallic=0.65)
    shadow_green_mat = make_material("debossed dark green side detail", (0.01, 0.09, 0.07, 1.0), 0.7)
    recess_mat = make_material("shadowed tea-can recesses", (0.045, 0.038, 0.032, 1.0), 0.78)
    guide_mat = make_material("assembled size guide", (0.3, 0.3, 0.3, 0.25), 0.4)
    text_green_mat = make_material("printed deep green text", (0.015, 0.11, 0.08, 1.0), 0.45)

    detail_materials = {
        "lid_panel": lid_panel_mat,
        "plaque": plaque_mat,
        "gold": gold_mat,
        "deep_green": text_green_mat,
        "shadow_green": shadow_green_mat,
        "body_rim": body_rim_mat,
        "tray": tray_mat,
        "recess": recess_mat,
    }

    lid_inner_l = OUTER_LENGTH_MM - 2.0 * WALL_THICKNESS_MM
    lid_inner_w = OUTER_WIDTH_MM - 2.0 * WALL_THICKNESS_MM
    body_l = lid_inner_l - 2.0 * LID_CLEARANCE_MM
    body_w = lid_inner_w - 2.0 * LID_CLEARANCE_MM

    body = create_open_body(
        "box body - separated",
        body_l,
        body_w,
        BODY_HEIGHT_MM,
        WALL_THICKNESS_MM,
        BOARD_THICKNESS_MM,
        CORNER_RADIUS_MM,
        body_mat,
    )

    lid = create_inverted_lid(
        "box lid - separated",
        OUTER_LENGTH_MM,
        OUTER_WIDTH_MM,
        LID_HEIGHT_MM,
        WALL_THICKNESS_MM,
        BOARD_THICKNESS_MM,
        CORNER_RADIUS_MM,
        lid_mat,
    )

    body.location.x = -(OUTER_LENGTH_MM + DISPLAY_GAP_MM) / 2.0
    lid.location.x = (OUTER_LENGTH_MM + DISPLAY_GAP_MM) / 2.0

    add_lid_details(lid.location.x, detail_materials)
    add_body_details(body.location.x, body_l, body_w, detail_materials)

    guide = add_dimension_box(
        "260 x 180 x 80 mm assembled envelope guide",
        OUTER_LENGTH_MM,
        OUTER_WIDTH_MM,
        ASSEMBLED_HEIGHT_MM,
        guide_mat,
    )
    guide.location.y = 150.0

    add_label("BOX BODY 252 x 172 x 72 mm", (body.location.x, -120.0, 10.0))
    add_label("BOX LID 260 x 180 x 24 mm", (lid.location.x, -120.0, 10.0))
    add_label("ASSEMBLED SIZE 260 x 180 x 80 mm", (0.0, 38.0, 92.0), size=7.0)

    overlap = BODY_HEIGHT_MM + LID_HEIGHT_MM - ASSEMBLED_HEIGHT_MM
    add_label(f"LID OVERLAP {overlap:.0f} mm / R{CORNER_RADIUS_MM:.0f} CORNERS", (0.0, 178.0, 10.0), size=6.5)

    setup_lighting_and_camera()

    if SAVE_BLEND:
        output_dir = Path(__file__).resolve().parent if "__file__" in globals() else Path.cwd()
        bpy.ops.wm.save_as_mainfile(filepath=str(output_dir / "tea_tiandi_gift_box.blend"))


if __name__ == "__main__":
    main()
