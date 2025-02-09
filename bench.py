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

    # Figure and Axes setup
    fig, ax = plt.subplots()
    fig.set_dpi(tile_size)
    fig.set_size_inches(1, 1)
    ax.set_aspect("equal")
    ax.set_position([0, 0, 1, 1])
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Snapshot current canvas state
    region = fig.canvas.copy_from_bbox(fig.bbox)

    # Fake data
    X, Y = np.meshgrid(np.linspace(0, 1, tile_size), np.linspace(0, 1, tile_size))

    # Rapidly plot images on same canvas
    N = 1000
    contours = None
    filled_contours = None
    quivers = None
    for i in range(N):
        U = np.random.rand() * X
        V = Y
        Z = np.sqrt(U**2 + V**2)
        print(i)
        fig.canvas.restore_region(region)

        # Filled contours
        if filled_contours:
            filled_contours.remove()
        filled_contours = ax.contourf(X, Y, Z, zorder=1)

        # Contours
        if contours:
            contours.remove()
        contours = ax.contour(X, Y, Z, linewidths=0.1, colors="gray", zorder=2)

        # Quivers every 2**N grid points
        step = 2 ** 4
        if quivers:
            quivers.remove()
        quivers = ax.quiver(X[::step, ::step], Y[::step, ::step], U[::step, ::step], V[::step, ::step], zorder=3)

        fig.canvas.blit(fig.bbox)
        fig.canvas.print_figure(f"pngs/{i}.png", dpi=tile_size)



if __name__ == "__main__":
    main()
