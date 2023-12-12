from diag.diag import Diagram, Colors
HEIGHT = 18
d =  Diagram("memsim/diag/diagsample3", "LR")
colors = Colors("p4")

box1 = d.add_box("file pointer", "box1")
box2 = d.add_box("file block 1", "box2")
box3 = d.add_box("file block 2", "box3")
box4 = d.add_box("file block 3", "box4")

t1 = d.add_tier("left", rank="sink")
t3 = d.add_tier("right", rank="source")

box1.add_section_to_box("header", "part of inode", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block1", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block2", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block3", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block4", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block5", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("block6", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box2.add_section_to_box("pointer", "ptr to next", None, colors.alternate(colors.color(3), -10), HEIGHT)

box3.add_section_to_box("block1", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("block2", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("block3", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("block4", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("block5", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("block6", "Data Block",None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("pointer", "ptr to next", None, colors.alternate(colors.color(3), -10), HEIGHT)

box4.add_section_to_box("block1", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("block2", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("block3", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("block4", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("block5", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("block6", "Data Block", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("pointer", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)

d.render_box(box1, t1) 
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)

d.add_edge("box1:header:c", "box2:block1", "red", tailclip="false")
d.add_edge("box2:pointer:c", "box3:block1", "red", tailclip="false")
d.add_edge("box3:pointer:c", "box4:block1", "red", tailclip="false")


d.generate_diagram()
