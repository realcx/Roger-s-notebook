import time
import numpy as np
import matplotlib.pyplot as plt
from point2d import Point2d
from ordered_set import OrderedSet
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection


class RandMap(object):

    def __init__(self, map_size=40, obstacle_num=5, random_obstacles=True):
        self.map_size = map_size
        self.map = {}
        self.obstacle_set = set()

        # init map and obstacle points image
        plt.axis('equal')
        plt.axis('off')
        plt.tight_layout()
        self.ax = plt.gca()
        self.ax.set_xlim([0, map_size])
        self.ax.set_ylim([0, map_size])

        # generate map points
        for x in range(self.map_size):
            for y in range(self.map_size):
                self.map[(x, y)] = Point2d(x, y)

        # generate obstacles points
        if random_obstacles:
            self.generate_random_obstacle(obstacle_num)

        # random pick start point until it is not in obstacle set
        (x, y) = self.generate_random_xy()
        while self.map[(x, y)] in self.obstacle_set:
            (x, y) = self.generate_random_xy()
        self.set_start_point(x, y)

        # random pick end point until it is not in obstacle set
        (x, y) = self.generate_random_xy()
        while self.map[(x, y)] in self.obstacle_set or self.map[(x, y)] == self.start_point:
            (x, y) = self.generate_random_xy()
        self.set_end_point(x, y)

        # init map images
        map_patches = []
        for point in self.map.values():
            if point == self.start_point or point == self.end_point or point in self.obstacle_set:
                continue
            rec = Rectangle((point.x(), point.y()), width=1, height=1)
            map_patches.append(rec)
        self.ax.add_collection(PatchCollection(
            map_patches, label='map_points', edgecolor='gray', facecolor='white'))

    def generate_random_xy(self):
        x = np.random.randint(0, self.map_size)
        y = np.random.randint(0, self.map_size)
        return (x, y)

    def generate_random_obstacle(self, obstacle_num):
        for i in range(obstacle_num):
            length = np.random.randint(2, self.map_size // 3)
            width = np.random.randint(2, self.map_size // 3)
            (x0, y0) = self.generate_random_xy()
            self.set_obstacle(x0, y0, length, width)

    def set_start_point(self, x, y):
        for patches in self.ax.collections:
            if patches.get_label() == 'start_point':
                patches.remove()
        self.start_point = self.map[(x, y)]
        self.start_point.set_cost(0)
        rec = Rectangle((x, y), width=1, height=1)
        self.ax.add_collection(PatchCollection([rec], label='start_point', facecolor='b'))

    def set_end_point(self, x, y):
        for patches in self.ax.collections:
            if patches.get_label() == 'end_point':
                patches.remove()
        self.end_point = self.map[(x, y)]
        rec = Rectangle((x, y), width=1, height=1)
        self.ax.add_collection(PatchCollection([rec], label='end_point', facecolor='r'))

    def set_obstacle(self, x0, y0, length, width):
        obstacle_patches = []
        for x in range(x0, min(x0 + width, self.map_size)):
            for y in range(y0, min(y0 + length, self.map_size)):
                self.obstacle_set.add(self.map[(x, y)])
                rec = Rectangle((x, y), width=1, height=1)
                obstacle_patches.append(rec)
                self.ax.add_collection(PatchCollection(
                    obstacle_patches, label='obstacle_points', facecolor='gray'))

    def is_out_of_map(self, point):
        if (point.x(), point.y()) not in self.map:
            return True
        return False

    def generate_path(self, point):
        path = {}
        path['x'] = []
        path['y'] = []
        while point.have_parent():
            path['x'].append(point.x() + 0.5)
            path['y'].append(point.y() + 0.5)
            point = point.parent()
        path['x'].append(point.x() + 0.5)
        path['y'].append(point.y() + 0.5)
        return path

    def save_image(self):
        millis = int(round(time.time() * 1000))
        filename = 'images/' + str(millis) + '.png'
        plt.savefig(filename)

    def plot_map(self, path_point=Point2d(0, 0), open_set=set(), close_set=set()):
        for patches in self.ax.collections:
            if patches.get_label() == 'open_set_points' or \
                    patches.get_label() == 'close_set_points':
                patches.remove()

        open_patches = []
        close_patches = []
        for point in open_set:
            if point == self.end_point:
                continue
            rec = Rectangle((point.x(), point.y()), width=1,
                            height=1, edgecolor='gray', facecolor='g')
            open_patches.append(rec)
        for point in close_set:
            if point == self.start_point:
                continue
            rec = Rectangle((point.x(), point.y()), width=1,
                            height=1, edgecolor='gray', facecolor='y')
            close_patches.append(rec)
        self.ax.add_collection(PatchCollection(
            open_patches, label='open_set_points', edgecolor='gray', facecolor='g'))
        self.ax.add_collection(PatchCollection(
            close_patches, label='close_set_points', edgecolor='gray', facecolor='y'))

        path = self.generate_path(path_point)
        plt.plot(path['x'], path['y'], color='r')
        self.save_image()


def main():
    rand_map = RandMap()
    rand_map.plot_map()


if __name__ == '__main__':
    main()
