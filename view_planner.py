import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import socket
from datetime import datetime as dt
from dash.dependencies import Input, Output, State
from assets.styling import *
from config import *


def new_num(id, min, max, val):
    return html.Div(children=[
        dcc.Input(
            id=id,
            type='number',
            min=min,
            max=max,
            value=val,
            style=style_num
        )]
    )


def new_drop(id, vals, placeholder):
    return html.Div([
        dcc.Dropdown(
            id=id,
            options=[{'label': val, 'value': val} for val in vals],
            style=style_drop,
            clearable=False,
            searchable=False,
            placeholder=placeholder
        ),
    ], style={'width': '250%'})


def get_header():
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Col(children=[
                    dbc.Label('CYCLE LENGTH (IN MONTHS)')
                ], style=style_firstcol),
                dbc.Col(children=[
                    new_num('cyc_len', 1, 100, 1)
                ], style=style_box_col)
            ], style=style_col),
            dbc.Col(children=[
                dbc.Col(children=[
                    dbc.Label('START MONTH')
                ], style=style_thirdcol),
                dbc.Col(children=[
                    dbc.Row(children=[
                        new_drop('start_mon', MONTHS, 'Months')
                    ], style={'margin-bottom': '0%'})
                ], style=style_drop_col)
            ], style=style_col)
        ], style=style_header_row),
        dbc.Row(
            children=[
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('CURRENT BANK BALANCE')
                    ], style=style_firstcol),
                    dbc.Col(children=[
                        new_num('cur_bal', 0, 100000000000, 0)
                    ], style=style_box_col)
                ], style=style_col),
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('DESIRED MINIMUM BALANCE')
                    ], style=style_thirdcol),
                    dbc.Col(children=[
                        new_num('des_bal', 0, 10000000000, 0)
                    ], style=style_box_col)
                ], style=style_col),
            ], style=style_header_row)
    ], style=style_header)


def new_entry():
    return html.Div(id='base_entry', children=[
        dbc.Row(children=[
            dbc.Col(children=[
                new_drop('type_entry', ['Inflow', 'Outflow'], 'Type of Entry')
            ], style=style_entrycol_1),
            dbc.Col(children=[
                new_drop('freq', ['Recurring', 'Adhoc'], 'Frequency')
            ], style=style_entrycol),
            dbc.Col(children=[
                html.Div(id='entry_data')
            ], style=style_entrycol2)],
            style=style_header_row)
    ])


def get_entries():
    return html.Div(children=[
        new_entry(),
        dbc.Row(children=[
            html.Button('+', id='new_row', n_clicks=0, style={'font-size': '25px', 'background-color':dark_blue, 'color':white})
        ], style=style_newrow)
    ], style={'border': black_border_thick})


def get_fd_planner():
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Label('FIXED DEPOSITS')
        ], style=style_sub_heading),
        get_header(),
        get_entries()
    ])


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dbc.Row(children=[
        dbc.Label('SAVINGS PLANNER')
    ], style=style_heading),
    dbc.Row(children=[
        html.Div(children=[
            get_fd_planner()
        ], style=style_fdInputs)
    ])
])


@app.callback(Output('base_entry', 'children'), [Input('new_row', 'n_clicks')], [State('base_entry', 'children')])
def add_new_row(n_clicks, old_output):
    if n_clicks == 0:
        return old_output
    return old_output + [new_entry()]


@app.callback(Output('entry_data', 'children'), [Input('freq', 'value')])
def entry_updater(freq):
    if freq == 'Recurring':
        return html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Commencement'),
                            style={'width': '100%'}),
                    dbc.Col(new_drop('start_mon_entry1', MONTHS, 'Months'),
                            style={'margin-left': '5%'}),
                    dbc.Col(new_num('start_year_entry1', 2020, 3020, 2020),
                            style={'margin-left': '5%'})
                ], style=style_col_1),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Duration')),
                    dbc.Col(new_num('time_dur_entry1',1, 1000000000, 12),
                            style={'margin-left': '5%'}),
                ], style=style_col_2),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Value')),
                    dbc.Col(new_num('value_entry1', 0, 10000000000, 0),
                            style={'margin-left': '5%'})
                ], style=style_col_3),
            ], style=style_row)])
    elif freq == 'Adhoc':
        return html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Col(dbc.Label('OnDate'),
                            style={'width': '100%'}),
                    dbc.Col(new_drop('start_mon_entry1', MONTHS, 'Months'),
                            style={'margin-left': '5%'}),
                    dbc.Col(new_num('start_year_entry1', 2020, 3020, 2020),
                            style={'margin-left': '5%'})
                ], style=adh_style_col_1),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Value')),
                    dbc.Col(new_num('value_entry1', 0, 10000000000, 0),
                            style={'margin-left': '5%'})
                ], style=adh_style_col_2),
            ], style=style_row)])


if __name__ == '__main__':
    print('Code execution has started')
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.server.run(port=8050, host=ip_address)
