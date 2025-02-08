# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
# ]
# ///
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    print("Hello from plot.py!")
    x = np.linspace(0, 1, 256)
    y = np.linspace(0, 1, 256)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + Y**2
    levels = np.linspace(0, 2, 20)


    dpi = 512
    fig = plt.figure(dpi=dpi)
    fig.set_size_inches(1, 1)
    ax = plt.gca()
    ax.set_aspect("equal")
    ax.set_position([0, 0, 1, 1])

    # Discrete colors related to surface current
    bounds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1.0, 1.5, 2.0]
    cmap = (mpl.colors.ListedColormap(['red', 'green', 'blue', 'cyan', "orange", "purple", "pink", "indigo", "violet", "teal", "black"])
            .with_extremes(under='yellow', over='magenta'))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="both")

    # Outlined contours
    plt.contourf(X, Y, Z, levels, zorder=1, cmap=cmap, norm=norm)
    plt.contour(X, Y, Z, levels, linewidths=0.1, colors="gray", zorder=2)

    # Vectors
    step = 2 ** 4
    offset = step // 2
    QX = X[offset::step, offset::step]
    QY = Y[offset::step, offset::step]
    U = QX**2
    V = QY**2
    plt.quiver(QX, QY, U, V, zorder=3)

    plt.axis("off")
    plt.ylim(min(y), max(y))
    plt.xlim(min(x), max(x))
    plt.savefig("image.png", pad_inches=0, dpi=dpi)


if __name__ == "__main__":
    main()
