# Coordinate Reference Systems

## What is a CRS?
A Coordinate Reference System (CRS) defines how geographic locations
on Earth are mapped to coordinates. Every spatial dataset has a CRS
that determines how to interpret its coordinate values.

## Geographic vs Projected CRS
Geographic CRS uses latitude and longitude (angular units, degrees)
on a 3D ellipsoid model of Earth. Example: EPSG:4326 (WGS 84).

Projected CRS converts 3D coordinates to a flat 2D surface using
a map projection. Units are typically meters or feet.
Example: EPSG:32610 (UTM Zone 10N).

## Common EPSG Codes
- EPSG:4326 — WGS 84 (GPS default, GeoJSON default)
- EPSG:3857 — Web Mercator (Google Maps, OpenStreetMap)
- EPSG:32610 — UTM Zone 10N (US West Coast)
- EPSG:32611 — UTM Zone 11N (US Mountain states)
- EPSG:32612 — UTM Zone 12N (US Rocky Mountains)
- EPSG:32614 — UTM Zone 14N (US Central Plains)
- EPSG:32618 — UTM Zone 18N (US East Coast)
- EPSG:27700 — British National Grid (UK)
- EPSG:2154 — RGF93 / Lambert-93 (France)
- EPSG:25832 — ETRS89 / UTM Zone 32N (Central Europe)
- EPSG:31468 — DHDN / Gauss-Krüger Zone 4 (Germany)
- EPSG:4269 — NAD83 (North America)
- EPSG:4267 — NAD27 (older North America surveys)
- EPSG:3310 — California Albers (California statewide analysis)
- EPSG:5070 — NAD83 / Conus Albers (continental US equal-area)
- EPSG:4230 — ED50 (European Datum 1950)
- EPSG:4258 — ETRS89 (European Terrestrial Reference System)
- EPSG:4283 — GDA94 (Australia)
- EPSG:7844 — GDA2020 (Australia, updated)
- EPSG:4167 — NZGD2000 (New Zealand)
- EPSG:2193 — NZTM2000 (New Zealand Transverse Mercator)
- EPSG:4326 is the default CRS for GeoJSON per RFC 7946

## Datums

A datum defines the size and shape of the Earth model and the origin of the coordinate system.

### Horizontal Datums
- **WGS 84** — World Geodetic System 1984; used by GPS globally
- **NAD83** — North American Datum 1983; closely aligned with WGS 84 but differs by up to 1 meter
- **NAD27** — North American Datum 1927; uses Clarke 1866 ellipsoid; can differ from NAD83 by 10–100 m
- **ETRS89** — European Terrestrial Reference System 1989; fixed to the stable part of the Eurasian plate
- **GDA2020** — Geocentric Datum of Australia 2020; aligned with ITRF2014 at epoch 2020.0

### Vertical Datums
- **EGM96** — Earth Gravitational Model 1996; global geoid model used for orthometric heights
- **EGM2008** — higher resolution geoid model, accurate to ~10 cm globally
- **NAVD88** — North American Vertical Datum 1988; used for elevations in the US
- **MSL** — Mean Sea Level; local tidal datum, varies by location

## Map Projections

A map projection is a mathematical transformation from a curved surface (ellipsoid) to a flat plane.

### Conformal Projections (preserve shape/angles)
- **Mercator** — standard for web maps; extreme area distortion at high latitudes
- **Transverse Mercator** — basis for UTM zones; accurate within narrow longitude bands
- **Lambert Conformal Conic** — common for mid-latitude regions; used in US State Plane

### Equal-Area Projections (preserve area)
- **Albers Equal-Area Conic** — used for US national maps; minimizes area distortion
- **Mollweide** — whole-world equal-area projection
- **Sinusoidal** — equal-area; used for some global raster datasets (MODIS)

### Equidistant Projections (preserve distance from specific points)
- **Azimuthal Equidistant** — distances from center point are true; used in UN emblem map
- **Equirectangular (Plate Carrée)** — simplest projection; 1° longitude = 1° latitude in pixels

### Compromise Projections (minimize overall distortion)
- **Robinson** — used by National Geographic for world maps until 1998
- **Winkel Tripel** — current National Geographic standard; balances area, shape, distance

## UTM (Universal Transverse Mercator)

UTM divides the world into 60 north-south zones, each 6° of longitude wide, numbered 1–60 from west to east starting at 180°W.

- Each zone has a central meridian at the middle of the 6° band
- False easting of 500,000 m is applied to keep all coordinates positive
- Northern hemisphere: false northing = 0; Southern hemisphere: false northing = 10,000,000 m
- Accurate within ±0.04% of true distance inside a zone
- Scale factor at central meridian: 0.9996

### Identifying UTM Zone from Longitude
Zone number = floor((longitude + 180) / 6) + 1

Example: longitude -122° (San Francisco) → floor(58/6) + 1 = zone 10

## CRS in Practice

### Checking CRS in Python (pyproj)
```python
from pyproj import CRS
crs = CRS.from_epsg(4326)
print(crs.name)          # WGS 84
print(crs.axis_info)     # [Lat, Lon] in degrees
```

### Reprojecting in Python (pyproj)
```python
from pyproj import Transformer
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3857", always_xy=True)
x, y = transformer.transform(-122.4, 37.8)  # lon, lat → meters
```

### Reprojecting a GeoDataFrame (geopandas)
```python
gdf = gdf.to_crs(epsg=3857)   # reproject to Web Mercator
gdf = gdf.to_crs(epsg=4326)   # back to WGS 84
```

### Checking CRS in QGIS
Layer Properties → Source → Coordinate Reference System shows the assigned CRS. Use the reproject tool (Vector → Data Management → Reproject Layer) to change it.

## CRS and Distance Calculations

- In a **geographic CRS** (EPSG:4326), coordinates are in degrees. You cannot use Euclidean distance — use the Haversine formula or geodesic distance.
- In a **projected CRS** (e.g., UTM), coordinates are in meters. Euclidean distance is valid within the projection's accuracy zone.
- Always reproject to an appropriate projected CRS before computing area or length in GIS software.

## On-the-fly Reprojection

Most GIS software (QGIS, ArcGIS, PostGIS) supports on-the-fly reprojection — displaying layers in a common CRS without altering the source data. The project/map CRS is separate from the layer's own CRS.

## CRS Mismatch Problems

A CRS mismatch occurs when two datasets are assumed to share a CRS but actually do not. Common symptoms:
- Layers that do not spatially align when overlaid
- Features appearing in the wrong country or ocean
- Distance/area calculations that are orders of magnitude off

Always verify CRS metadata when loading new datasets. Do not assume EPSG:4326 just because coordinates look like lat/lon.

## Axis Order

EPSG:4326 officially defines axis order as **latitude first, longitude second**. However, many software libraries (GeoJSON, Leaflet, Mapbox) use **longitude first, latitude second** (x, y order). Always check the library documentation.

In pyproj, use `always_xy=True` to force (longitude, latitude) order regardless of the CRS definition.

## State Plane Coordinate System (SPCS)

The US State Plane system divides states into zones, each with a custom projection optimized for that region. Uses either Lambert Conformal Conic (for east-west states) or Transverse Mercator (for north-south states). Units are typically US survey feet or meters. Highly accurate for local/state-level work but not suitable for multi-state analysis.

## CRS for Web Mapping

- **EPSG:3857** (Web Mercator) is used by all major tile providers (Google Maps, OpenStreetMap, Bing). Tile coordinates are in meters but displayed as if they were lat/lon.
- **EPSG:4326** is used for data exchange and GeoJSON.
- Leaflet and Mapbox accept coordinates in EPSG:4326 (lon, lat) and handle the display projection internally.