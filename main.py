import random
from tkinter import *
import tkinter as tk
import words
from tkinter import messagebox

# Define colors
LIGHT_GRAY = "#d3d3d3"
DARK_GRAY = "#a9a9a9"
LIGHT_BLUE = "#add8e6"  # Light Blue
DARK_BLUE = "#4682b4"   # Steel Blue

# Sample word list from words file
word_list = random.sample(words.words_use, 5)
word_dictionary = {word: 0 for word in word_list}

# Initialize Tkinter window
window = Tk()
window.title("Typing Highlighter")
window.config(padx=400, pady=300, bg=LIGHT_GRAY)

# Canvas dimensions
canvas_width = 800
canvas_height = 80
canvas = Canvas(window, bg=DARK_GRAY, width=canvas_width, height=canvas_height, highlightthickness=0)
canvas.grid(column=1, row=2)

x_position = 40
y_position = 40
line_height = 30

matched_words = []
incorrect_word_index = -1

old_one = ""
i = 0
score = 0
game_is_on = False

def display_words():
    global i, key, word_list, word_dictionary
    canvas.delete("all")
    x_pos = x_position
    y_pos = y_position
    space_width = 10

    for word in word_list:
        incorrect_word_index = word_dictionary[word]
        color = "white"

        if incorrect_word_index == 1:
            color = "blue"

        elif incorrect_word_index == -1:
            color = "red"

        # Display word with the chosen color
        canvas.create_text(x_pos, y_pos, text=word, anchor="w", fill=color, font=("Arial", 16))
        x_pos += space_width + 150

        if x_pos > canvas_width - 100:
            x_pos = x_position
            y_pos += line_height

def update_highlights(*args):
    global matched_words, incorrect_word_index, old_one, i, word_list, word_dictionary
    input_text = word_input_var.get()
    expected_text = word_list[i]
    word_dictionary[expected_text] = -1
    display_words()

    if " " in input_text:
        # Remove all spaces from the input_text
        input_text = input_text.replace(" ", "")
        input_text = input_text.replace(old_one, "")

        matched_words = []
        incorrect_word_index = -1

        expected_text = word_list[i]

        if input_text == expected_text:
            matched_words = expected_text
            word_dictionary[matched_words] = 1
            old_one = old_one + expected_text

            try:
                expected_text = word_list[i+1]
                word_dictionary[expected_text] = -1
            except:
                pass
            word_input.delete(0, tk.END)
            word_input_var.set("")
            i = i + 1
            score_calculation()
            print(i)
        else:
            word_dictionary[expected_text] = -1

        if i == 5:
            renew_words()

        display_words()

def renew_words():
    global i, word_dictionary, word_list
    i = 0
    word_list = random.sample(words.words_use, 5)
    word_dictionary = {word: 0 for word in word_list}
    expected_text = word_list[i]
    word_dictionary[expected_text] = -1
    display_words()

def score_calculation():
    global score
    score = score + 1
    score_label = Label(text=f"{score}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
    score_label.grid(column=1, row=5)


expected_text = word_list[i]
word_dictionary[expected_text] = -1
display_words()

word_input_var = tk.StringVar()
word_input = tk.Entry(window, textvariable=word_input_var, width=25, font=("Arial", 16), bg="white")
word_input.grid(column=1, row=3)
word_input.config(state="disabled")

word_input_var.trace("w", update_highlights)

score_indicator_label = Label(text="Your score 👇🏼", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
score_indicator_label.grid(column=1, row=4)

score_label = Label(text=f"{score}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
score_label.grid(column=1, row=5)

time_indicator_label = Label(text="Your time 👇🏼", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
time_indicator_label.grid(column=1, row=0)

stopwatch_time = 60
stopwatch_text = Label(text=f"{stopwatch_time}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
stopwatch_text.grid(column=1, row=1)

def update_stopwatch():
    global stopwatch_time, game_is_on
    if game_is_on == True:
        word_input.config(state="normal")
        if stopwatch_time > 0:
            stopwatch_time -= 1
            stopwatch_text = Label(text=f"{stopwatch_time}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
            stopwatch_text.grid(column=1, row=1)
            window.after(1000, update_stopwatch)
        else:
            stopwatch_text = Label(text="Your time is up!", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
            stopwatch_text.grid(column=1, row=1)
            start_button.config(state="active")
            stop_button.config(state="disabled")
            messagebox.showinfo(title="Info", message=f"Your final score is: {score} words per minute! \n I believe that you can do better!")
            word_input.config(state="disabled")
    else:
        stopwatch_text = Label(text=f"{stopwatch_time}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
        stopwatch_text.grid(column=1, row=1)

def stop_stopwatch():
    global stopwatch_time, game_is_on
    game_is_on = False
    stopwatch_time = 60
    start_button.config(state="active")
    stop_button.config(state="disabled")
    word_input.config(state="disabled")
    score_label = Label(text=f"Score: 0", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
    score_label.grid(column=1, row=5)
    update_stopwatch()

def start_game():
    global game_is_on, stopwatch_time, score
    game_is_on = True
    start_button.config(state="disabled")
    stop_button.config(state="active")
    stopwatch_time = 60  # Starting time for stopwatch (in seconds)
    stopwatch_text = Label(text=f"{stopwatch_time}", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
    score_label = Label(text=f"Score: 0", width=20, height=1, font=("Arial", 14), bg=LIGHT_BLUE)
    score = 0
    score_label.grid(column=1, row=5)
    update_stopwatch()

start_button = Button(text="Start!", command=lambda: start_game())
start_button.grid(column=1, row=6)

stop_button = Button(text="Stop!", command=stop_stopwatch)
stop_button.grid(column=1, row=7)
stop_button.config(state="disabled")



window.mainloop()
