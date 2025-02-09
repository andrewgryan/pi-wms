# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
# ]
# ///
import matplotlib
matplotlib.use("AGG")
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    print("Hello from bench.py!")
    tile_size = 256

    fig, ax = plt.subplots()
    fig.set_dpi(tile_size)
    fig.set_size_inches(1, 1)
    ax.set_aspect("equal")
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    X, Y = np.meshgrid(np.linspace(0, 1, tile_size), np.linspace(0, 1, tile_size))
    region = fig.canvas.copy_from_bbox(fig.bbox)

    Z = X**2 + Y**2

    N = 1000
    contours = None
    for i in range(N):
        print(i)
        fig.canvas.restore_region(region)
        if contours:
            contours.remove()
        contours = ax.contour(X, Y, Z + np.random.randn() * X)
        fig.canvas.blit(fig.bbox)
        fig.canvas.print_figure(f"pngs/{i}.png")



if __name__ == "__main__":
    main()
