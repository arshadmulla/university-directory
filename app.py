import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="European Universities Directory", layout="wide")

# ==============================
# 🌍 COUNTRY LIST
# ==============================

EUROPE_COUNTRIES = sorted([
    "Germany","France","Italy","Spain","Netherlands","Sweden",
    "Ireland","Austria","Finland","Denmark","Belgium","Portugal",
    "Czech Republic","Poland","Hungary","Greece","Estonia",
    "Luxembourg","Malta","Switzerland","Cyprus"
])

st.title("🎓 European Universities Directory")
st.write("Search, filter and download universities across Europe.")

# Sidebar filters
country = st.sidebar.selectbox("🌍 Select Country", EUROPE_COUNTRIES)
search_keyword = st.sidebar.text_input("🔍 Search University Name")
uni_type_filter = st.sidebar.selectbox(
    "🏛 Filter by Type",
    ["All", "Public", "Private"]
)

# ==============================
# FUNCTION TO CLASSIFY TYPE
# ==============================

def classify_university(name):
    private_keywords = ["Private", "Business School", "Catholic", "Institute of Technology"]
    
    for word in private_keywords:
        if word.lower() in name.lower():
            return "Private"
    return "Public"   # default assumption

# ==============================
# FETCH DATA
# ==============================

if st.sidebar.button("📋 Fetch Universities"):

    with st.spinner("Fetching universities..."):
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

                # Add university type column
                df["Type"] = df["name"].apply(classify_university)

                # Apply search filter
                if search_keyword:
                    df = df[df["name"].str.contains(search_keyword, case=False)]

                # Apply type filter
                if uni_type_filter != "All":
                    df = df[df["Type"] == uni_type_filter]

                st.success(f"Found {len(df)} universities 🎉")

                # Sort option
                sort_option = st.selectbox(
                    "Sort by",
                    ["Name (A-Z)", "Name (Z-A)"]
                )

                if sort_option == "Name (A-Z)":
                    df = df.sort_values("name")
                else:
                    df = df.sort_values("name", ascending=False)

                st.dataframe(df, use_container_width=True)

                # Download option
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Download CSV",
                    csv,
                    f"{country}_universities.csv",
                    "text/csv"
                )

        except Exception:
            st.error("Something went wrong while fetching data.")

st.markdown("---")
st.caption("Built by Arshad | European University Directory Tool 🚀")
