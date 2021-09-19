import tkinter as tk

from src.main_view import MainView

if __name__ == "__main__":
    app = tk.Tk(className="Differential Equation Solver")
    app.resizable(width=False, height=False)
    # root.iconbitmap('assets/icon.ico')
    app.geometry("1100x600")
    MainView(app).pack(side="top", fill="both", expand=True)
    app.mainloop()
