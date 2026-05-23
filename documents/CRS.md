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