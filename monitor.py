import tkinter as tk

class CPUHeatMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Thermal Monitor")
        self.root.geometry("400x250")
        self.root.configure(bg='black')
        self.label = tk.Label(root, text="--°C", font=("Arial", 95, "bold"), fg="#00FF00", bg="black")
        self.label.pack(expand=True)
        self.label = tk.Label(root, text="--°C", font=("Arial", 95, "bold"), fg="#00FF00", bg="black")
        self.label.pack(expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUHeatMonitor(root)
    root.mainloop()