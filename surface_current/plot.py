# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
# ]
# ///
import io
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np


def main() -> None:
    print("Hello from plot.py!")


def plot():
    x = np.linspace(0, 1, 512)
    y = np.linspace(0, 1, 512)
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
    color_list = ['#000000', '#380000', '#560000', '#760100', '#980300', '#bb0600', '#df0d00', '#f93500', '#fe6800', '#ff9100', '#ffb402', '#ffd407', '#fff324']
    cmap = (mpl.colors.ListedColormap(color_list)
            .with_extremes(under='yellow', over='magenta'))
    norm = mpl.colors.BoundaryNorm(bounds, cmap.N, extend="both")

    # Outlined contours
    plt.contourf(X, Y, Z, levels, zorder=1, cmap=cmap, norm=norm)
    plt.contour(X, Y, Z, levels, linewidths=0.1, colors="gray", zorder=2)

    # Vectors
    step = 2 ** 5
    offset = step // 2
    QX = X[offset::step, offset::step]
    QY = Y[offset::step, offset::step]
    U = QX**2
    V = QY**2
    plt.quiver(QX, QY, U, V, zorder=3)

    plt.axis("off")
    plt.ylim(min(y), max(y))
    plt.xlim(min(x), max(x))
    return fig


def save(dpi=512):
    buf = io.BytesIO()
    plt.savefig(buf, format="png", pad_inches=0, dpi=dpi)
    # plt.close()
    return buf


if __name__ == "__main__":
    main()
