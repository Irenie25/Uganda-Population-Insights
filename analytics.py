import duckdb


# Location of the DuckDB database
DATABASE_PATH = "data/uganda_population.duckdb"


# Connect to DuckDB
con = duckdb.connect(DATABASE_PATH)


# ------------------------------------------------
# 1. Get the earliest and latest population
# ------------------------------------------------

summary = con.execute("""
    SELECT
        MIN(year) AS first_year,
        MAX(year) AS latest_year,
        MIN(population) AS first_population,
        MAX(population) AS latest_population
    FROM population
""").fetchdf()


print("\nHistorical Population Summary")
print("-----------------------------")

print(summary)


# ------------------------------------------------
# 2. Calculate total population growth
# ------------------------------------------------

growth = con.execute("""
    SELECT
        MIN(year) AS first_year,
        MAX(year) AS latest_year,
        MIN(population) AS first_population,
        MAX(population) AS latest_population,

        MAX(population) - MIN(population)
            AS absolute_growth,

        ((MAX(population) - MIN(population))
            / MIN(population)) * 100
            AS percentage_growth

    FROM population
""").fetchdf()


print("\nPopulation Growth")
print("-----------------")

print(growth)


# ------------------------------------------------
# 3. Calculate Compound Annual Growth Rate
# ------------------------------------------------

cagr = con.execute("""
    SELECT
        MIN(year) AS first_year,
        MAX(year) AS latest_year,

        POWER(
            MAX(population) / MIN(population),
            1.0 / (MAX(year) - MIN(year))
        ) - 1 AS annual_growth_rate

    FROM population
""").fetchdf()


print("\nCompound Annual Growth Rate")
print("---------------------------")

print(cagr)


# ------------------------------------------------
# 4. Calculate year-by-year population growth
# ------------------------------------------------

annual_growth = con.execute("""
    SELECT
        year,
        population,

        LAG(population) OVER (
            ORDER BY year
        ) AS previous_population,

        (
            (population -
             LAG(population) OVER (ORDER BY year))
            /
            LAG(population) OVER (ORDER BY year)
        ) * 100 AS annual_growth_percent

    FROM population

    ORDER BY year
""").fetchdf()


print("\nAnnual Population Growth")
print("------------------------")

print(annual_growth.tail(10))


# Close the database
con.close()