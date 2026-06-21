import tkinter as tk
from tkinter import ttk, messagebox
import random

from process import Process

from algorithms.fcfs import fcfs
from algorithms.sjf import sjf
from algorithms.priority import priority_scheduling
from algorithms.round_robin import round_robin

from utils import calculate_averages, draw_gantt



class CPUSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x700")
        self.root.configure(bg="white")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(".", background="white", foreground="black")

        self.style.configure(
            "TLabel",
            background="white",
            foreground="black"
        )

        self.style.configure(
            "TLabelframe",
            background="white",
            foreground="black"
        )

        self.style.configure(
            "TLabelframe.Label",
            background="white",
            foreground="black",
            font=("Arial", 10, "bold")
        )

        self.style.configure(
            "TButton",
            padding=6
        )

        self.style.configure(
            "TEntry",
            fieldbackground="white",
            foreground="black"
        )

        self.style.configure(
            "TCombobox",
            fieldbackground="white",
            background="white",
            foreground="black"
        )

        self.style.map(
            "TCombobox",
            fieldbackground=[("readonly", "white")],
            selectbackground=[("readonly", "white")],
            selectforeground=[("readonly", "black")]
        )

        self.style.configure(
            "Treeview",
            background="white",
            foreground="black",
            fieldbackground="white",
            rowheight=25
        )

        self.style.configure(
            "Treeview.Heading",
            background="white",
            foreground="black",
            font=("Arial", 10, "bold")
        )

        self.processes = []
        self.gantt = []

        self.create_widgets()


    def create_widgets(self):
        title = ttk.Label(
            self.root,
            text="CPU Scheduling Simulator",
            font=("Arial", 20, "bold")
        )
        title.pack(pady=15)


        # =====================
        # Process Input
        # =====================
        input_frame = ttk.LabelFrame(
            self.root,
            text="Process Input",
            padding=10
        )
        input_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(input_frame, text="PID").grid(row=0, column=0, padx=5)
        ttk.Label(input_frame, text="Arrival").grid(row=0, column=1, padx=5)
        ttk.Label(input_frame, text="Burst").grid(row=0, column=2, padx=5)
        ttk.Label(input_frame, text="Priority").grid(row=0, column=3, padx=5)

        self.pid_entry = ttk.Entry(input_frame, width=12)
        self.arrival_entry = ttk.Entry(input_frame, width=12)
        self.burst_entry = ttk.Entry(input_frame, width=12)
        self.priority_entry = ttk.Entry(input_frame, width=12)

        self.pid_entry.grid(row=1, column=0, padx=5)
        self.arrival_entry.grid(row=1, column=1, padx=5)
        self.burst_entry.grid(row=1, column=2, padx=5)
        self.priority_entry.grid(row=1, column=3, padx=5)

        add_btn = ttk.Button(
            input_frame,
            text="Add Process",
            command=self.add_process
        )
        add_btn.grid(row=1, column=4, padx=15)


        # =====================
        # Random Workload
        # =====================
        random_frame = ttk.LabelFrame(
            self.root,
            text="Random Workload",
            padding=10
        )
        random_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(random_frame, text="Count").grid(row=0, column=0, padx=5)
        ttk.Label(random_frame, text="Arrival Max").grid(row=0, column=1, padx=5)
        ttk.Label(random_frame, text="Burst Max").grid(row=0, column=2, padx=5)
        ttk.Label(random_frame, text="Priority Max").grid(row=0, column=3, padx=5)

        self.random_count_entry = ttk.Entry(random_frame, width=12)
        self.random_arrival_entry = ttk.Entry(random_frame, width=12)
        self.random_burst_entry = ttk.Entry(random_frame, width=12)
        self.random_priority_entry = ttk.Entry(random_frame, width=12)

        self.random_count_entry.insert(0, "5")
        self.random_arrival_entry.insert(0, "10")
        self.random_burst_entry.insert(0, "10")
        self.random_priority_entry.insert(0, "5")

        self.random_count_entry.grid(row=1, column=0, padx=5)
        self.random_arrival_entry.grid(row=1, column=1, padx=5)
        self.random_burst_entry.grid(row=1, column=2, padx=5)
        self.random_priority_entry.grid(row=1, column=3, padx=5)

        generate_btn = ttk.Button(
            random_frame,
            text="Generate Random Workload",
            command=self.generate_random_workload
        )
        generate_btn.grid(row=1, column=4, padx=15)

        compare_btn = ttk.Button(
            random_frame,
            text="Compare Algorithms",
            command=self.compare_algorithms
        )
        compare_btn.grid(row=1, column=5, padx=5)


        # =====================
        # Process Table
        # =====================
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="x", padx=10, pady=10)

        self.process_table = ttk.Treeview(
            table_frame,
            columns=("PID", "Arrival", "Burst", "Priority"),
            show="headings",
            height=8
        )

        self.process_table.heading("PID", text="PID")
        self.process_table.heading("Arrival", text="Arrival Time")
        self.process_table.heading("Burst", text="Burst Time")
        self.process_table.heading("Priority", text="Priority")

        self.process_table.column("PID", width=120)
        self.process_table.column("Arrival", width=120)
        self.process_table.column("Burst", width=120)
        self.process_table.column("Priority", width=120)

        self.process_table.pack(fill="x")


        # =====================
        # Scheduling Options
        # =====================
        control_frame = ttk.LabelFrame(
            self.root,
            text="Scheduling Options",
            padding=10
        )
        control_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(
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
            state="readonly",
            width=15
        )

        self.algorithm_combo.grid(row=0, column=1, padx=10)

        self.algorithm_combo.current(0)

        ttk.Label(
            control_frame,
            text="Quantum:"
        ).grid(row=0, column=2)

        self.quantum_entry = ttk.Entry(
            control_frame,
            width=10
        )

        self.quantum_entry.insert(0, "2")
        self.quantum_entry.grid(row=0, column=3, padx=5)

        run_btn = ttk.Button(
            control_frame,
            text="Run Simulation",
            command=self.run_simulation
        )

        run_btn.grid(row=0, column=4, padx=20)

        gantt_btn = ttk.Button(
            control_frame,
            text="Show Gantt Chart",
            command=self.show_gantt
        )

        gantt_btn.grid(row=0, column=5)


        # =====================
        # Results
        # =====================
        result_frame = ttk.LabelFrame(
            self.root,
            text="Results",
            padding=10
        )

        result_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        result_notebook = ttk.Notebook(result_frame)
        result_notebook.pack(fill="both", expand=True)

        results_tab = ttk.Frame(result_notebook)
        comparison_tab = ttk.Frame(result_notebook)

        result_notebook.add(results_tab, text="Simulation Results")
        result_notebook.add(comparison_tab, text="Algorithm Comparison")

        results_content = ttk.Frame(results_tab)
        results_content.pack(fill="both", expand=True)

        results_left = ttk.Frame(results_content)
        results_left.grid(row=0, column=0, sticky="nsew")

        results_right = ttk.Frame(results_content)
        results_right.grid(row=0, column=1, sticky="nsew", padx=(15, 0))

        results_content.columnconfigure(0, weight=3)
        results_content.columnconfigure(1, weight=2)

        self.result_table = ttk.Treeview(
            results_left,
            columns=("PID", "WT", "TAT"),
            show="headings",
            height=8
        )

        self.result_table.heading("PID", text="PID")
        self.result_table.heading("WT", text="Waiting Time")
        self.result_table.heading("TAT", text="Turnaround Time")

        self.result_table.column("PID", width=120)
        self.result_table.column("WT", width=150)
        self.result_table.column("TAT", width=150)

        self.result_table.pack(fill="both", expand=True)

        avg_frame = ttk.LabelFrame(
            results_right,
            text="Averages",
            padding=10
        )
        avg_frame.pack(fill="both", expand=True)

        self.avg_table = ttk.Treeview(
            avg_frame,
            columns=("Metric", "Average"),
            show="headings",
            height=4
        )

        self.avg_table.heading("Metric", text="Metric")
        self.avg_table.heading("Average", text="Average")

        self.avg_table.column("Metric", width=190)
        self.avg_table.column("Average", width=110)

        self.avg_table.pack(fill="both", expand=True)

        comparison_frame = ttk.LabelFrame(
            comparison_tab,
            text="Algorithm Comparison",
            padding=10
        )
        comparison_frame.pack(fill="both", expand=True, padx=5, pady=5)

        ttk.Label(
            comparison_frame,
            text="Generate a random workload or use the current process list, then compare all algorithms.",
            wraplength=900
        ).pack(anchor="w", pady=(0, 10))

        self.comparison_table = ttk.Treeview(
            comparison_frame,
            columns=("Algorithm", "Avg WT", "Avg TAT"),
            show="headings",
            height=6
        )

        self.comparison_table.heading("Algorithm", text="Algorithm")
        self.comparison_table.heading("Avg WT", text="Average Waiting Time")
        self.comparison_table.heading("Avg TAT", text="Average Turnaround Time")

        self.comparison_table.column("Algorithm", width=160)
        self.comparison_table.column("Avg WT", width=180)
        self.comparison_table.column("Avg TAT", width=190)

        self.comparison_table.pack(fill="both", expand=True)


    # Adds a new process
    def add_process(self):
        try:
            pid = self.pid_entry.get().strip()

            if pid == "":
                raise ValueError

            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())

            process = Process(pid, arrival, burst, priority)

            self.processes.append(process)

            self.process_table.insert(
                "",
                "end",
                values=(pid, arrival, burst, priority)
            )

            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid process information."
            )


    def _clear_treeview(self, treeview):
        for row in treeview.get_children():
            treeview.delete(row)


    def _get_quantum(self, required=True, default=2):
        try:
            quantum = int(self.quantum_entry.get())

            if quantum <= 0:
                raise ValueError

            return quantum

        except ValueError:
            if required:
                messagebox.showerror(
                    "Input Error",
                    "Quantum must be a positive integer."
                )
                return None

            return default


    def _run_algorithm(self, algorithm, processes, quantum=None):
        copied = [p.copy() for p in processes]

        if algorithm == "FCFS":
            return fcfs(copied)

        if algorithm == "SJF":
            return sjf(copied)

        if algorithm == "Priority":
            return priority_scheduling(copied)

        return round_robin(copied, quantum)


    def generate_random_workload(self):
        try:
            count = int(self.random_count_entry.get())
            arrival_max = int(self.random_arrival_entry.get())
            burst_max = int(self.random_burst_entry.get())
            priority_max = int(self.random_priority_entry.get())

            if count <= 0 or arrival_max < 0 or burst_max <= 0 or priority_max <= 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Input Error",
                "Please enter valid random workload limits."
            )
            return

        self.processes = []
        self.gantt = []
        self._clear_treeview(self.process_table)
        self._clear_treeview(self.result_table)
        self._clear_treeview(self.avg_table)

        for index in range(1, count + 1):
            process = Process(
                f"P{index}",
                random.randint(0, arrival_max),
                random.randint(1, burst_max),
                random.randint(1, priority_max)
            )

            self.processes.append(process)

            self.process_table.insert(
                "",
                "end",
                values=(process.pid, process.arrival, process.burst, process.priority)
            )

        self.compare_algorithms()


    def compare_algorithms(self):
        if not self.processes:
            messagebox.showwarning(
                "Warning",
                "No processes available. Add or generate a workload first."
            )
            return

        quantum = self._get_quantum(required=False)
        if quantum is None:
            return

        comparison_rows = []

        for algorithm in ["FCFS", "SJF", "Priority", "Round Robin"]:
            results, _ = self._run_algorithm(algorithm, self.processes, quantum)
            avg_wt, avg_tat = calculate_averages(results)

            comparison_rows.append((
                algorithm,
                f"{avg_wt:.2f}",
                f"{avg_tat:.2f}"
            ))

        self._clear_treeview(self.comparison_table)

        for row in comparison_rows:
            self.comparison_table.insert("", "end", values=row)


    # Runs the selected scheduling algorithm
    def run_simulation(self):
        if not self.processes:
            messagebox.showwarning(
                "Warning",
                "No processes added."
            )
            return

        copied = [p.copy() for p in self.processes]

        algorithm = self.algorithm_var.get()

        if algorithm == "Round Robin":
            quantum = self._get_quantum(required=True)
            if quantum is None:
                return

            results, self.gantt = self._run_algorithm(algorithm, copied, quantum)

        else:
            results, self.gantt = self._run_algorithm(algorithm, copied)

        self._clear_treeview(self.result_table)

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

        avg_wt, avg_tat = calculate_averages(results)

        self._clear_treeview(self.avg_table)

        self.avg_table.insert(
            "",
            "end",
            values=("Average Waiting Time", f"{avg_wt:.2f}")
        )

        self.avg_table.insert(
            "",
            "end",
            values=("Average Turnaround Time", f"{avg_tat:.2f}")
        )


    # Draws the Gantt chart
    def show_gantt(self):
        if not self.gantt:
            messagebox.showwarning("Warning", "Run a simulation first.")
            return

        draw_gantt(self.gantt)



def run_gui():
    root = tk.Tk()
    CPUSchedulerGUI(root)
    root.mainloop()