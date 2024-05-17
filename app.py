from flask import Flask, render_template
import json
import pandas as pd

app = Flask(__name__)

#Since the data will not change, I will prepare it at the very beginning instead of processing it in every single request.
def prepare_data():
    with open('data/users.json') as user_data, open('data/simulations.json') as simulation_data:
        users = json.load(user_data)
        simulations = json.load(simulation_data)
    
    #I will approach this as they are sql tables, I will join them and make query logics
    users_df = pd.DataFrame(users['users'])
    simulations_df = pd.DataFrame(simulations['simulations'])
    user_simulations = pd.merge(users_df, simulations_df, on='simulation_id', how='inner')
    
    #Again continuing with sql logic, user count for every company: I would use group by.
    company_users = user_simulations.groupby('company_id').agg(
        company_name=('company_name', 'first'), 
        user_count=('company_id', 'size')
    ).reset_index()
    
    #I am taking integer part of daily_signups since we only care about days not hours or so..
    user_simulations['signup_datetime'] = user_simulations['signup_datetime'].round().astype(int)

    #This time I will group it with signup_datetime and make aggregate operations
    daily_signups = user_simulations.groupby('signup_datetime').agg(
        daily_count=('user_id', 'size')
    )
    #Now I will try to get 'sum over' functionality in sql, I have found a function called cumsum.
    daily_users = daily_signups.sort_values(by='signup_datetime')['daily_count'].cumsum()
    
    #I am converting my final results back to json now
    company_users_json = company_users.to_json(orient='records', indent=4, force_ascii=False)
    daily_users_json = daily_users.to_json(indent=4, force_ascii=False)

    return company_users_json, daily_users_json

company_users, daily_users = prepare_data()
     
@app.route('/')
def index():
    return render_template('index.html', company_users=company_users, daily_users=daily_users)

if __name__ == '__main__':
    app.run()