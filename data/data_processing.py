import pandas as pd
import os

def load_and_clean_data(save_clean=False):

    # read
    df = pd.read_csv("raw/health_lifestyle_dataset.csv")


    print(df.dtypes)
    df['gender'] = df['gender'].map({'Male': 0, 'Female': 1})

    print(df.isnull().sum())

    if save_clean:
        os.makedirs("cleaned", exist_ok=True)
        df.to_csv("cleaned/clean_health.csv", index=False)
        print("Cleaned CSV saved!")

    return df

load_and_clean_data(save_clean=True)
