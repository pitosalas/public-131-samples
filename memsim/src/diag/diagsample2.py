from diag.diag import Diagram
from diag.diag import Colors

HEIGHT = 18

d = Diagram("memsim/diag/diagsample2", "RL")
colors = Colors("p4")

box1 = d.add_box("part of inode", "box1")
box2 = d.add_box("Pointer Block Level 1", "box2")
box3 = d.add_box("Pointer Block Level 2", "box3")
box4 = d.add_box("File Data Blocks", "box4")

t1 = d.add_tier("left", rank="sink")
t2 = d.add_tier("middle", rank="same")
t3 = d.add_tier("right", rank="same")

box1.add_section_to_box(
    "header", "Header", None, colors.alternate(colors.color(3), -10), HEIGHT
)

box2.add_section_to_box(
    "pointer1", "pointer 1", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box2.add_section_to_box(
    "pointer2", "pointer 2", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box2.add_section_to_box(
    "pointer3", "pointer 3", None, colors.alternate(colors.color(3), -10), HEIGHT
)

box3.add_section_to_box(
    "pointer1", "Pointer 1", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer2", "Pointer 2", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer3", "Pointer 3", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer4", "Pointer 4", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer5", "Pointer 5", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer6", "Pointer 6", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box3.add_section_to_box(
    "pointer7", "Pointer 7", None, colors.alternate(colors.color(3), -10), HEIGHT
)

box4.add_section_to_box(
    "block1", "file data", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box4.add_section_to_box(
    "block2", "file data", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box4.add_section_to_box(
    "block3", "file data", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box4.add_section_to_box(
    "block4", "file data", None, colors.alternate(colors.color(3), -10), HEIGHT
)
box4.add_section_to_box(
    "block5", "file data", None, colors.alternate(colors.color(3), -10), HEIGHT
)

d.render_box(box1, t1)
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)

d.add_edge("box1:header", "box2:pointer1", "red")
d.add_edge("box2:pointer3", "box3:pointer1", "red")
d.add_edge("box3:pointer3", "box4:block1", "red")


d.generate_diagram()
