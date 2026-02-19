import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from dashboard.utils_pos import load_df, explode_tokens

dash.register_page(__name__, path="/top-verbs", name="Top Verbos")

layout = dbc.Container(
    [
        html.H3("Top 10 verbos por década"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(id="verbs_decade_dd", placeholder="Selecciona década"),
                    md=12,
                ),
            ],
            align="center",
        ),
        html.Br(),
        dcc.Graph(id="verbs_bar"),
    ],
    fluid=True,
)

@dash.callback(
    Output("verbs_decade_dd", "options"),
    Output("verbs_decade_dd", "value"),
    Input("verbs_bar", "id"),
)
def init_controls(_):
    df = load_df()
    decades = sorted(((df["year"] // 10) * 10).unique().tolist())
    options = [{"label": f"{int(d)}s", "value": int(d)} for d in decades]
    default = int(decades[0]) if decades else None
    return options, default

@dash.callback(
    Output("verbs_bar", "figure"),
    Input("verbs_decade_dd", "value"),
)
def update_verbs(decade):
    df = load_df()
    df["decade"] = (df["year"] // 10) * 10

    if decade is not None:
        df = df[df["decade"] == decade]

    tok = explode_tokens(df)

    # solo VERB
    v = tok[tok["pos"] == "VERB"].copy()
    v["token"] = v["token"].astype(str).str.lower()

    top_df = v["token"].value_counts().head(10).reset_index()
    top_df.columns = ["verb", "count"]

    title = f"Top 10 verbos en {int(decade)}s"

    fig = px.bar(
        top_df,
        x="verb",
        y="count",
        title=title,
    )
    fig.update_layout(
        xaxis_title="Verbo",
        yaxis_title="Frecuencia",
        xaxis_tickangle=-45,
    )

    return fig
