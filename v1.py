import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
class Robot:
    def __init__(self, G, start, target, rank, num, map, color):
        self.g = G
        self.target = target
        self.closelist = []
        self.length = 0
        self.rank = rank
        self.map = map
        self.color = color[num]
        self.place = start
        self.nextplace = start

    def findway(self, place):
        path = nx.dijkstra_path(self.g, place, self.target, weight='weight')
        pathlen = nx.dijkstra_path_length(self.g, place, self.target, weight='weight')
        return path, pathlen

    def checkaround(self):
        if self.place == self.target:
            return -1, -1
        Min = float('inf')
        for i in self.g.adj[self.place]:
            if (self.g.nodes[i]['feature'] == 0 or self.rank > self.g.nodes[i]['feature']) and self.g.adj[self.place][i]['state'] == 0 and self.closelist.count(i) == 0:
                kp, kl = self.findway(i)
                if kl+self.g.adj[self.place][i]['weight'] < Min:
                    Min = kl+self.g.adj[self.place][i]['weight']
                    self.nextplace = i
        if self.place != self.nextplace:
            self.g.adj[self.place][self.nextplace]['state'] = 1
            self.g.nodes[self.nextplace]['feature'] = self.rank
            self.map[self.place[1], self.place[0], 0] = 0
            self.map[self.place[1], self.place[0], 1] = 255
            self.map[self.place[1], self.place[0], 2] = 0
            return self.place, self.nextplace
        else:
            return -1, -2

    def domove(self):
        if self.place == self.target:
            return
        if self.place != self.nextplace:
            self.g.nodes[self.place]['feature'] = 0
            self.g[self.place][self.nextplace]['state'] = 0
            self.place = self.nextplace
            for i in range(0, 3):
                self.map[self.place[1], self.place[0], i] = self.color[i]
            self.closelist.append(self.place)
        if self.place == self.target:
            self.g.nodes[self.place]['feature'] = 7
            print(self.closelist)
            return

#匹配车辆在图中颜色
def matchcolor(car_num):
    color = [(0, 0, 0)]*car_num
    spnum = car_num//3 + 1
    pace = 240//spnum
    init = [0, 0, 0]
    for i in range(0, car_num):
        if init[1] < init[0]:
            init[1] += pace
        elif init[2] < init[1]:
            init[2] += pace
        else:
            init[0] += pace
        t = tuple(init)
        color[i] = t
    return color


def buildG():
    G = nx.Graph()
    for i in range(0, 20):
        for k in range(0, 20):
            G.add_node((i, k), feature=0)
    for i in range(0, 20):
        for k in range (0, 20):
            w = np.random.randint(1, 20, size=2)
            if i < 19:
                G.add_edge((i, k), (i+1, k), weight=w[0], state=0)
            if k < 19:
                G.add_edge((i, k), (i, k+1), weight=w[1], state=0)
    return G


Base = [[0, 255, 0]]*20
base1 = [Base]*20
mapbase = np.array(base1, ndmin=3)
G = buildG()
# a = int(input('请输入机器人数量'))
file = open("D:\pycharm\start.txt")
fileline = file.readlines()
a = len(fileline)

color = matchcolor(a)
robot = [None]*a
targetlist = []
for i in range(0, a):
    g = fileline[i].split(';')
    targetlist.append((int(g[2]),int(g[3])))
    robot[i] = Robot(G, (int(g[0]), int(g[1])), (int(g[2]), int(g[3])), 1, i, mapbase, color)
for i in targetlist:
    mapbase[i[1], i[0], 0] = 255
    mapbase[i[1], i[0], 1] = 255
    mapbase[i[1], i[0], 2] = 255
fig = plt.figure()
ax = fig.add_subplot()
x = np.arange(0, 20, 1)
y = np.arange(0, 20, 1)
ax.set(xlim=[0, 20], ylim=[0, 20], xticks=x, yticks=y)


while True:
    for i in range(0, a):
        k1, k2 = robot[i].checkaround()
        if k1 != -1:
            ax.arrow(x=k1[0], y=k1[1], dx=0.8 * (k2[0] - k1[0]), dy=0.8 * (k2[1] - k1[1]), width=0.06, color='black')
    for i in range(0, a):
        robot[i].domove()
    ax.imshow(mapbase, cmap=mpl.cm.spring, vmin=0, vmax=255)
    plt.grid(True)
    plt.show(block=False)
    plt.pause(1)
    flag = True
    for i in range(0, a):
        if G.nodes[targetlist[i]]['feature'] != 7:
            flag = False
            break
    if flag:
        break
