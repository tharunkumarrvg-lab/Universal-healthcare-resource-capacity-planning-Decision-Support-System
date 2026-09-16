# Universal Healthcare Resource Capacity Planning Decision Support System

This is an MSc Data Science project focused on hospital capacity planning during emergency patient surges.

The main idea of the project is to help hospitals understand when they may face ICU bed shortages and compare different ways of handling the shortage.

The project uses machine learning, simulation, PostgreSQL and a Streamlit dashboard to test different scenarios and compare their costs and capacity.

## What does the project do?

The system looks at hospital and environmental data and then:

- Predicts patient arrival times using machine learning
- Simulates patient movement and bed occupancy over 24 hours
- Checks for ICU and standard-bed capacity shortages
- Uses Monte Carlo simulation to analyse the risk of capacity breaches
- Allows users to test different bed capacity scenarios
- Compares the cost of different solutions
- Shows the results through an interactive dashboard

## Technologies Used

- Python
- Pandas
- Scikit-learn
- PostgreSQL
- Neon PostgreSQL
- Streamlit
- Matplotlib
- Jupyter Notebook
- SQL
- Monte Carlo Simulation
- Queue Simulation
- Open-Meteo API

## Machine Learning

A Random Forest Regressor was used to predict patient arrival hours.

The model uses features such as:

- Temperature
- Region
- Day of the week

The model results in our project were:

- R²: 0.78
- MSE: 4.05

## Simulation

The system simulates hospital capacity over a 24-hour period.

For the baseline scenario, the model uses:

- 239 Standard Care Beds
- 31 ICU Beds

The simulated ICU demand reaches 75 beds at the peak, which creates a shortage of 44 ICU beds.

The simulation also uses different retention rates for standard and ICU beds to represent patient stay and discharge behaviour.

## Scenarios Tested

We tested four different scenarios:

| Scenario | Solution | ICU Capacity | ICU Buffer | Cost |
|---|---|---:|---:|---:|
| 1 | No additional capacity | 31 | -44 | $0 |
| 2 | Convert 44 standard beds | 75 | 0 | $35,200 |
| 3 | Convert 50 standard beds | 81 | +6 | $40,000 |
| 4 | Rent 50 ICU units | 81 | +6 | $100,000 |

These results are from our project simulation and depend on the assumptions and data used in the model.

## Dashboard

The project includes a Streamlit dashboard where users can change:

- Number of standard beds to rent
- Number of ICU units to rent
- Number of standard beds to convert

The dashboard then shows the resulting capacity, utilization, breach periods and cost.

## Project Files

### `dashboard.py`
The Streamlit dashboard for testing the different scenarios.

### `DS26_Healthcare_DSS_Data_Harmonization.ipynb`
Jupyter Notebook used for data preparation and harmonisation.

### `DSS_Final_Report_99871705_74937166.pdf`
The final academic project report.

### CSV files
The repository also contains the datasets and simulation results used in the project.


  ↓
Scenario Comparison
