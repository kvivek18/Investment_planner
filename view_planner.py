import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import socket
import dash_table
from dash.dependencies import Input, Output, State, MATCH, ALL
from assets.styling import *
from config import *
import pandas as pd

from fd_calculator import fdCalculator


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


def create_table(table):
    return dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in table.columns],
        data=table.to_dict('records'),
        style_cell={'textAlign': 'center', 'border': black_border_thin, 'font-size': '14px', 'backgroundColor': white,
                    'whiteSpace': 'normal', 'height': 'auto', 'min-width': '185px'},
        style_header={'textAlign': 'center', 'backgroundColor': light_blue, 'fontWeight': 'bold', 'font-size': '15px'},
        style_header_conditional=[{}]
    )


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
                    dbc.Col(children=[
                        dbc.Label('START MONTH')
                    ], style=style_third1col),
                    dbc.Col(children=[
                        dbc.Row(children=[
                            new_drop('start_mon', MONTHS, 'Months')
                        ], style={'margin-bottom': '0%'})
                    ], style=style_drop_col)
                ], style=style_col),
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('START YEAR')
                    ], style=style_thirdcol),
                    dbc.Col(children=[
                        dbc.Row(children=[
                            new_num('start_year', 2020, 3020, 2020)
                        ], style={'margin-bottom': '0%'})
                    ], style=style_drop_col)
                ], style=style_col),
            ], style=style_col)
        ], style=style_header_row),
        dbc.Row(
            children=[
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('CURRENT BANK BALANCE (IN ₹)')
                    ], style=style_firstcol),
                    dbc.Col(children=[
                        new_num('cur_bal', 0, 100000000000, 0)
                    ], style=style_box_col)
                ], style=style_col),
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('DESIRED MINIMUM BALANCE (IN ₹)')
                    ], style=style_thirdcol),
                    dbc.Col(children=[
                        new_num('des_bal', 0, 10000000000, 0)
                    ], style=style_box_col)
                ], style=style_col),
            ], style=style_header_row)
    ], style=style_header)


def new_entry(n_clicks):
    return html.Div(id='row_' + str(n_clicks), children=[
        dbc.Row(children=[
            dbc.Col(children=[
                new_drop({'type': 'entry_type', 'index': n_clicks}, ['Inflow', 'Outflow'], 'Type of Entry')
            ], style=style_entrycol_1),
            dbc.Col(children=[
                new_drop({'type': 'entry_freq', 'index': n_clicks}, ['Recurring', 'Adhoc'], 'Frequency')
            ], style=style_entrycol),
            dbc.Col(children=[
                html.Div(id={'type': 'entry_data', 'index': n_clicks})
            ], style=style_entrycol2)],
            style=style_row)
    ])


def get_entries():
    return html.Div(children=[
        html.Div(children=[
            dbc.Row(dbc.Label('INPUT TABLE'),
                    style={'padding-left': '43.5%', 'background-color': dark_blue, 'color': white,
                           'border-bottom': black_border_thin, 'border-left': black_border_thick,
                           'border-top': black_border_thick, 'border-right': black_border_thick, 'fontWeight': 'bold',
                           'font-size': '125%',
                           'font-family': cambria, }),
            html.Div(id='input_table', children=[])
        ]),
        html.Div(children=[
            dbc.Row(dbc.Label('TABLE ENTRIES'),
                    style={'padding-left': '43.5%', 'background-color': dark_blue, 'color': white,
                           'border-bottom': black_border_thick, 'fontWeight': 'bold',
                           'font-size': '125%',
                           'font-family': cambria, }),
            html.Div(id='input_row', children=[new_entry(0)]),
            dbc.Row(children=[
                html.Button('+', id='new_row', n_clicks=0,
                            style={'font-size': '22px', 'background-color': dark_blue, 'color': white})
            ], style=style_newrow),
            dbc.Row(children=[
                html.Button('SUBMIT', id='submit', n_clicks=0,
                            style={'font-size': '18px', 'background-color': dark_blue, 'color': white,
                                   'fontWeight': 'bold',
                                   'font-family': cambria
                                   })
            ], style=style_submit)
        ], style={'border': black_border_thick, 'margin-top': '1%'})
    ], style={'margin-top': '1%'})


def get_fd_planner():
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Label('GLOBAL INPUTS')
        ], style=style_sub_heading),
        get_header(),
        get_entries(),
        html.Div(children=[dbc.Row(dbc.Label('AGGREGATED TABLE'),
                                   style={'padding-left': '42%', 'background-color': dark_blue, 'color': white,
                                          'border': black_border_thick, 'fontWeight': 'bold', 'font-size': '125%',
                                          'font-family': cambria}),
                           dbc.Row(id='report_table', children=[])
                           ], style={'margin-top': '1%'})
    ])


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dbc.Row(children=[
        dbc.Col(dbc.Label('FIXED DEPOSITS PLANNER'), style=style_heading),
        dbc.Col(html.Button('RESET', id='reset', n_clicks=0,
                            style={'font-size': '18px', 'background-color': dark_blue, 'color': white,
                                   'fontWeight': 'bold',
                                   'font-family': cambria}),
                style={'margin-left': '30%'})

    ], style=style_top_row),
    dbc.Row(children=[
        html.Div(children=[
            get_fd_planner()
        ], style=style_fdInputs)
    ]),
    dash_table.DataTable(id='temp_table'),
    dbc.Row(id='lol', children=[])

])

#
# @app.callback(Output('temp_table', 'data'), [Input('reset', 'n_clicks')])
# def reset_it(n_clicks):
#     print('1')
#     return pd.DataFrame([[None, None, None, None, None, None]], columns=COLUMNS).to_dict('rows')

#
# @app.callback(Output('lol', 'children'), [Input('temp_table', 'data')])
# def check(temp_table):
#     print(temp_table)
#     print(pd.DataFrame(temp_table, columns=COLUMNS))
#     return None


@app.callback([Output('input_table', 'children'), Output('input_row', 'children'), Output('temp_table', 'data')],
              [Input('new_row', 'n_clicks')],
              [State({'type': 'entry_type', 'index': ALL}, 'value'),State({'type': 'entry_freq', 'index': ALL}, 'value'),
               State({'type': 'start_mon_entry', 'index': ALL}, 'value'),State({'type': 'start_year_entry', 'index': ALL}, 'value'),
               State({'type': 'time_dur_entry', 'index': ALL}, 'value'),State({'type': 'value_entry', 'index': ALL}, 'value'),
               State('temp_table','data')])
def input_table_updater(n_clicks, type, freq, start_mon, start_year, time_dur, val, temp_table):
    if n_clicks == 0:
        curr_df = pd.DataFrame([[None, None, None, None, None, None]], columns=COLUMNS)
        return [create_table(curr_df), new_entry(n_clicks),curr_df.to_dict('rows')]
    curr_time = None if len(time_dur) == 0 else int(time_dur[0])
    if n_clicks == 1:
        curr_df = pd.DataFrame([[type[0], freq[0], start_mon[0], start_year[0], curr_time, val[0]]], columns=COLUMNS)
        return [create_table(curr_df), new_entry(n_clicks), curr_df.to_dict('rows')]
    temp_df = pd.DataFrame([[type[0], freq[0], start_mon[0], start_year[0], curr_time, val[0]]], columns=COLUMNS)
    prev_df = pd.DataFrame(temp_table, columns=COLUMNS)
    curr_df = pd.concat([prev_df, temp_df]).reset_index(drop=True)
    return [create_table(curr_df), new_entry(n_clicks), curr_df.to_dict('rows')]


@app.callback(Output('report_table', 'children'), [Input('submit', 'n_clicks')],
              [State('start_mon', 'value'), State('start_year', 'value'), State('cur_bal', 'value'),
               State('des_bal', 'value'), State('temp_table', 'data')])
def report_table_generator(n_clicks, glob_start_mon, glob_start_year, cur_bal, des_bal, temp_table):
    if n_clicks == 0:
        return create_table(pd.DataFrame([[None, None, None, None]], columns=REPORT_COLUMNS))
    pres_df = pd.DataFrame(temp_table, columns=COLUMNS)
    print(pres_df)
    cols = pres_df.columns
    df_res = fdCalculator.aggTable_generator(glob_start_mon, glob_start_year, cur_bal, des_bal,
                                             pres_df[cols[0]].tolist(),
                                             pres_df[cols[1]].tolist(), pres_df[cols[2]].tolist(),
                                             pres_df[cols[3]].tolist(), pres_df[cols[4]].tolist(),
                                             pres_df[cols[5]].tolist())
    return create_table(df_res)


@app.callback(Output({'type': 'entry_data', 'index': MATCH}, 'children'),
              [Input({'type': 'entry_freq', 'index': MATCH}, 'value')],
              [State({'type': 'entry_freq', 'index': MATCH}, 'id')])
def entry_updater(freq, val):
    curr_index = val['index']
    if freq == 'Recurring':
        return (html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Commencement'),
                            style={'width': '100%'}),
                    dbc.Col(new_drop({'type': 'start_mon_entry', 'index': curr_index}, MONTHS, 'Months'),
                            style={'margin-left': '5%'}),
                    dbc.Col(new_num({'type': 'start_year_entry', 'index': curr_index}, 2020, 3020, 2020),
                            style={'margin-left': '5%'})
                ], style=style_col_1),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Duration')),
                    dbc.Col(new_num({'type': 'time_dur_entry', 'index': curr_index}, 1, 1000000000, 12),
                            style={'margin-left': '5%'}),
                ], style=style_col_2),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Value')),
                    dbc.Col(new_num({'type': 'value_entry', 'index': curr_index}, 0, 10000000000, 0),
                            style={'margin-left': '5%'})
                ], style=style_col_3),
            ], style=style_spl_row)]))
    elif freq == 'Adhoc':
        return (html.Div(children=[
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Col(dbc.Label('OnDate'),
                            style={'width': '100%'}),
                    dbc.Col(new_drop({'type': 'start_mon_entry', 'index': curr_index}, MONTHS, 'Months'),
                            style={'margin-left': '5%'}),
                    dbc.Col(new_num({'type': 'start_year_entry', 'index': curr_index}, 2020, 3020, 2020),
                            style={'margin-left': '5%'})
                ], style=adh_style_col_1),
                dbc.Col(children=[
                    dbc.Col(dbc.Label('Value')),
                    dbc.Col(new_num({'type': 'value_entry', 'index': curr_index}, 0, 10000000000, 0),
                            style={'margin-left': '5%'})
                ], style=adh_style_col_2),
            ], style=style_spl_row)]))
    else:
        return None


if __name__ == '__main__':
    print('Code execution has started')
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.server.run(port=8050, host=ip_address)
