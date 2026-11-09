# 🚕 OLA Ride Data Analysis Dashboard

## 📌 Project Overview
The OLA Ride Data Analysis project focuses on analyzing ride booking data to understand customer behaviour, ride performance, revenue generation, and cancellation patterns.

This project uses Python, SQL, MySQL Workbench, and Streamlit to develop an interactive dashboard that provides meaningful business insights and data-driven recommendations.

## 🎯 Project Objectives
- Analyze total ride bookings and completed rides.
- Understand ride cancellation patterns.
- Analyze revenue and average ride value.
- Identify popular vehicle types.
- Analyze pickup locations and ride distances.
- Generate business insights and recommendations.

## 🛠️ Technologies Used
- **Python** – Data analysis and data cleaning
- **Pandas & NumPy** – Data manipulation
- **Plotly** – Interactive visualizations
- **Streamlit** – Interactive dashboard development
- **MySQL Workbench** – Database management and SQL queries
- **VS Code** – Development environment
- **Excel / CSV** – Dataset management

## 📂 Project Structure

```text
OLA_Ride_Analysis/
│
├── app.py
├── db_connection.py
├── OLA_DataSet.xlsx
├── requirements.txt
└── README.md
```

## 📊 Dashboard Features
- Project overview
- KPI cards
- Total ride bookings
- Revenue analysis
- Completed and cancelled rides
- Vehicle type analysis
- Revenue trends
- Pickup location analysis
- Interactive filters
- Business recommendations
- Download cleaned dataset

## 📈 Key Performance Indicators (KPIs)
1. Total Rides
2. Total Revenue
3. Completed Rides
4. Cancelled Rides
5. Average Ride Value
6. Cancellation Rate

## 🗄️ SQL Database
Database Name: `ola_ride_analysis`

The project uses MySQL Workbench to store and retrieve ride booking data.

Example SQL queries:

```sql
SELECT COUNT(*) AS total_rides
FROM ola_rides;

SELECT booking_status,
       COUNT(*) AS total_bookings
FROM ola_rides
GROUP BY booking_status;

SELECT SUM(booking_value) AS total_revenue
FROM ola_rides;

SELECT vehicle_type,
       COUNT(*) AS total_rides
FROM ola_rides
GROUP
