from collections import deque

def round_robin(processes, quantum=2):
    processes = sorted(processes, key=lambda p: p.arrival)
    
    remaining = {p.pid: p.burst for p in processes}
    queue = deque()
    gantt = []
    
    current_time = 0
    index = 0
    
    while (index < len(processes) and processes[index].arrival <= current_time):
        queue.append(processes[index])
        index += 1
    
    while queue:
        current = queue.popleft()
        run_time = min(quantum, remaining[current.pid])
        
        start_time = current_time
        current_time += run_time
        end_time = current_time
        
        gantt.append((current.pid, start_time, end_time))
        
        remaining[current.pid] -= run_time
        
        while (index < len(processes) and processes[index].arrival <= current_time):
            queue.append(processes[index])
            index += 1
        
        if remaining[current.pid] > 0:
            queue.append(current)
        
        else:
            current.completion_time = current_time
            current.turnaround_time = current.completion_time - current.arrival
            current.waiting_time = current.turnaround_time - current.burst
    

        if (not queue and index < len(processes)):
            current_time = processes[index].arrival
            queue.append(processes[index])
            index += 1
    
    return processes, gantt