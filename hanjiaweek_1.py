import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import random

class Node(object):
    def __init__(self, x, y):
        self.father = None
        self.g_value = 0
        self.f_value = 0
        self.x = x
        self.y = y
        self.id = 20*y + x - 20
        self.pos = (x, y)
        self.block = 0

    def compute_fx(self, target, father):
        if father == None:
            print('未设置当前节点的父节点！')
        gx_father = father.g_value
        # 曼哈顿距离
        h_value = abs(self.x - target.x) + abs(self.y - target.y)
        g_value = father.g_value + 1
        f_value = g_value + h_value
        return g_value, f_value

    def set_fx(self, target, father):
        self.g_value, self.f_value = self.compute_fx(target, father)
        self.father = father

    def update_fx(self, target, father):
        g_value, f_value = self.compute_fx(target, father)
        if f_value < self.f_value:
            self.g_value, self.f_value = g_value, f_value
            self.father = father
def get_map(block_list):
    G = nx.Graph()
    for i in range(1, 21):
        for j in range(1, 21):
            t = Node(i, j)
            G.add_node((i, j))
    for i in range(1, 20):
        for j in range(1, 21):
            t = Node(i, j)
            m = Node(i + 1, j)
            flag = 0
            for k in block_list:
                if (t.pos == k or m.pos == k):
                    flag = 1
            if (flag == 0):
                G.add_edge((i,j),(i+1,j))
    for i in range(1, 21):
        for j in range(1, 20):
            t = Node(i, j)
            m = Node(i, j + 1)
            flag = 0
            for k in block_list:
                if (t.pos == k or m.pos == k):
                    flag = 1
            if (flag == 0):
                G.add_edge((i,j),(i,j+1))
    return G
def draw(cur_pos_list, next_pos_list, tar_pos_list):
    plt.figure()
    plt.clf()
    plt.xlim(0.5, 20.5)
    plt.ylim(0.5, 20.5)
    my_x_ticks = np.arange(0, 21, 1)
    my_y_ticks = np.arange(0, 21, 1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    list_length = len(cur_pos_list)
    for i in range(0, list_length):
        plt.scatter(cur_pos_list[i][0], cur_pos_list[i][1], s=100, marker="s", color="y")
        plt.scatter(tar_pos_list[i][0], tar_pos_list[i][1], s=100, marker="s", color="b")
        plt.arrow(cur_pos_list[i][0], cur_pos_list[i][1], next_pos_list[i][0]-cur_pos_list[i][0], next_pos_list[i][1]-cur_pos_list[i][1], head_width=0.3, width=0.2, color='r', length_includes_head=True)
    plt.grid()
    plt.draw()
    plt.show()

def extend(current_node, G, target_node,closed_list, block_list, open_list):
    nodes_neighbor = G[(current_node.x, current_node.y)]
    for node_pos in nodes_neighbor:
        node = Node(node_pos[0], node_pos[1])
        if node_pos in list(map(lambda x: x.pos, closed_list)) or node_pos in block_list:
            continue
        else:
            if node_pos in list(map(lambda x: x.pos, open_list)):
                node.update_fx(target_node, current_node)
            else:
                node.set_fx(target_node, current_node)
                open_list.append(node)
    return current_node

def get_minroute(target_node, start_node):
    minroute = []
    if target_node.pos == start_node.pos:
        minroute.append(start_node.pos)
        minroute.append(start_node.pos)
        return minroute
    current_node = target_node
    while (True):
    # while (current_node.father):
        minroute.append(current_node.pos)
        current_node = current_node.father
        if current_node.pos == start_node.pos:
            break

    minroute.append(start_node.pos)
    minroute.reverse()
    return minroute


class robot(object):
    def __init__(self, sta_pos, tar_pos, G, block_list):
        self.cur_pos = sta_pos
        self.tar_pos = tar_pos
        self.G = G
        self.next_pos = sta_pos
        self.nnext_pos = sta_pos
        self.block_list = block_list
        self.finish_flag = 0

    def Astar(self, cur_pos, tar_pos, block_list):
        G = get_map(block_list)
        finish_flag = self.finish_flag
        next_pos = self.next_pos
        open_list = []  # 创建open_list
        closed_list = []  # 创建closed_list
        start_node = Node(cur_pos[0], cur_pos[1])
        target_node = Node(tar_pos[0], tar_pos[1])
        current_node = start_node
        open_list.append(start_node)
        while (len(open_list) > 0):
            # 查找openlist中fx最小的节点
            fxlist = list(map(lambda x: x.f_value, open_list))
            index_min = fxlist.index(min(fxlist))
            current_node = open_list[index_min]
            del open_list[index_min]
            closed_list.append(current_node)

            # 扩展当前fx最小的节点，并进入下一次循环搜索
            # current_node = extend(current_node, target_node, G, open_list, closed_list, block_list, x_size, y_size)
            current_node = extend(current_node, G, target_node, closed_list, block_list, open_list)
            # 如果open_list列表为空，或者当前搜索节点为目标节点，则跳出循环
            if len(open_list) == 0 or current_node.pos == target_node.pos:
                break
        if current_node.pos == target_node.pos:
            target_node.father = current_node.father
            route_list = get_minroute(target_node, start_node)
            cur_pos = route_list[1]
            if cur_pos == tar_pos:
                finish_flag = 1
                return cur_pos, cur_pos, finish_flag
            else:
                next_pos = route_list[2]
                return cur_pos, next_pos, finish_flag

def main():
    flag = 0
    block_list = []
    car_list = []
    cur_pos_list = []
    tar_pos_list = []
    # next_pos_list = []
    new_cur_pos_list = []
    new_next_pos_list = []
    new_block_list = []
    G = get_map(block_list)
    car_num = input("请输入小车数量：")
    car_num = int(car_num)
    for i in range(0, car_num):
        sta_pos_x = random.randint(1, 20)
        sta_pos_y = random.randint(1, 20)
        tar_pos_x = random.randint(1, 20)
        tar_pos_y = random.randint(1, 20)
        sta_pos = (sta_pos_x, sta_pos_y)
        tar_pos = (tar_pos_x, tar_pos_y)
        car = robot(sta_pos, tar_pos, G, block_list)
        car_list.append(car)
        cur_pos_list.append(sta_pos)
        tar_pos_list.append(tar_pos)
    car_list_length = len(car_list)
    for i in range(0, car_list_length):
        block_list_for_car_i = block_list
        car_list[i].cur_pos, car_list[i].next_pos, car_list[i].finish_flag = car_list[i].Astar(cur_pos_list[i],tar_pos_list[i],block_list_for_car_i)
        new_cur_pos_list.append(car_list[i].cur_pos)
        new_next_pos_list.append(car_list[i].next_pos)
        new_block_list.append(car_list[i].cur_pos)
        new_block_list.append(car_list[i].next_pos)
    cur_pos_list = new_cur_pos_list
    next_pos_list = new_next_pos_list
    block_list = new_block_list
    draw(cur_pos_list, next_pos_list, tar_pos_list)
    while flag == 0:
        new_cur_pos_list = []
        new_next_pos_list = []
        new_block_list = []
        for i in range(0, car_list_length):
            block_list_for_car_i = block_list
            block_list_for_car_i.remove(car_list[i].cur_pos)
            block_list_for_car_i.remove(car_list[i].next_pos)
            car_list[i].cur_pos, car_list[i].next_pos, car_list[i].finish_flag = car_list[i].Astar(cur_pos_list[i], tar_pos_list[i], block_list_for_car_i)
            new_cur_pos_list.append(car_list[i].cur_pos)
            new_next_pos_list.append(car_list[i].next_pos)
            new_block_list.append(car_list[i].cur_pos)
            new_block_list.append(car_list[i].next_pos)
        cur_pos_list = new_cur_pos_list
        next_pos_list = new_next_pos_list
        block_list = new_block_list
        draw(cur_pos_list, next_pos_list, tar_pos_list)
        finish = 0
        for car in car_list:
            if car.finish_flag == 1:
                finish = finish + 1
        if finish == car_list_length:
            flag = 1

if __name__ == '__main__':
    main()