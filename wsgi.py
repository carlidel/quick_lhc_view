# import plotly and dash
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import ALL, MATCH, Input, Output, State
from PIL import Image

from figure_gatherer import path_gatherer

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
application = app.server

###############################################################################

LHC_LIST = [
    {"label": "Beam 1, worst seed", "value": "0"},
    {"label": "Beam 1, average seed", "value": "1"},
    {"label": "Beam 1, best seed", "value": "2"},
    {"label": "Beam 2, worst seed", "value": "3"},
    {"label": "Beam 2, average seed", "value": "4"},
    {"label": "Beam 2, best seed", "value": "5"},
]

ZETA_LIST = [
    {"label": "center", "value": "0"},
    {"label": "halfway", "value": "1"},
    {"label": "border", "value": "2"},
]

KERNEL_LIST = [
    {"label": "No conv", "value": "none"},
    {"label": "3", "value": "3"},
    {"label": "5", "value": "5"},
]

DYNAMIC_LIST = [
    {"label": "Ground Truth", "value": "ground_truth"},
    {"label": "Fast Lyapunov Indicator", "value": "fli"},
    {"label": "Ortho Lyapunov avg", "value": "ofli_avg"},
    {"label": "Ortho Lyapunov max", "value": "ofli_max"},
    {"label": "Reversibility Error", "value": "rem"},
    {"label": "SALI", "value": "sali"},
    {"label": "GALI", "value": "gali"},
    {"label": "Tune", "value": "tune"},
]

PLOT_KIND_LIST = [
    {"label": "Colormap", "value": "colormap"},
    {"label": "Performance", "value": "performance"},
    {"label": "Convolution Performance", "value": "convolution_performance"},
    {"label": "All A Posteriori performances", "value": "a_posteriori_comparison"},
    {"label": "All A Priori performances", "value": "a_priori_comparison"},
    {"label": "Histogram", "value": "histogram"},
]

ZOOM_LIST = [
    {"label": "[0.00 - 1.0]", "value": "0.0"},
    {"label": "[0.25 - 1.0]", "value": "0.25"},
    {"label": "[0.50 - 1.0]", "value": "0.5"},
    {"label": "[0.75 - 1.0]", "value": "0.75"},
    {"label": "[0.90 - 1.0]", "value": "0.9"},
    {"label": "[0.95 - 1.0]", "value": "0.95"},
    {"label": "[0.99 - 1.0]", "value": "0.99"},
]

# picker_1 = [
#     dcc.Dropdown(
#         id={"type": "picker_1", "index": i},
#         options=OMEGA_LIST,
#         value=OMEGA_LIST[0]["value"],
#         clearable=False,
#         multi=False,
#     )
#     for i in range(6)
# ]

picker_2 = [
    dcc.Dropdown(
        id={"type": "picker_2", "index": i},
        options=LHC_LIST,
        value=LHC_LIST[0]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

picker_3 = [
    dcc.Dropdown(
        id={"type": "picker_3", "index": i},
        options=ZETA_LIST,
        value=ZETA_LIST[0]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

picker_4 = [
    dcc.Dropdown(
        id={"type": "picker_4", "index": i},
        options=KERNEL_LIST,
        value=KERNEL_LIST[0]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

picker_5 = [
    dcc.Dropdown(
        id={"type": "picker_5", "index": i},
        options=DYNAMIC_LIST,
        value=DYNAMIC_LIST[0]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

picker_6 = [
    dcc.Dropdown(
        id={"type": "picker_6", "index": i},
        options=PLOT_KIND_LIST,
        value=PLOT_KIND_LIST[0]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

picker_7 = [
    dcc.Dropdown(
        id={"type": "picker_7", "index": i},
        options=ZOOM_LIST,
        value=ZOOM_LIST[3]["value"],
        clearable=False,
        multi=False,
    )
    for i in range(6)
]

figures = [
    dcc.Loading(
        id=f"loading-{i}",
        type="default",
        children=dcc.Graph(
            id={"type": "figure", "index": i}, figure={"data": [], "layout": {}}
        ),
    )
    for i in range(6)
]

blocks = [
    dbc.Col(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            # dbc.FormGroup([
                            # dbc.Label("Omega Picker"),
                            # picker_1[i],
                            dbc.Label("LHC Picker"),
                            picker_2[i],
                            dbc.Label("Zeta Picker"),
                            picker_3[i],
                            dbc.Label("Kernel Picker"),
                            picker_4[i],
                            dbc.Label("Dynamic Picker"),
                            picker_5[i],
                            dbc.Label("Plot Kind Picker"),
                            picker_6[i],
                            dbc.Label("Zoom level Picker\n(for performance plots)"),
                            picker_7[i],
                            # ]),
                        ],
                        width=2,
                    ),
                    dbc.Col([figures[i]]),
                ]
            )
        ]
    )
    for i in range(6)
]

app.layout = html.Div(
    [
        dbc.Col(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Zoom scale:"),
                                dcc.Slider(
                                    min=0.05,
                                    max=2.0,
                                    step=0.05,
                                    value=0.5,
                                    id="Scale",
                                    tooltip={
                                        "placement": "bottom",
                                        "always_visible": True,
                                    },
                                ),
                            ]
                        )
                    ]
                ),
                dbc.Row([blocks[0], blocks[1],]),
                dbc.Row([blocks[2], blocks[3],]),
                dbc.Row([blocks[4], blocks[5],]),
            ]
        ),
    ]
)

###############################################################################


@app.callback(
    Output({"type": "figure", "index": MATCH}, "figure"),
    [
        # Input({"type": "picker_1", "index": MATCH}, "value"),
        Input({"type": "picker_2", "index": MATCH}, "value"),
        Input({"type": "picker_3", "index": MATCH}, "value"),
        Input({"type": "picker_4", "index": MATCH}, "value"),
        Input({"type": "picker_5", "index": MATCH}, "value"),
        Input({"type": "picker_6", "index": MATCH}, "value"),
        Input("Scale", "value"),
        Input({"type": "picker_7", "index": MATCH}, "value"),
    ],
)
def update_fig(*args):
    lhc = args[0]
    zeta = args[1]
    kernel = args[2]
    dynamic = args[3]
    plot_kind = args[4]

    fig = go.Figure()

    try:
        figpath = path_gatherer(
            lhc=lhc,
            zeta=zeta,
            dynamic_indicator=dynamic,
            plot_kind=plot_kind,
            zoom=args[7],
            kernel=kernel,
        )
    except Exception:
        return fig

    # open the jpeg at figpath and get the size in pixel
    img = Image.open(figpath)
    img_width, img_height = img.size
    scale_factor = args[6]

    img_width = 1920
    img_height = 1080

    # Add invisible scatter trace.
    # This trace is added to help the autoresize logic work.
    fig.add_trace(
        go.Scatter(
            x=[0, img_width * scale_factor],
            y=[0, img_height * scale_factor],
            mode="markers",
            marker_opacity=0,
        )
    )

    # Configure axes
    fig.update_xaxes(visible=False, range=[0, img_width * scale_factor])

    fig.update_yaxes(
        visible=False,
        range=[0, img_height * scale_factor],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x",
    )

    # Add image
    fig.add_layout_image(
        dict(
            x=0,
            sizex=img_width * scale_factor,
            y=img_height * scale_factor,
            sizey=img_height * scale_factor,
            xref="x",
            yref="y",
            opacity=1.0,
            layer="below",
            sizing="contain",
            source=img,
        )
    )

    # Configure other layout
    fig.update_layout(
        width=img_width * scale_factor,
        height=img_height * scale_factor,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

    return fig


###############################################################################

if __name__ == "__main__":
    print("Test")
    app.run_server(host="0.0.0.0", port=8080, debug=True)
