import duckdb
import os

from ingest import fetch_population_data


# Create the data folder if it doesn't exist
os.makedirs("data", exist_ok=True)


# Database location
DATABASE_PATH = "data/uganda_population.duckdb"


# Fetch fresh data from the World Bank API
population_df = fetch_population_data()


# Connect to DuckDB
con = duckdb.connect(DATABASE_PATH)


# Create the population table
con.execute("""
    CREATE TABLE IF NOT EXISTS population (
        country_code VARCHAR,
        year INTEGER,
        population DOUBLE,
        indicator VARCHAR
    )
""")


# Remove old records
con.execute("DELETE FROM population")


# Register the Pandas DataFrame
con.register("population_df", population_df)


# Insert the fresh data into DuckDB
con.execute("""
    INSERT INTO population
    SELECT
        country_code,
        year,
        population,
        indicator
    FROM population_df
""")


# Count the records
count = con.execute("""
    SELECT COUNT(*)
    FROM population
""").fetchone()[0]


print("\nDuckDB Database Updated")
print("-----------------------")

print(f"Records stored: {count}")


# Display the five most recent records
latest = con.execute("""
    SELECT
        year,
        population
    FROM population
    ORDER BY year DESC
    LIMIT 5
""").fetchdf()


print("\nLatest Population Records")
print("-------------------------")

print(latest)


# Close the database
con.close()