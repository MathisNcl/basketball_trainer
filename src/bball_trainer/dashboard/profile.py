import dash_bootstrap_components as dbc
from dash import html

layout = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("User id"),
                                html.H6(id="profile_id"),
                                dbc.Label("Username"),
                                html.H6(id="profile_username"),
                                dbc.Label("Lastname"),
                                html.H6(id="profile_lastname"),
                            ],
                            style={"textAlign": "center", "fontWeight": "bold"},
                        ),
                    ],
                    width=6,
                ),
                dbc.Col(
                    [
                        html.Div(
                            [
                                dbc.Label("Firstname"),
                                html.H6(id="profile_firstname"),
                                dbc.Label("Age"),
                                html.H6(id="profile_age"),
                                dbc.Label("Creation date"),
                                html.H6(id="profile_date"),
                                # dbc.Label("Best score"),
                                # dbc.Label(id="profile_best_score"),
                            ],
                            style={"textAlign": "center", "fontWeight": "bold"},
                        )
                    ],
                    width=6,
                ),
            ]
        )
    ],
    body=True,
)
