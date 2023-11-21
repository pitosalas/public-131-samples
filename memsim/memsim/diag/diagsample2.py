from diag import Diagram


d =  Diagram("diag/diagsample2", "RL")

box1 = d.add_box("file system root", "box1")
box2 = d.add_box("Pointer Block Level 1", "box2")
box3 = d.add_box("Pointer Block Level 2", "box3")
box4 = d.add_box("File Data Blocks", "box4")

t1 = d.add_tier("left", rank="sink")
t2 = d.add_tier("middle", rank="same")
t3 = d.add_tier("right", rank="same")

box1.add_section_to_box("header", "known place on disk")

box2.add_section_to_box("pointer1", "pointer 1")
box2.add_section_to_box("pointer2", "pointer 2")
box2.add_section_to_box("pointer3", "pointer 3")

box3.add_section_to_box("pointer1", "pointer to next level")
box3.add_section_to_box("pointer2", "pointer to next level")
box3.add_section_to_box("pointer3", "pointer to next level")
box3.add_section_to_box("pointer4", "pointer to next level")
box3.add_section_to_box("pointer5", "pointer to next level")
box3.add_section_to_box("pointer6", "pointer to next level")
box3.add_section_to_box("pointer7", "pointer to next level")

box4.add_section_to_box("block1", "file data")
box4.add_section_to_box("block2", "file data")
box4.add_section_to_box("block3", "file data")
box4.add_section_to_box("block4", "file data")
box4.add_section_to_box("block5", "file data")

d.render_box(box1, t1) 
d.render_box(box2, t3)
d.render_box(box3, t3)
d.render_box(box4, t3)

d.add_edge("box1:header", "box2:pointer1", "red")
d.add_edge("box2:pointer3", "box3:pointer1", "red")
d.add_edge("box3:pointer3", "box4:block1", "red")


d.generate_diagram()
