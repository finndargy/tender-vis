import plotly.express as px
import pandas as pd
import plotly
import psycopg2

conn = psycopg2.connect(dbname="austender", user="postgres", password="password", host="localhost", port="5432")
query = "SELECT agency_name, category_name, value_aud FROM contracts"

# Load data into a pandas DataFrame
df = pd.read_sql(query, conn)
# Filter for Department of Defense (replace with the actual name in your dataset)
df_defence = df[df['agency_name'] == 'Department of Defence']

# Group by category and calculate the total spending by category
category_totals = df_defence.groupby('category_name')['value_aud'].sum().sort_values(ascending=False).reset_index()


# Create a Treemap
fig = px.treemap(category_totals, 
                 path=['category_name'],  # Labels for the treemap
                 values='value_aud',  # Values for the size of each square
                 title="Total Spending by Category - Department of Defense")

# Show the plot
fig.show()
