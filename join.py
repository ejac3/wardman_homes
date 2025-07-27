import pandas as pd
import geopandas as gpd

# Load your Wardman homes GeoJSON
wardman = gpd.read_file("wardman_buildings.geojson")

# Load MAR address CSV (from Open Data DC)
mar = pd.read_csv("Address_Residential_Units.csv", dtype=str)

# Preview columns to confirm structure
print("Wardman columns:", wardman.columns)
print("MAR columns:", mar.columns)

# Clean and normalize addresses for better matching
wardman['address_clean'] = wardman['address'].str.strip().str.upper()
mar['address_clean'] = mar['PRIMARY_ADDRESS'].str.strip().str.upper()

# Perform the join on the cleaned address field
joined = pd.merge(
    wardman,
    mar,
    how='left',
    on='address_clean'
)

# Convert back to GeoDataFrame
joined_gdf = gpd.GeoDataFrame(joined, geometry='geometry', crs=wardman.crs)

# Save result
joined_gdf.to_file("wardman_with_mar_ids.geojson", driver="GeoJSON")

print(f"✅ {len(joined_gdf)} rows saved to 'wardman_with_mar_ids.geojson'.")
