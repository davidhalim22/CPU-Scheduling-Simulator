from process import Process
from utils import (calculate_averages, draw_gantt)
from sample_data import (case_1, case_2, case_3)
from gui import run_gui

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin


processes = case_1()  # Change this to case_2() or case_3() for different test cases

result,gantt = fcfs(processes)

for p in result:
  print(p.pid, p.waiting_time, p.turnaround_time)

avg_wt, avg_tat = calculate_averages(result)

print(f"""
Average Waiting Time: {avg_wt, 2}
Average Turnaround Time: {avg_tat, 2}
""")

draw_gantt(gantt)


# run_gui()