
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="OLA Ride Analysis Dashboard",
    page_icon="🚕",
    layout="wide"
)

st.title("🚕 OLA Ride Data Analysis Dashboard")
st.markdown(
    "Analyze ride bookings, revenue, cancellations "
    "and customer behaviour."
)

# --------------------------------
# DATA UPLOAD
# --------------------------------
uploaded_file = st.sidebar.file_uploader(
    "Upload OLA Ride Dataset",
    type=["csv", "xlsx"]
)

if uploaded_file is not None:

    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    df.columns = df.columns.str.strip()

    # --------------------------------
    # DATA CLEANING
    # --------------------------------
    df = df.drop_duplicates()

    st.sidebar.success("Dataset loaded successfully!")

    st.sidebar.header("🔎 Dashboard Filters")

    # Detect common columns
    def find_column(possible_names):
        for col in df.columns:
            if col.lower().replace(" ", "_") in possible_names:
                return col
        return None

    date_col = find_column([
        "date", "booking_date", "ride_date"
    ])

    status_col = find_column([
        "booking_status", "ride_status", "status"
    ])

    revenue_col = find_column([
        "booking_value", "revenue", "ride_fare",
        "fare", "amount"
    ])

    vehicle_col = find_column([
        "vehicle_type", "vehicle"
    ])

    city_col = find_column([
        "pickup_location", "city", "pickup_city"
    ])

    distance_col = find_column([
        "ride_distance", "distance", "distance_km"
    ])

    # --------------------------------
    # FILTERS
    # --------------------------------
    filtered_df = df.copy()

    if status_col:
        statuses = df[status_col].dropna().unique().tolist()
        selected_status = st.sidebar.multiselect(
            "Booking Status",
            statuses,
            default=statuses
        )
        filtered_df = filtered_df[
            filtered_df[status_col].isin(selected_status)
        ]

    if vehicle_col:
        vehicles = df[vehicle_col].dropna().unique().tolist()
        selected_vehicle = st.sidebar.multiselect(
            "Vehicle Type",
            vehicles,
            default=vehicles
        )
        filtered_df = filtered_df[
            filtered_df[vehicle_col].isin(selected_vehicle)
        ]

    if city_col:
        cities = df[city_col].dropna().unique().tolist()
        selected_city = st.sidebar.multiselect(
            "Pickup Location",
            cities,
            default=cities
        )
        filtered_df = filtered_df[
            filtered_df[city_col].isin(selected_city)
        ]

    # --------------------------------
    # KPI CARDS
    # --------------------------------
    st.subheader("📊 Key Performance Indicators")

    total_rides = len(filtered_df)

    if revenue_col:
        filtered_df[revenue_col] = pd.to_numeric(
            filtered_df[revenue_col], errors="coerce"
        )
        total_revenue = filtered_df[revenue_col].sum()
        avg_revenue = filtered_df[revenue_col].mean()
    else:
        total_revenue = 0
        avg_revenue = 0

    if status_col:
        completed = (
            filtered_df[status_col].astype(str).str.lower()
            .str.contains("success|complete", regex=True).sum()
        )
        cancelled = (
            filtered_df[status_col].astype(str).str.lower()
            .str.contains("cancel", regex=True).sum()
        )
    else:
        completed = 0
        cancelled = 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Rides", f"{total_rides:,}")
    c2.metric("Total Revenue", f"₹{total_revenue:,.2f}")
    c3.metric("Completed Rides", f"{completed:,}")
    c4.metric("Cancelled Rides", f"{cancelled:,}")

    st.divider()

    # --------------------------------
    # CHARTS
    # --------------------------------
    st.subheader("📈 Data Visualizations")

    col1, col2 = st.columns(2)

    with col1:
        if status_col:
            status_data = filtered_df[status_col].value_counts().reset_index()
            status_data.columns = ["Status", "Count"]

            fig = px.pie(
                status_data,
                names="Status",
                values="Count",
                title="Ride Booking Status",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)

        elif revenue_col:
            st.info("Booking status column not available.")

    with col2:
        if vehicle_col:
            vehicle_data = filtered_df[vehicle_col].value_counts().reset_index()
            vehicle_data.columns = ["Vehicle", "Rides"]

            fig = px.bar(
                vehicle_data,
                x="Vehicle",
                y="Rides",
                title="Rides by Vehicle Type",
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Vehicle type column not available.")

    col3, col4 = st.columns(2)

    with col3:
        if date_col and revenue_col:
            trend = filtered_df.copy()
            trend[date_col] = pd.to_datetime(
                trend[date_col], errors="coerce"
            )
            trend = trend.dropna(subset=[date_col])

            trend_data = (
                trend.groupby(trend[date_col].dt.date)[revenue_col]
                .sum().reset_index()
            )
            trend_data.columns = ["Date", "Revenue"]

            fig = px.line(
                trend_data,
                x="Date",
                y="Revenue",
                title="Revenue Trend",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Date or revenue column not available.")

    with col4:
        if city_col:
            city_data = filtered_df[city_col].value_counts().head(10).reset_index()
            city_data.columns = ["Location", "Rides"]

            fig = px.bar(
                city_data,
                x="Location",
                y="Rides",
                title="Top 10 Pickup Locations",
                text_auto=True
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("Pickup location column not available.")

    # --------------------------------
    # DISTANCE ANALYSIS
    # --------------------------------
    st.subheader("🛣️ Ride Distance Analysis")

    if distance_col:
        filtered_df[distance_col] = pd.to_numeric(
            filtered_df[distance_col], errors="coerce"
        )

        fig = px.histogram(
            filtered_df,
            x=distance_col,
            nbins=30,
            title="Distribution of Ride Distances"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Ride distance column not available.")

    # --------------------------------
    # BUSINESS INSIGHTS
    # --------------------------------
    st.subheader("💡 Business Insights & Recommendations")

    st.write(f"• Total rides analyzed: {total_rides:,}")

    if status_col and total_rides > 0:
        cancellation_rate = cancelled / total_rides * 100
        st.write(
            f"• Cancellation rate: {cancellation_rate:.2f}%"
        )

        if cancellation_rate > 20:
            st.warning(
                "High cancellations detected. Improve driver "
                "availability and booking reliability."
            )
        else:
            st.success("Cancellation rate is relatively low.")

    if revenue_col:
        st.write(f"• Total revenue: ₹{total_revenue:,.2f}")
        st.write(f"• Average ride value: ₹{avg_revenue:,.2f}")

    if vehicle_col and not filtered_df.empty:
        popular_vehicle = filtered_df[vehicle_col].mode()
        if not popular_vehicle.empty:
            st.write(
                f"• Most popular vehicle: {popular_vehicle.iloc[0]}"
            )

    if city_col and not filtered_df.empty:
        popular_city = filtered_df[city_col].mode()
        if not popular_city.empty:
            st.write(
                f"• Top pickup location: {popular_city.iloc[0]}"
            )

    # --------------------------------
    # DATASET PREVIEW
    # --------------------------------
    st.subheader("📋 Dataset Preview")

    st.write("Rows:", len(filtered_df))
    st.write("Columns:", len(filtered_df.columns))

    st.dataframe(filtered_df, use_container_width=True)

    # --------------------------------
    # DOWNLOAD CLEANED DATA
    # --------------------------------
    csv = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇️ Download Cleaned Dataset",
        data=csv,
        file_name="ola_cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload your OLA Ride CSV or Excel dataset.")
    st.write("Your dashboard will appear after uploading the dataset.")
