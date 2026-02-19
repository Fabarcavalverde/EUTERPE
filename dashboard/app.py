import dash
from dash import html
import dash_bootstrap_components as dbc
import plotly.io as pio



app = dash.Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.CYBORG],
)
pio.templates.default = "plotly_dark"
navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(" ", className="fw-bold fs-4"),
            dbc.Nav(
                [
                    dbc.NavLink("Pronombres", href="/top-pronouns", active="exact"),
                    dbc.NavLink("Top Verbos", href="/top-verbs", active="exact"),
                    dbc.NavLink("Temporal", href="/temporal", active="exact"),
                    dbc.NavLink("Promedios", href="/song-stats", active="exact"),
                ],
                pills=True,
                className="ms-auto",
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky="top",
)

app.layout = dbc.Container(
    [
        navbar,
        html.Br(),

        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H2("EUTERPE", className="fw-bold mb-1"),
                            html.Div(
                                "Análisis de estructuras gramaticales en letras musicales por décadas.",
                                className="text-muted",
                            ),
                        ]
                    ),
                    className="shadow-lg border-0",
                ),
                md=12,
            )
        ),

        html.Br(),

        dash.page_container,

        html.Br(),
        html.Hr(),
        html.Div("© 2026 ·Colegio Universitario de Cartago · Big Data  ", className="text-muted small text-center"),
        html.Br(),
    ],
    fluid=True,
)

if __name__ == "__main__":
    app.run(debug=True)

