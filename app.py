import matplotlib
matplotlib.use('Agg')

import dash
from dash import dcc, html, dash_table
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load the data
df = pd.read_csv('data/Jumia-DealsDF.csv')

# Descriptive statistics
descriptive_stats = df.describe()

# Filter ratings between 1 and 5
filtered_df = df[(df['Rating'] >= 1) & (df['Rating'] <= 5)]

# Create rating ranges
rating_bins = [0, 1, 2, 3, 4, 5]
df['Rating Range'] = pd.cut(df['Rating'], bins=rating_bins)

# Calculate average discount for each rating range
avg_discount_by_rating = df.groupby('Rating Range')['Discount'].mean()

# Get the top 10 rated products ordered by ratings count
top_rated_products = df.nlargest(10, 'Ratings Count')

# Define a helper function to convert matplotlib plots to base64
def mpl_to_base64(fig):
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    return "data:image/png;base64,{}".format(data)

# Distribution of ratings plot
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.hist(df['Rating'], bins=20, edgecolor='k', alpha=0.7)
ax1.set_title('Distribution of Product Ratings')
ax1.set_xlabel('Rating')
ax1.set_ylabel('Frequency')
ax1.grid(True)
dist_ratings_img = mpl_to_base64(fig1)

# Boxplot and histogram of ratings
fig2, axes = plt.subplots(1, 2, figsize=(16, 8))
filtered_df[['Rating']].boxplot(ax=axes[0])
axes[0].set_title('Boxplot of Ratings')
axes[0].set_ylabel('Values')
axes[0].grid(True)
axes[1].hist(filtered_df['Rating'], bins=20, edgecolor='k', alpha=0.7)
axes[1].set_title('Distribution of Product Ratings (1-5)')
axes[1].set_xlabel('Rating')
axes[1].set_ylabel('Frequency')
axes[1].grid(True)
plt.tight_layout()
box_hist_ratings_img = mpl_to_base64(fig2)

# Scatter plot of Old Price vs New Price
fig3, ax3 = plt.subplots(figsize=(12, 8))
scatter = ax3.scatter(df['Old Price'], df['New Price'], 
                      c=df['Discount'], s=df['Rating']*20, 
                      alpha=0.7, cmap='viridis', edgecolor='k')
cbar = plt.colorbar(scatter, ax=ax3)
cbar.set_label('Discount (%)')
z = np.polyfit(df['Old Price'], df['New Price'], 1)
p = np.poly1d(z)
ax3.plot(df['Old Price'], p(df['Old Price']), "r--")
ax3.set_title('Old Price vs New Price with Discount and Rating')
ax3.set_xlabel('Old Price')
ax3.set_ylabel('New Price')
ax3.grid(True)
scatter_img = mpl_to_base64(fig3)

# Distribution of Discounts and Boxplot
fig4, axes = plt.subplots(1, 2, figsize=(16, 8))
axes[0].hist(df['Discount'], bins=20, edgecolor='k', alpha=0.7)
axes[0].set_title('Distribution of Discounts')
axes[0].set_xlabel('Discount (%)')
axes[0].set_ylabel('Frequency')
axes[0].grid(True)
df[['Discount']].boxplot(ax=axes[1])
axes[1].set_title('Boxplot of Discounts')
axes[1].set_xlabel('Discount (%)')
axes[1].grid(True)
plt.tight_layout()
discounts_box_hist_img = mpl_to_base64(fig4)

# Scatter plot of Discounts vs Ratings with trendline
fig5, ax5 = plt.subplots(figsize=(10, 6))
ax5.scatter(df['Discount'], df['Rating'], alpha=0.7, edgecolor='k')
z = np.polyfit(df['Discount'], df['Rating'], 1)
p = np.poly1d(z)
ax5.plot(df['Discount'], p(df['Discount']), "r--")
ax5.set_title('Discounts vs Ratings')
ax5.set_xlabel('Discount (%)')
ax5.set_ylabel('Rating')
ax5.grid(True)
discounts_ratings_img = mpl_to_base64(fig5)

# Average Discount by Rating Range
fig6, ax6 = plt.subplots(figsize=(10, 6))
avg_discount_by_rating.plot(kind='bar', color='skyblue', edgecolor='k', ax=ax6)
ax6.set_title('Average Discount by Rating Range')
ax6.set_xlabel('Rating Range')
ax6.set_ylabel('Average Discount (%)')
ax6.grid(True)
avg_discount_rating_img = mpl_to_base64(fig6)

# Bar plot for top rated products by ratings count
fig7, ax7 = plt.subplots(figsize=(12, 8))
ax7.barh(top_rated_products['Product Name'], top_rated_products['Ratings Count'], color='skyblue', edgecolor='k')
ax7.set_xlabel('Ratings Count')
ax7.set_title('Most bought products by Ratings Count')
ax7.invert_yaxis()
ax7.grid(True)
top_rated_img = mpl_to_base64(fig7)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Jumia Deals Analysis"),
    
    html.H2("Descriptive Statistics"),
    dash_table.DataTable(
        data=descriptive_stats.reset_index().to_dict('records'),
        columns=[{"name": i, "id": i} for i in descriptive_stats.reset_index().columns],
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'center'},
        style_header={'backgroundColor': 'lightgrey', 'fontWeight': 'bold'}
    ),

    html.H2("Distribution of Product Ratings"),
    html.Img(src=dist_ratings_img),

    html.H2("Boxplot and Histogram of Ratings"),
    html.Img(src=box_hist_ratings_img),

    html.H2("Old Price vs New Price with Discount and Rating"),
    html.Img(src=scatter_img),

    html.H2("Distribution of Discounts and Boxplot"),
    html.Img(src=discounts_box_hist_img),

    html.H2("Discounts vs Ratings"),
    html.Img(src=discounts_ratings_img),

    html.H2("Average Discount by Rating Range"),
    html.Img(src=avg_discount_rating_img),

    html.H2("Most Bought Products by Ratings Count"),
    html.Img(src=top_rated_img)
])

if __name__ == '__main__':
    app.run_server(debug=True)