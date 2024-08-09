import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

CSV_DIR = "./data/PRSA_Data_20130301-20170228/"
csv_filename_list = os.listdir(CSV_DIR)

# Load dataframe
list_raw_df = [
    pd.read_csv(os.path.join(CSV_DIR, filename)) for filename in csv_filename_list
]
df = pd.concat(list_raw_df)

# Add datetime
datetime_column =  ["year", "month", "day", "hour"]
df["datetime"] = pd.to_datetime(df[datetime_column])

df.dropna(inplace=True)

df["POLUTANT"] = df["PM2.5"] + df["PM10"] + df["SO2"] + df["NO2"] + df["CO"] + df["O3"]


wd_mapping = {
    'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
    'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
    'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
    'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
}

df["wd_in_deg"] = df["wd"].map(wd_mapping)

unused_cols = ["No", "year", "month", "day", "hour", "TEMP", "PRES", "DEWP", "WSPM"]
df.drop(columns=unused_cols, axis=1, inplace=True)

station_list = df["station"].unique()

df_by_station = {}

for station in station_list:
    df_by_station[station] = df.loc[df["station"] == station]


def normalize(df):
    df = df.set_index("datetime")
    
    df_resampled = df.resample("ME").agg({
        "station": lambda st: st.unique()[0] if len(st.unique()) > 0 else None,
        "wd": lambda wd: wd.mode().iloc[0] if not wd.mode().empty else None,
        "wd_in_deg": "mean",
        "RAIN": "mean",
        "PM2.5": "mean",
        "PM10": "mean",
        "SO2": "mean",
        "NO2": "mean",
        "CO": "mean",
        "O3": "mean",
        "POLUTANT": "mean",
    })

    df_resampled.dropna(inplace = True)
    
    return df_resampled

df_aot = normalize(df_by_station["Aotizhongxin"])
df_cha = normalize(df_by_station["Changping"])
df_din = normalize(df_by_station["Dingling"])
df_don = normalize(df_by_station["Dongsi"])
df_gua = normalize(df_by_station["Guanyuan"])
df_guc = normalize(df_by_station["Gucheng"])
df_hua = normalize(df_by_station["Huairou"])
df_non = normalize(df_by_station["Nongzhanguan"])
df_shu = normalize(df_by_station["Shunyi"])
df_tia = normalize(df_by_station["Tiantan"])
df_wan = normalize(df_by_station["Wanliu"])
df_was = normalize(df_by_station["Wanshouxigong"])

all_clean_df = pd.concat([df_aot, df_cha, df_din, df_don, df_gua, df_guc, df_hua, df_non, df_shu, df_tia])

