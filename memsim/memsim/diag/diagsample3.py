from diag import Diagram

d =  Diagram("diag3", "LR")

box1 = d.add_box("file pointer", "box1")
box2 = d.add_box("file block 1", "box2")
box3 = d.add_box("file block 2", "box3")
box4 = d.add_box("file block 3", "box4")

t1 = d.add_tier("left", rank="sink")
t3 = d.add_tier("right", rank="source")

box1.add_section_to_box("header", "File Header", "known place on disk", "cornsilk2")

box2.add_section_to_box("block1", "Data Block", "data", "cornsilk2")
box2.add_section_to_box("block2", "Data Block", "data", "cornsilk")
box2.add_section_to_box("block3", "Data Block", "data", "cornsilk2")
box2.add_section_to_box("block4", "Data Block", "data", "cornsilk")
box2.add_section_to_box("block5", "Data Block", "data", "cornsilk2")
box2.add_section_to_box("block6", "Data Block", "data", "cornsilk")
box2.add_section_to_box("pointer", "pointer", "to next block", "cornsilk2")

box3.add_section_to_box("block1", "Data Block","data", "cornsilk2")
box3.add_section_to_box("block2", "Data Block","data", "cornsilk")
box3.add_section_to_box("block3", "Data Block","data", "cornsilk2")
box3.add_section_to_box("block4", "Data Block","data", "cornsilk")
box3.add_section_to_box("block5", "Data Block","data", "cornsilk2")
box3.add_section_to_box("block6", "Data Block","data", "cornsilk")
box3.add_section_to_box("pointer", "Pointer", "pointer to next block", "cornsilk2")

box4.add_section_to_box("block1", "Data Block", "data", "cornsilk2")
box4.add_section_to_box("block2", "Data Block", "data", "cornsilk")
box4.add_section_to_box("block3", "Data Block", "data", "cornsilk2")
box4.add_section_to_box("block4", "Data Block", "data", "cornsilk")
box4.add_section_to_box("block5", "Data Block", "data", "cornsilk2")
box4.add_section_to_box("block6", "Data Block", "data", "cornsilk")
box4.add_section_to_box("pointer", "Pointer", "NULL", "cornsilk2")

d.render_box(box1, t1) 
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)

d.add_edge("box1:header", "box2:block1", "grey")
d.add_edge("box2:pointer", "box3:block1", "grey")
d.add_edge("box3:pointer", "box4:block1", "grey")


d.generate_diagram()
