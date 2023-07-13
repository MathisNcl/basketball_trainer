from subprocess import call
from typing import Any, Dict, List, Optional

import dash_auth
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import requests
from dash import Dash, Input, Output, State, ctx, dash_table, dcc, html
from dash.exceptions import PreventUpdate
from flask import Flask

from bball_trainer import settings
from bball_trainer.dashboard import controls, main_page, profile

server = Flask(__name__)
# FIXME: add a real user managing
VALID_USERNAME_PASSWORD_PAIRS = {"localadmin": "localadmin"}
USER_ID: int = 9999999
app = Dash(
    __name__,
    server=server,
    title="Basketball Trainer",
    update_title="Loading...",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.css.config.serve_locally = True

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)

app.layout = html.Div([dbc.Row(id="topPageContent", children=main_page.layout), dbc.Row(id="PageContent")])


################################################################################
# LOGIN BUTTON CLICKED - Blocked input
################################################################################
@app.callback(
    [
        Output("usernameBox", "disabled"),
        Output("passwordBox", "disabled"),
        Output("loginButton", "hidden"),
        Output("logoutButton", "hidden"),
        Output("usernameBox", "value"),
        Output("usernameBox", "className"),
        Output("passwordBox", "value"),
        Output("passwordBox", "className"),
        Output("signInButton", "hidden"),
    ],
    [Input("loginButton", "n_clicks"), Input("passwordBox", "n_submit"), Input("logoutButton", "n_clicks")],
    [State("usernameBox", "value"), State("passwordBox", "value")],
)
def login_logout(login_click: int, passwordSubmit: int, logout_click: int, username: str, password: str) -> List[Any]:
    response: requests.Response = requests.post(
        url=f"{settings.URL}/user/login/",
        json={"pseudo": username, "password": password},
    )
    data: Dict[str, Any] = response.json()
    if ctx.triggered_id in ["loginButton", "passwordBox"]:
        if response.status_code == 202 and data["connected"]:
            global USER_ID
            USER_ID = data["id"]
            return [True] * 3 + [False, username, "form-control is-valid", password, "form-control is-valid", True]
        else:
            return [False] * 3 + [True, "", "form-control is-invalid", "", "form-control is-invalid", False]
    elif ctx.triggered_id == "logoutButton":
        return [False] * 3 + [True, "", "form-control", "", "form-control", False]
    else:
        raise PreventUpdate


################################################################################
# SIGNIN Modal
################################################################################
@app.callback(
    [Output("signInModal", "is_open"), Output("modal_error", "children")],
    [
        Input("signInButton", "n_clicks"),
        Input("modal_submit_button", "n_clicks"),
        Input("modal_cancel_button", "n_clicks"),
    ],
    [
        State("signInModal", "is_open"),
        State("modal_username", "value"),
        State("modal_password", "value"),
        State("modal_lastname", "value"),
        State("modal_firstname", "value"),
        State("modal_age", "value"),
    ],
)
def show_modal_signin(
    n_add: int,
    n_submit: int,
    n_cancel: int,
    is_open: bool,
    username: str,
    password: str,
    lastname: str,
    firstname: str,
    age: Optional[int],
) -> tuple[bool, str]:
    """Show modal for signing in"""
    if ctx.triggered_id == "signInButton":
        return True, ""
    elif ctx.triggered_id == "modal_submit_button":
        response: requests.Response = requests.post(
            url=f"{settings.URL}/user/",
            json={"pseudo": username, "last_name": lastname, "first_name": firstname, "age": age, "password": password},
        )
        if response.status_code != 201:
            return True, response.json()["detail"]
    return False, ""


################################################################################
# Display infos when connected
################################################################################
@app.callback(
    Output("PageContent", "children"),
    [Input("logoutButton", "hidden")],
    [State("usernameBox", "value")],
)
def display_card_infos(logoutButton: bool, username: str) -> Any:
    if logoutButton is False:
        return dbc.Container(
            [
                html.H1("Enhance your handles!", id="title-page"),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(controls.layout, md=4),
                        dbc.Col(dcc.Graph(id="progession-graph"), md=8),
                        html.Div(id="useless"),
                    ],
                    align="center",
                ),
                dbc.Row(
                    [
                        dbc.Col(profile.layout, width=4),
                        dbc.Col(
                            html.Button(
                                children="Reload",
                                n_clicks=0,
                                type="submit",
                                id="reloadButton",
                                className="btn btn-primary",
                            ),
                            width=1,
                        ),
                        dbc.Col(
                            dash_table.DataTable(
                                id="leaderboard-table",
                                columns=[
                                    {"name": "Index", "id": "index"},
                                    {"name": "User ID", "id": "user_id"},
                                    {"name": "Score", "id": "score"},
                                    {"name": "Time", "id": "time"},
                                    {"name": "Point per second", "id": "point_per_sec"},
                                    {"name": "Created At", "id": "created_at"},
                                ],
                                style_table={"height": "300px", "overflowY": "scroll"},
                                style_data={"whiteSpace": "normal", "height": "auto"},
                                style_cell={"textAlign": "left"},
                                style_header={"fontWeight": "bold"},
                            )
                        ),
                    ]
                ),
            ],
            fluid=True,
        )
    else:
        pass


################################################################################
# Run the game
################################################################################
@app.callback(
    Output("useless", "children"),
    [Input("startingButton", "n_clicks")],
    [
        State("game-time", "value"),
        State("game-difficulty", "value"),
        State("game-hand-constraint-switch", "on"),
    ],
)
def launch_game(n_start: int, time: int, difficulty: str, hand_constraint: bool) -> str:
    # FIXME: find a way to test it
    if ctx.triggered_id == "startingButton":  # pragma: nocover
        script_path = settings.PACKAGE_DIR / "game.py"
        call(
            ["python3", script_path, "-u", str(USER_ID), "-t", str(time), "-d", difficulty, "-hc", str(hand_constraint)]
        )

    return ""


################################################################################
# Fill profile
################################################################################
@app.callback(
    [
        Output("profile_id", "children"),
        Output("profile_username", "children"),
        Output("profile_lastname", "children"),
        Output("profile_firstname", "children"),
        Output("profile_age", "children"),
        Output("profile_date", "children"),
    ],
    [Input("logoutButton", "hidden")],
)
def show_profile(logout_h: bool) -> tuple[int, str, str, str, Optional[int], str]:
    if logout_h is False:
        # requests
        response: requests.Response = requests.get(
            url=f"{settings.URL}/user/{USER_ID}/",
        )
        data = response.json()
        return (data["id"], data["pseudo"], data["last_name"], data["first_name"], data["age"], data["created_at"])
    else:
        raise PreventUpdate


################################################################################
# Output graph games
################################################################################
@app.callback(
    Output("progession-graph", "figure"),
    [Input("logoutButton", "hidden"), Input("reloadButton", "n_clicks")],
)
def show_graph(logout_h: bool, reload_n: int) -> Any:
    if ctx.triggered_id == "reloadButton" or logout_h is False:
        # requests
        response: requests.Response = requests.get(
            url=f"{settings.URL}/game_record/{USER_ID}/",
        )
        df = pd.DataFrame(response.json())
        data = [
            go.Scatter(
                x=[i for i in range(len(df))],
                y=df["score"],
                mode="lines+markers",
                text=df["created_at"],
                marker={"size": 8},
                hoverinfo="text+y",
            )
        ]
        layout = {
            "xaxis": {"title": "Games", "showticklabels": False},
            "yaxis": {"title": "Score", "tick0": 0, "dtick": 1},
        }
        return go.Figure(data=data, layout=layout)
    else:
        raise PreventUpdate


################################################################################
# Output leaderboard
################################################################################
@app.callback(
    Output("leaderboard-table", "data"),
    [Input("logoutButton", "hidden"), Input("reloadButton", "n_clicks")],
)
def show_leaderboard(logout_h: bool, reload_n: int) -> Any:
    if ctx.triggered_id == "reloadButton" or logout_h is False:
        # requests
        response: requests.Response = requests.get(
            url=f"{settings.URL}/leaderboard/",
        )
        df = pd.DataFrame(response.json())
        df["index"] = range(1, len(df) + 1)
        return df.to_dict("records")
    else:
        raise PreventUpdate


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)  # pragma: nocover
