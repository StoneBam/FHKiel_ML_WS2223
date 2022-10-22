#!/usr/bin/env python3.10
import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

from point import Point


class RandomPointCloud(random.Random):

    def __init__(self, seed: str | int | None = None) -> None:
        super().__init__(seed)

    def create(self, n_pts: int, bounds: tuple[float, float], biases: tuple[float, float, float], dims: int = 2) -> list[Point]:
        return [Point(
            x=self.uniform(*bounds) + biases[0] if dims >= 1 else 0.0,
            y=self.uniform(*bounds) + biases[1] if dims >= 2 else 0.0,
            z=self.uniform(*bounds) + biases[2] if dims >= 3 else 0.0
            ) for _ in range(n_pts)]


global x_m
global y_m
global z_m


if __name__ == '__main__':
    mpl.rcParams['animation.ffmpeg_path'] = r"C:\ffmpeg-5.1.2-essentials_build\bin\ffmpeg.exe"
    rpc = RandomPointCloud('test')
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    rand_point_cloud_a: list[Point] = rpc.create(10, (0, 5), (0, 0, 0), dims=3)
    rand_point_cloud_b: list[Point] = rpc.create(10, (0, 5), (5, 5, 5), dims=3)
    m_points: list[Point] = rpc.create(1, (4, 6), (0, 0, 0), dims=3)
    x, y, z = list(zip(*[(pt.x, pt.y, pt.z) for pt in rand_point_cloud_a]))
    x_2, y_2, z_2 = list(zip(*[(pt.x, pt.y, pt.z) for pt in rand_point_cloud_b]))
    x_m, y_m, z_m = list(zip(*[(pt.x, pt.y, pt.z) for pt in m_points]))
    ax.scatter(x, y, z)
    ax.scatter(x_2, y_2, z_2)
    quiv = ax.quiver(x_m, y_m, z_m, 1, 1, 1, length=1)
    scat = ax.scatter(x_m, y_m, z_m, marker='^')

    def fla(x):
        global x_m
        global y_m
        global z_m
        x_m, y_m, z_m = [(1 + x,), (1 + x,), (1 + x,)]

        global quiv
        global scat
        quiv.remove()
        quiv = ax.quiver(x_m, y_m, z_m, 1, 1, 1, length=1, color='firebrick')
        scat.remove()
        scat = ax.scatter(x_m, y_m, z_m, marker='o', c='firebrick')

    ani = animation.FuncAnimation(fig, func=fla, frames=np.linspace(0, 10, 100), interval=50)
    ani.save("mov.mp4")
    plt.show()
