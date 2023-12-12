from diag.diag import Diagram


d =  Diagram("test")

box1 = d.add_box("Box1", "box1")
box2 = d.add_box("Box2", "box2")
box3 = d.add_box("Box3", "box3")
box4 = d.add_box("Box4", "box4")

t1 = d.add_tier("left", rank="sink")
t2 = d.add_tier("middle", rank="source")
t3 = d.add_tier("right", rank="source")

box1.add_section_to_box("a", "life is good")
box1.add_section_to_box("b", "life is good")
box1.add_section_to_box("c", "life is good")
box1.add_section_to_box("d", "life is good")
box1.add_section_to_box("e", "life is good")
box1.add_section_to_box("f", "life is good")
box1.add_section_to_box("g", "life is good")
box1.add_section_to_box("h", "life is good")
box1.add_section_to_box("i", "life is good")
box1.add_section_to_box("j", "life is good")
box1.add_section_to_box("k", "life is good")
box1.add_section_to_box("l", "life is good")
box1.add_section_to_box("m", "life is good")
box1.add_section_to_box("n", "life is good")
box1.add_section_to_box("o", "life is good")
box1.add_section_to_box("p", "life is good")
box1.add_section_to_box("q", "life is good")
box2.add_section_to_box("a", "life is good")
box2.add_section_to_box("b", "life is good")
box2.add_section_to_box("c", "life is good")
box3.add_section_to_box("a", "life is good")
box3.add_section_to_box("b", "life is good")
box3.add_section_to_box("c", "life is good")
box4.add_section_to_box("a", "life is good")
box4.add_section_to_box("b", "life is good")
box4.add_section_to_box("c", "life is good")
box4.add_section_to_box("d", "life is good")
box4.add_section_to_box("e", "life is good")
box4.add_section_to_box("f", "life is good")

d.render_box(box1, t1) 
d.render_box(box2, t2)
d.render_box(box3, t2)
d.render_box(box4, t3)

d.add_edge("box2:a", "box1:a", "red")
d.add_edge("box3:a", "box1:a", "green")
d.add_edge("box3:b", "box1:g", "green")
d.add_edge("box2:a", "box1:c", "red")
d.add_edge("box4:a", "box1:d", "blue")
d.add_edge("box4:c", "box1:c", "blue")



d.generate_diagram()
