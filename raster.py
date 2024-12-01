import os
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
import xarray as xr
import numpy as np
import datashader as ds
import datashader.transfer_functions as tf
import colorcet

"""
Example of how to use canvas.raster  

NOTE: This has been copied out of server.py,
      it may need further adjustment to work.
"""


def f(x,y):
    return np.cos((x**2 + y**2)**2)


def sample(fn, n=50, range_=(0.0,2.4)):
    xs = ys = np.linspace(range_[0], range_[1], n)
    x,y = np.meshgrid(xs,ys)
    z = fn(x,y)
    return xr.DataArray(z, coords=[("y", ys), ("x", xs)])


def iterpng(file_like):
    yield from file_like


# On server load
print("rasterization")
da = sample(f)
canvas = ds.Canvas(plot_width=256, plot_height=256)
rasters = {
    "nearest": canvas.raster(da, interpolate="nearest"),
    "linear": canvas.raster(da, interpolate="linear"),
}

@app.get("/image")
async def image(c: str = "fire", interpolate: str = "nearest", encoding: str = "bytesio"):
    print(f"image: {c} {interpolate}")
    shader = tf.shade(rasters[interpolate], cmap=getattr(colorcet, c))
    if encoding.lower() == "pil":
        file_like = shader.to_pil()
    else:
        file_like = shader.to_bytesio()
    print(file_like)
    return StreamingResponse(iterpng(file_like),
        media_type="image/png"
    )

