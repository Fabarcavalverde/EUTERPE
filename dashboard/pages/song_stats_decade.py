import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

from dashboard.utils_pos import load_df, add_decade
import numpy as np

dash.register_page(__name__, path="/song-stats", name="Promedios por canción")

def compute_song_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula métricas por canción usando pos_spacy (np.ndarray de np.ndarray).
    Retorna: year, decade, tokens_count, unique_words, unique_pos, ttr
    """
    rows = []
    for year, seq in df[["year", "pos_spacy"]].itertuples(index=False):
        if not isinstance(seq, np.ndarray) or len(seq) == 0:
            continue

        tokens = []
        pos_tags = []

        for it in seq:
            if isinstance(it, np.ndarray) and it.size >= 2:
                tok = it[0]
                pos = it[1]
                if tok is not None:
                    tokens.append(str(tok).lower())
                if pos is not None:
                    pos_tags.append(str(pos))

        if len(tokens) == 0:
            continue

        tokens_count = len(tokens)
        unique_words = len(set(tokens))
        unique_pos = len(set(pos_tags))
        ttr = unique_words / tokens_count

        rows.append((int(year), tokens_count, unique_words, unique_pos, ttr))

    out = pd.DataFrame(rows, columns=["year", "tokens_count", "unique_words", "unique_pos", "ttr"])
    out["decade"] = (out["year"] // 10) * 10
    return out

layout = dbc.Container(
    [
        html.H3("Promedios por canción por década"),
        html.P("Métricas: largo (tokens), riqueza léxica (unique words), variedad gramatical (unique POS), TTR."),
        dcc.Dropdown(
            id="metric_dd",
            options=[
                {"label": "Tokens promedio por canción", "value": "tokens_count"},
                {"label": "Palabras únicas promedio", "value": "unique_words"},
                {"label": "POS únicos promedio", "value": "unique_pos"},
                {"label": "TTR promedio (unique/tokens)", "value": "ttr"},
            ],
            value="tokens_count",
            clearable=False,
        ),
        html.Br(),
        dcc.Graph(id="metric_chart"),
    ],
    fluid=True,
)

@dash.callback(
    dash.Output("metric_chart", "figure"),
    dash.Input("metric_dd", "value"),
)
def update_metric(metric):
    df = load_df()
    df = add_decade(df)

    stats = compute_song_stats(df)

    agg = stats.groupby("decade")[metric].mean().reset_index()
    agg = agg.sort_values("decade")

    title_map = {
        "tokens_count": "Tokens promedio por canción por década",
        "unique_words": "Palabras únicas promedio por canción por década",
        "unique_pos": "POS únicos promedio por canción por década",
        "ttr": "TTR promedio por canción por década",
    }

    fig = px.line(agg, x="decade", y=metric, markers=True, title=title_map.get(metric, metric))
    fig.update_layout(xaxis_title="Década", yaxis_title="Promedio")
    fig.update_xaxes(type="category")
    return fig
