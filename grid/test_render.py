import pytest
import cartopy
import numpy as np
from render import to_y, to_x

@pytest.mark.parametrize("phi", [
    0,
    45,
])
def test_y(phi):
    src = cartopy.crs.PlateCarree()
    dst = cartopy.crs.Mercator.GOOGLE
    _, y = dst.transform_point(0, phi, src)
    assert np.isclose(to_y(phi), y)

@pytest.mark.parametrize("lam", [
    0,
    45,
])
def test_to_x(lam):
    src = cartopy.crs.PlateCarree()
    dst = cartopy.crs.Mercator.GOOGLE
    x, _ = dst.transform_point(lam, 0, src)
    assert np.isclose(to_x(lam), x)
