import matplotlib.pyplot as plt


# Statistics calculation
def calculate_averages(processes):
    avg_wt = (sum(p.waiting_time for p in processes) / len(processes))
    
    avg_tat = (sum(p.turnaround_time for p in processes) / len(processes))

    return avg_wt, avg_tat
  


# Gantt chart drawing
def draw_gantt(gantt):
    fig, ax = plt.subplots()

    for pid, start, end in gantt:
        ax.barh(0, end-start, left=start)
        ax.text(start + (end-start)/2, 0, pid, ha="center", va="center")

    ax.set_title("CPU Scheduling Gantt Chart")

    plt.show()