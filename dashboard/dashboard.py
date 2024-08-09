import streamlit as st
import utils
import matplotlib.pyplot as plt
import seaborn as sns


st.title("Proyek Analisis Data: Air Quality Dataset")
st.markdown("""
- **Nama:** Nurfian Qodar
- **Email:** 77nurfianqodar@gmail.com
- **ID Dicoding:** nurfianqodar
""")


datasets, analysis = st.tabs(["Dashboard", "Analisis"])

with datasets:
    st.header("Dataset")
    options = ["All"] + list(utils.station_list)
    show = st.selectbox(label="Station", options=options)

    if show == "All":
        st.subheader("Full Dataset")
        st.caption("Concatenated dataset")
        st.dataframe(utils.all_clean_df)

        st.subheader("Ringkasan Statistik")
        st.write(utils.all_clean_df.describe())
    
    else:
        st.subheader(show)
        st.caption(f"{show} dateset")
        df = utils.all_clean_df.loc[utils.all_clean_df["station"] == show ]
        st.dataframe(df)

        st.subheader("Ringkasan Statistik")
        st.write(df.describe())

    st.subheader("Legenda")
    st.markdown("""
        - datetime: Waktu pengambilan data.
        - station: Nama stasiun pengukuran.
        - wd: Arah angin pada saat pengukuran.
        - wd_in_deg: Arah angin dalam derajat. 
        - RAIN: Curah hujan pada saat pengukuran, biasanya diukur dalam milimeter (mm).
        - PM2.5: Konsentrasi partikel PM2.5 (partikel dengan diameter kurang dari 2.5 mikrometer) dalam udara, biasanya diukur dalam mikrogram per meter kubik (µg/m³).
        - PM10: Konsentrasi partikel PM10 (partikel dengan diameter kurang dari 10 mikrometer) dalam udara, diukur dalam µg/m³.
        - SO2: Konsentrasi sulfur dioksida dalam udara, diukur dalam µg/m³.
        - NO2: Konsentrasi nitrogen dioksida dalam udara, diukur dalam µg/m³.
        - CO: Konsentrasi karbon monoksida dalam udara, diukur dalam mikrogram per meter kubik (µg/m³).
        - O3: Konsentrasi ozon dalam udara, diukur dalam µg/m³.
    """)


with analysis:
    st.header("Grafik Konsentrasi Polutan di Udara Dalam 4 Tahun")

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.lineplot(data=utils.all_clean_df, x=utils.all_clean_df.index, y='POLUTANT', hue='station', palette='tab10')

    ax.set_title('Konsentrasi Polutan dari Waktu ke Waktu untuk Beberapa Daerah')
    ax.set_xlabel('Tanggal')
    ax.set_ylabel('Konsentrasi Polutan (µg/m³)')
    ax.grid(True)
    ax.legend(title='Daerah')
    
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(16, 8))
    sns.scatterplot(x=utils.df_guc.index.unique(), y=utils.df_guc["POLUTANT"], facecolor = "red", label = "Gucheng")
    sns.scatterplot(x=utils.df_din.index.unique(), y=utils.df_din["POLUTANT"], facecolor = "blue", label = "Dingling")
    sns.scatterplot(x=utils.df_aot.index.unique(), y=utils.df_aot["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_cha.index.unique(), y=utils.df_cha["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_don.index.unique(), y=utils.df_don["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_gua.index.unique(), y=utils.df_gua["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_hua.index.unique(), y=utils.df_hua["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_non.index.unique(), y=utils.df_non["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_shu.index.unique(), y=utils.df_shu["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_tia.index.unique(), y=utils.df_tia["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_wan.index.unique(), y=utils.df_wan["POLUTANT"], facecolor = "lightgrey")
    sns.scatterplot(x=utils.df_was.index.unique(), y=utils.df_was["POLUTANT"], facecolor = "lightgrey")

    st.pyplot(fig)


    lowest = utils.all_clean_df.loc[utils.all_clean_df["POLUTANT"] == utils.all_clean_df["POLUTANT"].min()]
    st.header("Daerah Dengan Kualitas Udara Terbaik")
    st.dataframe(lowest)
    st.metric(value=(lowest["POLUTANT"].iloc[0].round(3)), label=(lowest["station"].iloc[0]), help="Averrage Polutant Concentrate")

    st.header("Daerah Dengan Kualitas Udara Terbaik")
    highest = utils.all_clean_df.loc[utils.all_clean_df["POLUTANT"] == utils.all_clean_df["POLUTANT"].max()]
    st.dataframe(highest)
    st.metric(value=(highest["POLUTANT"].iloc[0].round(3)), label=(highest["station"].iloc[0]), help="Averrage Polutant Concentrate")

    st.header("Korelasi Antara Arah Angin Dengan Konsentrasi Polutan di Udara")

    fig, ax = plt.subplots(figsize=(16,8))
    sns.regplot(x="wd_in_deg", y="POLUTANT", data=utils.all_clean_df)
    ax.set_title('Scatter Plot: Korelasi Konsentrasi Polutant dengan Arah Angin (Derajat)')
    ax.set_xlabel('Arah Angin (Derajat)')
    ax.set_ylabel('Konsentrasi Polutan')

    st.pyplot(fig)
    st.caption("Tabel korelasi")

    cor = utils.all_clean_df[["wd_in_deg", "POLUTANT"]].corr()
    st.write(cor)
    st.metric(label="Correlation Value", value=cor["wd_in_deg"].iloc[1].round(5))



    st.header("Korelasi Antara Curah Hujan Dengan Konsentrasi Polutan di Udara")

    fig, ax = plt.subplots(figsize=(16,8))
    sns.regplot(x="RAIN", y="POLUTANT", data=utils.all_clean_df)
    ax.set_title('Scatter Plot: Korelasi Konsentrasi Polutant dengan Curah Hujan')
    ax.set_xlabel('Curah Hujan')
    ax.set_ylabel('Konsentrasi Polutan')
    
    st.pyplot(fig)
    st.caption("Tabel korelasi")
    cor = utils.all_clean_df[["RAIN", "POLUTANT"]].corr()
    st.write(cor)
    st.metric(label="Correlation Value", value=cor["RAIN"].iloc[1].round(5))



