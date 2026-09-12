\# Uganda Population Insights



\## Historical Trends, Forecasts and Data Story



This project is a predictive data dashboard exploring how Uganda's population has changed over time and what historical trends suggest about future population levels.



\## Research Question



How has Uganda's population changed over time, and what does the historical trend suggest about future population levels?



\## Project Objectives



\- Collect Uganda population data from the World Bank API.

\- Store and manage the data using DuckDB.

\- Use SQL queries to analyse historical population trends.

\- Forecast future population levels using a SARIMAX model.

\- Visualize historical trends, forecasts and uncertainty intervals.

\- Deploy the dashboard using Streamlit Community Cloud.



\## Data Source



World Bank Open Data API.



Indicator: Population, total (`SP.POP.TOTL`)



Country: Uganda (`UGA`)



\## Technology Stack



\- Python

\- Pandas

\- Requests

\- DuckDB

\- SQL

\- Statsmodels

\- Plotly

\- Streamlit

\- GitHub Actions



\## Project Pipeline



World Bank API → Python Data Ingestion → Pandas → DuckDB → SQL Analysis → Forecasting → Streamlit Dashboard



\## Key Finding



Uganda's population increased substantially from 1960 to 2025. While the long-term population trend is strongly upward, the recent annual population growth rate has gradually declined.



The forecasting model estimates Uganda's population at approximately \*\*66.9 million people by 2035\*\*, with an uncertainty interval shown in the dashboard.



\## Model Validation



The SARIMAX model was back-tested using historical data from 1960–2020 and tested against 2021–2025 observations.



The model achieved a Mean Absolute Percentage Error (MAPE) of approximately \*\*1.08%\*\* on the test period.



\## Author



Irenie25



\## Disclaimer



The forecast is an analytical estimate based on historical population trends. It should not be interpreted as an official population projection.

