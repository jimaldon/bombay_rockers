from flask import Flask, jsonify, request
import dash
import logging
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go


logger = logging.getLogger(__name__)
server = Flask(__name__)

@server.route('/br', methods=['POST'])
def index():
    logger.info('covfefe')
    return jsonify(request.json)

@server.route('/br', methods=['GET'])
def get_index():
    logger.info('got requested')
    return 'covfefe'

app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/'
)


fig = go.Figure(go.Scattermapbox(
        lat=(45.5305185,),
        lon=(-73.6132051,),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=14
        ),
    ))
fig.update_layout(
        hovermode='closest',
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoiamZ0YWlsbG9uIiwiYSI6ImNqeTBqNjhjYTAzcG0zb214cGE1bjB0djYifQ._sUkIemdyART3dhuOiDTow',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=45.5305185,
                lon=-73.6132051,
            ),
            pitch=0,
            zoom=20
        )
    )

app.layout = html.Div([
        dcc.Graph(
            id='map',
            figure=fig
        )
    ]
)


def main():
    app.run_server()
    fig.show()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
