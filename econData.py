from flask import Flask, render_template
import pandas as pd
import plotly.express as px
from fredapi import Fred

app = Flask(__name__)

@app.route('/')
def index():
    # Your Fred API key
    fred_key = '1d9f2645898e9ed1556ae8a6f84239bc'

    # Initialize Fred API
    fred = Fred(api_key=fred_key)

    # Search for job openings data
    job_openings = fred.search(
        text='Job Openings',
        filter=('frequency', 'Monthly')
    )
    job_openings = job_openings.query('seasonal_adjustment == "Seasonally Adjusted" and units =="Rate"')
    job_openings = job_openings.loc[job_openings['title'].str.contains('Job Openings: ')]
    not_req = ['JTS00NEJOR', 'JTS00MWJOR', 'JTS00WEJOR', 'JTS00SOJOR']
    job_openings = job_openings.query('seasonal_adjustment == "Seasonally Adjusted" and units =="Rate" and id not in @not_req')

    # Fetch time series data for job openings
    all_results = []
    for my_id in job_openings.index:
        results = fred.get_series(my_id)
        results = results.to_frame(name=my_id)
        all_results.append(results)

    job_openings_results = pd.concat(all_results, axis=1)
    job_openings_results.index.name = 'Date'

    # Drop NaN values
    job_openings_results = job_openings_results.dropna()

    # Rename columns based on sector
    id_to_sector = job_openings['title'].str.replace('Job Openings: ', '').to_dict()
    job_openings_results.columns = [id_to_sector[c] for c in job_openings_results.columns]

    # Plot using Plotly Express
    fig = px.line(job_openings_results, labels={
                     "Date": "TimeFrame",
                     "value": "Rate employment",
                     "variable": "Sector"
                 }, width=1100, height=600)

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    # Render the template with the Plotly HTML
    return render_template('index.html', plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True,port=4000)
