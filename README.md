# CA4021 - 2023/2024 Data Science Final Year Project

## Price Profile Computer Application for EV Charging Stations 

- Authors: Krzysztof Baran and Xi Zhang

- Supervisor: Mohammed Amine Togou

- [Final Report](./docs/Price_Profile_Computer_Application_for_EV_Charging_Stations.pdf)

- [Data Source](https://data.cityofpaloalto.org/dataviews/257812/electric-vehicle-charging-station-usage-july-2011-dec-2020/): The data used in this project is an open data resource containing information on the use of electric vehicle charging stations in Palo Alto, California, USA. The dataset contains records from July 2011 to December 2020.

### 1. Abstract
This project aims to develop data-driven strategies for opti- mising management of electric vehicle (EV) charging stations. Regression models such as SARIMA (seasonal auto-regressive integrated moving aver- age), LSTM (long short-term memory), GRU (gated recurrent unit) and TBATS (trigonometric seasonality, Box-Cox transformation, ARMA errors, trend and seasonal components) are constructed to forecast demand of an EV charging station based on past demand data. The models are analysed on accuracy and execution time to determine viability in deploying them in applications. In addition, two algorithms for demand-proportional pricing of electricity at EV charging stations were proposed, denoted as range pricing and percentile pricing. The pricing methods are compared with traditional flat and time of use rates to determine their financial performance and demand-proportionality. Finally, a Python computer application is presented, allowing for exploitation of the aforementioned demand forecasting models and demand-proportional pricing methods by EV charging station analysts. 

### 2. Repository Structure

#### 2.1 application

- [data](./application/data)
- [images](./application/images)
- [screenshots](./application/screenshots)
- [requirements.txt](./application/requirements.txt)
- [scripts](./application/scripts)

#### 2.2 docs

- [Project Proposal](./docs/CA4021 Project Proposal.pdf)
- [Final Report](./docs/Price_Profile_Computer_Application_for_EV_Charging_Stations.pdf) 

#### 2.3 tests
- [data](./tests/data)
    - [accuracy_results](./tests/data/accuracy_results)
    - [clean_data](./tests/data/clean_data)
    - [data_for_queries](./tests/data/data_for_queries)
    - [demand_proportionality_results](./tests/data/demand_proportionality_results)
    - [execution_time_results](./tests/data/execution_time_results)
    - [queries_results](./tests/data/queries_results)
    - [raw_data](./tests/data/raw_data)
    - [results_summary](./tests/data/results_summary)
    - [revenue_results](./tests/data/revenue_results)

- [scripts](./tests/scripts)
    - [accuracy_tests](./tests/scripts/accuracy_tests)
    - [data_preprocessing](./tests/scripts/data_preprocessing)
    - [demand_proportionality](./tests/scripts/demand_proportionality)
    - [execution_time_tests](./tests/scripts/execution_time_tests)
    - [hyperparameter_tuning](./tests/scripts/hyperparameter_tuning)
    - [queries](./tests/scripts/queries)
    - [results_summary](./tests/scripts/results_summary)
    - [revenue_tests](./tests/scripts/revenue_tests)
    - [visualisations](./tests/scripts/visualisations)

- [visualisations](./tests/visualisations)
    - [demand_models_accuracy](./tests/visualisations/demand_models_accuracy)
    - [execution_time](./tests/visualisations/execution_time)
    - [forecast_periods_accuracy](./tests/visualisations/forecast_periods_accuracy)
    - [hyperparameter_tuning](./tests/visualisations/hyperparameter_tuning)
    - [pricing_methods_demand_proportionality](./tests/visualisations/pricing_methods_demand_proportionality)
    - [pricing_methods_revenue](./tests/visualisations/pricing_methods_revenue)
    - [summary](./tests/visualisations/summary)
    - [training_methods_accuracy](./tests/visualisations/training_methods_accuracy)




