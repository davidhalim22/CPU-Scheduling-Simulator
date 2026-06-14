class Process:
    def __init__(self, pid, arrival, burst, priority):
        self.pid = pid
        self.arrival = arrival
        self.burst = burst
        self.priority = priority

        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def reset(self):
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0

    def copy(self):
        return Process(
            self.pid,
            self.arrival,
            self.burst,
            self.priority
        )