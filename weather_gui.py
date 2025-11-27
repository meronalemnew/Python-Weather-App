import tkinter as tk

root = tk.Tk()
root.title("TEST LAYOUT")
root.geometry("500x400")

# Make rows stretch
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)

label1 = tk.Label(root, text="ROW 0 - RED", font=("Arial", 20), bg="red", fg="white")
label1.grid(row=0, column=0, sticky="nsew")

label2 = tk.Label(root, text="ROW 1 - GREEN", font=("Arial", 20), bg="green", fg="black")
label2.grid(row=1, column=0, sticky="nsew")

label3 = tk.Label(root, text="ROW 2 - BLUE", font=("Arial", 20), bg="blue", fg="white")
label3.grid(row=2, column=0, sticky="nsew")

root.mainloop()
