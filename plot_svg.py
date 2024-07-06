import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import xml.etree.ElementTree as ET

def svg2plt(filename, pltname, xlim, ylim):
    plt.gcf().clf()
    plt.gca().cla()
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root[0][1:]:
        if "path" in child.tag:
            style = child.attrib["style"]
            data = child.attrib["d"]
            styles = {}
            for kv in style.split(";"):
                if len(kv.split(":")) > 1:
                    k = kv.split(":")[0].strip()
                    v = kv.split(":")[1].strip()
                    styles[k] = v
            if "fill" in styles:
                if styles["fill"] == "none":
                    coords = []
                    cnt = 0
                    while cnt < len(data):
                        if data[cnt] == "M":
                            c = data[cnt+1:].split()[:2]
                            coords.append(c)
                        elif data[cnt] == "L":
                            c = data[cnt+1:].split()[:2]
                            coords.append(c)
                        # cnt += 1
                        cnt += (1+len(" ".join(data[cnt].split()[:2])))
                    coords = np.array(coords, dtype=np.float32)
                    stroke_width = 0.5 if int(styles["stroke-width"]) == 2 else 1
                    color = "#c6d4e2" if int(styles["stroke-width"]) == 2 else "#8ba5c1"
                    plt.plot(coords[:,0], coords[:,1], linewidth=stroke_width, c=color)
                else:
                    coords = []
                    cc = []
                    lc = 0
                    cnt = 0
                    while cnt < len(data):
                        if data[cnt] == "M":
                            if cnt > 0:
                                coords = np.array(coords, dtype=np.float32)
                                poly = Polygon(coords, animated=False)
                                plt.gca().add_patch(poly)
                                coords = []
                            c = data[cnt+1:].split()[:2]
                        elif data[cnt] == "L":
                            c = data[cnt+1:].split()[:2]
                        cnt += (1+len(" ".join(data[cnt].split()[:2])))
                        coords.append(c)
                        cc.append(lc)
                        lc += 1
                    coords = np.array(coords, dtype=np.float32)

    plt.gca().set_aspect("equal")
    plt.xlim(*xlim)
    plt.ylim(*ylim)
    plt.savefig(pltname, dpi=300)

svg2plt("pitt.svg", "pitt_mpl.png", xlim=(0,500), ylim=(1000,0))
# svg2plt("phila.svg", "phila_mpl.png", xlim=(0,500), ylim=(1000,0))
# svg2plt("penn_state.svg", "penn_state_mpl.png", xlim=(0,500), ylim=(1000,0))