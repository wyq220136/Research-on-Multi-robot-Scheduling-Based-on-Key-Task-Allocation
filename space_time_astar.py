import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import networkx as nx

reach = []
res = []
# rrA星类
class rrA:
    def __init__(self, target, G):
        self.target = target
        self.g = G
        self.open = {}
        self.close = {}  # 使用字典来存储关闭列表中的节点和其对应的值

    def getg(self, a):
        if a in self.close:
            return self.close.get(a)
        else:
            p = self.searchb(a)
            if p:
                return p
            else:
                return self.searchf(a)

    def searchb(self, a):
        self.open[self.target] = [abs(a[0]-self.target[0])+abs(a[1]-self.target[1]), 0]
        while self.open:
            n = min(self.open, key=lambda x: self.open[x][0])
            m = self.open[n][1]
            del self.open[n]
            self.close[n] = m
            if n == a:
                return m

            for i in self.g.adj[n]:
                if i not in self.close:
                    g = m+1
                    h = abs(i[0]-a[0])+abs(i[1]-a[1])
                    if i in self.open:
                        if self.open[i][0] > g+h:
                            self.open[i] = [g+h, g]
                    else:
                        self.open[i] = [g+h, g]

    def searchf(self, a):
        self.open[a] = [abs(a[0] - self.target[0]) + abs(a[1] - self.target[1]), 0]
        tmp = {}
        while self.open:
            n = min(self.open, key=lambda x: self.open[x][0])
            m = self.open[n][1]
            del self.open[n]
            tmp[n] = m
            if n in self.close:
                return m + self.close[n]
            for i in self.g.adj[n]:
                if i not in tmp:
                    g = m + 1
                    h = abs(i[0] - self.target[0]) + abs(i[1] - self.target[1])
                    if i in self.open:
                        if self.open[i][0] > g + h:
                            self.open[i] = [g + h, g]
                    else:
                        self.open[i] = [g + h, g]

# 机器人类，只有移动和反馈当前位置功能
class Robot:
    def __init__(self, G, rank, num, color, start, target, map):
        self.rank = rank
        self.num = num
        self.color = color
        self.place = start
        self.target = target
        self.g = G
        self.map = map
        self.footprint = [start]

    def domove(self, path):
        if self.place == self.target:
            return
        if not path:
            return
        tmp = self.place
        self.place = (path[0][0], path[0][1])
        self.map[tmp[1], tmp[0], 0] = 0
        self.map[tmp[1], tmp[0], 2] = 0
        self.map[tmp[1], tmp[0], 1] = 255
        for i in range(0, 3):
            self.map[self.place[1], self.place[0], i] = self.color[i]
        path.pop(0)
        self.footprint.append(self.place)
        if self.place == self.target:
            self.g.nodes[self.place]['feature'] = 1
            reach.append(self.num)
            obsper.append((self.target[0], self.target[1]))
            plt.text(self.target[0]-0.1, self.target[1]-0.1, self.num, color='white')
            print(self.num, self.footprint)
            res.append(self.footprint)
            return

    def getinfo(self):
        return self.place, self.target

obs = []
path = []
obsper = []
tmpobs = []

# 时空A星生成预定表函数
def reservelist(place, target, g, num):
    global tmpobs
    Min = float("inf")
    next = None
    for i in g.adj[place]:
        if g.adj[(i[0], i[1], place[2])][(place[0], place[1], i[2])]['state'] == 1:
            print("=====")
        if obs.count(i) == 0 and g.adj[(i[0], i[1], place[2])][(place[0], place[1], i[2])]['state'] != 1 and obsper.count((i[0], i[1])) == 0 and tmpobs.count((i[0], i[1])) == 0:
            el = rrastar[num].getg((i[0], i[1]))
            if el < Min:
                Min = el
                next = i
    if len(path) >= 3:
        p = path[len(path)-2]
        if (place[0], place[1]) != target and (p[0], p[1]) == (place[0], place[1]) and (place[0], place[1]) == (next[0], next[1]):
            last = next
            Min = float('inf')
            for i in g.adj[place]:
                if obs.count(i) == 0 and g.adj[(i[0], i[1], place[2])][(place[0], place[1], i[2])]['state'] != 1 and obsper.count((i[0], i[1])) == 0 and i != last:
                    el = rrastar[num].getg((i[0], i[1]))
                    if el < Min:
                        Min = el
                        next = i
            tmpobs.append((last[0], last[1]))
    path.append(next)
    g.adj[(place[0], place[1], place[2])][(next[0], next[1], place[2]+1)]['state'] = 1
    if next[2] == 15:
        tmpobs = []
        obs.extend(path)
        return
    else:
        reservelist(next, target, g, num)

# 生成移动窗口拓扑图
def buildtmp():
    G = nx.DiGraph()
    for i in range(0, 50):
        for k in range(0, 50):
            for p in range(16):
                G.add_node((i, k, p))
    for i in range(0, 50):
        for k in range(0, 50):
            for t in range(15):
                if i < 49:
                    G.add_edge((i, k, t), (i+1, k, t+1), weight=1, state=0)
                if k < 49:
                    G.add_edge((i, k, t), (i, k+1, t+1), weight=1, state=0)
                if i > 0:
                    G.add_edge((i, k, t), (i-1, k, t+1), weight=1, state=0)
                if k > 0:
                    G.add_edge((i, k, t), (i, k-1, t+1), weight=1, state=0)
                G.add_edge((i, k, t), (i, k, t+1), weight=1, state=0)
    return G

# 颜色匹配函数，保证机器人颜色在可视化地图中有区分度，用处不大
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

def check(l, G):
    flag = 1
    for i in l:
        if G.nodes[i]['feature'] == 0:
            flag = 0
            break
    return flag

# 随机生成优先级
def matchrank(num):
    r = np.random.randint(0, num, size=num)
    return r

# 生成地图
def buildG():
    G = nx.Graph()
    for i in range(0, 50):
        for k in range(0, 50):
            G.add_node((i, k), feature=0)
    for i in range(0, 50):
        for k in range(0, 50):
            if i < 49:
                G.add_edge((i, k), (i + 1, k), weight=1)
            if k < 49:
                G.add_edge((i, k), (i, k + 1), weight=1)
    return G

Base = [[0, 255, 0]]*50
base1 = [Base]*50
mapbase = np.array(base1, ndmin=3)
G = buildG()
file = open("D:\pycharm\start.txt")         # 将随机生成的起点终点列表导入txt文件，通过读txt文件获得车辆信息
fileline = file.readlines()
a = len(fileline)

color = matchcolor(a)
rank = matchrank(a)
seq = [(rank[i], i) for i in range(a)]
seq.sort()
robot = [None]*a
rrastar = [None]*a
tmp = [None]*a
targetlist = []
startlist = []
for i in range(0, a):
    g = fileline[i].split(' ')
    startlist.append((int(g[0]), int(g[1])))
    targetlist.append((int(g[2]), int(g[3])))


fig = plt.figure()
ax = fig.add_subplot()
x = np.arange(0, 50, 1)
y = np.arange(0, 50, 1)
ax.set(xlim=[0, 50], ylim=[0, 50], xticks=x, yticks=y)
for i in targetlist:
    ax.scatter(i[0], i[1], color='red', s=30, marker='*')

for i in range(len(targetlist)):
    rrastar[i] = rrA(targetlist[i], G)

G1 = buildtmp()
for i in range(len(seq)):
    reservelist((startlist[seq[i][1]][0], startlist[seq[i][1]][1], 0), targetlist[seq[i][1]], G1, seq[i][1])
    robot[seq[i][1]] = Robot(G, rank[i], seq[i][1], color[i], startlist[seq[i][1]], targetlist[seq[i][1]], mapbase)
    tmp[seq[i][1]] = path
    path = []
# 主循环
while True:
    for i in range(16):
        for k in range(a):
            if reach.count(k) == 0:
                robot[k].domove(tmp[k])
        ax.imshow(mapbase, cmap=mpl.cm.spring, vmin=0, vmax=255)
        plt.grid(True)
        plt.show(block=False)
        plt.pause(1)
    tmp = [None]*a
    if check(targetlist, G):
        break
    G1 = buildtmp()
    for i in range(len(seq)):
        if reach.count(seq[i][1]) == 0:
            a1, a2 = robot[int(seq[i][1])].getinfo()
            reservelist((a1[0], a1[1], 0), a2, G1, seq[i][1])
            tmp[seq[i][1]] = path
            path = []
    obs = []
# 标志程序运行完成，输出“oh,yeah"
print("oh, yeah")

con = 0
for i in range(0, 50):
    for j in range(i+1, 50):
        x = res[i]
        y = res[j]
        if len(x) < len(y):
            for k in range(0, len(x)):
                if x[k] == y[k]:
                    con += 1
        else:
            for k in range(0, len(y)):
                if x[k] == y[k]:
                    con += 1
print(con)
print("total time:", len(res[len(res)-1]))

