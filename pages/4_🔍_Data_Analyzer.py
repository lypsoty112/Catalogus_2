import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly

from src.datachain import Response, call_llm
from src.database import Database
import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots


st.set_page_config(
    page_title="Data Analyzer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)


def answer_question(df: pd.DataFrame):
    return df

@st.cache_data  # 👈 Add the caching decorator
def load_data():
    db = Database()
    return db.get_data()

data: pd.DataFrame = load_data()

st.title("Data analyser")

with st.form(key="Question_form") as form:
    st.header("AI-assisted analyser")
    question = st.text_input(label="Ask your question here")
    if st.form_submit_button("Ask your question!"):
        try:
            with st.spinner("Performing some magic"):
                for _ in range(10):
                    try:
                        response = call_llm(
                            question,
                            data
                        )
                        print(response)
                        # Execute the code
                        exec(response)
                        break
                    except Exception as e:
                        print(e) 
                        continue
                
            
            response = answer_question(data)
            if isinstance(response, pd.DataFrame):
                st.dataframe(response)
            elif response is None:
                st.text("No answer was found by the AI, or something went wrong.")
            else:
                st.plotly_chart(response, use_container_width=True)
        except Exception as e:
            print(e)
            st.error("Something went wrong :(")

        
        

st.divider()

st.header("**General analysis**")
st.dataframe(data=data)


# Count the occurrences of each country
country_counts = data['lando'].value_counts().reset_index()
country_counts.columns = ['Country', 'Count']

# Sort the data by count in descending order
country_counts = country_counts.sort_values('Count', ascending=False)

# Create the bar chart
fig1 = px.bar(country_counts, 
             x='Country', 
             y='Count', 
             title='Distribution of Esperanto Coins/Medals by Country',
             labels={'Country': 'Country', 'Count': 'Number of Coins/Medals'},
             color='Count',
             color_continuous_scale='Viridis')

# Customize the layout
fig1.update_layout(
    xaxis_title='Country',
    yaxis_title='Number of Coins/Medals',
    xaxis_tickangle=-45,
    bargap=0.2,
    height=600,
    width=1000
)

st.plotly_chart(fig1, use_container_width=True)

# Convert 'jaro' to integer and count occurrences per year
year_counts = data['jaro'].dropna().astype(int).value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']

# Create the line chart
fig = px.line(year_counts, 
              x='Year', 
              y='Count', 
              title='Timeline of Esperanto Coin/Medal Production',
              labels={'Year': 'Year', 'Count': 'Number of Coins/Medals'},
              line_shape='linear',
              markers=True)

# Customize the layout
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Number of Coins/Medals',
    height=500,
    width=900
)

st.plotly_chart(fig, use_container_width=True)

# Create the histogram
fig = px.histogram(data, 
                   x='diametro', 
                   nbins=20,
                   title='Diameter Distribution of Esperanto Coins/Medals',
                   labels={'diametro': 'Diameter (mm)', 'count': 'Number of Coins/Medals'},
                   color_discrete_sequence=['#636EFA'])

# Customize the layout
fig.update_layout(
    xaxis_title='Diameter (mm)',
    yaxis_title='Number of Coins/Medals',
    bargap=0.1,
    height=500,
    width=900
)

st.plotly_chart(fig, use_container_width=True)

# Create the scatter plot
fig = px.scatter(data, 
                 x='pezo', 
                 y='diametro',
                 title='Weight vs. Diameter of Esperanto Coins/Medals',
                 labels={'pezo': 'Weight (g)', 'diametro': 'Diameter (mm)'},
                 color='metalo',
                 hover_data=['name'])

# Customize the layout
fig.update_layout(
    xaxis_title='Weight (g)',
    yaxis_title='Diameter (mm)',
    height=600,
    width=900
)

st.plotly_chart(fig, use_container_width=True)

# Count the occurrences of each artist/medalist
artist_counts = data['artisto / medalisto'].value_counts().nlargest(10).reset_index()
artist_counts.columns = ['Artist', 'Count']

# Create the horizontal bar chart
fig = px.bar(artist_counts, 
             y='Artist', 
             x='Count', 
             title='Top 10 Artists/Medalists of Esperanto Coins/Medals',
             labels={'Artist': 'Artist/Medalist', 'Count': 'Number of Coins/Medals'},
             orientation='h',
             color='Count',
             color_continuous_scale='Viridis')

# Customize the layout
fig.update_layout(
    yaxis_title='Artist/Medalist',
    xaxis_title='Number of Coins/Medals',
    height=600,
    width=900
)

# Show the plot
st.plotly_chart(fig, use_container_width=True)

# Count the occurrences of each metal
metal_counts = data['metalo'].value_counts().reset_index()
metal_counts.columns = ['Metal', 'Count']

# Create the pie chart
fig = px.pie(metal_counts, 
             values='Count', 
             names='Metal',
             title='Metal Composition of Esperanto Coins/Medals',
             color_discrete_sequence=px.colors.qualitative.Plotly)

# Customize the layout
fig.update_layout(
    height=600,
    width=900
)

st.plotly_chart(fig, use_container_width=True)
# Create the box plot
fig = px.box(data, 
             x='metalo', 
             y='diko',
             title='Thickness Distribution by Metal for Esperanto Coins/Medals',
             labels={'metalo': 'Metal', 'diko': 'Thickness (mm)'},
             color='metalo',
             color_discrete_sequence=px.colors.qualitative.Plotly)

# Customize the layout
fig.update_layout(
    xaxis_title='Metal',
    yaxis_title='Thickness (mm)',
    height=600,
    width=900
)
st.plotly_chart(fig, use_container_width=True)

# Filter out rows with missing values
filtered_data = data.dropna(subset=['jaro', 'diametro', 'kvanto'])

# Create the bubble chart
fig = px.scatter(filtered_data, 
                 x='jaro', 
                 y='diametro',
                 size='kvanto',
                 color='metalo',
                 hover_name='name',
                 title='Production Quantity of Esperanto Coins/Medals Over Time',
                 labels={'jaro': 'Year', 'diametro': 'Diameter (mm)', 'kvanto': 'Quantity', 'metalo': 'Metal'},
                 size_max=50)

# Customize the layout
fig.update_layout(
    xaxis_title='Year',
    yaxis_title='Diameter (mm)',
    height=600,
    width=1000
)

st.plotly_chart(fig, use_container_width=True)

# Create a cross-tabulation of countries and metals
heatmap_data = pd.crosstab(data['lando'], data['metalo'])

# Create the heatmap
fig = px.imshow(heatmap_data,
                labels=dict(x='Metal', y='Country', color='Count'),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale='Viridis',
                title='Heatmap of Esperanto Coin/Medal Characteristics')

# Customize the layout
fig.update_layout(
    xaxis_title='Metal',
    yaxis_title='Country',
    height=800,
    width=1000
)

st.plotly_chart(fig, use_container_width=True)

# Join all names into a single string
text = ' '.join(data['name'].dropna())

# Create and generate a word cloud image
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)

# Display the generated image
fig = plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('Word Cloud of Esperanto Coin/Medal Names')

st.pyplot(fig)

# Select a few random samples for comparison
sample_size = len(data.index) // 10
samples = data.sample(sample_size)

# Normalize the data for better visualization
max_values = data[['diametro', 'pezo', 'diko']].max()
samples_normalized = samples[['diametro', 'pezo', 'diko']] / max_values

# Create the radar chart
fig = go.Figure()

for i, row in samples_normalized.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=[row['diametro'], row['pezo'], row['diko']],
        theta=['Diameter', 'Weight', 'Thickness'],
        fill='toself',
        name=f"Sample {i}"
    ))

fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, 1]  # Normalized data
        )),
    showlegend=True,
    title='Radar Chart of Physical Properties of Esperanto Coins/Medals',
    height=600,
    width=800
)

# Add hover information
for i, row in samples.iterrows():
    fig.add_trace(go.Scatterpolar(
        r=[row['diametro']/max_values['diametro'], row['pezo']/max_values['pezo'], row['diko']/max_values['diko']],
        theta=['Diameter', 'Weight', 'Thickness'],
        mode='markers',
        marker=dict(size=1),
        hoverinfo='text',
        hovertext=[
            f"Diameter: {row['diametro']:.2f} mm<br>"
            f"Weight: {row['pezo']:.2f} g<br>"
            f"Thickness: {row['diko']:.2f} mm"
        ],
        showlegend=False
    ))

# Use a colorful palette

st.plotly_chart(fig, use_container_width=True)

# Get top 5 countries
top_5_countries = data['lando'].value_counts().nlargest(5).index

# Create subplots
fig = make_subplots(rows=1, cols=1)

# Add traces for each country
for country in top_5_countries:
    country_data = data[data['lando'] == country]
    fig.add_trace(go.Violin(x=country_data['lando'], 
                            y=country_data['pezo'], 
                            name=country, 
                            box_visible=True, 
                            meanline_visible=True))

# Update layout
fig.update_layout(title='Weight Distribution of Esperanto Coins/Medals by Top 5 Countries',
                  xaxis_title='Country',
                  yaxis_title='Weight (g)',
                  height=600,
                  width=1000)

# Show the plot
st.plotly_chart(fig, use_container_width=True)

# Prepare the data
parallel_data = data[['jaro', 'diametro', 'pezo', 'diko']].dropna()

# Create the parallel coordinates plot
fig = px.parallel_coordinates(parallel_data,
                              color='jaro',
                              labels={'jaro': 'Year',
                                      'diametro': 'Diameter',
                                      'pezo': 'Weight',
                                      'diko': 'Thickness'},
                              title='Multivariate Comparison of Esperanto Coin/Medal Characteristics')

# Customize the layout
fig.update_layout(
    height=600,
    width=1000
)

st.plotly_chart(fig, use_container_width=True)

treemap_data = data.groupby(['lando', 'metalo']).size().reset_index(name='count')

# Create the treemap
fig = px.treemap(treemap_data, 
                 path=['lando', 'metalo'], 
                 values='count',
                 title='Hierarchical View of Esperanto Coins/Medals by Country and Metal')

# Customize the layout
fig.update_layout(
    height=700,
    width=1000
)

st.plotly_chart(fig, use_container_width=True)
