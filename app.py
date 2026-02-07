import streamlit as st
import requests
import pandas as pd

# ==============================
# 🌍 FULL EUROPE COUNTRY LIST (20)
# ==============================

EUROPE_COUNTRIES = [
    "Germany",
    "France",
    "Italy",
    "Spain",
    "Netherlands",
    "Sweden",
    "Ireland",
    "Austria",
    "Finland",
    "Denmark",
    "Belgium",
    "Portugal",
    "Czech Republic",
    "Poland",
    "Hungary",
    "Greece",
    "Estonia",
    "Luxembourg",
    "Malta",
    "Cyprus"
]

st.title("🎓 European Universities Directory")

country = st.selectbox("🌍 Select European Country", EUROPE_COUNTRIES)

if st.button("📋 Fetch Universities"):

    st.info("Fetching universities...")

    try:
        url = f"http://universities.hipolabs.com/search?country={country}"
        response = requests.get(url)
        data = response.json()

        if not data:
            st.warning("No universities found.")
        else:
            df = pd.DataFrame(data)

            df = df[["name", "country", "web_pages"]]
            df["website"] = df["web_pages"].apply(lambda x: x[0])
            df = df.drop(columns=["web_pages"])

            st.success(f"Found {len(df)} universities in {country} 🎉")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download CSV",
                csv,
                f"{country}_universities.csv",
                "text/csv"
            )

    except Exception as e:
        st.error("Something went wrong while fetching data.")

st.markdown("---")
st.caption("Built by Arshad | European University Directory Tool")
