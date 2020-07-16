from config import *
import pandas as pd
import datetime


class fdCalculator:
    @staticmethod
    def aggTable_generator(start_mon_glob, start_year_glob, type, freq, start_mon, start_year, time_dur, val):
        pres_inc, nxt_inc = [0] * 12, [0] * 12
        pres_exp, nxt_exp = [0] * 12, [0] * 12
        curr_year_st = [start_mon_glob, start_year_glob]
        nxt_year_st = [start_mon_glob, start_year_glob + 1]
        start_mon_glob = MON_MAP[start_mon_glob]
        for i in range(len(type)):
            if type[i] is None:
                continue
            curr_mon = MON_MAP[start_mon[i]]
            if freq[i] == RECUR:
                division = fdCalculator.year_check(curr_mon, start_year[i], start_mon_glob, start_year_glob,
                                                   time_dur[i])
                if division == -1:
                    for mon in range(curr_mon, curr_mon + time_dur[i]):
                        if type[i] == INFLOW:
                            pres_inc[mon % 12] = pres_inc[mon % 12] + val[i]
                        elif type[i] == OUTFLOW:
                            pres_exp[mon % 12] = pres_exp[mon % 12] + val[i]
                    i = i + 1
                elif division == 1:
                    for mon in range(curr_mon, curr_mon + time_dur[i]):
                        if type[i] == INFLOW:
                            nxt_inc[mon % 12] = nxt_inc[mon % 12] + val[i]
                        elif type[i] == OUTFLOW:
                            nxt_exp[mon % 12] = nxt_exp[mon % 12] + val[i]
                    i = i + 1
                elif division == 0:
                    count = 0
                    for mon in range(curr_mon, 12):
                        if type[i] == INFLOW:
                            pres_inc[mon % 12] = pres_inc[mon % 12] + val[i]
                        elif type[i] == OUTFLOW:
                            pres_exp[mon % 12] = pres_exp[mon % 12] + val[i]
                        count = count + 1
                    for mon in range(start_mon_glob):
                        if type[i] == INFLOW:
                            pres_inc[mon % 12] = pres_inc[mon % 12] + val[i]
                        elif type[i] == OUTFLOW:
                            pres_exp[mon % 12] = pres_exp[mon % 12] + val[i]
                        count = count + 1
                    for mon in range(start_mon_glob, start_mon_glob + time_dur[i] - count):
                        if type[i] == INFLOW:
                            nxt_inc[mon % 12] = nxt_inc[mon % 12] + val[i]
                        elif type[i] == OUTFLOW:
                            nxt_exp[mon % 12] = nxt_exp[mon % 12] + val[i]
                    i = i + 1
            elif freq[i] == ADH:
                if fdCalculator.year_check(curr_mon, start_year[i], start_mon_glob, start_year_glob) == -1:
                    if type[i] == INFLOW:
                        pres_inc[curr_mon] = pres_inc[curr_mon] + val[i]
                    elif type[i] == OUTFLOW:
                        pres_exp[curr_mon] = pres_exp[curr_mon] + val[i]
                elif fdCalculator.year_check(curr_mon, start_year[i], start_mon_glob, start_year_glob) == 1:
                    if type[i] == INFLOW:
                        nxt_inc[curr_mon] = nxt_inc[curr_mon] + val[i]
                    elif type[i] == OUTFLOW:
                        nxt_exp[curr_mon] = nxt_exp[curr_mon] + val[i]
        monthly_fds_pres, monthly_fds_nxt = fdCalculator.fds_calculator(start_mon_glob, start_year_glob, pres_inc,
                                                                        pres_exp, nxt_inc,
                                                                        nxt_exp)
        monthly_fds_pres = fdCalculator.decorate(monthly_fds_pres)
        return monthly_fds_pres

    @staticmethod
    def decorate(fds):
        for mon in range(len(fds)):
            curr_fds = fds[mon]
            fd_str = ''
            count = 1
            for fd in curr_fds[3]:
                if count == len(curr_fds[3]):
                    fd_str = fd_str + 'FD '+str(count) + ' valuing to ' + str(fd[0]) + ' for a priod of ' + str( fd[1]) + ' months'
                else:
                    fd_str = fd_str + 'FD ' + str(count) + ' valuing to ' + str(fd[0]) + ' for a priod of ' + str(
                        fd[1]) + ' months; '
                count = count + 1
            fds[mon][3] = fd_str
        fd_table = pd.DataFrame(fds, columns=REPORT_COLUMNS)
        return fd_table

    @staticmethod
    def fds_calculator(start_mon_glob, start_year_glob, pres_inc, pres_exp, nxt_inc, nxt_exp):
        pres_fd = [0] * 12
        delta_mature = [0] * 12
        nxt_fd = [0] * 12
        permonth_avg = (sum(pres_inc) + sum(nxt_inc) - sum(pres_exp) - sum(nxt_exp)) / 12
        for i in range(12):
            pres_fd[i % 12] = round(pres_inc[i % 12] - pres_exp[i % 12], 1)
            delta_mature[i % 12] = round(permonth_avg - (nxt_inc[i % 12] - nxt_exp[i % 12]), 1)
            nxt_fd[i % 12] = round(delta_mature[i % 12] + nxt_inc[i % 12] - nxt_exp[i % 12], 1)
        pres_fd, delta_mature, nxt_fd = fdCalculator.remove_negatives(start_mon_glob, pres_fd, delta_mature, nxt_fd)
        monthly_fds_pres, monthly_fds_nxt = [], []
        i = start_mon_glob
        j = start_mon_glob
        while 1:
            temp = []
            cur_value = pres_fd[i]
            count = 1
            while cur_value > 0:
                curr_red = min(cur_value, delta_mature[j])
                delta_mature[j] = delta_mature[j] - curr_red
                cur_value = cur_value - curr_red
                temp.append([round(curr_red, 2), j - i + 12])
                if delta_mature[j] == 0:
                    j = (j + 1) % 12
                count = count + 1
                if j == start_mon_glob - 1:
                    break
            cur_mon = 'Jan'
            for key in MON_MAP:
                if MON_MAP[key] == i:
                    cur_mon = key
                    break
            monthly_fds_pres.append([cur_mon,pres_inc[i], pres_exp[i], temp])
            i = (i + 1) % 12
            if i == start_mon_glob:
                break
        # monthly_fds_pres = pd.DataFrame(monthly_fds_pres, columns=['Month', 'Fds'])
        i = start_mon_glob
        while 1:
            temp = []
            temp.append([round(nxt_fd[i], 2), 12])
            cur_mon = 'Jan'
            for key in MON_MAP:
                if MON_MAP[key] == i:
                    cur_mon = key
                    break
            monthly_fds_nxt.append([cur_mon, temp])
            i = (i + 1) % 12
            if i == start_mon_glob:
                break
        return monthly_fds_pres, monthly_fds_nxt

    @staticmethod
    def remove_negatives(start_mon_glob, pres_fd, delta_mature, nxt_fd):
        i = start_mon_glob
        while 1:
            curr_val = 0
            if pres_fd[i] < 0:
                curr_val = pres_fd[i] * -1
                pres_fd[i] = 0
                j = i - 1
                if j < start_mon_glob:
                    while j >= 0:
                        curr_red = min(pres_fd[j], curr_val)
                        pres_fd[j] = pres_fd[j] - curr_red
                        curr_val = curr_val - curr_red
                        if curr_val == 0:
                            break
                        j = j - 1
                    j = 11
                while j >= start_mon_glob:
                    curr_red = min(pres_fd[j], curr_val)
                    pres_fd[j] = pres_fd[j] - curr_red
                    curr_val = curr_val - curr_red
                    if curr_val == 0:
                        break
                    j = j - 1
            i = (i + 1) % 12
            if i == start_mon_glob:
                break
        i = start_mon_glob
        while 1:
            curr_val = 0
            if delta_mature[i] < 0:
                months_left = (start_mon_glob - 1) % 12 - i
                curr_val = round(delta_mature[i] * -1 / months_left, 2)
                delta_mature[i] = 0
                for j in range(i + 1, 12):
                    delta_mature[j] = delta_mature[j] + curr_val
                for j in range(start_mon_glob):
                    delta_mature[j] = delta_mature[j] + curr_val
            i = (i + 1) % 12
            if i == start_mon_glob - 1:
                break
        for i in range(len(pres_fd)):
            nxt_fd[i] = pres_fd[i] + delta_mature[i]
        return pres_fd, delta_mature, nxt_fd

    @staticmethod
    def year_check(pres_mon, pres_year, start_mon_glob, start_year_glob, time_dur=0):
        end_mon, end_year = end_date(pres_mon, pres_year, time_dur)
        start_entry_date = datetime.datetime(pres_year, pres_mon + 1, 1)
        end_entry_date = datetime.datetime(end_year, end_mon + 1, 28)
        end_year_date = datetime.datetime(start_year_glob + 1, start_mon_glob + 1, 1)
        if end_entry_date < end_year_date:
            return -1
        if start_entry_date >= end_year_date:
            return 1
        return 0

#
# pres_fds = fdCalculator.aggTable_generator('April', 2020,
#                                            [INFLOW, INFLOW, INFLOW, INFLOW, INFLOW, INFLOW, INFLOW, INFLOW,
#                                             OUTFLOW, OUTFLOW, OUTFLOW, OUTFLOW, OUTFLOW, OUTFLOW, OUTFLOW,
#                                             OUTFLOW],
#                                            [RECUR, ADH, ADH, ADH, ADH, ADH, RECUR, ADH, RECUR, RECUR, ADH, ADH,
#                                             ADH, RECUR, RECUR, ADH],
#                                            [APR, JUN, AUG, OCT, DEC, FEB, APR, SEP, APR, APR, SEP, NOV, MAR,
#                                             APR,
#                                             APR, DEC],
#                                            [2020, 2020, 2020, 2020, 2020, 2020, 2021, 2021, 2020, 2020, 2020,
#                                             2020, 2020, 2021, 2021, 2021],
#                                            [12, 12, 12, 12, 12, 12],
#                                            [1, 4, 4, 5, 4, 4, 1.08, 8, 0.5, 0.3, 3.6, 0.2, 2, 0.53, 0.4, 3])
# print(pres_fds)
