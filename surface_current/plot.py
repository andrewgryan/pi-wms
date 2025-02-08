# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "matplotlib",
# ]
# ///
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
    plt.contourf(X, Y, Z, levels)
    plt.contour(X, Y, Z, levels, linewidths=0.1, colors="gray")
    plt.axis("off")
    plt.ylim(min(y), max(y))
    plt.xlim(min(x), max(x))
    plt.savefig("image.png", pad_inches=0, dpi=dpi)


if __name__ == "__main__":
    main()
