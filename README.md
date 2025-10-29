# Daily Web Activity Analyzer

## Overview
This project collects, processes, and visualizes daily web browsing activity. 
It demonstrates an end-to-end pipeline using **Python and SQL**, with optional integration for **Power BI dashboards**.

The pipeline can process real Chrome browsing history or a sample dataset, providing insights into website categories, time-of-day activity, and domain popularity.

## Features
- Extracts browsing history from Chrome or a sample CSV
- Stores aggregated data in an **SQLite database**
- Python ETL script processes data, calculates metrics, and prepares features
- **ML-based URL categorization** using KMeans to classify websites into meaningful activity groups
- Optional Power BI integration for interactive dashboards

## Technologies Used
- Python: pandas, matplotlib, seaborn, sqlite3
- SQL: SQLite
- Power BI Desktop (optional)

## Setup Instructions
1. Clone the repository  
2. Install required packages:
   ```bash
   pip install -r requirements.txt
3. Run Python scripts or Jupyter notebooks in the notebooks/ folder


