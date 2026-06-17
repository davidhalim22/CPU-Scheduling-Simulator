def fcfs(processes):
    processes = sorted(processes, key=lambda p: p.arrival)

    current_time = 0
    gantt = []
    
    for p in processes:       # Simulate the process execution
        if current_time < p.arrival:
            current_time = p.arrival  # Wait for the process to arrive
        
        start_time = current_time
        current_time += p.burst
        end_time = current_time
        
        p.completion_time = end_time
        p.turnaround_time = p.completion_time - p.arrival
        p.waiting_time = p.turnaround_time - p.burst
        
        gantt.append((p.pid, start_time, end_time))
        
    return gantt, processes