import requests
import pandas as pd


# World Bank API for Uganda population
API_URL = (
    "https://api.worldbank.org/v2/country/UGA/"
    "indicator/SP.POP.TOTL"
    "?format=json&per_page=100"
)


def fetch_population_data():

    # Connect to the World Bank API
    response = requests.get(API_URL, timeout=30)

    # Check whether the request was successful
    response.raise_for_status()

    # Convert the response to Python data
    data = response.json()

    # World Bank records are in the second item
    records = data[1]

    # Convert records into a Pandas DataFrame
    df = pd.DataFrame(records)

    # Keep the columns we need
    df = df[
        [
            "countryiso3code",
            "date",
            "value",
            "indicator"
        ]
    ]

    # Rename the columns
    df.columns = [
        "country_code",
        "year",
        "population",
        "indicator"
    ]

    # Extract the indicator name from the World Bank dictionary
    df["indicator"] = df["indicator"].apply(
        lambda x: x["value"] if isinstance(x, dict) else x
    )

    # Convert values to numbers
    df["year"] = pd.to_numeric(df["year"])
    df["population"] = pd.to_numeric(df["population"])

    # Remove missing population values
    df = df.dropna(subset=["population"])

    # Arrange data from oldest to newest
    df = df.sort_values("year")

    return df


# Run the function
if __name__ == "__main__":

    population = fetch_population_data()

    print("\nUganda Population Data")
    print("----------------------")

    print(population.head())

    print("\nLatest Population Records")
    print("-------------------------")

    print(population.tail())