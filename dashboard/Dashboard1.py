import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

st.title('Air Pollution and Weather Conditions Dashboard')

st.sidebar.header('Choose an option:')
options = st.sidebar.radio("Select a visualization", ['Data Wrangling', 'Exploratory Data Analysis', 'Pollution Heatmap', 'Weather Heatmap'])

@st.cache
def load_data():
    combined_data = pd.read_csv("CombinedData_better.csv")
    clean_data = pd.read_csv("CombinedData_clean.csv")
    pollution_data = pd.read_csv("Pollution_Groups.csv")  
    weather_data = pd.read_csv("Weather_Groups.csv")      
    return combined_data, clean_data, pollution_data, weather_data

combined_data, clean_data, pollution_data, weather_data = load_data()

if options == 'Pollution Heatmap':
    st.subheader('Pollution Conditions Across Cities')
    pollutant = st.selectbox("Select a pollutant:", ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3'])
    
    fig = px.histogram(clean_data, x='station', y=pollutant, color='station', barmode='group')
    fig.update_layout(title=f'{pollutant} Levels Across Stations')
    st.plotly_chart(fig)

    pivotTablePollution = pollution_data.pivot_table(
        index='station',
        columns=['PM25_Category', 'PM10_Category', 'SO2_Category', 'NO2_Category', 'CO_Category', 'O3_Category'],
        values='Count',
        fill_value=0
    )

    pivotTablePollution = pivotTablePollution.loc[:, pivotTablePollution.sum(axis=0) >= 2500]

    fig, ax = plt.subplots(figsize=(25, 8))
    sns.heatmap(pivotTablePollution, annot=True, cmap='YlGnBu', ax=ax, fmt='g')
    ax.set_title('Pollution Across Cities', fontsize=16)
    ax.set_xlabel('Pollution Categories', fontsize=14)
    ax.set_ylabel('City Station', fontsize=14)
    st.pyplot(fig)

    st.subheader("Do cities with similar weather condition experience similar pollution trends?")

    st.markdown("""
    - Shunyi, Dingling, and Huairou have consistently high pollution counts, particularly for combinations involving high PM10, CO, and O3 levels, as indicated by darker blue colors in the matrix.
    - Aotizhongxin and Dongsi appear to have relatively lower pollution levels in the majority of pollution categories (predominantly light green shades).
    - Some combinations, such as "Normal-Low-Low-Normal-Low-High", seem to be prevalent across stations (Changping, Guanyuan, Tiantan), suggesting moderate but widespread pollution levels.
                """)

elif options == 'Weather Heatmap':
    st.subheader('Weather Conditions Across Cities')
    weather_var = st.selectbox("Select a weather parameter:", ['TEMP', 'PRES', 'DEWP', 'RAIN'])
    
    fig = px.box(clean_data, x='station', y=weather_var, color='station')
    fig.update_layout(title=f'{weather_var} Distribution Across Stations')
    st.plotly_chart(fig)

    pivotTableWeather = weather_data.pivot_table(
        index='station',
        columns=['TEMP_Category', 'PRES_Category', 'DEWP_Category', 'WSPM_Category'],
        values='Count',
        fill_value=0
    )

    pivotTableWeather = pivotTableWeather.loc[:, pivotTableWeather.sum(axis=0) >= 2500]

    fig, ax = plt.subplots(figsize=(25, 8))
    sns.heatmap(pivotTableWeather, annot=True, cmap='YlGnBu', ax=ax, fmt='g')
    ax.set_title('Weather Conditions Across Cities', fontsize=16)
    ax.set_xlabel('Weather Categories', fontsize=14)
    ax.set_ylabel('City Station', fontsize=14)
    st.pyplot(fig)

    st.subheader("Do cities with similar weather condition experience similar pollution trends?")
    st.markdown("""
    - Shunyi and Guanyuan seem to experience frequent extreme weather conditions such as "Mild-Low-Humid-Breezy" and "Cold-Normal-Moderate-Breezy" (dark blue areas).
    - Stations like Huairou show consistently higher values across various weather categories, indicating more variability or extremes in weather patterns compared to other stations.
    - Tiantan and Nongzhanguan show relatively stable weather conditions (lighter green areas) with moderate occurrences across different combinations, such as "Cold-Normal-Dry-Calm".
                """)

elif options == 'Exploratory Data Analysis':
    st.subheader('Pollution and Weather Data')

    st.write("## Pollution Data")
    st.dataframe(pollution_data.head())

    st.write("## Weather Data")
    st.dataframe(weather_data.head())

    st.subheader('Correlation of Weather and Pollution')
    st.write('How much does the weather affects the pollution level of cities.')

    corrMat = clean_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'WSPM', 'PRES', 'DEWP', 'RAIN', 'WSPM']].corr()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corrMat, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader('Answer to Question #1')
    st.markdown("""
    This correlation matrix shows that some parameters do indeed affect other parametes, such as:
    - Almost every pollution parameters affects each other, with the level of PM2.5 and CO as the highest one with correlation value of 0.79
    - An exception of this is the level of O3 which is affected a lot by the current temperature of the city
    - The weather parameters also affects each other, with the level of TEMP and DEWP as the highest one with correlation value of 0.82

    Note that (+) value means that each parameter positively affects each other, if one parameter goes up in value then the respective parameter will also go up in value. That also means a (-) value will negatively affect their respective parameter.
    """)

elif options == 'Data Wrangling':
    st.subheader("Gathering Data")
    st.dataframe(combined_data.head())

    st.markdown("""
    ### **1. PM2.5**  
    **Particulate Matter ≤ 2.5 micrometers** – Fine inhalable particles that can penetrate the respiratory system, often associated with health risks.

    ### **2. PM10**  
    **Particulate Matter ≤ 10 micrometers** – Coarse inhalable particles that can affect the respiratory system, though less harmful than PM2.5.

    ### **3. SO2**  
    **Sulfur Dioxide** – A gas produced by volcanic eruptions and industrial processes, known for contributing to air pollution and acid rain.

    ### **4. NO2**  
    **Nitrogen Dioxide** – A pollutant primarily produced by motor vehicles and industrial activity, associated with respiratory problems and smog formation.

    ### **5. CO**  
    **Carbon Monoxide** – A colorless, odorless gas resulting from incomplete combustion, harmful in high concentrations and can reduce oxygen delivery in the body.

    ### **6. O3**  
    **Ozone** – A gas found both in the earth’s upper atmosphere (protective layer) and at ground level (harmful pollutant causing respiratory issues).

    ### **7. TEMP**  
    **Temperature** – The air temperature, usually measured in degrees Celsius, influencing weather conditions and pollutant dispersion.

    ### **8. PRES**  
    **Atmospheric Pressure** – The weight of the atmosphere pressing down on the earth’s surface, often measured in hectopascals (hPa) or millibars (mb).

    ### **9. DEWP**  
    **Dew Point** – The temperature at which air becomes saturated with moisture and dew forms, an indicator of humidity levels.

    ### **10. RAIN**  
    **Rainfall** – The amount of precipitation, typically measured in millimeters (mm), which can affect air quality by removing pollutants from the atmosphere.

    ### **11. wd**  
    **Wind Direction** – The direction from which the wind is blowing, usually measured in degrees (0 to 360) or compass points (N, E, S, W).

    ### **12. WSPM**  
    **Wind Speed in Meters per Second (m/s)** – The speed of wind, which influences the dispersion and movement of pollutants.

    ### **13. station**  
    **Station Identifier** – The name or code of the air quality monitoring station where the data was collected.
    """)
    
    st.write('## **Missing Values**')
    st.write("Filling in missing values on 'wd' using forward fill since it's mostly dependent on the previous wind direction")
    
    missing_values = combined_data.isnull().sum()
    st.dataframe(missing_values)

    st.write('## **Outliers Handling Code**')
    st.write("Getting rid of outliers by appointing each outlier by each max or min values")

    code_snippet = """
    for col in floatCol:
        data = combined_data[col].dropna()
        q25, q75 = np.percentile(data, 25), np.percentile(data, 75)
        iqr = q75 - q25
        cutOff = iqr * 1.5
        minVal, maxVal = q25 - cutOff, q75 + cutOff
        combined_data[col] = np.where(combined_data[col] < minVal, minVal, combined_data[col])
        combined_data[col] = np.where(combined_data[col] > maxVal, maxVal, combined_data[col])
    """
    st.code(code_snippet, language='python')

    st.write('## Clean Data')
    st.dataframe(combined_data.head())

# Footer
st.sidebar.write("Dashboard created with Streamlit")
