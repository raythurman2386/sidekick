from tkinter import scrolledtext, END
import customtkinter as ctk

from db.database import init_db
import threading

from utils.openai import ask_gpt


def handle_response(response):
    text_area.insert(END, response)
    text_area.see(END)  # scroll to end


# Function to handle the 'Generate' button click
def on_generate_click():
    prompt = prompt_entry.get()
    model = model_dropdown.get()
    temperature = temperature_slider.get()
    prompt_entry.delete(0, "end")

    def do_generate():
        response = ask_gpt(prompt, model, temperature)
        
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                threading.Thread(target=handle_response, args=(chunk.choices[0].delta.content,)).start()

    threading.Thread(target=do_generate).start()


# Main window
root = ctk.CTk()
root.title("AI Text Generator")
root.geometry("600x625")

default_font = ctk.CTkFont(family="Roboto", size=12)
text_area_font = ctk.CTkFont(family="Roboto", size=14)

# Input frame
input_frame = ctk.CTkFrame(root)
input_frame.pack(pady=20, padx=20, fill="x")

# Prompt input
prompt_label = ctk.CTkLabel(input_frame, text="Enter Prompt:", font=default_font)
prompt_label.pack(side="left", padx=10)
prompt_entry = ctk.CTkEntry(input_frame, width=200)
prompt_entry.pack(side="left", expand=True, fill="x")

# Generate button
generate_button = ctk.CTkButton(
    input_frame, text="Generate", command=on_generate_click, font=default_font
)
generate_button.pack(side="left", padx=10)

# Text area for output
text_area = scrolledtext.ScrolledText(root, wrap="word", font=text_area_font)
text_area.pack(pady=10, padx=20, expand=True, fill="both")

# Settings panel
settings_panel = ctk.CTkFrame(root)
settings_panel.pack(pady=10, padx=20, fill="x")

# Model dropdown
model_label = ctk.CTkLabel(settings_panel, text="Model:", font=default_font)
model_label.pack(side="left", padx=10)
model_dropdown = ctk.CTkComboBox(
    settings_panel, values=["GPT 3.5 Turbo", "GPT 4", "GPT 4 Turbo"], font=default_font
)
model_dropdown.set("GPT 3.5 Turbo")
model_dropdown.pack(side="left", padx=10)

# Temperature slider
temperature_label = ctk.CTkLabel(settings_panel, text="Temperature:", font=default_font)
temperature_label.pack(side="left", padx=10)
temperature_slider = ctk.CTkSlider(settings_panel, number_of_steps=100)
temperature_slider.set(0.2)
temperature_slider.pack(side="left", padx=10)

# Run the application
if __name__ == "__main__":
    init_db()
    root.mainloop()
