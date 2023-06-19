from typing import Any, Dict, List

import dash_auth
import dash_bootstrap_components as dbc
import requests
from dash import Dash, html
from dash.dependencies import Input, Output, State
from flask import Flask

from bball_trainer.dashboard import main_page

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
            return [True] * 3 + [0, False, 0, username, "form-control", password, "form-control", 0]
        else:
            return [False, False, False, 0, True, 0, "", "form-control is-invalid", "", "form-control is-invalid", 0]

    return [False, False, False, 0, True, 0, "", "form-control", "", "form-control", 0]


if __name__ == "__main__":
    app.run_server(debug=True)
