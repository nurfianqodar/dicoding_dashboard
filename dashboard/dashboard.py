import streamlit as st
import utils


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

