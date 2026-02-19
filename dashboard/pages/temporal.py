import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

from dashboard.utils_pos import load_df, explode_tokens

dash.register_page(__name__, path="/temporal", name="Temporal")

layout = dbc.Container(
    [
        html.H3("Proporción de POS por década"),
        dbc.Row(
            [
                dbc.Col(dcc.Dropdown(id="temp_pos_multi", placeholder="POS tags", multi=True), md=12),
            ]
        ),
        html.Br(),
        dcc.Graph(id="temp_pos_ts"),
    ],
    fluid=True,
)

@dash.callback(
    Output("temp_pos_multi", "options"),
    Output("temp_pos_multi", "value"),
    Input("temp_pos_ts", "id"),
)
def init_controls(_):
    df = load_df()
    sample = df.sample(min(len(df), 2000), random_state=7)
    tok = explode_tokens(sample)
    pos_tags = sorted(tok["pos"].unique().tolist())
    default = [p for p in ["NOUN", "VERB", "ADJ", "PRON"] if p in pos_tags] or pos_tags[:4]
    return (
        [{"label": p, "value": p} for p in pos_tags],
        default,
    )

@dash.callback(
    Output("temp_pos_ts", "figure"),
    Input("temp_pos_multi", "value"),
)
def update_ts(pos_list):
    df = load_df()
    tok = explode_tokens(df)

    # crear decade en token-level
    tok["decade"] = (tok["year"] // 10) * 10

    if pos_list:
        tok = tok[tok["pos"].isin(pos_list)]

    g = tok.groupby(["decade", "pos"]).size().reset_index(name="count")
    totals = g.groupby("decade")["count"].transform("sum")
    g["pct"] = g["count"] / totals

    fig = px.line(
        g.sort_values("decade"),
        x="decade",
        y="pct",
        color="pos",
        markers=True,
        title="Proporción de POS por década",
    )
    fig.update_layout(xaxis_title="Década", yaxis_title="Proporción")
    fig.update_xaxes(type="category")
    return fig
