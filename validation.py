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
# 2. Get population data
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
# 3. Prepare the data
# -----------------------------------------

df["year"] = pd.to_numeric(df["year"])
df["population"] = pd.to_numeric(df["population"])

df = df.dropna()

df = df.set_index("year")


# -----------------------------------------
# 4. Split into training and testing data
# -----------------------------------------

train = df.loc[:2020]

test = df.loc[2021:2025]


print("\nModel Validation")
print("----------------")

print(f"Training years: {train.index.min()}–{train.index.max()}")
print(f"Testing years: {test.index.min()}–{test.index.max()}")


# -----------------------------------------
# 5. Fit the model using training data
# -----------------------------------------

model = SARIMAX(
    train["population"],
    order=(1, 1, 1),
    enforce_stationarity=False,
    enforce_invertibility=False
)

results = model.fit(disp=False)


# -----------------------------------------
# 6. Predict the testing period
# -----------------------------------------

forecast = results.get_forecast(
    steps=len(test)
)

predicted = forecast.predicted_mean


# -----------------------------------------
# 7. Create comparison table
# -----------------------------------------

comparison = pd.DataFrame({
    "year": test.index,
    "actual_population": test["population"].values,
    "predicted_population": predicted.values
})


# -----------------------------------------
# 8. Calculate prediction error
# -----------------------------------------

comparison["error"] = (
    comparison["actual_population"]
    - comparison["predicted_population"]
)

comparison["absolute_error"] = (
    comparison["error"].abs()
)

comparison["percentage_error"] = (
    comparison["absolute_error"]
    / comparison["actual_population"]
) * 100


# -----------------------------------------
# 9. Calculate performance metrics
# -----------------------------------------

mae = comparison["absolute_error"].mean()

mape = comparison["percentage_error"].mean()


print("\nActual vs Predicted Population")
print("------------------------------")

print(comparison)


print("\nModel Performance")
print("-----------------")

print(f"Mean Absolute Error: {mae:,.0f} people")

print(f"Mean Absolute Percentage Error: {mape:.2f}%")


# -----------------------------------------
# 10. Interpretation
# -----------------------------------------

print("\nInterpretation")
print("--------------")

if mape < 5:
    print("The model shows very strong predictive accuracy.")
elif mape < 10:
    print("The model shows good predictive accuracy.")
elif mape < 20:
    print("The model shows reasonable predictive accuracy.")
else:
    print("The model has relatively high prediction error.")