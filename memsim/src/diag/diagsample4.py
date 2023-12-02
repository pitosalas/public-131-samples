from diag.diag import Diagram, Colors

HEIGHT=19
d =  Diagram("memsim/diag/diagsample4", "LR")
colors = Colors("p4")

box1 = d.add_box("part of inode", "box1")
box2 = d.add_box("Disk block", "box2")
box3 = d.add_box("Disk block", "box3")
box4 = d.add_box("Disk block", "box4")
box5 = d.add_box("Disk block", "box5")

t1 = d.add_tier("left", rank="sink")
t3 = d.add_tier("right", rank="source")

box1.add_section_to_box("pointer1", "to block 1", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("pointer2", "to block 2", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("pointer3", "to block 3", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("pointer4", "to block 4", None, colors.alternate(colors.color(3), -10), HEIGHT)

box1.add_section_to_box("null1", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("null2", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("null3", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("null4", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)
box1.add_section_to_box("null5", "NULL", None, colors.alternate(colors.color(3), -10), HEIGHT)

box2.add_section_to_box("data1", "data block 1", None, colors.alternate(colors.color(3), -10), HEIGHT)
box3.add_section_to_box("data1", "data block 2", None, colors.alternate(colors.color(3), -10), HEIGHT)
box4.add_section_to_box("data1", "data block 3", None, colors.alternate(colors.color(3), -10), HEIGHT)
box5.add_section_to_box("data1", "data block 4", None, colors.alternate(colors.color(3), -10), HEIGHT)

d.render_box(box1, t1) 
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)
d.render_box(box5, t3)

d.add_edge("box1:pointer1:c", "box2:data1", "red", tailclip="false")
d.add_edge("box1:pointer2:c", "box3:data1", "red",tailclip="false")
d.add_edge("box1:pointer3:c","box4:data1", "red", tailclip="false")
d.add_edge("box1:pointer4:c", "box5:data1", "red", tailclip="false")

d.generate_diagram()