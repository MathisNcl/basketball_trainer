import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html

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
                    className="btn btn-warning",
                ),
            ],
            style={"textAlign": "center"},
        ),
    ],
    body=True,
)
