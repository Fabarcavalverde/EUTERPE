import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px


from dashboard.utils_pos import load_df, explode_tokens

dash.register_page(__name__, path="/top-pronouns", name="Pronombres")

# sets simples (puedes expandir si quieres)
FIRST_PERSON = {"i", "me", "my", "mine", "we", "us", "our", "ours"}
SECOND_PERSON = {"you", "your", "yours", "u"}
THIRD_PERSON = {"he", "him", "his", "she", "her", "hers", "they", "them", "their", "theirs", "it", "its"}

layout = dbc.Container(
    [
        html.H3("Top pronombres por década"),
dbc.Row(
    [
        dbc.Col(dcc.Dropdown(id="decade_dd_p", placeholder="Selecciona década"), md=6),
        dbc.Col(
            dcc.Dropdown(
                id="person_filter",
                options=[
                    {"label": "Todos", "value": "all"},
                    {"label": "1ra persona", "value": "first"},
                    {"label": "2da persona", "value": "second"},
                    {"label": "3ra persona", "value": "third"},
                ],
                value="all",
                clearable=False,
            ),
            md=6,
        ),
    ],
    align="center",
),

        html.Br(),
        dcc.Graph(id="pron_bar"),
    ],
    fluid=True,
)

@dash.callback(
    Output("decade_dd_p", "options"),
    Output("decade_dd_p", "value"),
    Input("pron_bar", "id"),
)
def init_controls(_):
    df = load_df()
    decades = sorted(((df["year"] // 10) * 10).unique().tolist())
    opts = [{"label": f"{int(d)}s", "value": int(d)} for d in decades]
    default = int(decades[0]) if decades else None
    return opts, default
@dash.callback(
    Output("pron_bar", "figure"),
    Input("decade_dd_p", "value"),
    Input("person_filter", "value"),
)
def update_pronouns(decade, person):
    df = load_df()
    df["decade"] = (df["year"] // 10) * 10
    if decade is not None:
        df = df[df["decade"] == decade]

    tok = explode_tokens(df)

    p = tok[tok["pos"] == "PRON"].copy()
    p["token"] = p["token"].astype(str).str.lower()

    if person == "first":
        p = p[p["token"].isin(FIRST_PERSON)]
    elif person == "second":
        p = p[p["token"].isin(SECOND_PERSON)]
    elif person == "third":
        p = p[p["token"].isin(THIRD_PERSON)]

    top_df = p["token"].value_counts().head(10).reset_index()
    top_df.columns = ["pronoun", "count"]

    title = f"Top 10 pronombres en {int(decade)}s"
    if person != "all":
        title += f" ({person})"

    fig = px.bar(top_df, x="pronoun", y="count", title=title)
    fig.update_layout(xaxis_title="Pronombre", yaxis_title="Frecuencia", xaxis_tickangle=-45)
    return fig
