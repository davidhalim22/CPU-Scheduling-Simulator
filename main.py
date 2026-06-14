from process import Process
from utils import (calculate_averages, draw_gantt)
from sample_data import (case_1, case_2, case_3)

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin


processes = case_1()  # Change this to case_2() or case_3() for different test cases

result,gantt = fcfs(processes)