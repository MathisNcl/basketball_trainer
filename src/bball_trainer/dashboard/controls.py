import dash_bootstrap_components as dbc
import dash_daq as daq
from dash import dcc, html
from dash_extensions import WebSocket

game_modal = dbc.Modal(
    [
        dbc.ModalBody(html.Img(id="img_game", className="image")),
        dbc.ModalFooter(
            [
                dbc.Button(
                    "Restart",
                    id="button_restart",
                    className="btn btn-primary",
                ),
                dbc.Button("Stop", id="button_stop", className="btn btn-danger"),
            ]
        ),
    ],
    id="modal_game",
    centered=False,
    className="modal-dialog image-modal-dialog",
)

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
                WebSocket(url="ws://127.0.0.1:5000/stream", id="ws"),
                game_modal,
            ],
            style={"textAlign": "center"},
        ),
    ],
    body=True,
)
