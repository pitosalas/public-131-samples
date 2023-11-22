from diag import Diagram

d =  Diagram("diagsample5", "RL")

t1 = d.add_tier("left", rank="sink")
t2 = d.add_tier("second", rank="source")
t3 = d.add_tier("thrd", rank="min")


box1 = d.add_box("File header", "box1")
colors = ["bisque2", "bisque2"]
for i in range(1, 10):
    box1.add_section_to_box(f"d{i}", "direct", "(pointer)", colors[i % 2])

colors = ["cadetblue1", "cadetblue1"]
for i in range(10, 13):
    box1.add_section_to_box(f"d{i}", "indirect", "(pointer)", colors[i % 2])

label = ["ind ptr index", "dbl ind ptrs", "trip ind ptrs"]
colors = ["deepskyblue", "cornsilk1", "cornsilk2"]
for i in range(0,3):
    box = d.add_box(label[i], f"indir{i}")
    for j in range(0,5):
        box.add_section_to_box(f"{i}{j}", "indirect", "(pointer)", colors[i])
    d.render_box(box, t2)

for i in range(0,6):
    box = d.add_box(f"block", f"tiny{i}")
    box.add_section_to_box("only", "data", "data", "grey")
    d.render_box(box, t3)

d.add_edge("box1:d10","indir0", "grey")
d.add_edge("box1:d11","indir1", "grey")
d.add_edge("box1:d12","indir2", "grey")
d.render_box(box1, t1)
d.generate_diagram()
