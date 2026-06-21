from utils import (calculate_averages, draw_gantt)
from sample_data import (case_1, case_2, case_3)
from gui import run_gui

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin


if __name__ == "__main__":
    processes = case_3()  # Change this to case_2() or case_3() for different test cases

    result, gantt = round_robin(processes)

    for p in result:
        print(p.pid, p.waiting_time, p.turnaround_time)

    avg_wt, avg_tat = calculate_averages(result)

    print(f"Average Waiting Time: {avg_wt:.2f}")
    print(f"Average Turnaround Time: {avg_tat:.2f}")

    # draw_gantt(gantt)

    run_gui()