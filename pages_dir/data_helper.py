import pandas as pd


def summary_table(df):
    """
    Return a summary table with the descriptive statistics about the dataframe.
    """
    nulls = df.isnull().sum().sum()
    dups = df.duplicated().sum()
    summary = {
        "Number of Days": len(df),
        "Missing Cells": nulls,
        "Missing Cells (%)": round(nulls / df.shape[0] * 100, 2),
        "Duplicated Rows": dups,
        "Duplicated Rows (%)": round(dups / df.shape[0] * 100, 2),
        "Length of Categorical Variables": len([i for i in df.columns if df[i].dtype == object]),
        "Length of Numerical Variables": len([i for i in df.columns if df[i].dtype != object])
    }

    df = pd.DataFrame(summary.items(), columns=['Description', 'Value'], dtype=object)
    return df
