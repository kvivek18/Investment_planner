import pandas
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import socket
from datetime import datetime as dt
from dash.dependencies import Input, Output
from assets.styling import *


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


def get_recurr_box(ids):
    divs = []
    count = 0
    for id_name in ids:
        count = count + 1
        divs.append(
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Label('Value of Entity ' + str(count)+' (in ₹)')
                ], style=style_col),
                dbc.Col(children=[
                    new_num(id_name, 0, None, 0)
                ], style=style_box_col)
            ], style=style_sub_sub_row)
        )
    return html.Div(children=divs)


def get_adhoc_box(ids):
    divs = []
    count = 0
    for id_name in ids:
        count = count + 1
        divs.append(
            dbc.Row(children=[
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('Month of Entity ' + str(count))
                    ], style=style_col),
                    dbc.Col(children=[
                        new_num(id_name + '_mon', 0, None, 0)
                    ], style=style_box_col)
                ], style=style_col),
                dbc.Col(children=[
                    dbc.Col(children=[
                        dbc.Label('Value of Entity ' + str(count)+' (in ₹)')
                    ], style=style_col),
                    dbc.Col(children=[
                        new_num(id_name + '_val', 0, None, 0)
                    ], style=style_box_col)
                ], style=style_col)
            ], style=style_sub_sub_row)
        )
    return html.Div(children=divs)


def count_of_entities(id):
    return dbc.Row(children=[
        dbc.Col(children=[
            dbc.Label('Number of Entities')
        ], style=style_col),
        dbc.Col(children=[
            new_num(id, 0, 100, 0)
        ], style=style_box_col)
    ], style=style_sub_row)


def get_fd_planner():
    return html.Div(children=[
        dbc.Row(children=[
            dbc.Label('FIXED DEPOSITS')
        ], style=style_sub_heading),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Cycle Length (in years)')
            ], style=style_col),
            dbc.Col(children=[
                new_num('cyc_len', 1, 100, 1)
            ], style=style_box_col)
        ], style=style_row),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Col(children=[
                    dbc.Label('Start Month')
                ], style=style_col),
                dbc.Col(children=[
                    new_num('st_mon', 1, 12, 4)
                ], style=style_box_col)
            ], style=style_col),
            dbc.Col(children=[
                dbc.Col(children=[
                    dbc.Label('Start Year')
                ], style=style_col),
                dbc.Col(children=[
                    new_num('st_yr', 2020, 2120, 2020)
                ], style=style_box_col)
            ], style=style_col)
        ], style=style_row),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Present Year Total Monthly Recurring Income')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_pres_rec_inc'),
        html.Div(id='pres_rec_inc'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Present Year Total Monthly Adhoc Income')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_pres_adh_inc'),
        html.Div(id='pres_adh_inc'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Present Year Total Monthly Recurring Expenses')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_pres_rec_exp'),
        html.Div(id='pres_rec_exp'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Present Year Total Monthly Adhoc Expenses')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_pres_adh_exp'),
        html.Div(id='pres_adh_exp'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Next Year Total Monthly Recurring Income')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_nxt_rec_inc'),
        html.Div(id='nxt_rec_inc'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Next Year Total Monthly Adhoc Income')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_nxt_adh_inc'),
        html.Div(id='nxt_adh_inc'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Next Year Total Monthly Recurring Expenses')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_nxt_rec_exp'),
        html.Div(id='nxt_rec_exp'),
        dbc.Row(children=[
            dbc.Col(children=[
                dbc.Label('Next Year Total Monthly Adhoc Expenses')
            ], style=style_col_head),
        ], style=style_row),
        count_of_entities('count_nxt_adh_exp'),
        html.Div(id='nxt_adh_exp'),

    ])


app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dbc.Row(children=[
        dbc.Label('SAVINGS PLANNER')
    ], style=style_heading),
    dbc.Row(children=[
        dbc.Col(children=[
            get_fd_planner()
        ], style=style_fdInputs)
    ])
])

ids_glob = ['pres_rec_inc', 'pres_adh_inc', 'pres_rec_exp', 'pres_adh_exp', 'nxt_rec_inc', 'nxt_adh_inc', 'nxt_rec_exp',
            'nxt_adh_exp']
OUTPUT = []
for id in ids_glob:
    OUTPUT.append(Output(id, 'children'))
INPUT = []
for id in ids_glob:
    INPUT.append(Input('count_' + id, 'value'))


@app.callback(OUTPUT, INPUT)
def rec_boxes_shown(count_pres_rec_inc, count_pres_adh_inc, count_pres_rec_exp, count_pres_adh_exp,
                    count_nxt_rec_inc, count_nxt_adh_inc, count_nxt_rec_exp, count_nxt_adh_exp):
    counts = [count_pres_rec_inc, count_pres_adh_inc, count_pres_rec_exp, count_pres_adh_exp,
              count_nxt_rec_inc, count_nxt_adh_inc, count_nxt_rec_exp, count_nxt_adh_exp]
    ids = []
    for count in counts:
        curr_ids = []
        for i in range(count):
            curr_ids.append(ids_glob[count] + str(i))
        ids.append(curr_ids)

    return_res = []
    i = 0
    while i < len(counts):
        return_res.append(get_recurr_box(ids[i]))
        i = i + 1
        return_res.append(get_adhoc_box(ids[i]))
        i = i + 1
    return return_res


if __name__ == '__main__':
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    app.server.run(port=8050, host=ip_address)

html.Div().app
