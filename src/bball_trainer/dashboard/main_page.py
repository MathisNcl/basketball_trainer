import dash_bootstrap_components as dbc
from dash import dcc, html

layout = dbc.Row(
    [
        dbc.Col(
            html.A(
                dbc.CardImg(
                    src="/assets/coach.png",
                    top=True,
                    style={"maxWidth": "100px"},
                ),
                href="/",
            ),
            width=1,
        ),
        dbc.Col(
            dbc.Container(
                id="loginTypeUser",
                children=[
                    dcc.Input(
                        value="",
                        placeholder="Identifiant",
                        type="text",
                        id="usernameBox",
                        className="form-control",
                        debounce=True,
                        n_submit=0,
                    ),
                ],
            ),
            width=4,
        ),
        dbc.Col(
            dbc.Container(
                id="loginTypePassword",
                children=[
                    dcc.Input(
                        value="",
                        placeholder="Mot de passe",
                        type="password",
                        id="passwordBox",
                        className="form-control",
                        debounce=True,
                        n_submit=0,
                    ),
                ],
            ),
            width=4,
        ),
        dbc.Col(
            html.Button(
                children="Login",
                n_clicks=0,
                type="submit",
                id="loginButton",
                className="btn btn-lg",
                style={"color": "white", "backgroundColor": "#134074"},
            ),
            width=1,
        ),
        dbc.Col(
            html.Button(
                children="Logout",
                n_clicks=0,
                type="submit",
                id="logoutButton",
                className="btn btn-lg",
                style={"color": "white", "backgroundColor": "#731212"},
                hidden=True,
            ),
            width=1,
        ),
    ],
    className="form-group",
)
