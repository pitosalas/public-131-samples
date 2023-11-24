from diag import Diagram

palette = ["antiquewhite", "antiquewhite2", "bisque2", "burlywood2", "cornsilk"]
d =  Diagram("memsim/diag/diagsample5", "TB")

left = d.add_tier("left", rank="source")
middle = d.add_tier("second", rank="same")
right = d.add_tier("third", rank="sink")

# Top level pointers
top = d.add_box("File header", "top")
colors = ["bisque2", "bisque2"]
for i in range(0, 9):
    top.add_section_to_box(f"{i}", "direct", "(pointer)", colors[i % 2])
for i in range(10, 13):
    top.add_section_to_box(f"{i}", "indirect", "(pointer)", "antiquewhite")
d.render_box(top, left)

# Indirect pointer table (3x)
for i in range(0,3):
    ibox = d.add_box(f"indirect ptrs {i}" , f"ibox{i}")
    for j in range(0,6):
        ibox.add_section_to_box(f"{j}", "indirect", "(pointer)", "bisque2")
        if i == 0:
            d.render_box(ibox, middle)
        else:
            d.render_box(ibox, right)

d.add_edge("top:10","ibox0", "red")
d.add_edge("ibox0:4","tiny0", "red")
d.add_edge("ibox1:3","tiny1", "red")

# Double indirect pointer table
for i in range(0,3):
    dbox = d.add_box("dbl indirect ptrs", f"dbox{i}")
    for j in range(0,5):
        dbox.add_section_to_box(f"{j}", "indirect", "(pointer)", "cornsilk")
    if i == 0:
        d.render_box(dbox, middle)
    else:
        d.render_box(dbox, right)

d.add_edge("top:11","dbox0:0","blue")
d.add_edge("dbox1:3", "ibox1:0", "purple")

# Triple indirect pointer table
tbox = d.add_box("trip indirect ptrs", "tbox0")
for i in range(0,5):
    tbox.add_section_to_box(f"{i}", "indirect", "(pointer)", "burlywood2")
d.render_box(tbox, middle)
d.add_edge("top:12","tbox0", "green")
d.add_edge("tbox0:2","dbox2", "orange")
d.add_edge("dbox1:4","ibox2", "red")

# Actual Data Blocks
for i in range(0,6):
    box = d.add_box("block", f"tiny{i}")
    box.add_section_to_box("only", "data", "data", "cornsilk")
    d.render_box(box, right)

d.generate_diagram()
