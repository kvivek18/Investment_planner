class InputsManipulator:
    @staticmethod
    def include_balance(cur_bal, des_bal, start_mon_glob, pres_fd, delta_mature, nxt_fd):
        temp_bal = cur_bal
        i = start_mon_glob
        while 1:
            if temp_bal == des_bal:
                i = (i + 1) % 12
                if i == start_mon_glob - 1:
                    break
                continue

            i = (i + 1) % 12
            if i == start_mon_glob - 1:
                break

        return pres_fd, delta_mature, nxt_fd

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
