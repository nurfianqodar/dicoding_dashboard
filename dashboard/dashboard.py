import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Fungsi untuk memuat dan membersihkan dataset
def load_and_clean_data():
    CSV_DIR = "../data/PRSA_Data_20130301-20170228/"
    csv_filename_list = os.listdir(CSV_DIR)
    
    list_df = [pd.read_csv(os.path.join(CSV_DIR, filename)) for filename in csv_filename_list]
    df = pd.concat(list_df)
    
    # Data cleaning steps
    datetime_column = ["year", "month", "day", "hour"]
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
        df_resampled.dropna(inplace=True)
        return df_resampled
    
    df_by_station = {station: normalize(df.loc[df["station"] == station]) for station in station_list}
    
    all_clean_df = pd.concat(df_by_station.values())
    return df, df_by_station, all_clean_df

# Memuat data
df, df_by_station, all_clean_df = load_and_clean_data()

# Sidebar untuk navigasi
page = st.sidebar.selectbox("Pilih Halaman", ["Data", "Visualisasi"])

# Halaman 1: Menampilkan dataset dan summary
if page == "Data":
    st.title("Dataset Kualitas Udara")
    st.write("### Full Dataset Clean")
    st.dataframe(all_clean_df)
    
    st.write("### Dataset dari Setiap Kota Beserta Summary")
    selected_city = st.selectbox("Pilih Kota", list(df_by_station.keys()))
    city_df = df_by_station[selected_city]
    st.dataframe(city_df)
    st.write("Summary:")
    st.write(city_df.describe())

# Halaman 2: Visualisasi
elif page == "Visualisasi":
    st.title("Visualisasi Kualitas Udara")
    
    # Plot 1: Scatter plot untuk korelasi wd_in_deg dan POLUTANT
    st.write("### Korelasi antara Arah Angin dan Konsentrasi Polutan")
    sns.regplot(x="wd_in_deg", y="POLUTANT", data=all_clean_df)
    st.pyplot(plt)
    
    # Plot 2: Scatter plot untuk korelasi RAIN dan POLUTANT
    st.write("### Korelasi antara Curah Hujan dan Konsentrasi Polutan")
    sns.regplot(x="RAIN", y="POLUTANT", data=all_clean_df)
    st.pyplot(plt)
    
    # Plot 3: Konsentrasi Polutan dari Waktu ke Waktu
    st.write("### Konsentrasi Polutan dari Waktu ke Waktu untuk Beberapa Daerah")
    plt.figure(figsize=(16, 8))
    sns.lineplot(data=all_clean_df, x=all_clean_df.index, y='POLUTANT', hue='station', palette='tab10')
    st.pyplot(plt)
