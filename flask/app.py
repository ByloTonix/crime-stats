from flask import Flask, request, jsonify, send_file
import plotly.express as px
import pandas as pd
import io

app = Flask(__name__)

def process_data():
    df = pd.read_csv(PATH, parse_dates=["month"], dayfirst=True)
    date = df["month"].dt.year

    crime_sum = int(df['Total_crimes'].sum())
    data_info = str(df.mean(numeric_only=True)).split()
    data_info_simplified = [[data_info[i], data_info[i+1]] for i in range(0, len(data_info), 2)][:-1]
    data_info = "\n".join([f"{i}: {j}" for i, j in data_info_simplified])

    return df, date, data_info

@app.route('/')
def index():
    return "Finally! This piece of code (Flask Server) is running!"

@app.route('/process_data', methods=['POST'])
def process_data_route():
    data = request.get_json()
    action = data.get('action')

    if data.get('year'):
        year = data.get('year')

    if action == 'get_crimes':
        df, _, _ = process_data()
        fig = px.line(df, x='month', y='Total_crimes', title='Total Crimes Over Time')
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')

    elif action == 'get_dataset_info':
        _, _, processed_data = process_data()
        
    elif action == 'get_graph':
        df, date, _ = process_data()
        filtered_data = df[date == year]
        crime_data = filtered_data.iloc[:, 2:].sum().sort_values(ascending=False)
        fig = px.bar(
            x=crime_data.index,
            y=crime_data.values,
            labels={"x": "Crime Types", "y": "Total Crimes"},
            title=f"Crimes in {year}",
            color=crime_data.index,
            height=500
        )
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')
    else:
        processed_data = "Incorrect request"

    return jsonify({'result': processed_data})

if __name__ == '__main__':
    app.run()
