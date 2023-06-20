from subprocess import call
from typing import Any, Dict, List, Optional

import dash_auth
import dash_bootstrap_components as dbc
import requests
from dash import Dash, Input, Output, State, ctx, html
from flask import Flask

from bball_trainer import settings
from bball_trainer.dashboard import controls, main_page

server = Flask(__name__)
# FIXME: add a real user managing
VALID_USERNAME_PASSWORD_PAIRS = {"localadmin": "localadmin"}
URL: str = "http://localhost:8000"

app = Dash(
    __name__,
    server=server,
    title="Basketball Trainer",
    update_title="Loading...",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
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
        Output("loginButton", "n_clicks"),
        Output("logoutButton", "hidden"),
        Output("logoutButton", "n_clicks"),
        Output("usernameBox", "value"),
        Output("usernameBox", "className"),
        Output("passwordBox", "value"),
        Output("passwordBox", "className"),
        Output("passwordBox", "n_submit"),
        Output("signInButton", "hidden"),
    ],
    [Input("loginButton", "n_clicks"), Input("passwordBox", "n_submit"), Input("logoutButton", "n_clicks")],
    [State("usernameBox", "value"), State("passwordBox", "value")],
)
def login_logout(login_click: int, passwordSubmit: int, logout_click: int, username: str, password: str) -> List[Any]:
    response: requests.Response = requests.post(
        url=f"{URL}/user/login/",
        json={"pseudo": username, "password": password},
    )
    data: Dict[str, Any] = response.json()
    if login_click > 0 or passwordSubmit > 0:
        if response.status_code == 202 and data["connected"]:
            return [True] * 3 + [
                0,
                False,
                0,
                username,
                "form-control is-valid",
                password,
                "form-control is-valid",
                0,
                True,
            ]
        else:
            return [False] * 3 + [0, True, 0, "", "form-control is-invalid", "", "form-control is-invalid", 0, False]

    return [False] * 3 + [0, True, 0, "", "form-control", "", "form-control", 0, False]


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
            url=f"{URL}/user/",
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
                        # dbc.Col(dcc.Graph(id="progession-graph"), md=8),
                        html.Div(id="useless"),
                    ],
                    align="center",
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
    # TODO: add args
    if ctx.triggered_id == "startingButton":
        script_path = settings.PACKAGE_DIR / "game.py"
        call(["python3", script_path, "-t", str(time), "-d", difficulty, "-hc", str(hand_constraint)])

    return ""


if __name__ == "__main__":
    app.run_server(debug=True)  # pragma: nocover
