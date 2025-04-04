# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "cartopy",
#     "matplotlib",
# ]
# ///
from collections import namedtuple
import matplotlib.pyplot as plt
import cartopy
import cartopy.crs as ccrs
import numpy as np

EARTH_RADIUS = 6378137.0

BBox = namedtuple("BBox", ("x_min", "y_min", "x_max", "y_max"))


def main() -> None:
    print("Hello from render.py!")
    tile_size = 512
    bbox = BBox(
        x_min=-np.pi * EARTH_RADIUS,
        y_min=-np.pi * EARTH_RADIUS,
        x_max=+np.pi * EARTH_RADIUS,
        y_max=+np.pi * EARTH_RADIUS,
    )
    fig, ax = plt.subplots(subplot_kw={"projection": ccrs.Mercator.GOOGLE})
    fig.set_dpi(tile_size)
    fig.set_size_inches(1, 1)
    ax.set_aspect("equal")
    ax.set_position([0, 0, 1, 1])
    ax.axis("off")
    ax.set_xlim(bbox.x_min, bbox.x_max)
    ax.set_ylim(bbox.y_min, bbox.y_max)

    # Features
    linewidths = 0.04
    ax.coastlines(linewidths=linewidths)
    ax.add_feature(cartopy.feature.BORDERS, linewidths=linewidths)

    # Equator
    fontsize = 1.2
    text = ax.text(0, 0, "0", fontsize=fontsize, va="center", ha="center", color="#333")
    extent = text.get_transform().inverted().transform(text.get_window_extent())
    text_bbox = BBox(x_min=extent[0, 0], y_min=extent[0, 1], x_max=extent[1, 0], y_max=extent[1, 1])
    ax.hlines(0, bbox.x_min, text_bbox.x_min, linewidth=linewidths)
    ax.hlines(0, text_bbox.x_max, bbox.x_max, linewidth=linewidths)

    for lat in [-80, -60, -40, -20, 20, 40, 60, 80]:
        y = EARTH_RADIUS * np.pi * np.sin(np.pi * lat / 180)
        text = ax.text(0, lat, f"{lat}", fontsize=fontsize, va="center", ha="center", color="#333", transform=ccrs.PlateCarree())
        extent = text.get_transform().inverted().transform(text.get_window_extent())
        text_bbox = BBox(x_min=extent[0, 0], y_min=extent[0, 1], x_max=extent[1, 0], y_max=extent[1, 1])
        ax.hlines(y, bbox.x_min, text_bbox.x_min, linewidth=linewidths)
        ax.hlines(y, text_bbox.x_max, bbox.x_max, linewidth=linewidths)

    for lon in [-150, -120, -90, -60, -30, 30, 60, 90, 120, 150]:
        text = ax.text(lon, 0, f"{lon}", fontsize=fontsize, va="center", ha="center", color="#333", transform=ccrs.PlateCarree())

    plt.savefig("tile.png", dpi=tile_size)


if __name__ == "__main__":
    main()
