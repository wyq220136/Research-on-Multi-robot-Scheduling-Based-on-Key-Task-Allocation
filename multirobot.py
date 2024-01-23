import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import random
class Car:
    def __init__(self, name, uid, begin, end):
        self.name = name
        self.uid = uid
        self.begin = begin
        self.end = end
        self.position = begin

    def print_car(self):
        print(self.uid, self.begin, self.end)

    def car_show(self, G):
        G._node[self.begin]['id'] = 2
        G._node[self.end]['id'] = 10

    def find_road(self, G, height, width):
        if self.position != self.end:
            G._node[self.position]['id'] = 2
            path = nx.astar_path(G, self.position, self.end)
            self.position = path[1]




def create_map(height, width):
    G = nx.DiGraph()
    num = 1
    for i in range(width):
        for j in range(height):
            G.add_node((i, j), id=1)
            num += 1
    for x in range(width):
        for y in range(height):
                if x != 0:
                        G.add_edge((x, y), (x-1, y), weight=1)
                if y != 0:
                        G.add_edge((x, y), (x, y-1), weight=1)
                if x != width-1:
                        G.add_edge((x, y), (x+1, y), weight=1)
                if y != height-1:
                        G.add_edge((x, y), (x, y+1), weight=1)
    return G

def draw_map(G, height, width):
    plt.figure(figsize=(width, height))  # 为了防止x,y轴间隔不一样长，影响最后的表现效果，所以手动设定等长
    plt.xlim(-1, width)
    plt.ylim(-1, height)
    my_x_ticks = np.arange(0, width, 1)
    my_y_ticks = np.arange(0, height, 1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.grid(True)
    num = 1
    for i in range(width):
        for j in range(height):
            if G._node[(i, j)]['id'] == 1:
                plt.scatter(i, j, s=200, c='green', marker='s')
                num += 1
            elif G._node[(i, j)]['id'] == 2:
                plt.scatter(i, j, s=200, c='blue', marker='s')
                num += 1
            elif G._node[(i, j)]['id'] == 10:
                plt.scatter(i, j, s=200, c='red', marker='s')
                num += 1
    plt.title("grid map simulation")




if __name__ == '__main__':
    height = 30
    width = 30
    matrix = np.ones((height, width), dtype=int)
    G = create_map(height, width)
    cars = list()
    car1 = Car('car1', 2, (12, 26), (10, 10))
    car2 = Car('car2', 2, (2, 3), (9, 7))
    car3 = Car('car3', 2, (5, 9), (16, 19))
    car4 = Car('Car4', 2, (21, 18), (13, 19))
    car5 = Car('car5', 2, (9, 15), (25, 3))
    cars.append(car1)
    cars.append(car2)
    cars.append(car3)
    cars.append(car4)
    cars.append(car5)
    sum = len(cars)
    for i in range(sum):
        cars[i].car_show(G)
    finish = False
    print(sum)
    while finish != True:
        num = 0
        for i in range(sum):
            if cars[i].position == cars[i].end:
                num += 1
        if num == sum:
            finish = True
            break
        else:
            for i in range(sum):
                cars[i].find_road(G, height, width)
                plt.clf()
                plt.xlim(-1, width)
                plt.ylim(-1, height)
                my_x_ticks = np.arange(0, width, 1)
                my_y_ticks = np.arange(0, height, 1)
                plt.xticks(my_x_ticks)
                plt.yticks(my_y_ticks)
                plt.grid(True)  # 开启栅格
                num = 1
                for i in range(width):
                    for j in range(height):
                        if G._node[(i, j)]['id'] == 1:
                            plt.scatter(i, j, s=200, c='green', marker='s')
                            num += 1
                        elif G._node[(i, j)]['id'] == 2:
                            plt.scatter(i, j, s=200, c='blue', marker='s')
                            num += 1
                        elif G._node[(i, j)]['id'] == 10:
                            plt.scatter(i, j, s=200, c='red', marker='s')
                            num += 1
                plt.title("grid map simulation ")
                plt.pause(0.01)




