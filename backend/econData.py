from flask import Flask, render_template
import pandas as pd
import plotly.express as px
from fredapi import Fred
from pymongo import MongoClient
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

try:
    mongo_client = MongoClient("mongodb+srv://singhmanraj8:Manrajat16@jobsopenings1.qecqz4w.mongodb.net/")
    db = mongo_client["jobsopenings1"]
    collection = db["openings"]
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

try:
    fred_key = '1d9f2645898e9ed1556ae8a6f84239bc'
    fred = Fred(api_key=fred_key)
except Exception as e:
    print(f"Error connecting to Fred: {e}")

def check_duplicate(date):
    # Check if a document with the given date already exists in the collection
    return collection.find_one({'Date': date}) is not None

@app.route('/')
def index():
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

    # Check for duplicates and insert data to MongoDB
    for date in job_openings_results.index:
        if not check_duplicate(date):
            data_to_insert = {
                'Date': date,
                'Data': job_openings_results.loc[date].to_dict()
            }
            collection.insert_one(data_to_insert)

    # Plot using Plotly Express
    fig = px.line(job_openings_results, labels={
                    "Date": "TimeFrame",
                    "value": "Rate employment",
                    "variable": "Sector"
                }, width=1100, height=600)

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)
    
    message='Data Updated'
    # Render the template with the Plotly HTML
    return render_template('index.html', plot_html=plot_html, message=message)

@app.route('/databaseGet')
def databaseGet():
    # Fetch data from MongoDB
    cursor = collection.find()
    job_openings_results = pd.DataFrame(list(cursor))

    # Convert 'Date' to datetime and set it as the index
    job_openings_results['Date'] = pd.to_datetime(job_openings_results['Date'])
    job_openings_results.set_index('Date', inplace=True)

    # Flatten the 'Data' column
    flattened_data = pd.json_normalize(job_openings_results['Data'])
    flattened_data['Date'] = job_openings_results.index

    # Sort the DataFrame based on the 'Date' column
    flattened_data = flattened_data.sort_values('Date')

    # Set 'Date' as the index
    flattened_data.set_index('Date', inplace=True)

    data_list = flattened_data.to_dict(orient='records')
    
    # Convert DataFrame to list of dictionaries including the date
    data_list = []
    for date, row in flattened_data.iterrows():
        data_dict = {'Date': date.strftime('%Y-%m-%d')}
        data_dict.update(row.to_dict())
        data_list.append(data_dict)
    print('-----------------------------')
    print(data_list)

    # Plot using Plotly Express
    fig = px.line(flattened_data, labels={
        "Date": "TimeFrame",
        "value": "Rate employment",
        "variable": "Sector"
    }, width=1100, height=600)

    # Convert the Plotly figure to HTML
    plot_html = fig.to_html(full_html=False)

    message='Recieved Data'
    # Render the template with the Plotly HTML
    return data_list,message


if __name__ == '__main__':
    app.run(debug=True,port=4000)
