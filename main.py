import os
from tkinter import messagebox, scrolledtext, END
import threading
import customtkinter as ctk

from PIL import Image, ImageTk

from db.database import add_message, init_db

from utils.openai import ask_gpt


class Sidekick(ctk.CTk):
    def __init__(self):
        super().__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "images/sidekick.png")
        # bitmap_path = os.path.join(base_path, "images/sidekick.png")
        self.title("Sidekick")
        self.geometry("600x625")
        self.db = init_db()
        self.full_response = ""
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.logo = Image.open(logo_path)
        self.logo_img = ImageTk.PhotoImage(self.logo)
        self.iconphoto(True, self.logo_img)
        # self.iconbitmap(bitmap_path)

    def create_widgets(self):
        # Fonts
        default_font = ctk.CTkFont(family="Roboto", size=12)
        text_area_font = ctk.CTkFont(family="Roboto", size=14)

        # Input frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")

        # Prompt label
        prompt_label = ctk.CTkLabel(
            input_frame, text="Enter Prompt:", font=default_font
        )
        prompt_label.pack(side="left", padx=10)

        # Prompt entry
        self.prompt_entry = ctk.CTkEntry(input_frame, width=200)
        self.prompt_entry.pack(side="left", expand=True, fill="x", padx=10)
        self.prompt_entry.bind("<Return>", self.generate_text)

        # Generate button
        generate_button = ctk.CTkButton(
            input_frame, text="Generate", command=self.generate_text, font=default_font
        )
        generate_button.pack(side="left", padx=10)

        # Text area
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap="word",
            font=text_area_font,
        )
        self.text_area.pack(pady=10, padx=20, expand=True, fill="both")

        # Settings frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=10, padx=20, fill="x")

        # Model dropdown
        model_label = ctk.CTkLabel(settings_frame, text="Model:", font=default_font)
        model_label.pack(side="left", padx=10)

        self.model_dropdown = ctk.CTkComboBox(
            settings_frame,
            values=["GPT 3.5 Turbo", "GPT 4", "GPT 4 Turbo", "GPT 4o"],
            font=default_font,
        )
        self.model_dropdown.set("GPT 3.5 Turbo")
        self.model_dropdown.pack(side="left", padx=10)

        # Temperature slider
        temp_label = ctk.CTkLabel(
            settings_frame, text="Temperature:", font=default_font
        )
        temp_label.pack(side="left", padx=10)

        self.temp_slider = ctk.CTkSlider(
            settings_frame, from_=0, to=1, number_of_steps=100
        )
        self.temp_slider.set(0.2)
        self.temp_slider.pack(side="left", padx=10)

    def generate_text(self, event=None):
        if not self.prompt_entry.get():
            return

        if self.full_response:
            self.save_to_db("assistant", self.full_response)
            self.full_response = ""

        # Just adding a new line to the text area here for now
        self.text_area.insert(END, "\n")
        prompt = self.prompt_entry.get()
        model = self.model_dropdown.get()
        temperature = self.temp_slider.get()

        def process_response(response):
            self.full_response += response
            self.text_area.insert(END, response)
            self.text_area.see(END)

        def do_generate():
            self.save_to_db("user", prompt)
            response = ask_gpt(model, temperature)
            for chunk in response:
                if chunk.choices[0].delta.content is not None:
                    threading.Thread(
                        target=process_response, args=(chunk.choices[0].delta.content,)
                    ).start()

        threading.Thread(target=do_generate).start()

    def save_to_db(self, role, question):
        if self.full_response and role == "assistant":
            add_message(role, question)
            self.full_response = ""

        if role == "user":
            add_message(role, question)
            self.prompt_entry.delete(0, END)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if self.full_response != "":
                self.save_to_db("assistant", self.full_response)
            self.destroy()


if __name__ == "__main__":
    app = Sidekick()
    app.mainloop()
