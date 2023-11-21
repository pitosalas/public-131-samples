from diag import Diagram

d =  Diagram("diag3", "LR")

box1 = d.add_box("File header", "box1")
box2 = d.add_box("Disk block", "box2")
box3 = d.add_box("Disk block", "box3")
box4 = d.add_box("Disk block", "box4")
box5 = d.add_box("Disk block", "box5")

t1 = d.add_tier("left", rank="sink")
t3 = d.add_tier("right", rank="source")

box1.add_section_to_box("pointer1", "pointer", "to block 1", "cornsilk")
box1.add_section_to_box("pointer2", "pointer", "to block 2", "cornsilk2")
box1.add_section_to_box("pointer3", "pointer", "to block 3", "cornsilk")
box1.add_section_to_box("pointer4", "pointer", "to block 4", "cornsilk2")

box1.add_section_to_box("null1", "NULL", "null", "cornsilk")
box1.add_section_to_box("null2", "NULL", "null", "cornsilk2")
box1.add_section_to_box("null3", "NULL", "null", "cornsilk")
box1.add_section_to_box("null4", "NULL", "null", "cornsilk2")
box1.add_section_to_box("null5", "NULL", "null", "cornsilk")

box2.add_section_to_box("data1", "data block 1", "for file", "cornsilk2")
box3.add_section_to_box("data1", "data block 2", "for file", "cornsilk2")
box4.add_section_to_box("data1", "data block 3", "for file", "cornsilk2")
box5.add_section_to_box("data1", "data block 4", "for file", "cornsilk2")

d.render_box(box1, t1) 
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)
d.render_box(box5, t3)


d.add_edge("box1:pointer1", "box2:data1", "grey")
d.add_edge("box1:pointer2", "box3:data1", "grey")
d.add_edge("box1:pointer3", "box4:data1", "grey")
d.add_edge("box1:pointer4", "box5:data1", "grey")


d.generate_diagram()
