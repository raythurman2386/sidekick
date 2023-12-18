import customtkinter as ctk
from tkinter import scrolledtext, END
from db.database import init_db

from utils.openai import ask_gpt

# Function to handle the 'Generate' button click
def on_generate_click():
    prompt = prompt_entry.get()
    model = model_dropdown.get()
    temperature = temperature_slider.get()
    response = ask_gpt(prompt, model, temperature)
    # You would add your logic here to use the prompt, model, and temperature
    # to generate text and stream it back to the text_area.
    # For demonstration purposes, we'll just echo the input.
    text_area.insert(END, f"Prompt: {prompt}\nModel: {model}\nTemperature: {temperature}\n\nResponse:\n{response}\n\n")

# Main window
root = ctk.CTk()
root.title("AI Text Generator")
root.geometry("600x625")
init_db()
# Input frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=20, padx=20, fill='x')

# Prompt input
prompt_label = ctk.CTkLabel(input_frame, text="Enter Prompt:")
prompt_label.pack(side='left', padx=10)
prompt_entry = ctk.CTkEntry(input_frame, width=200)
prompt_entry.pack(side='left', expand=True, fill='x')

# Generate button
generate_button = ctk.CTkButton(input_frame, text="Generate", command=on_generate_click)
generate_button.pack(side='left', padx=10)

# Text area for output
text_area = scrolledtext.ScrolledText(root, wrap='word')
text_area.pack(pady=10, padx=20, expand=True, fill='both')

# Settings panel
settings_panel = ctk.CTkFrame(root)
settings_panel.pack(pady=10, padx=20, fill='x')

# Model dropdown
model_label = ctk.CTkLabel(settings_panel, text="Model:")
model_label.pack(side='left', padx=10)
model_dropdown = ctk.CTkComboBox(settings_panel, values=["GPT 3.5 Turbo", "GPT 4", "GPT 4 Turbo"])
model_dropdown.set("GPT 3.5 Turbo")
model_dropdown.pack(side='left', padx=10)

# Temperature slider
temperature_label = ctk.CTkLabel(settings_panel, text="Temperature:")
temperature_label.pack(side='left', padx=10)
temperature_slider = ctk.CTkSlider(settings_panel, number_of_steps=100)
temperature_slider.set(0.2)
temperature_slider.pack(side='left', padx=10)

# Run the application
root.mainloop()