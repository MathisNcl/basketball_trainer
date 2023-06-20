import dash_bootstrap_components as dbc
from dash import html, dcc
import dash_daq as daq

layout = dbc.Card(
    [
        html.Div(
            [
                dbc.Label("Time"),
                dbc.Input(id="game-time", type="number", value=30),
            ]
        ),
        html.Div(
            [
                dbc.Label("Difficulty"),
                dcc.Dropdown(
                    id="game-difficulty",
                    options=[{"label": col, "value": col} for col in ["Easy", "Medium", "Hard"]],
                    value="Easy",
                ),
            ]
        ),
        html.Div(
            [
                dbc.Label("Activate hand constraint"),
                # TODO: add a modal
                daq.BooleanSwitch(id="game-hand-constraint-switch", on=False),
            ],
            className="form-check",
        ),
        html.Div(
            [
                html.Br(),
                html.Button(
                    children="Start a game",
                    n_clicks=0,
                    type="submit",
                    id="startingButton",
                    className="btn btn-lg",
                    style={"color": "white", "backgroundColor": "#fb5607"},
                ),
            ],
            style={"textAlign": "center"},
        ),
    ],
    body=True,
)
