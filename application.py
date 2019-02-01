import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

import pickle as pkl
import numpy as np
import pandas as pd

fname = "pickle_RF_model.pkl"
with open(fname, "rb") as InFile:
    model = pkl.load(InFile)

fname = "pickle_RF_model_names.pkl"
with open(fname, "rb") as InFile:
    cols = pkl.load(InFile)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {"background": "#ffb549", "text": "#111111"}

app.layout = html.Div(
    style={
        "backgroundColor": colors["background"],
        "width": "95%",
        "margin-left": "auto",
        "margin-right": "auto",
    },
    children=[
        html.H1(
            children='"Lyme Spotter"',
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Div(
            "A companion diagnostic tool for patients with suspected Lyme disease",
            style={"textAlign": "center", "color": colors["text"]},
        ),
        html.Label("Sex"),
        dcc.Dropdown(
            id="sex",
            options=[
                {"label": "Male", "value": "0"},
                {"label": "Female", "value": "1"},
            ],
        ),
        html.Label("Rash Size"),
        dcc.Dropdown(
            id="large_rash",
            options=[
                {"label": "> 5 cm", "value": "1"},
                {"label": "< 5 cm", "value": "0"},
            ],
        ),
        html.Label("Prophylactic Antibiotics Taken Today or Prior to Today?"),
        dcc.Dropdown(
            id="proph_abs",
            options=[{"label": "No", "value": "0"}, {"label": "Yes", "value": "1"}],
        ),
        html.Label("Ethnicity"),
        dcc.Dropdown(
            id="ethnicity_binary",
            options=[
                {"label": "White", "value": "1"},
                {"label": "Other", "value": "0"},
            ],
        ),
        html.Label("Rash Expansion"),
        dcc.Dropdown(
            id="expansion",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Bullseye Shape Rash"),
        dcc.Dropdown(
            id="bullseye_shape",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Past History of Lyme Disease"),
        dcc.Dropdown(
            id="past_history_lyme",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Past History of Cancer"),
        dcc.Dropdown(
            id="cancer_history",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Currently Taking Other Medications"),
        dcc.Dropdown(
            id="other_meds",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Observed Tick?"),
        dcc.Dropdown(
            id="recall_current_bite",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Headache"),
        dcc.Dropdown(
            id="headache",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Fatigue"),
        dcc.Dropdown(
            id="fatigue",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Fever"),
        dcc.Dropdown(
            id="fever",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Chills"),
        dcc.Dropdown(
            id="chills",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Joint and/or Muscle Pain"),
        dcc.Dropdown(
            id="joint_or_muscle_pain",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("City of Residence is Endemic (Eastern Seaboard)"),
        dcc.Dropdown(
            id="city_binary",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Multiple Locations of Rash on Body"),
        dcc.Dropdown(
            id="multiple_EM",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Age: "),
        dcc.Input(id="age", value="0", type="number"),
        html.Br(),
        html.Label("Number of Symptoms: "),
        dcc.Input(id="number_of_symptoms", value="0", type="number"),
        html.Br(),
        html.Label("Month of Entry (no zero): "),
        dcc.Input(id="month_entry", value="0", type="number"),
        html.Br(),
        html.Label("Body Mass Index: "),
        dcc.Input(id="body_mass_index", value="0", type="number"),
        html.Br(),
        html.Label("Years Living at Permanent Endemic Site Residence: "),
        dcc.Input(id="yrs_at_residence", value="0", type="number"),
        html.Br(),
        html.Button(id="submit-button", children="Submit"),
        html.Div(id="output-a", style={"font-size": "36px", "text-align": "center"}),
    ]
)


@app.callback(
    Output("output-a", "children"),
    [Input("submit-button", "n_clicks")],
    [
        State("sex", "value"),
        State("large_rash", "value"),
        State("proph_abs", "value"),
        State("ethnicity_binary", "value"),
        State("expansion", "value"),
        State("bullseye_shape", "value"),
        State("past_history_lyme", "value"),
        State("cancer_history", "value"),
        State("other_meds", "value"),
        State("recall_current_bite", "value"),
        State("headache", "value"),
        State("fatigue", "value"),
        State("fever", "value"),
        State("chills", "value"),
        State("joint_or_muscle_pain", "value"),
        State("city_binary", "value"),
        State("multiple_EM", "value"),
        State("age", "value"),
        State("number_of_symptoms", "value"),
        State("month_entry", "value"),
        State("body_mass_index", "value"),
        State("yrs_at_residence", "value"),
    ],
)
def predict(
    n_clicks,
    sex,
    large_rash,
    proph_abs,
    ethnicity_binary,
    expansion,
    bullseye_shape,
    past_history_lyme,
    cancer_history,
    other_meds,
    recall_current_bite,
    headache,
    fatigue,
    fever,
    chills,
    joint_or_muscle_pain,
    city_binary,
    multiple_EM,
    age,
    number_of_symptoms,
    month_entry,
    body_mass_index,
    yrs_at_residence,
):
    imp = dict()
    imp["sex"] = sex
    imp["large_rash"] = large_rash
    imp["proph_abs"] = proph_abs
    imp["ethnicity_binary"] = ethnicity_binary
    imp["expansion"] = expansion
    imp["bullseye_shape"] = bullseye_shape
    imp["past_history_lyme"] = past_history_lyme
    imp["cancer_history"] = cancer_history
    imp["other_meds"] = other_meds
    imp["recall_current_bite"] = recall_current_bite
    imp["headache"] = headache
    imp["fatigue"] = fatigue
    imp["fever"] = fever
    imp["chills"] = chills
    imp["joint_or_muscle_pain"] = joint_or_muscle_pain
    imp["city_binary"] = ethnicity_binary
    imp["multiple_EM"] = multiple_EM
    imp["age"] = age
    imp["number_of_symptoms"] = number_of_symptoms
    imp["month_entry"] = month_entry
    imp["body_mass_index"] = body_mass_index
    imp["yrs_at_residence"] = yrs_at_residence

    imp = pd.Series(imp)
    print(imp)
    print(imp.dtypes)

    probs = model.predict_proba(imp.values.reshape(1, -1)) * 100
    print(probs)
    return f"{probs[0][1]:.2f}% risk of being positive for Lyme disease"


if __name__ == "__main__":
    app.run_server(debug=True, port = 8050, host = '0.0.0.0')
