from diag import Diagram, Colors

d = Diagram("memsim/diag/diagsample5", "LR")

first = d.add_tier("cluster_first", rank="sink")
second = d.add_tier("cluster_second", rank="same")
third = d.add_tier("cluster_third", rank="same")
fourth = d.add_tier("cluster_fourth", rank="min")
fifth = d.add_tier("cluster_fifth", rank="source")

# Top level pointers
top = d.add_box("inode", "top")

top.add_section_to_box(f"meta", "meta data", "names, sizes, <br/>owners, dates,<br/> etc.", "darkseagreen2", 50)

colors = Colors("p4")

for i in range(0, 8):
    top.add_section_to_box(f"{i}", "ptr", None, colors.color(6), 18)

top.add_section_to_box("8", "to indirect", None, colors.color(3), 18)
top.add_section_to_box("9", "to dbl indirect", None, colors.color(2), 18)
top.add_section_to_box("10", "to trpl indirect", None, colors.color(3), 18)

d.render_box_in_tier(first, top)

# Indirect pointer table (3x)
for i in range(0, 3):
    ibox = d.add_box(f"Ind Ptrs {i}", f"ibox{i}")
    for j in range(0, 8):
        ibox.add_section_to_box(f"{j}", "-", None, colors.alternate(colors.color(3), -10), 18)

d.render_boxname_in_tier(third, "ibox0")
d.render_boxname_in_tier(second, "ibox1")
d.render_boxname_in_tier(third, "ibox2")

# Double indirect pointer table
for i in range(0, 2):
    dbox = d.add_box(f"Dbl Indirect Ptrs {i}", f"dbox{i}")
    for j in range(0, 8):
        dbox.add_section_to_box(f"{j}", "-", None, colors.alternate(colors.color(2), -10), 18)

d.render_boxname_in_tier(second, "dbox0")
d.render_boxname_in_tier(third, "dbox1")

d.add_edge("top:9:c", "dbox0", "green", tailclip="false")

# Triple indirect pointer table
tbox = d.add_box("Tripl Ind Ptrs", "tbox0")
for i in range(0, 8):
    tbox.add_section_to_box(f"{i}", "-", None, colors.alternate(colors.color(6), -10), 18)
d.render_box_in_tier(second, tbox)

d.add_edge("top:10:c", "tbox0", "orange", tailclip="false")
d.add_edge("dbox1:1:c", "ibox2", "red", tailclip="false")
d.add_edge("tbox0:3:c", "dbox1", "green", tailclip="false")

# Actual Data Blocks
for i in range(0, 9):
    box = d.add_box(f"block{i}", f"tiny{i}")
    box.add_section_to_box("only", "data", None, colors.color(6), 18)
    d.render_box_in_tier(fourth, box)
d.render_boxname_in_tier(second, "tiny0")

d.add_edge("top:8:c", "ibox1", "red", tailclip="false")
d.add_edge("ibox0:4:c", "tiny2", "blue", tailclip="false")
d.add_edge("ibox1:3:c", "tiny1", "blue", tailclip="false")
d.add_edge("ibox1:2:c", "tiny3", "blue", tailclip="false")
d.add_edge("ibox2:3:c", "tiny4", "blue", tailclip="false")
d.add_edge("top:1:c", "tiny0", "blue", tailclip="false")
d.add_edge("dbox0:3:c", "ibox0", "red", tailclip="false")
d.generate_diagram()
