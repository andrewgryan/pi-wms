# pi-wms

A demonstration of performing WMS tiling on a Raspberry Pi Zero 2W

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
