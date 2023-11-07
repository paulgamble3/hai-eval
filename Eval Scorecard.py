import streamlit as st
from sample_url_config import sample_url_config
from firebase.firebase_utils import write_task_item
import json

st.set_page_config(layout="wide")

display_names = json.load(open("./app_configs/display_names.json"))

questions = json.load(open("./question_configs/main_scorecard.json"))

with st.form("test-form"):

    def generate_url(models, scripts):
        # model will come in as the actual model string
        # script will come in as the script name, so need a linker for that to the script ID
        # patient will come in as the name or 'all' - which means sample from all patients for a script

        # so given these three, I need to read from the configs, gather the relevant urls
        # and then sample from them

        url = sample_url_config(models, scripts)
        #st.write("sampled call from: " + str(models) + " " + str(scripts))
        return url
    


    # read in these lists from some dir

    url_elements = json.load(open("./app_configs/url_sampling_config.json"))


    model_list = url_elements["models"]
    script_list = url_elements["script_names"]


    models = st.multiselect(
        'Select models to sample:',
        model_list,
        model_list)
    
    scripts = st.multiselect(
        'Select scripts to sample:',
        script_list,
        script_list)
    
    
    # I actually can't seem to generate the hash on the fly
    # need to have these pre-generated and stored somewhere

    submitted = st.form_submit_button("Generate URL")

    if submitted:
        url_config = generate_url(models, scripts)
        url= url_config["url"]
        st.session_state.model = url_config["config"]["model"]
        #st.write(url)
        st.session_state.blinded = set(models) == set(model_list)
        st.header(f"[Call Page]({url})")

with st.form("feedback-form"):

    feedback_object = {}


    def submit_feedback():
        print("submitting feedback")

        feedback_object["username"] = st.session_state.username
        feedback_object["call_id"] = st.session_state.call_id
        feedback_object["blinded"] = st.session_state.blinded
        feedback_object["model"] = st.session_state.model

        for question in questions["Model"]:
            feedback_object[question["key"]] = st.session_state[question["key"]]
            st.session_state[question["key"]] = question["answer_choices"][0]
        
        for question in questions["System"]:
            feedback_object[question["key"]] = st.session_state[question["key"]]
            st.session_state[question["key"]] = question["answer_choices"][0]

        feedback_object["comments"] = st.session_state.comments
        feedback_object["include"] = st.session_state.include
        st.session_state.comments = ""
        st.session_state.include = "Yes"

        print(feedback_object)
        write_task_item(feedback_object, "hai-scorecard")
        
        st.session_state.call_id = ""


    username = st.text_input("Enter your name:", key="username")
    call_id = st.text_input("Paste the call ID:", key="call_id")

    st.header("Model")

    for question in questions["Model"]:
        st.radio("**" + question["key"] + "** - " + question["question"], question["answer_choices"], key=question["key"], horizontal=True)

    st.header("System")

    for question in questions["System"]:
        st.radio("**" + question["key"] + "** - " + question["question"], question["answer_choices"], key=question["key"], horizontal=True)

    st.header("Feedback")
    comments = st.text_area("Any comments on the call:", height=80, key="comments")
    include = st.radio("Should this call be included in the eval results?", ["Yes", "No"], key="include", horizontal=True)

    feedback_submitted = st.form_submit_button("Submit Feedback", on_click=submit_feedback)


    

    