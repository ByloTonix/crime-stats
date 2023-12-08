from flask import Flask, request, jsonify, send_file
import pandas as pd
import plotly.express as px
import io

app = Flask(__name__)

df = pd.read_csv("../data/crime.csv", parse_dates=["month"], dayfirst=True)
crime_sum = int(df['Total_crimes'].sum())
data_info = str(df.mean(numeric_only=True)).split()
x = [[data_info[i], data_info[i+1]] for i in range(0, len(data_info), 2)][:-1]
s = ""
for i, j in x:
    s += f"{i}: {j} \n"
date = df["month"].dt.year

@app.route('/')
def index():
    return "Finally! This piece of code (Flask Server) is running!"

@app.route('/process_data', methods=['POST'])
def process_data():
    data = request.get_json()
    action = data.get('action')

    if data.get('year'):
        year = data.get('year')

    if action == 'get_crimes':
        fig = px.line(df, x='month', y='Total_crimes', title='Total Crimes Over Time')
        img_bytes = io.BytesIO()
        fig.write_image(img_bytes, format='png')
        img_bytes.seek(0)
        return send_file(img_bytes, mimetype='image/png')

    elif action == 'get_dataset_info':
        processed_data = s
    elif action == 'get_graph':
        
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
    app.run(debug=True)
