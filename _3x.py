import tkinter as tk
from tkinter import ttk
import json
import matplotlib.pyplot as plt

# File path for memoization data
memo_file = "memo.json"
current_num_file = "current_num.txt"

# Load memoization data from file if it exists
try:
    with open(memo_file, "r") as file:
        memo = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    memo = {}

# Load the current number from file if it exists
try:
    with open(current_num_file, "r") as file:
        current_number = int(file.read())
except (FileNotFoundError, ValueError):
    current_number = 1

# Create a set of memoized numbers for fast lookup
memoized_numbers = set(memo.keys())

def save_memo():
    with open(memo_file, "w") as file:
        json.dump(memo, file)

def save_current_number():
    with open(current_num_file, "w") as file:
        file.write(str(current_number))

def collatz(n):
    if n in memo:
        return memo[n]

    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1

        if n in memoized_numbers:
            sequence.extend(memo[n])
            break

        sequence.append(n)

    memo[sequence[0]] = sequence
    memoized_numbers.add(sequence[0])
    return sequence

def calculate_collatz(n):
    if n in memoized_numbers:
        return n, memo[n]
    
    sequence = collatz(n)
    return n, sequence

def update_output_text():
    global current_number
    result = calculate_collatz(current_number)
    num, sequence = result
    if show_output.get():  # Check if the output should be displayed
        output_text.delete(1.0, tk.END)  # Clear the previous sequence
        for num in sequence:
            if num in memoized_numbers:
                output_text.insert(tk.END, str(num) + " ", "green")
            else:
                output_text.insert(tk.END, str(num) + " ", "red")
    current_number += 1
    current_num_text.set("Current Number: {}".format(current_number))  # Update the current number label
    memo_count_text.set("Memo Count: {}".format(len(memo)))  # Update the memo count label
    save_current_number()
    root.after(10, update_output_text)  # Schedule the next update after 10 milliseconds

def toggle_output():
    if show_output.get():
        show_output.set(False)
        toggle_button.config(text="Show Output")
    else:
        show_output.set(True)
        toggle_button.config(text="Hide Output")

def plot_histogram():
    values = [len(sequence) for sequence in memo.values()]
    plt.hist(values, bins=20, alpha=0.7)
    plt.xlabel('Length of Sequence')
    plt.ylabel('Frequency')
    plt.title('Collatz Sequence Length Histogram')
    plt.grid(True)
    plt.show()

def on_closing():
    save_memo()
    save_current_number()
    root.destroy()

root = tk.Tk()
root.title("Collatz Conjecture Calculator")

# Output Text
output_text = tk.Text(root, width=40, height=20)
output_text.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

# Toggle Button
show_output = tk.BooleanVar()
toggle_button = ttk.Button(root, text="Show Output", command=toggle_output)
toggle_button.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Current Number Label
current_num_text = tk.StringVar()
current_num_label = ttk.Label(root, textvariable=current_num_text)
current_num_label.grid(row=1, column=1, padx=10, pady=5, sticky="e")
current_num_text.set("Current Number: {}".format(current_number))

# Memo Count Label
memo_count_text = tk.StringVar()
memo_count_label = ttk.Label(root, textvariable=memo_count_text)
memo_count_label.grid(row=2, column=1, padx=10, pady=5, sticky="e")
memo_count_text.set("Memo Count: {}".format(len(memo)))

# Histogram Button
histogram_button = ttk.Button(root, text="Show Histogram", command=plot_histogram)
histogram_button.grid(row=2, column=0, padx=10, pady=5, sticky="w")

root.protocol("WM_DELETE_WINDOW", on_closing)

root.after(10, update_output_text)  # Start updating the output text

root.mainloop()
