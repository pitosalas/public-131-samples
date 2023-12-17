import random

import graphviz # type: ignore

BOX_FONTSIZE = "11"
LABEL_FONTSIZE = "10"
SUB_LABEL_FONTSIZE = "9"


class Box:
    def __init__(self, label: str, handle: str, dot: graphviz.Digraph, width:int = 80):
        self.handle = handle
        self.label = label
        self.dot = dot
        self.width = width
        self.sections: list[dict[str,object]] = []

    def add_section_to_box(
        self, ident: str, label: str, sub: str, color: str, height: int = 21
    ):
        self.sections.append(
            {
                "ident": ident,
                "label": label,
                "sublabel": sub,
                "height": height,
                "color": color,
            }
        )

    def __str__(self):
        return f"Box: {self.label}  {self.handle}  {self.sections}"


class Tier:
    def __init__(self, label: str, dot: graphviz.Digraph, rank: str):
        self.label = label
        self.dot = dot
        self.boxes: list[Box] = []
        self.rank = rank
        self.digraph = graphviz.Digraph(name=label)

    def add_box_to_tier(self, box: Box):
        self.boxes.append(box)


class Diagram:
    def __init__(self, name: str, rankdir: str = "RL"):
        self.name = name
        self.dot = graphviz.Digraph(name=name)
        self.dot.attr("graph", rankdir=rankdir, ranksep="1.0", fontname="Helvetica")
        self.dot.attr(
            "node",
            shape="none",
            width="0.8",
            margin="0.04 0.04",
            fontsize="8",
            fontname="Helvetica",
        )
        self.dot.attr("edge", arrowsize="0.4")
        self.boxes: dict = {}
        self.tiers: dict = {}

    def add_edge(self, src: str, dest: str, col: str = "black", headclip: str = "true", tailclip: str = "true"):
        self.dot.edge(src, dest, color=col, headclip=headclip, tailclip=tailclip)

    def add_tier(self, name: str, rank: str = "same"):
        self.tiers[name] = Tier(name, self.dot, rank)
        return self.tiers[name]

    def generate_diagram(self):
        for tier in self.tiers.values():
            tier.digraph.attr(rank=tier.rank)
            self.dot.subgraph(tier.digraph)
        self.dot.render(outfile=f"{self.name}.pdf")

    def add_box(self, label: str, handle: str, height: int = 80):
        self.boxes[handle] = Box(label, handle, self.dot, height)
        return self.boxes[handle]

    def render_boxname_in_tier(self, tier: Tier, box_name: str):
        box = self.boxes[box_name]
        self.render_box(box, tier)

    def render_box_in_tier(self, tier: Tier, box: Box):
        self.render_box(box, tier)

    def render_box(self, box, tier: Tier):
        label_start = f"""<<table border="0.1" cellborder="1" cellspacing="0"><TR><TD border="0.0" ><font face="helvetica" color="grey15" point-size="12">{box.label}</font></TD></TR>"""
        label_end = """</table>>"""
        label = label_start
        for section in box.sections:
            sublabel = (
                f"""<br></br><font point-size="{SUB_LABEL_FONTSIZE}">{section["sublabel"]}</font>"""
                if section["sublabel"] is not None
                else ""
            )
            label += f"""<tr><td align="text" color="grey" bgcolor="{section["color"]}" height="{section["height"]}" port="{section["ident"]}">"""
            label += f"""<font point-size="{BOX_FONTSIZE}">{section["label"]}</font>{sublabel}</td></tr>"""
        label += label_end
        subgraph = tier.digraph
        subgraph.node(box.handle, label=label)


pallettes = {
    "p1": ["slategray1", "lightgrey", "cornsilk", "ivory2"],
    "p2": [
        "red",
        "green",
        "blue",
        "orange",
        "purple",
        "pink",
        "brown",
        "black",
        "white",
    ],
    "p3": ["#a6998c", "#f1e0c5", "#9c95dc", "#e84a65", "#cc66c0"],
    "p4": ["#6B240C", "#994D1C", "#E48F45", "#F5CCA0"],
    "p5": ["#c1b8ae", "#c2adbc", "#bd92dd", "#a48cae", "#8b867e", "#6e85af"],
    "p6": ["#FDF7E4", "#FAEED1", "#DED0B6", "#BBAB8C"]
}

class Colors:
    def __init__(self, pallette: str):
        self.palette = pallettes[pallette]
        self.last = 0
        self.flip_flop = True

    def random_color(self) -> str:
        return random.choice(self.palette)

    def color(self, index: int) -> str:
        return self.palette[index % len(self.palette)]

    def rotate(self, max: int = 99) -> str:
        self.last += 1
        max_val = min(max, len(self.palette))
        return self.palette[self.last % max_val]
    
    def adjust_color(self, color: str, amount: int) -> str:
        color_hex = int(color.lstrip("#"), 16)
        red = (color_hex >> 16) & 0xFF
        green = (color_hex >> 8) & 0xFF
        blue = color_hex & 0xFF
        newRed = min(red + amount, 255)
        newGreen = min(green + amount, 255)
        newBlue = min(blue + amount, 255)
        newColor = (newRed << 16) + (newGreen << 8) + newBlue
        hex_str = hex(newColor) # convert int to hex 
        hex_str = hex_str.lstrip("0x") # remove 0x prefix
        return f"#{hex_str}"
    
    def alternate(self, color: str, amount: int) -> str:
        if (self.flip_flop):
            self.flip_flop = False
            return self.adjust_color(color, amount)
        else:
            self.flip_flop = True
            return color