import time
from common.point2d import Point2d
from common.rand_map import RandMap
from ordered_set import OrderedSet


class BSF(object):

    def __init__(self, rand_map):
        self.map = rand_map
        self.close_set = set()
        self.open_set = OrderedSet([self.map.start_point])
        self.order_list = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def search(self, save_images=False):
        start_time = time.time()
        while len(self.open_set) > 0:
            # get point from open set and put it into close set
            point = self.open_set[0]
            self.open_set.remove(point)
            self.close_set.add(point)

            # start to expend
            for order in self.order_list:
                (x, y) = (point.x() + order[0], point.y() + order[1])

                # check whether valid
                if self.is_invalid_point(Point2d(x, y)):
                    continue

                # get new point from map
                new_point = self.map.map[(x, y)]
                new_point.set_parent(point)

                # find end point and end searching
                if new_point == self.map.end_point:
                    self.map.plot_map(new_point, self.open_set, self.close_set)
                    print "find end point, cost time: %.2f s" % (time.time() - start_time)
                    return True

                # update open set
                self.open_set.add(new_point)
                if save_images:
                    self.map.plot_map(open_set=self.open_set, close_set=self.close_set)

        return False

    def is_invalid_point(self, point):
        if (self.map.is_out_of_map(point)) or \
                (point in self.map.obstacle_set) or \
                (point in self.close_set):
            return True
        return False


def main():
    rand_map = RandMap(map_size=10, obstacle_num=4)
    rand_map.set_start_point(0, 4)
    rand_map.set_end_point(9, 4)
    rand_map.plot_map()
    obj = BSF(rand_map)
    obj.search(save_images=True)


if __name__ == '__main__':
    main()
