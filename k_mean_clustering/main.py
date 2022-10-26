#!/usr/bin/env python3.10
import random
import matplotlib.pyplot as plt

from point import Point


class RandomPointCloud(random.Random):

    def __init__(self, seed: str | int | None = None) -> None:
        super().__init__(seed)

    def create(
            self,
            n_pts: int,
            bounds: tuple[float, float] = (0.0, 1.0),
            biases: tuple[float, float, float] = (0.0, 0.0, 0.0),
            dims: int = 2) -> list[Point]:
        return [Point(
            x=self.uniform(*bounds) + biases[0] if dims >= 1 else 0.0,
            y=self.uniform(*bounds) + biases[1] if dims >= 2 else 0.0,
            z=self.uniform(*bounds) + biases[2] if dims >= 3 else 0.0
            ) for _ in range(n_pts)]


class K_Means:

    def __init__(self, k: list[Point], points: list[Point]) -> None:
        self.k_points = k
        self.k_lists = None
        self.points = points
        self.iterations = 0
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(projection='3d')

    def k_distribute(self) -> None:
        self.k_lists = [[] for _ in range(len(self.k_points))]
        for point in self.points:
            shortest = None
            group = None
            for index, k_point in enumerate(self.k_points):
                distance = k_point.distance(point)
                if shortest is None:
                    shortest = distance
                    group = index
                elif shortest > distance:
                    shortest = distance
                    group = index
            self.k_lists[group].append(point)

    def k_mean(self) -> list[Point]:
        ret = []
        for pt_list in self.k_lists:
            length = len(pt_list)
            point = Point()
            for pt in pt_list:
                point += pt
            point /= length
            ret.append(point)
        return ret

    def rec_mean(self) -> None:
        self.iterations += 1
        self.k_distribute()
        pt_mean = self.k_mean()
        end = True
        for m_pt, k_pt in zip(pt_mean, self.k_points):
            if m_pt != k_pt:
                end = False
        print(f"Current points: {self.k_points}\nTarget points: {pt_mean}\nIterations: {self.iterations}")
        x, y, z = Point.extract_from_ptlist(self.k_lists[0])
        x_2, y_2, z_2 = Point.extract_from_ptlist(self.k_lists[1])
        x_3, y_3, z_3 = Point.extract_from_ptlist(self.k_lists[2])
        x_m, y_m, z_m = Point.extract_from_ptlist(self.k_points)
        x_s, y_s, z_s = Point.extract_from_ptlist(Point.subtract_elementwise_ptlist(pt_mean, self.k_points))
        self.ax.clear()
        self.ax.scatter(x, y, z, c='#ff00008f')
        self.ax.scatter(x_2, y_2, z_2, c='#00ff008f')
        self.ax.scatter(x_3, y_3, z_3, c='#0000ff8f')
        self.ax.scatter(x_m, y_m, z_m, c='#000000ff')
        self.ax.quiver(x_m, y_m, z_m, x_s, y_s, z_s, color='#000000ff')
        self.fig.show()
        str_curr_pts = [x.round_display(2) for x in self.k_points]
        str_next_pts = [x.round_display(2) for x in pt_mean]
        plt.title(f'Iteration: {self.iterations}\nCurrent points: {str_curr_pts}\nTarget points: {str_next_pts}\n')
        for angle in range(0, 360 + 1, 3):
            # Normalize the angle to the range [-180, 180] for display
            angle_norm = (angle + 180) % 360 - 180

            # Cycle through a full rotation of elevation, then azimuth, roll, and all
            elev = azim = roll = 0
            if angle <= 360:
                azim = angle_norm

            # Update the axis view and title
            self.ax.view_init(elev, azim, roll)
            plt.draw()
            plt.pause(.001)
        self.k_points = pt_mean
        if not end:
            self.rec_mean()
        else:
            input('Press enter to stop...')


if __name__ == '__main__':
    rpt = RandomPointCloud('test_2')
    tc = rpt.create(100, biases=(1, 0, 0), dims=3)
    tc.extend(rpt.create(100, biases=(0, 1, 0), dims=3))
    tc.extend(rpt.create(100, biases=(0, 0, 1), dims=3))
    km = K_Means(rpt.create(3, dims=2), tc)
    km.rec_mean()
