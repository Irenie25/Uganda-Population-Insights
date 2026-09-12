import duckdb
import pandas as pd
import numpy as np

from statsmodels.tsa.statespace.sarimax import SARIMAX


# -----------------------------------------
# 1. Connect to DuckDB
# -----------------------------------------

DATABASE_PATH = "data/uganda_population.duckdb"

con = duckdb.connect(DATABASE_PATH)


# -----------------------------------------
# 2. Retrieve historical population data
# -----------------------------------------

df = con.execute("""
    SELECT
        year,
        population
    FROM population
    ORDER BY year
""").fetchdf()


con.close()


# -----------------------------------------
# 3. Prepare the time series
# -----------------------------------------

df["year"] = pd.to_numeric(df["year"])
df["population"] = pd.to_numeric(df["population"])

df = df.dropna()

df = df.set_index("year")


# -----------------------------------------
# 4. Fit the forecasting model
# -----------------------------------------

model = SARIMAX(
    df["population"],
    order=(1, 1, 1),
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit(disp=False)


# -----------------------------------------
# 5. Forecast the next 10 years
# -----------------------------------------

forecast = results.get_forecast(steps=10)


forecast_mean = forecast.predicted_mean

confidence = forecast.conf_int()


# -----------------------------------------
# 6. Create forecast dataframe
# -----------------------------------------

forecast_df = pd.DataFrame({
    "year": forecast_mean.index,
    "predicted_population": forecast_mean.values,
    "lower_bound": confidence.iloc[:, 0].values,
    "upper_bound": confidence.iloc[:, 1].values
})


# -----------------------------------------
# 7. Display results
# -----------------------------------------

print("\nPopulation Forecast: 2026–2035")
print("--------------------------------")

print(forecast_df)


# -----------------------------------------
# 8. Display latest historical population
# -----------------------------------------

latest_year = df.index.max()

latest_population = df.loc[
    latest_year,
    "population"
]

print("\nLatest Historical Population")
print("----------------------------")

print(f"{latest_year}: {latest_population:,.0f}")


# -----------------------------------------
# 9. Display 2035 prediction
# -----------------------------------------

prediction_2035 = forecast_df.iloc[-1]

print("\n2035 Forecast")
print("-------------")

print(
    f"Predicted population: "
    f"{prediction_2035['predicted_population']:,.0f}"
)

print(
    f"Lower bound: "
    f"{prediction_2035['lower_bound']:,.0f}"
)

print(
    f"Upper bound: "
    f"{prediction_2035['upper_bound']:,.0f}"
)