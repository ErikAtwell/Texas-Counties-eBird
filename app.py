from flask import Flask, request, render_template
import pandas as pd
import re 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    county_input = request.form['county']  # Get county input from user
    personal_data = request.files['personal_data'] # Get personal eBird data from user

    # Built in general eBird data for Texas Counties
    general_df = pd.read_csv(r"C:\Users\erika\OneDrive\Desktop\eBird\TexasCountyBirdData.csv")

    personal_df = pd.read_csv(personal_data)



    # Read the selected county
    general_county_data = general_df[general_df['County'].str.lower() == county_input.lower()]
    personal_county_data = personal_df[personal_df['County'].str.lower() == county_input.lower()]

    # If user has no birds in that county
    if personal_county_data.empty:
        return render_template('index.html', tables=[], error=f"0 birds in {county_input} county")

    # select unique species from your personal county list
    personal_species_set = set(personal_county_data['Common Name'].str.lower())

    # Initialize dataframe
    weeks = [
        'Jan1', 'Jan2', 'Jan3', 'Jan4', 
        'Feb1', 'Feb2', 'Feb3', 'Feb4', 
        'Mar1', 'Mar2', 'Mar3', 'Mar4',
        'Apr1', 'Apr2', 'Apr3', 'Apr4',
        'May1', 'May2', 'May3', 'May4',
        'Jun1', 'Jun2', 'Jun3', 'Jun4',
        'Jul1', 'Jul2', 'Jul3', 'Jul4',
        'Aug1', 'Aug2', 'Aug3', 'Aug4',
        'Sep1', 'Sep2', 'Sep3', 'Sep4',
        'Oct1', 'Oct2', 'Oct3', 'Oct4',
        'Nov1', 'Nov2', 'Nov3', 'Nov4',
        'Dec1', 'Dec2', 'Dec3', 'Dec4'
    ]


    # Initialize a dictionary to hold counts for each week
    week_counts = {week: 0 for week in weeks}

    # Check if the species is not in the personal data
    for _, row in general_county_data.iterrows():
        common_name = row['Common Name'].lower()
        if not re.search(r'[/x]| x |sp\.|domestic', common_name):
            if common_name not in personal_species_set:
                # Check each week's percentage for the species
                for week in weeks:
                    percentage = row[week]
                    if percentage > 0.05:
                        week_counts[week] += 1


    result_df = pd.DataFrame(week_counts.items(), columns=['Week', 'Count'])


    reshaped_df = pd.DataFrame(columns=['Week', 'Count'])

    for i in range(12):  # 12 rows
            row_data = []
            for j in range(4):  # 4 columns
                index = i * 4 + j
                if index < len(result_df):
                    row_data.append(result_df.iloc[index].values)
            reshaped_df = pd.concat([reshaped_df, pd.DataFrame(row_data, columns=['Week', 'Count'])], ignore_index=True)


    return render_template('index.html', tables=[reshaped_df.to_html(classes='data', index=False)])

if __name__ == '__main__':
    app.run(debug=True)
