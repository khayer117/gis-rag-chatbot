# Bangladesh Geography and Weather

## 1. Geographic Location
Bangladesh is located in South Asia, bordered by India on three sides (west, north, east),
Myanmar to the southeast, and the Bay of Bengal to the south.
Its geographic coordinates span roughly 20.7°N–26.6°N latitude and 88.0°E–92.7°E longitude.
The country covers an area of approximately 147,570 km².

## 2. Coordinate Reference System for Bangladesh
The standard CRS used in Bangladesh GIS work is EPSG:32646 (WGS 84 / UTM Zone 46N).
For nationwide web maps, EPSG:3857 (Web Mercator) is common.
The national datum is aligned with WGS 84 (EPSG:4326) for GPS compatibility.

## 3. Topography
Bangladesh is one of the world's flattest countries. Over 80% of the land is floodplain
formed by three major river systems. Elevation is generally below 10 meters above sea level
across most of the country. The Chittagong Hill Tracts in the southeast are the only significant
highland, with peaks reaching up to 1,052 m (Keokradong).

## 4. Major River Systems
Bangladesh has three principal river systems:
- **Padma** — lower course of the Ganges; flows southwest into the Bay of Bengal.
- **Jamuna** — local name for the Brahmaputra; one of the widest rivers in the world.
- **Meghna** — formed by the confluence of the Padma and Jamuna near Chandpur.
Together they form the Ganges–Brahmaputra–Meghna (GBM) Delta, the world's largest river delta.

## 5. The Sundarbans
The Sundarbans is the world's largest contiguous mangrove forest, shared between Bangladesh
(approximately 6,017 km²) and India. It lies in the southwest of Bangladesh in the Khulna division.
It is a UNESCO World Heritage Site and home to the Bengal tiger.
Its CRS in spatial analysis is typically EPSG:32646 or EPSG:4326.

## 6. Administrative Divisions
Bangladesh is divided into 8 divisions: Dhaka, Chittagong (Chattogram), Rajshahi, Khulna,
Sylhet, Barisal (Barishal), Rangpur, and Mymensingh. These are subdivided into
64 districts (zila) and further into upazilas. GIS shapefiles of administrative boundaries
are maintained by the Bangladesh Bureau of Statistics (BBS).

## 7. Climate Classification
Bangladesh has a tropical monsoon climate (Köppen: Am/Aw). The climate is characterized
by high humidity, warm temperatures, and distinct wet and dry seasons driven by the monsoon.
Mean annual temperature ranges from 25°C to 30°C across the country.

## 8. Monsoon Season
The southwest monsoon arrives in Bangladesh typically in June and withdraws in October.
This season brings approximately 80% of the country's annual rainfall. Sylhet division in
the northeast receives the highest rainfall, averaging over 4,000 mm/year, while the
western Rajshahi division is comparatively drier at around 1,400 mm/year.

## 9. Annual Rainfall Distribution
Average annual rainfall by division (approximate):
- Sylhet: 4,000–5,000 mm
- Chittagong: 2,800–3,500 mm
- Dhaka: 1,800–2,200 mm
- Khulna: 1,600–1,900 mm
- Rajshahi: 1,400–1,600 mm
Rainfall data is collected by the Bangladesh Meteorological Department (BMD).

## 10. Temperature Extremes
Winter (December–February): temperatures can fall to 5–10°C in the northwest (Rajshahi,
Rangpur divisions). Summer (March–May): pre-monsoon heat brings temperatures above 38°C,
with record highs near 42°C in Rajshahi. Coastal areas near the Bay of Bengal have more
moderate temperatures year-round due to sea influence.

## 11. Cyclone Risk and Bay of Bengal
Bangladesh is one of the most cyclone-prone countries in the world. Tropical cyclones
form in the Bay of Bengal and intensify as they move northward, funneling into the narrowing
coastline. The low elevation of coastal Bangladesh amplifies storm surges.
Notable cyclones: Sidr (2007, Category 4), Aila (2009), Amphan (2020).

## 12. Flood Hazard Zones
Annual flooding affects 20–30% of Bangladesh in a normal year, rising to 60–80% in
severe flood years (e.g., 1988, 1998, 2004). Three types of flooding occur:
- **Riverine flooding** — overflow from the Padma, Jamuna, Meghna.
- **Flash floods** — rapid runoff from hilly areas in Sylhet and Chittagong.
- **Storm surge flooding** — coastal inundation driven by cyclones.
Flood extent mapping in Bangladesh uses Sentinel-1 SAR imagery in EPSG:32646.

## 13. Sea Level Rise Vulnerability
Bangladesh's low-lying coast and delta make it extremely vulnerable to sea level rise.
Current projections estimate 0.5–1.0 m of sea level rise by 2100 under moderate scenarios,
which could inundate up to 17% of the country's land area and displace millions.
The southern coastal belt (Khulna, Barisal, Chittagong coast) is the most at risk.

## 14. Drought and Dry Season
The dry season runs from November to March. Northwestern Bangladesh (Rajshahi, Chapai
Nawabganj) experiences occasional drought due to low rainfall and high evapotranspiration.
The Barind Tract in the northwest is a drought-prone upland area where groundwater
irrigation is critical for agriculture.

## 15. Haor Basin — Wetland Geography
The Haor basin in Sylhet and Mymensingh divisions is a unique bowl-shaped wetland ecosystem
flooded for 6–8 months annually. Major Haors include Hakaluki Haor, Tanguar Haor (Ramsar site),
and Hail Haor. These areas are important for fisheries and biodiversity but face flash floods
from early monsoon that destroy crops before harvest (known as "borna" floods).

## 16. Char Islands
Chars are dynamic riverine islands formed by sediment deposition in the braided channels
of the Jamuna and Padma rivers. They appear, disappear, and shift position frequently.
Bangladesh has thousands of chars, home to millions of people with high flood exposure.
Monitoring char dynamics requires multi-temporal satellite imagery and EPSG:32646 projection.

## 17. Land Use and Agriculture
About 70% of Bangladesh's land area is used for agriculture, primarily rice cultivation.
Land use categories in GIS data:
- Agricultural land: ~8.5 million hectares
- Forest: ~2.5 million hectares (including Sundarbans)
- Water bodies: ~7% of total area
- Urban/built-up: rapidly expanding, especially around Dhaka.

## 18. Urban Heat Island — Dhaka
Dhaka, the capital, is one of the most densely populated cities in the world (~44,000 people/km²).
Rapid urbanization has intensified the urban heat island (UHI) effect. Land surface temperature
(LST) in central Dhaka can exceed surrounding rural areas by 4–8°C during summer.
LST analysis uses Landsat 8/9 Band 10 thermal data reprojected to EPSG:32646.

## 19. Groundwater and Arsenic Contamination
The alluvial aquifers of Bangladesh contain naturally occurring arsenic, affecting an estimated
20 million people who rely on shallow tube wells. Arsenic concentration maps in GIS show
the highest contamination in the Meghna floodplain and southeastern districts.
Spatial data on arsenic is maintained by the Department of Public Health Engineering (DPHE).

## 20. Weather Monitoring Network
The Bangladesh Meteorological Department (BMD) operates a network of weather stations
across the country. Key synoptic stations include Dhaka, Chittagong, Sylhet, Rajshahi,
Khulna, Barisal, Cox's Bazar, and Teknaf. Cox's Bazar station is critical for early
cyclone tracking given its coastal position. BMD data is used for rainfall interpolation
(IDW or Kriging) in GIS to produce spatial rainfall surfaces in EPSG:32646.
