# US Funds Dashboard

This repository explores the US Funds dataset available at [Kaggle](https://www.kaggle.com/datasets/stefanoleone992/mutual-funds-and-etfs) and provides a dashborad solution using streamlit.

## Setup

Use `conda` or `mamba` to create a virtural environment:

```
conda env create -f environment.yml
conda activate us-funds-dashboard
```

## Notebook and Dashboard

The data exploration notebook is availble at [`exploration.ipynb`](exploration.ipynb). To run the dashboard, use the following command:

```
streamlit run app.py
```