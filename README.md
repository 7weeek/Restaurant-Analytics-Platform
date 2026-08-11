# RestaurantIQ

RestaurantIQ is an end-to-end restaurant analytics and business intelligence project designed to turn scattered operational data into structured, decision-ready insights.

The project combines a Streamlit-based data management portal, Python/Pandas ETL, PostgreSQL, SQL analytics, and Power BI dashboards.

## Project Overview

Restaurant data can come from multiple business functions such as:

- Orders
- Customers
- Restaurants
- Deliveries
- Payments
- Reviews

RestaurantIQ brings these sources into a repeatable analytics workflow:

```text
CSV / Excel Files
        ↓
Streamlit Data Management Portal
        ↓
Validation & Data Quality Checks
        ↓
Python + Pandas ETL
        ↓
PostgreSQL
        ↓
SQL Analytics
        ↓
Power BI
        ↓
Business Dashboards & KPIs
```

## What the Project Does

- Ingests CSV and Excel business files
- Validates incoming datasets and their schemas
- Cleans and transforms raw data using Python and Pandas
- Combines related operational datasets
- Stores processed data in PostgreSQL
- Uses SQL for analytical queries and business metrics
- Builds Power BI dashboards for interactive reporting
- Provides KPIs and analysis around sales, customers, restaurants, delivery performance, payments, and ratings

## Input Data

The planned input layer consists of six datasets:

| Dataset | Purpose |
|---|---|
| Orders | Orders, revenue, discounts, taxes and status |
| Customers | Customer profiles, demographics and membership |
| Restaurants | Restaurant, city, cuisine and pricing information |
| Deliveries | Delivery times and delivery performance |
| Payments | Payment methods, status and cashback |
| Reviews | Ratings and customer experience |

The Streamlit application is intended to accept these files and process them through the ETL pipeline.

## Analytics

The Power BI layer is designed around practical business questions, including:

### Sales & Revenue
- Revenue trends
- Order volume
- Average Order Value
- Revenue by city
- Revenue by cuisine
- Top-performing restaurants
- Weekend vs weekday performance

### Customer Analytics
- New vs returning customers
- Customer segments
- Membership distribution
- Order frequency
- High-value customers

### Restaurant Performance
- Restaurant rankings
- Restaurant revenue
- Cuisine performance
- Restaurant ratings
- Order contribution

### Delivery & Operations
- Average delivery time
- On-time delivery rate
- Late deliveries
- Delivery performance by city and restaurant
- Peak ordering periods

### Payments & Reviews
- Payment method distribution
- Payment status
- Cashback
- Rating distribution
- Food vs delivery ratings

## Technology Stack

- **Python** — data processing and ETL
- **Pandas** — data cleaning and transformation
- **Streamlit** — data management and file ingestion portal
- **PostgreSQL** — centralized relational data store
- **SQL** — analytics and business queries
- **Power BI** — dashboards and business intelligence
- **DAX** — calculated measures and KPIs
- **Power Query** — data transformation where required

## Repository Structure

```text
RestaurantIQ/
│
├── index.html
├── style.css
├── streamlit.jpg
├── README.md
│
├── streamlit/
│   └── ...
│
├── etl/
│   └── ...
│
├── sql/
│   └── ...
│
└── powerbi/
    └── ...
```

The repository structure can be expanded as each part of the platform is implemented.

## Project Website

The project walkthrough website documents the architecture, workflow, data sources, analytics use cases, and technology stack.

The website is a presentation layer only; the actual data processing and analytics components are built separately.

## Current Status

- [x] Project concept and architecture
- [x] Project walkthrough website
- [x] Sample analytical dataset
- [ ] Streamlit ingestion portal
- [ ] Data validation layer
- [ ] PostgreSQL integration
- [ ] Production ETL pipeline
- [ ] SQL analytics layer
- [ ] Power BI dashboard
- [ ] End-to-end integration

## Goal

The goal of RestaurantIQ is to demonstrate a realistic end-to-end analytics workflow rather than a standalone dashboard — starting from raw business files and ending with interactive business intelligence reporting.
