# Raspberry Pi WMS

A demonstration of performing WMS tiling on a Raspberry Pi Zero 2W

![17330911557838338604639678332975](https://github.com/user-attachments/assets/2fb1ff87-ad36-4722-8f74-0d1dd8ee05da)


## Render technology

It is difficult,
but not impossible,
to build a scientific software stack on a Pi Zero.

To rapidly render images,
I chose datashader for my image pipeline.

- `datashader`
- `xarray`
- `colorcet`
- `numpy`


## Server technology

To get this weekend project going quickly,
I used FastAPI to implement HTTP capabilities.

- `fastapi`
- `uvicorn`

## Container technology

A raspberry pi zero has 0.5GB of RAM and 4 cpus.

- `containerd`
- `nerdctl`

Example commands,
they work just like docker.

```sh
# Build the image
nerdctl build -t server:latest .
```

```sh
# Run the image
nerdctl run -d --cpus 1 --memory 250mb -t server:latest --name wms
```

# Benchmark imagery

A matplotlib contour script `bench.py` was optimized to draw contours.

N images | Tile size | N cores | print_png | Artists | Elapsed(s)
-- | -- |-- | -- | -- | --
500  | 256 | 1 | Y | Contours | 15
1000 | 256 | 1 | Y | Contours | 31
1000 | 256 | 1 | Y | Filled | 32
1000 | 256 | 1 | Y | Contours and Filled | 52
1000 | 256 | 1 | Y | Filled then Contour | 35
1000 | 256 | 1 | Y | Filled then Contour w/zorder | 52
1000 | 256 | 1 | Y | Filled, Contour and Quiver | 55
1000 | 256 | 4 | Y | Filled, Contour and Quiver | 15
1000 | 512 | 4 | Y | Filled, Contour and Quiver | 48
1000 | 512 | 4 | Y | Filled, Contour and Quiver | 48
1000 | 512 | 4 | N | Filled, Contour and Quiver | 38

For the 1000 images at 512x512px 70MB were written to disk.
Turning i/o off shaves 10 seconds off a 48 second run.
The problem seems to be compute limited, not disk limited.
