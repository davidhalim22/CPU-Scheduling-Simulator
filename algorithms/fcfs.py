def fcfs(processes):
    processes = sorted(processes, key=lambda p: p.arrival)

    current_time = 0
    gantt = []
    
    for p in processes:       # Simulate the process execution
        ...