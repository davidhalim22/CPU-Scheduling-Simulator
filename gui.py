import tkinter as tk
from tkinter import ttk, messagebox

from process import Process

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin

from utils import (calculate_averages, draw_gantt)


class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x700")

        self.processes = []
        self.gantt = []
        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(
            self.root,
            text="CPU Scheduling Simulator",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=10)

        input_frame = tk.LabelFrame(
            self.root,
            text="Process Input",
            padx=10,
            pady=10
        )
        input_frame.pack(fill="x", padx=10)

        tk.Label(input_frame, text="PID").grid(row=0, column=0)
        tk.Label(input_frame, text="Arrival").grid(row=0, column=1)
        tk.Label(input_frame, text="Burst").grid(row=0, column=2)
        tk.Label(input_frame, text="Priority").grid(row=0, column=3)

        self.pid_entry = tk.Entry(input_frame, width=10)
        self.arrival_entry = tk.Entry(input_frame, width=10)
        self.burst_entry = tk.Entry(input_frame, width=10)
        self.priority_entry = tk.Entry(input_frame, width=10)

        self.pid_entry.grid(row=1, column=0)
        self.arrival_entry.grid(row=1, column=1)
        self.burst_entry.grid(row=1, column=2)
        self.priority_entry.grid(row=1, column=3)

        add_btn = tk.Button(
            input_frame,
            text="Add Process",
            command=self.add_process
        )
        add_btn.grid(row=1, column=4, padx=10)

        # Process Table

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.process_table = ttk.Treeview(
            table_frame,
            columns=(
                "PID",
                "Arrival",
                "Burst",
                "Priority"
            ),
            show="headings",
            height=8
        )

        self.process_table.heading("PID", text="PID")
        self.process_table.heading("Arrival", text="Arrival")
        self.process_table.heading("Burst", text="Burst")
        self.process_table.heading("Priority", text="Priority")

        self.process_table.pack(fill="x")

        # Controls

        control_frame = tk.LabelFrame(
            self.root,
            text="Scheduling Options",
            padx=10,
            pady=10
        )
        control_frame.pack(fill="x", padx=10)

        tk.Label(
            control_frame,
            text="Algorithm:"
        ).grid(row=0, column=0)

        self.algorithm_var = tk.StringVar()

        self.algorithm_combo = ttk.Combobox(
            control_frame,
            textvariable=self.algorithm_var,
            values=[
                "FCFS",
                "SJF",
                "Priority",
                "Round Robin"
            ],
            state="readonly"
        )

        self.algorithm_combo.grid(row=0, column=1, padx=10)

        self.algorithm_combo.current(0)
        
        tk.Label(control_frame, text="Quantum:").grid(row=0, column=2)

        self.quantum_entry = tk.Entry(control_frame, width=10)
        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=0, column=3)

        run_btn = tk.Button(
            control_frame,
            text="Run Simulation",
            command=self.run_simulation
        )

        run_btn.grid(
            row=0,
            column=4,
            padx=20
        )

        gantt_btn = tk.Button(
            control_frame,
            text="Show Gantt Chart",
            command=self.show_gantt
        )

        gantt_btn.grid(row=0, column=5)

        # Results Table

        result_frame = tk.LabelFrame(
            self.root,
            text="Results",
            padx=10,
            pady=10
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.result_table = ttk.Treeview(
            result_frame,
            columns=(
                "PID",
                "WT",
                "TAT"
            ),
            show="headings",
            height=8
        )

        self.result_table.heading(
            "PID",
            text="PID"
        )

        self.result_table.heading(
            "WT",
            text="Waiting Time"
        )

        self.result_table.heading(
            "TAT",
            text="Turnaround Time"
        )

        self.result_table.pack(fill="x")

        self.avg_label = tk.Label(
            result_frame,
            text=""
        )

        self.avg_label.pack(pady=10)

    def add_process(self):
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())

            process = Process(
                pid,
                arrival,
                burst,
                priority
            )

            self.processes.append(process)

            self.process_table.insert(
                "",
                "end",
                values=(
                    pid,
                    arrival,
                    burst,
                    priority
                )
            )

            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid values.")


    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning("Warning", "No processes added.")

            return

        copied = [
            p.copy()
            for p in self.processes]

        algorithm = self.algorithm_var.get()

        if algorithm == "FCFS":
            results, self.gantt = fcfs(copied)

        elif algorithm == "SJF":
            results, self.gantt = sjf(copied)

        elif algorithm == "Priority":
            results, self.gantt = priority_scheduling(copied)

        else:
            quantum = int(self.quantum_entry.get())

            results, self.gantt = round_robin(copied, quantum)

        for row in self.result_table.get_children():
            self.result_table.delete(row)

        for p in results:
            self.result_table.insert(
                "",
                "end",
                values=(
                    p.pid,
                    p.waiting_time,
                    p.turnaround_time
                )
            )

        avg_wt, avg_tat = (calculate_averages(results))

        self.avg_label.config(
            text=
            f"Average WT: {avg_wt:.2f}    "
            f"Average TAT: {avg_tat:.2f}"
        )

    def show_gantt(self):
        if not self.gantt:
            messagebox.showwarning("Warning", "Run a simulation first.")
            return

        draw_gantt(self.gantt)


def run_gui():
    root = tk.Tk()
    app = CPUSchedulerGUI(root)
    root.mainloop()