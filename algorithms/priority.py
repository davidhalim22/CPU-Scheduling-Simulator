def priority_scheduling(processes):
    processes = processes[:]

    completed = []
    gantt = []

    current_time = 0

    while processes:
        ready = [p for p in processes if p.arrival <= current_time]

        if not ready:
            current_time += 1
            continue

        selected = min(ready, key=lambda p: p.priority)
        start_time = current_time
        current_time += selected.burst
        end_time = current_time

        selected.completion_time = end_time
        selected.turnaround_time = end_time - selected.arrival
        selected.waiting_time = selected.turnaround_time - selected.burst

        gantt.append((selected.pid, start_time, end_time))

        completed.append(selected)
        processes.remove(selected)
        
    return completed, gantt