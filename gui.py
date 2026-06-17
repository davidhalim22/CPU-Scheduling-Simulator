import tkinter as tk
from tkinter import ttk, messagebox

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

        self.result_table = ttk.Treeview(
            result_frame,
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

        self.result_table.pack(fill="x")

        self.avg_label = ttk.Label(
            result_frame,
            text="",
            font=("Arial", 11, "bold")
        )

        self.avg_label.pack(pady=15)


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

        if algorithm == "FCFS":
            results, self.gantt = fcfs(copied)

        elif algorithm == "SJF":
            results, self.gantt = sjf(copied)

        elif algorithm == "Priority":
            results, self.gantt = priority_scheduling(copied)

        else:
            try:
                quantum = int(self.quantum_entry.get())

                if quantum <= 0:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Input Error",
                    "Quantum must be a positive integer."
                )
                return

            results, self.gantt = round_robin(
                copied,
                quantum
            )

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

        avg_wt, avg_tat = calculate_averages(results)

        self.avg_label.config(
            text=
            f"Average Waiting Time: {avg_wt:.2f}     |     "
            f"Average Turnaround Time: {avg_tat:.2f}"
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