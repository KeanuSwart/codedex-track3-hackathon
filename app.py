from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# Load the data
data_path = 'processed_olympic_predictions_2024.csv'
data = pd.read_csv(data_path)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/prediction_sequence')
def prediction_sequence():
    # The country with the highest total predicted medals
    country_medal_counts = data.groupby(['country_name'])[['pred_first', 'pred_second', 'pred_third']].sum()
    country_medal_counts['total_predicted_medals'] = country_medal_counts.sum(axis=1)
    top_country = country_medal_counts['total_predicted_medals'].idxmax()
    
    return render_template('prediction_sequence.html', top_country=top_country)


@app.route('/predictions')
def predictions():
    discipline_filter = request.args.get('discipline', 'All')
    medal_filter = request.args.get('medal', 'All')
    country1 = request.args.get('country1', 'None')
    country2 = request.args.get('country2', 'None')

    # Filter data based on the selected filters
    filtered_data = data.copy()
    if discipline_filter != 'All':
        filtered_data = filtered_data[filtered_data['discipline'] == discipline_filter]
    if medal_filter == 'Gold':
        filtered_data['total_predicted_medals'] = filtered_data['pred_first']
    elif medal_filter == 'Silver':
        filtered_data['total_predicted_medals'] = filtered_data['pred_second']
    elif medal_filter == 'Bronze':
        filtered_data['total_predicted_medals'] = filtered_data['pred_third']
    else:
        filtered_data['total_predicted_medals'] = filtered_data['pred_first'] + filtered_data['pred_second'] + filtered_data['pred_third']

    filtered_country_medal_counts = filtered_data.groupby(['country_name', 'country_3_letter_code'])['total_predicted_medals'].sum().reset_index()
    filtered_country_medal_counts = filtered_country_medal_counts[filtered_country_medal_counts['total_predicted_medals'] > 0]

    # Sort by total_predicted_medals and take the top 10 countries for filtered data
    top_10_countries_filtered = filtered_country_medal_counts.sort_values(by='total_predicted_medals', ascending=False).head(10)

    colorscale = [
        [0, '#075C6C'],
        [1, '#15B7AF']
    ]

    gradient_colors = [
        "#14b8af", "#00a9a9", "#0099a1", "#008a98", "#007b8f", "#006d84", "#005f78", "#00516c", "#00435f", "#013651"
    ]

    bar_fig = px.bar(top_10_countries_filtered, x='country_3_letter_code', y='total_predicted_medals',
                    #  hover_data=[''],
                     title='Top 10 Filtered Nations',
                     labels={'total_predicted_medals': 'Total Predicted Medals', 'country_3_letter_code': 'Nation'},
                     color='total_predicted_medals',
                     color_continuous_scale=colorscale)
    bar_fig.update_layout(xaxis={'categoryorder': 'total descending'})

    pie_fig = px.pie(top_10_countries_filtered, names='country_3_letter_code', values='total_predicted_medals',
                     title='Distribution of Predicted Medals',
                     labels={'total_predicted_medals': 'Total Predicted Medals', 'country_3_letter_code': 'Nation'})
    
    pie_fig.update_traces(marker=dict(colors=gradient_colors[:len(top_10_countries_filtered)]))


    bar_graph_json = pio.to_json(bar_fig)
    pie_chart_json = pio.to_json(pie_fig)

    # Get unique disciplines for filter options
    disciplines = ['All'] + sorted(data['discipline'].unique().tolist())
    medals = ['All', 'Gold', 'Silver', 'Bronze']
    countries = sorted(data['country_name'].unique().tolist())

    country_medal_counts = data.groupby(['country_name', 'country_3_letter_code'])[['pred_first', 'pred_second', 'pred_third']].sum().reset_index()
    country_medal_counts['total_predicted_medals'] = country_medal_counts['pred_first'] + country_medal_counts['pred_second'] + country_medal_counts['pred_third']
    country_medal_counts = country_medal_counts.rename(columns={
        'pred_first': 'gold_count',
        'pred_second': 'silver_count',
        'pred_third': 'bronze_count',
        'total_predicted_medals': 'total'
    })
    top_5_countries = country_medal_counts.sort_values(by='total', ascending=False).head(5).to_dict(orient='records')
    for idx, row in enumerate(top_5_countries):
        row['ranking'] = idx + 1

    return render_template('index.html', bar_graph_json=bar_graph_json, pie_chart_json=pie_chart_json,
                           disciplines=disciplines, medals=medals, countries=countries,
                           selected_discipline=discipline_filter, selected_medal=medal_filter,
                           selected_country1=country1, selected_country2=country2,
                           table_data=top_10_countries_filtered.to_dict(orient='records'), top_5_countries=top_5_countries)

@app.route('/compare_nations')
def compare_nations():
    country1 = request.args.get('country1', 'None')
    country2 = request.args.get('country2', 'None')

    color_discrete_map = {}
    if country1 != 'None':
        color_discrete_map[country1] = '#075C6C'
    if country2 != 'None':
        color_discrete_map[country2] = '#15B7AF'

    comparison_data = None
    if country1 != 'None' and country2 != 'None':
        comparison_data = data[(data['country_name'] == country1) | (data['country_name'] == country2)]
        comparison_data = comparison_data.groupby(['discipline', 'country_name'])[['pred_first', 'pred_second', 'pred_third']].sum().reset_index()
        comparison_data['total_predicted_medals'] = comparison_data['pred_first'] + comparison_data['pred_second'] + comparison_data['pred_third']
        
        top_10_disciplines = comparison_data.groupby('discipline')['total_predicted_medals'].sum().reset_index().sort_values(by='total_predicted_medals', ascending=False).head(10)['discipline']
        comparison_data = comparison_data[comparison_data['discipline'].isin(top_10_disciplines)]
        
        top_10_table_data = comparison_data.sort_values(by='total_predicted_medals', ascending=False).head(10).to_dict(orient='records')

        top_10_bar_fig = px.bar(comparison_data, x='discipline', y='total_predicted_medals', color='country_name',
                                title='Top 10 Events by Predicted Medals for 2024',
                                labels={'total_predicted_medals': 'Total Predicted Medals', 'discipline': 'Event', 'country_name': 'Nation'},
                                color_discrete_map=color_discrete_map)
        top_10_bar_fig.update_layout(xaxis={'categoryorder': 'total descending'})
        top_10_bar_graph_json = pio.to_json(top_10_bar_fig)
    else:
        top_10_table_data = []
        top_10_bar_graph_json = None

    countries = sorted(data['country_name'].unique().tolist())

    return render_template('compare_nations.html', countries=countries,
                           selected_country1=country1, selected_country2=country2,
                           top_10_table_data=top_10_table_data, top_10_bar_graph_json=top_10_bar_graph_json)

@app.route('/data_description')
def data_description():
    with open('remove_data.py', 'r') as file:
        remove_data_script = file.read()
    with open('clean_data.py', 'r') as file:
        clean_data_script = file.read()
    with open('predict_script.py', 'r') as file:
        predict_script = file.read()

    return render_template('data_description.html', remove_data_script=remove_data_script, 
                           clean_data_script=clean_data_script, predict_script=predict_script)

@app.route('/view_all_data')
def view_all_data():
    country_medal_counts = data.groupby(['country_name', 'country_3_letter_code'])[['pred_first', 'pred_second', 'pred_third']].sum().reset_index()
    country_medal_counts['total'] = country_medal_counts['pred_first'] + country_medal_counts['pred_second'] + country_medal_counts['pred_third']
    country_medal_counts = country_medal_counts.rename(columns={
        'pred_first': 'gold_count',
        'pred_second': 'silver_count',
        'pred_third': 'bronze_count'
    })
    country_medal_counts = country_medal_counts.sort_values(by='total', ascending=False)

    most_golds = country_medal_counts.loc[country_medal_counts['gold_count'].idxmax()]
    most_silvers = country_medal_counts.loc[country_medal_counts['silver_count'].idxmax()]
    most_bronzes = country_medal_counts.loc[country_medal_counts['bronze_count'].idxmax()]
    least_medals = country_medal_counts.loc[country_medal_counts['total'].idxmin()]

    insights = {
        'most_golds': most_golds.to_dict(),
        'most_silvers': most_silvers.to_dict(),
        'most_bronzes': most_bronzes.to_dict(),
        'least_medals': least_medals.to_dict()
    }

    country_medal_counts = country_medal_counts.reset_index(drop=True)
    country_medal_counts['ranking'] = country_medal_counts.index + 1
    country_medal_counts = country_medal_counts.to_dict(orient='records')

    return render_template('view_all_data.html', country_medal_counts=country_medal_counts, insights=insights)


if __name__ == '__main__':
    app.run(debug=True)
