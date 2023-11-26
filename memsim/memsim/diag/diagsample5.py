from diag import Diagram

palette = ["antiquewhite", "antiquewhite2", "bisque2", "burlywood2", "cornsilk"]
d =  Diagram("memsim/diag/diagsample5", "LR")

first = d.add_tier("cluster_first", rank="sink")
second = d.add_tier("cluster_second", rank="same")
third = d.add_tier("cluster_third", rank="same")
fourth = d.add_tier("cluster_fourth", rank="same")
fifth = d.add_tier("cluster_fifth", rank="source")

# Top level pointers
top = d.add_box("File header", "top")
colors = ["bisque2", "bisque2"]
for i in range(0, 13):
    top.add_section_to_box(f"{i}", "direct", "to data", colors[i % 2], 15)
top.add_section_to_box("13", "to indirect", " ", "antiquewhite")
top.add_section_to_box("14", "to dbl indirect", " ", "antiquewhite")
top.add_section_to_box("15", "to trpl indirect", " ", "antiquewhite")

d.render_box_in_tier(first, top)

# Indirect pointer table (3x)
for i in range(0,3):
    ibox = d.add_box(f"Ind Ptrs {i}" , f"ibox{i}")
    for j in range(0,16):
        ibox.add_section_to_box(f"{j}", " ", " ", "bisque2", 15)

d.render_boxname_in_tier(third, "ibox0")
d.render_boxname_in_tier(second, "ibox1")
d.render_boxname_in_tier(fourth, "ibox2")

# Double indirect pointer table
for i in range(0,2):
    dbox = d.add_box(f"Dbl Indirect Ptrs {i}", f"dbox{i}")
    for j in range(0,10):
        dbox.add_section_to_box(f"{j}", " ", " ", "cornsilk", 15)

d.render_boxname_in_tier(second, "dbox0")
d.render_boxname_in_tier(third, "dbox1")

d.add_edge("top:14","dbox0:4","blue")

# Triple indirect pointer table
tbox = d.add_box("Tripl Ind Ptrs", "tbox0")
for i in range(0,10):
    tbox.add_section_to_box(f"{i}", " ", " ", "burlywood2", 15)
d.render_box_in_tier(second, tbox)

d.add_edge("top:15","tbox0", "green")
d.add_edge("dbox1:1","ibox2", "red")
d.add_edge("tbox0:3","dbox1", "red")

# Actual Data Blocks
for i in range(0,9):
    box = d.add_box(f"block{i}", f"tiny{i}")
    box.add_section_to_box("only", " ", " ", "cornsilk", 10)
    d.render_box_in_tier(fifth, box)

d.add_edge("top:13:c","ibox1", "red")
d.add_edge("ibox0:4:c","tiny2", "red")
d.add_edge("ibox1:3:c","tiny1", "red")
d.add_edge("ibox1:2:c","tiny3", "red")
d.add_edge("ibox2:3:c","tiny4", "red")
d.add_edge("top:0:c","tiny0", "blue")
d.add_edge("dbox0:3:c","ibox0", "orange")
d.generate_diagram()
