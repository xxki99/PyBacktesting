import statistics
import numpy as np

def cal_sma(ls, n):
    sma = []
    for i in range(len(ls)):
        end_pos = i + 1
        start_pos = end_pos - n
        if (start_pos < 0) or (end_pos >= len(ls)):
            sma.append(np.nan)
            continue
        else:
            avg = statistics.mean(ls[start_pos:end_pos])
            sma.append(avg)
    return sma


