import streamlit as st
import numpy as np
import pandas as pd
import json
from firebase.firebase_utils import retrieve_feedback




# by default, load in all data
def load_all_data():
    results = retrieve_feedback("hai-scorecard")
    #build dataframe
    df = pd.DataFrame(results)
    return df

def cache_data(results_df):
    results_df.to_csv("./data/current_results.csv")

def conditional_formatting(val):
    min_val = 0.1
    max_val = 0.9



    percent = (val - min_val) / (max_val - min_val)
    percent = max(0, min(1, percent))


    max_color = [68,177,118]
    min_color = [230, 124, 115]

    r = int(min_color[0] + percent * (max_color[0] - min_color[0]))
    g = int(min_color[1] + percent * (max_color[1] - min_color[1]))
    b = int(min_color[2] + percent * (max_color[2] - min_color[2]))
    c = f'background-color: rgb({r}, {g}, {b})'
    return c


st.set_page_config(layout="wide")
st.header("UNDER CONSTRUCTION")




results_df = load_all_data()
cache_data(results_df)
# really want this to be non blocking...
# figure that out later


# get list of unique users
users = list(results_df["username"].unique())
all_models = list(results_df["model"].unique())
#users = ["paul", "Sophia", "Alex", "Meenesh", "Michelle", "Dan", "bob"]


with st.form("results-filter"):
    
    filtered_models = st.multiselect(
        'Select models to filter by:',
        all_models,
        all_models)
    # filter by users HAI vs others
    #user_type = st.radio("User Type", ["HAI", "Other"], key="user_type",horizontal=True)
    users = st.multiselect(
        'Select users to filter by:',
        users,
        users)
    # blinded calls only
    blinded = st.radio("Blinded Calls Only", ["Yes", "No"], key="blinded",horizontal=True)
    st.form_submit_button("Refresh and Filter")


# filter df
filtered_df = results_df
filtered_df = filtered_df[filtered_df["username"].isin(users)]
filtered_df = filtered_df[filtered_df["model"].isin(filtered_models)]
if blinded == "Yes":
    filtered_df = results_df[results_df["blinded"] == True]

# process df
# convert each cell to a 1 or 0 based on good or not
# need to keep track of the not asessed count


questions = json.load(open("./question_configs/main_scorecard.json"))
for q in questions["Model"] + questions["System"]:
    if q["key"] == "Overall":
        filtered_df[q["key"]] = filtered_df[q["key"]].astype(float) / 7.0
        continue
    # this is assuming 0 is bad and 1 is good
    filtered_df[q["key"]] = filtered_df[q["key"]] == q["answer_choices"][1]
    filtered_df[q["key"]] = filtered_df[q["key"]].astype(int)


def load_row_names():
    questions = json.load(open("./question_configs/main_scorecard.json"))
    model_questions = [question["key"] for question in questions["Model"]]
    system_questions = [question["key"] for question in questions["System"]]
    return {
        "Model": model_questions,
        "System": system_questions
    }

row_names = load_row_names()
#aggregate
model_question_scores = filtered_df[row_names["Model"] + ["model"]]
system_question_scores = filtered_df[row_names["System"]  + ["model"]]

model_scores = model_question_scores.groupby(["model"]).mean().T
system_scores = system_question_scores.groupby(["model"]).mean().T

print(model_scores)


models = list(model_scores.columns)

# for m in models:
#     model_scores.iloc[-1][m] = model_scores.iloc[-1][m] / 7.
# group by model
# sum each column
# divide by count
# write to df
# write to table
print(model_scores)

# TODO include count
# TODO all scores should be % good response




model_df = pd.DataFrame(model_scores, columns = models, index=row_names["Model"])
model_df = model_df.style.applymap(conditional_formatting)


st.header("Model Scores")
st.table(model_df)

system_df = pd.DataFrame(system_scores, columns = models, index=row_names["System"])
system_df = system_df.style.applymap(conditional_formatting)
st.header("System Scores")
st.table(system_df)
