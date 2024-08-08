# %% [markdown]
# # Proyek Analisis Data: Air Quality Dataset
# - **Nama:** Nurfian Qodar
# - **Email:** 77nurfianqodar@gmail.com
# - **ID Dicoding:** nurfianqodar

# %% [markdown]
# ## Menentukan Pertanyaan Bisnis

# %% [markdown]
# - Apakah arah angin (wd) mempengaruhi konsentrasi polutan di udara?
# - Apakah curah hujan (RAIN) memiliki pengaruh terhadap konsentrasi polutan di udara?
# - Kapan (datetime) dan di daerah (station) mana yang memiliki kualitas udara terburuk?
# - Kapan (datetime) dan di daerah (station) mana yang memiliki kualitas udara terbaik?

# %% [markdown]
# ## Import Semua Packages/Library yang Digunakan

# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# %% [markdown]
# ## Data Wrangling

# %% [markdown]
# ### Gathering Data

# %% [markdown]
# #### 1. List Dataset (CSV File)

# %%
CSV_DIR = "../data/PRSA_Data_20130301-20170228/"
csv_filename_list = os.listdir(CSV_DIR)
csv_filename_list

# %% [markdown]
# #### 2. Menggabungkan Semua Dataset

# %%
list_df = [
    pd.read_csv(os.path.join(CSV_DIR, filename)) for filename in csv_filename_list
]
df = pd.concat(list_df)
df.head()

# %%
df.tail()

# %% [markdown]
# Dataset berhasil terbaca dan digabungkan.

# %% [markdown]
# ### Assessing Data

# %% [markdown]
# #### 1. Memeriksa Missing Value

# %%
df.isna().sum()

# %% [markdown]
# Terdapat missing value pada kolom PM2.5, PM10, SO2, NO2, CO, O3, TEMP, PRES, DEWP, RAIN, wd, dan WSPM

# %% [markdown]
# #### 2. Memeriksa Duplicated Value

# %%
sum_duplicated = df.duplicated().sum()
print(f"Total data duplikat: {sum_duplicated}")

# %% [markdown]
# Tidak ditemukan duplikasi pada data

# %% [markdown]
# #### 3. Memeriksa Invalid Data Type

# %%
df.info()

# %% [markdown]
# Datetime direpresentasikan sebagai integer dalam kolom year, month, day, dan hour yang terpisah.

# %% [markdown]
# ### Cleaning Data

# %% [markdown]
# #### 1. Normalisasi Datetime

# %% [markdown]
# - Membuat kolom datetime

# %%
datetime_column =  ["year", "month", "day", "hour"]
df["datetime"] = pd.to_datetime(df[datetime_column])
df.head()

# %% [markdown]
# - Menghapus Data yang memiliki Missing Value

# %%
df.dropna(inplace=True)
df.isna().sum()

# %% [markdown]
# - Membuat kolom Konsentrasi Polutan yang menggabungkan konsentrasi dari semua polutan
# 
# Hal ini bisa dilakukan karena konsentrasi polutan memiliki satuan yang sama

# %%
df["POLUTANT"] = df["PM2.5"] + df["PM10"] + df["SO2"] + df["NO2"] + df["CO"] + df["O3"]

df.head()

# %% [markdown]
# - Membuat kolom wd dalam derajat agar bisa dihitung korelasinya

# %%
wd_mapping = {
    'N': 0, 'NNE': 22.5, 'NE': 45, 'ENE': 67.5,
    'E': 90, 'ESE': 112.5, 'SE': 135, 'SSE': 157.5,
    'S': 180, 'SSW': 202.5, 'SW': 225, 'WSW': 247.5,
    'W': 270, 'WNW': 292.5, 'NW': 315, 'NNW': 337.5
}

df["wd_in_deg"] = df["wd"].map(wd_mapping)

# %% [markdown]
# - Menghapus kolom yang tidak diperlukan

# %%
unused_cols = ["No", "year", "month", "day", "hour", "TEMP", "PRES", "DEWP", "WSPM"]
df.drop(columns=unused_cols, axis=1, inplace=True)
df.head()

# %% [markdown]
# - Memisahkan kembali dataframe berdasarkan nama daerah dan melakukan resample menjadi data bulanan

# %%
station_list = df["station"].unique()

df_by_station = {}

print("Station List:")
for station in station_list:
    print(f"- {station}")
    df_by_station[station] = df.loc[df["station"] == station]

# %%
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



# %%
df_aot = normalize(df_by_station["Aotizhongxin"])
df_aot.info()

# %%
df_cha = normalize(df_by_station["Changping"])
df_cha.info()

# %%
df_din = normalize(df_by_station["Dingling"])
df_din.info()


# %%
df_don = normalize(df_by_station["Dongsi"])
df_don.info()

# %%
df_gua = normalize(df_by_station["Guanyuan"])
df_gua.info()

# %%
df_guc = normalize(df_by_station["Gucheng"])
df_guc.info()

# %%
df_hua = normalize(df_by_station["Huairou"])
df_hua.info()

# %%
df_non = normalize(df_by_station["Nongzhanguan"])
df_non.info()

# %%
df_shu = normalize(df_by_station["Shunyi"])
df_shu.info()

# %%
df_tia = normalize(df_by_station["Tiantan"])

df_tia.info()

# %%
df_wan = normalize(df_by_station["Wanliu"])

df_wan.info()

# %%
df_was = normalize(df_by_station["Wanshouxigong"])
df_was.info()

# %% [markdown]
# - Gabungan Clean Dataframe

# %%
all_clean_df = pd.concat([df_aot, df_cha, df_din, df_don, df_gua, df_guc, df_hua, df_non, df_shu, df_tia])
all_clean_df.info()

# %% [markdown]
# ## Exploratory Data Analysis (EDA)

# %% [markdown]
# ### Eksplorasi Mencari Pengaruh Arah Angin Terhadap Konsentrasi Polutan

# %%
all_clean_df[["wd_in_deg", "POLUTANT"]].corr()

# %% [markdown]
# Nilai korelasi sebesar -0.19433 menunjukkan adanya korelasi negatif yang sangat lemah antara wd_in_deg dan POLUTANT.
# Ini berarti bahwa perubahan dalam arah angin (dalam derajat) hanya sedikit mempengaruhi konsentrasi polutan. Korelasi negatif yang lemah menunjukkan bahwa meskipun ada hubungan, kekuatannya kecil dan tidak signifikan.

# %% [markdown]
# ### Eksplorasi Mencari Pengaruh Curah Hujan Terhadap Konsentrasi Polutan

# %%
all_clean_df[["RAIN", "POLUTANT"]].corr()

# %% [markdown]
# Nilai korelasi sebesar -0.350329 menunjukkan adanya korelasi negatif sedang antara RAIN dan POLUTANT.
# Ini berarti bahwa ketika curah hujan meningkat, konsentrasi polutan cenderung menurun, meskipun hubungan ini tidak sangat kuat. Korelasi negatif menunjukkan bahwa ada kecenderungan bahwa curah hujan dan konsentrasi polutan bergerak dalam arah yang berlawanan, tetapi tidak secara signifikan atau secara konsisten.

# %% [markdown]
# ### Eksplorasi Mencari Daerah dan Waktu dengan Kualitas Udara Paling Buruk

# %%
highest_polutant = all_clean_df["POLUTANT"].max()
highest_polutant

# %%
worst = all_clean_df.loc[all_clean_df["POLUTANT"] == highest_polutant]
worst

# %%
print(f"""
{worst["station"].iloc[0]} adalah daerah dengan kualitas udara terburuk pada {worst.index.strftime("%m-%Y")[0]}.
Konsentrasi polutan yang terkandung adalah {worst["POLUTANT"].iloc[0]}.
""")

# %% [markdown]
# ### Eksplorasi Mencari Daerah dan Waktu dengan Kualitas Udara Paling Baik

# %%
lowest_polutant = all_clean_df["POLUTANT"].min()
lowest_polutant

# %%
good = all_clean_df.loc[all_clean_df["POLUTANT"] == lowest_polutant]
good

# %%
print(f"""
{good["station"].iloc[0]} adalah daerah dengan kualitas udara terbaik pada {good.index.strftime("%m-%Y")[0]}.
Konsentrasi polutan yang terkandung adalah {good["POLUTANT"].iloc[0]}.
""")

# %% [markdown]
# ## Visualization & Explanatory Analysis

# %% [markdown]
# ### Pertanyaan 1: Apakah arah angin (wd) mempengaruhi konsentrasi polutan di udara?

# %%
sns.regplot(x="wd_in_deg", y="POLUTANT", data=all_clean_df)
plt.title('Scatter Plot: Korelasi Konsentrasi Polutant dengan Arah Angin (Derajat)')
plt.xlabel('Arah Angin (Derajat)')
plt.ylabel('Konsentrasi Polutan')
plt.show()


# %% [markdown]
# Terlihat bahwa distribusi data tidak mengikuti garis regresi menandakan bahwa korelasi yang sangat kecil antara arah angin dengan konsentrasi polutan di udara atau kualitas udara.

# %% [markdown]
# ### Pertanyaan 2: Apakah curah hujan (RAIN) memiliki pengaruh terhadap konsentrasi polutan di udara?

# %%
sns.regplot(x="RAIN", y="POLUTANT", data=all_clean_df)
plt.title('Scatter Plot: Korelasi Konsentrasi Polutant dengan Curah Hujan')
plt.xlabel('Curah Hujan')
plt.ylabel('Konsentrasi Polutan')
plt.show()

# %% [markdown]
# Terlihat pada scatterplot tersebut, saat curah hujan 0 atau musim kemarau, banyak data yang menunjukkan bahwa konsentrasi polutan meningkat.

# %% [markdown]
# ### Pertanyaan 3 dan 4: Kapan dan Dimana Daerah Dengan Kualitas Udara Terburuk dan Terbaik

# %%
plt.figure(figsize=(16, 8))
sns.lineplot(data=all_clean_df, x=all_clean_df.index, y='POLUTANT', hue='station', palette='tab10')

plt.title('Konsentrasi Polutan dari Waktu ke Waktu untuk Beberapa Daerah')
plt.xlabel('Tanggal')
plt.ylabel('Konsentrasi Polutan (µg/m³)')
plt.grid(True)
plt.legend(title='Daerah')
plt.show()

# %%
plt.figure(figsize=(16, 8))
sns.scatterplot(x=df_guc.index.unique(), y=df_guc["POLUTANT"], facecolor = "red", label = "Gucheng")
sns.scatterplot(x=df_din.index.unique(), y=df_din["POLUTANT"], facecolor = "blue", label = "Dingling")
sns.scatterplot(x=df_aot.index.unique(), y=df_aot["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_cha.index.unique(), y=df_cha["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_don.index.unique(), y=df_don["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_gua.index.unique(), y=df_gua["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_hua.index.unique(), y=df_hua["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_non.index.unique(), y=df_non["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_shu.index.unique(), y=df_shu["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_tia.index.unique(), y=df_tia["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_wan.index.unique(), y=df_wan["POLUTANT"], facecolor = "lightgrey")
sns.scatterplot(x=df_was.index.unique(), y=df_was["POLUTANT"], facecolor = "lightgrey")
plt.show()

# %% [markdown]
# Terlihat bahwa hasil analisis di station Dingling memiliki kualitas udara yang baik dengan konsentrasi polutan rendah.
# 
# Sebaliknya, di station Gucheng kulaitas udaranya buruk dengan konsentrasi polutan yang tinggi.

# %% [markdown]
# ## Conclusion

# %% [markdown]
# - Arah angin tidak memiliki pengaruh terhadap kualitas udara di suatu daerah.
# - Curah hujan memiliki pengaruh sedang terhadap kualitas udara di suatu daerah, semakin rendah curah hujan maka semakin buruk kualitas udara pada daerah tersebut.
# - Gucheng adalah daerah dengan kualitas udara terburuk pada 12-2015.
# Konsentrasi polutan yang terkandung adalah 3674.3212795549375.
# - Dingling adalah daerah dengan kualitas udara terbaik pada 09-2016.
# Konsentrasi polutan yang terkandung adalah 624.0857605177994.


