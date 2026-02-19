import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from dashboard.utils_pos import load_df, explode_tokens


dash.register_page(__name__, path="/", name="Distribución POS")

layout = dbc.Container(
    [
        html.H3("Distribución de POS (spaCy)"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(id="home_decade_dd", placeholder="Selecciona década"),
                    md=12,
                ),
            ],
            align="center",
        ),
        html.Br(),
        dcc.Graph(id="pos_bar"),
    ],
    fluid=True,
)

@dash.callback(
    Output("home_decade_dd", "options"),
    Output("home_decade_dd", "value"),
    Input("pos_bar", "id"),
)
def init_controls(_):
    from dashboard.utils_pos import add_decade
    df = add_decade(load_df())
    decades = sorted(df["decade"].unique().tolist())
    options = [{"label": f"{int(d)}s", "value": int(d)} for d in decades]
    return options, int(decades[0])


@dash.callback(
    Output("pos_bar", "figure"),
    Input("home_decade_dd", "value"),
)
def update_pos_bar(decade):
    from dashboard.utils_pos import add_decade
    df = add_decade(load_df())
    df = df[df["decade"] == decade]

    tok = explode_tokens(df)

    counts = tok["pos"].value_counts().reset_index()
    counts.columns = ["pos", "count"]
    counts["pct"] = counts["count"] / counts["count"].sum()

    fig = px.bar(counts, x="pos", y="pct",
                 title=f"Distribución POS en {decade}s")
    return fig

