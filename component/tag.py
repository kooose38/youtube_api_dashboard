import dash 
import dash_core_components as dcc 
import dash_html_components as html

def create_tag(title: str, stats: int, app: object, img_name: str=""):
    return html.Div([
                html.Span([title, html.Br()]),
                html.Br(),
                html.Img(
                    title=title,
                    src=app.get_asset_url(f"../img/{img_name}.png"),
                    id="",
                    style={
                        "height": "80px",
                        "width": "80px",
                        "margin-bottom": "0px"
                    },
                ),
                html.Br(),
                html.Span(
                    str(int(stats)) + "回", 
                    style={'font-size': '30px','font-weight': 'bold'}
                ),
            ], style={
                'background-color': '#ffffff',
                'text-align': 'center',
                'border-radius': '5px',
                'width': '200px',
                'margin':'10px 10px 0px 10px',
                'padding': '15px',
                'position': 'relative',
                'box-shadow': 
                '4px 4px 4px lightgrey'}
            )