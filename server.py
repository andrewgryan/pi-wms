import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse, FileResponse
import xarray as xr
import numpy as np
import datashader as ds
import datashader.transfer_functions as tf
import colorcet

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def index():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
	<base target="_top">
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Pi WMS</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
	<style>
		html, body {
			height: 100%;
			margin: 0;
		}
		.leaflet-container {
			height: 100svh;
			width: 600px;
			max-width: 100%;
			max-height: 100%;
		}
	</style>
</head>
<body>
<div id="map" style="width: 600px; height: 400px;"></div>
<script>
    const map = L.map('map').setView([51.505, -0.09], 13);
    const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);

	// WMS
    const wmsLayer = L.tileLayer.wms("/wms?", {"layers": "foo", "styles": "rainbow"}).addTo(map)
</script>
</body>
</html>
"""

def pre_render():
    n = 32
    path = "tile.png"
    canvas = ds.Canvas(plot_width=256, plot_height=256)
    cmap = getattr(colorcet, "fire")
    q = tf.shade(canvas.quadmesh(rect_data(n),x='x', y='y', agg=ds.mean('Z')), cmap=cmap, alpha=int(0.4 * 255))
    print(q)

    # Save PIL image
    pil = q.to_pil()
    pil.save(path)


# Quadmesh
def rect_data(n):
    # Use realistic Mercator coordinates
    scale = 20e6
    max_x = scale
    min_x = -scale
    max_y = scale
    min_y = -scale
    xs = np.linspace(min_x, max_x, n)
    ys = np.linspace(min_y, max_y, n)
    zs = np.sin(xs * ys[:, np.newaxis] / scale)
    da = xr.DataArray(zs, coords=[('y', ys), ('x', xs)], name='Z')
    return da


DATA_ARRAY = rect_data(128)


@app.get("/wms")
def wms(response_class=HTMLResponse,
        bbox: str = None,
        service: str = "WMS",
        request: str = "GetMap",
        layers: str = "",
        styles: str = "fire",
        transparent: bool = False,
        format: str = "image/png",
        width: int = 256,
        height: int = 256,
    ):
    """Endpoint to satisfy WMS requests"""
    global DATA_ARRAY
    if bbox is not None:
        path = f"{bbox}.png"
        if os.path.exists(path):
            return FileResponse(path)
        else:
            x_min, y_min, x_max, y_max = [float(b) for b in bbox.split(",")]
            canvas = ds.Canvas(plot_width=256, plot_height=256, x_range=(x_min, x_max), y_range=(y_min, y_max))
            cmap = getattr(colorcet, styles)
            q = tf.shade(canvas.quadmesh(DATA_ARRAY, x='x', y='y', agg=ds.mean('Z')), cmap=cmap)
            print(q)

            # Save PIL image
            pil = q.to_pil()
            pil.save(path)
            return FileResponse(path)
    else:
        return FileResponse("tile.png")

@app.get("/quadmesh")
async def quadmesh(n: int = 20, c: str = "fire"):
    path = f"quadmesh_{n}_{c}.png"
    if not os.path.exists(path):
        canvas = ds.Canvas(plot_width=256, plot_height=256)
        cmap = getattr(colorcet, c)
        q = tf.shade(canvas.quadmesh(rect_data(n),x='x', y='y', agg=ds.mean('Z')), cmap=cmap)
        print(q)

        # Save PIL image
        pil = q.to_pil()
        pil.save(path)
    return FileResponse(path)


# On server load
pre_render()

