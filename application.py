import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, Event

import pickle as pkl
import numpy as np
import pandas as pd

fname = "pickle_logreg4_model.pkl"
with open(fname, "rb") as InFile:
    model = pkl.load(InFile)

fname = "pickle_logreg4_model_names.pkl"
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
        html.Label("Boston MA"),
        dcc.Dropdown(
            id="SITE__BO",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("East Hamptons NY"),
        dcc.Dropdown(
            id="SITE__EH",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Marthas Vinyard"),
        dcc.Dropdown(
            id="SITE__MV",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("California"),
        dcc.Dropdown(
            id="SITE__CA",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Year 2014"),
        dcc.Dropdown(
            id="YR__2014",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Year 2015"),
        dcc.Dropdown(
            id="YR__2015",
            options=[{"label": "Yes", "value": "1"}, {"label": "No", "value": "0"}],
        ),
        html.Label("Year 2016"),
        dcc.Dropdown(
            id="YR__2016",
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
        State("SITE__BO", "value"),
        State("SITE__EH", "value"),
        State("SITE__MV", "value"),
        State("SITE__CA", "value"),
        State("YR__2014", "value"),
        State("YR__2015", "value"),
        State("YR__2016", "value"),
        State("age", "value"),
        State("number_of_symptoms", "value"),
        State("month_entry", "value"),
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
    SITE__BO,
    SITE__EH,
    SITE__MV,
    SITE__CA,
    YR__2014,
    YR__2015,
    YR__2016,
    age,
    number_of_symptoms,
    month_entry,
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
    imp["SITE__BO"] = SITE__BO
    imp["SITE__EH"] = SITE__EH
    imp["SITE__MV"] = SITE__MV
    imp["SITE__CA"] = SITE__CA
    imp["YR__2014"] = YR__2014
    imp["YR__2015"] = YR__2015
    imp["YR__2016"] = YR__2016
    imp["age"] = age
    imp["number_of_symptoms"] = number_of_symptoms
    imp["month_entry"] = month_entry

    imp = pd.Series(imp)
    print(imp)
    print(imp.dtypes)

    probs = model.predict_proba(imp.values.reshape(1, -1)) * 100
    print(probs)
    return f"{probs[0][1]:.2f}% risk of being positive for Lyme disease"


if __name__ == "__main__":
    app.run_server(debug=True)
