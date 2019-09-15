import os
import json
from flask import Flask, jsonify, request
import dash
import logging
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import base64


logger = logging.getLogger(__name__)
server = Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


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
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets
)

pin_data = []

with open('pin_data.json') as f:
    pin_data = json.load(f)


fig = go.Figure(go.Scattermapbox(
        lon=[point['lon'] for point in pin_data],
        lat=[point['lat'] for point in pin_data],
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

logo_png = '../docs/logo.png'
logo_base64 = base64.b64encode(open(logo_png, 'rb').read()).decode('ascii')


app.layout = html.Div([
        html.Div([
            html.Img(src='data:image/png;base64,{}'.format(logo_base64),
                style={
                    'height' : '5%',
                    'width' : '5%',
                    'float' : 'middle',
                    'position' : 'relative',
                    'padding-top' : 0,
                    'padding-left' : 0},),
            dcc.Markdown('''# Plant Disease Monitoring''')]),
        dcc.Markdown('''---'''),
        html.Div(
            id='main',
            children=[
                dcc.Graph(
                    id='map',
                    style={'height': '500px'},
                    figure=fig
                ),
                html.Div(
                    id='pinInfo',
                    children=[
                        html.Div(
                            'Location',
                            id='location-label',
                            style={'fontSize': 14}),
                        html.Img(
                            id='body-image',
                            src=''
                        ),
                    ]
                )
            ])
    ],
    style={'textAlign': 'center'}
)
app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})



@app.callback(Output("body-image", "src"),
              [Input("map", "hoverData")])
def update_body_image(hover_data):
    if hover_data:
        point_index = hover_data['points'][0]['pointIndex']
        src = get_image(point_index)
    else:
        src = ''

    return src


def get_image(index: int):
    if index >= len(pin_data):
        index = 0
    return pin_data[index]['image_path']


@app.callback(
    Output(component_id='location-label', component_property='children'),
    [Input("map", "hoverData")]
)
def update_output_div(hover_data):
    if hover_data:
        point_index = hover_data['points'][0]['pointIndex']

        lon = pin_data[point_index]['lon']
        lat = pin_data[point_index]['lat']
        disease = pin_data[point_index]['disease_name']
        time = pin_data[point_index]['timestamp']
        location_text = f'({lon}, {lat}) | Disease: {disease} | Time: {time}'
    else:
        location_text = ''

    return location_text


def main():
    app.run_server(debug=True)
    fig.show()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
