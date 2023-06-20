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
                href="https://github.com/MathisNcl/basketball_trainer",
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
                children="Sign In",
                n_clicks=0,
                type="submit",
                id="signInButton",
                className="btn btn-lg",
                style={"color": "black", "backgroundColor": "white", "borderColor": "black"},
            ),
            width=1,
        ),
        dbc.Col(
            html.Button(
                children="Login",
                n_clicks=0,
                type="submit",
                id="loginButton",
                className="btn btn-lg",
                style={"color": "white", "backgroundColor": "#0066ff"},
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
                style={"color": "white", "backgroundColor": "#6c757d"},
                hidden=True,
            ),
            width=1,
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Sign in"),
                dbc.ModalBody(
                    [
                        dbc.Label("Username:"),
                        dbc.Input(id="modal_username", type="text", required=True, minLength=5),
                        dbc.Label("Password:"),
                        dbc.Input(id="modal_password", type="password", required=True, minLength=5),
                        dbc.Label("Lastname:"),
                        dbc.Input(id="modal_lastname", type="text", debounce=True, required=True),
                        dbc.Label("Firstname:"),
                        dbc.Input(id="modal_firstname", type="text", debounce=True, required=True),
                        dbc.Label("Age:"),
                        dbc.Input(id="modal_age", type="number", required=False, min=13),
                        html.Br(),
                        dbc.Label(id="modal_error", style={"color": "red"}),
                    ]
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Submit", color="primary", id="modal_submit_button"),
                        dbc.Button("Cancel", id="modal_cancel_button"),
                    ]
                ),
            ],
            id="signInModal",
        ),
    ],
    className="form-group",
)
