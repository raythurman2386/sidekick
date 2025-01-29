import os
import threading
import json
from tkinter import messagebox, scrolledtext, END
import customtkinter as ctk
from PIL import Image, ImageTk

from db.database import add_message, init_db
from utils.ollama import generate_chat_completion, list_models


class Sidekick(ctk.CTk):
    def __init__(self):
        super().__init__()
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "images/sidekick.png")
        
        self.title("Sidekick AI Assistant")
        self.geometry("800x700")
        self.db = init_db()
        self.full_response = ""
        self.is_generating = False
        
        self.logo = Image.open(logo_path)
        self.logo_img = ImageTk.PhotoImage(self.logo)
        self.iconphoto(True, self.logo_img)
        
        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Configure fonts
        default_font = ctk.CTkFont(family="Roboto", size=12)
        text_area_font = ctk.CTkFont(family="Roboto", size=14)
        
        # Input frame
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        # Prompt label and entry
        prompt_label = ctk.CTkLabel(input_frame, text="Enter Prompt:", font=default_font)
        prompt_label.pack(side="left", padx=10)
        
        self.prompt_entry = ctk.CTkEntry(input_frame, width=200, font=default_font)
        self.prompt_entry.pack(side="left", expand=True, fill="x", padx=10)
        self.prompt_entry.bind("<Return>", self.generate_text)
        
        # Generate button
        self.generate_button = ctk.CTkButton(
            input_frame,
            text="Generate",
            command=self.generate_text,
            font=default_font,
            width=100
        )
        self.generate_button.pack(side="left", padx=10)
        
        # Stop button
        self.stop_button = ctk.CTkButton(
            input_frame,
            text="Stop",
            command=self.stop_generation,
            font=default_font,
            width=100,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=10)
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(
            self,
            wrap="word",
            font=text_area_font,
            height=20
        )
        self.text_area.pack(pady=10, padx=20, expand=True, fill="both")
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self)
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        # Model selection
        model_label = ctk.CTkLabel(settings_frame, text="Model:", font=default_font)
        model_label.pack(side="left", padx=10)
        
        self.available_models = list_models() or ["deepseek-r1"]
        self.model_dropdown = ctk.CTkComboBox(
            settings_frame,
            values=self.available_models,
            font=default_font,
        )
        self.model_dropdown.set(self.available_models[0])
        self.model_dropdown.pack(side="left", padx=10)
        
        # Temperature control
        temp_label = ctk.CTkLabel(settings_frame, text="Temperature:", font=default_font)
        temp_label.pack(side="left", padx=10)
        
        self.temp_slider = ctk.CTkSlider(
            settings_frame,
            from_=0,
            to=1,
            number_of_steps=100
        )
        self.temp_slider.set(0.4)
        self.temp_slider.pack(side="left", padx=10, expand=True, fill="x")
        
        self.temp_value_label = ctk.CTkLabel(
            settings_frame,
            text="0.4",
            font=default_font,
            width=30
        )
        self.temp_value_label.pack(side="left", padx=10)
        self.temp_slider.configure(command=self.update_temp_label)

    def update_temp_label(self, value):
        """Update temperature label when slider moves"""
        self.temp_value_label.configure(text=f"{float(value):.1f}")

    def update_text_area(self, content):
        """Safely update the text area from any thread"""
        self.text_area.insert(END, content)
        self.text_area.see(END)
        self.full_response += content

    def generate_in_thread(self, prompt):
        """Handle text generation in a separate thread"""
        try:
            messages = [{"role": "user", "content": prompt}]
            response = generate_chat_completion(
                messages,
                self.model_dropdown.get(),
                self.temp_slider.get()
            )
            
            for line in response.iter_lines():
                if not self.is_generating:
                    break
                if line:
                    try:
                        decoded_line = line.decode('utf-8')
                        content = json.loads(decoded_line)["message"]["content"]
                        # Schedule UI update in the main thread
                        self.after(0, self.update_text_area, content)
                    except Exception as e:
                        print(f"Error processing line: {e}")
        except Exception as e:
            self.after(0, messagebox.showerror, "Error", f"An error occurred: {str(e)}")
        finally:
            self.after(0, self.cleanup_generation)

    def cleanup_generation(self):
        """Clean up after generation is complete"""
        self.is_generating = False
        self.generate_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.prompt_entry.delete(0, END)

    def generate_text(self, event=None):
        """Handle text generation"""
        if not self.prompt_entry.get() or self.is_generating:
            return
            
        self.is_generating = True
        self.generate_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        if self.full_response:
            self.save_to_db("assistant", self.full_response)
            self.full_response = ""
        
        self.text_area.insert(END, "\n\n")
        prompt = self.prompt_entry.get()
        self.save_to_db("user", prompt)
        
        # Start generation in a separate thread
        self.generator_thread = threading.Thread(target=self.generate_in_thread, args=(prompt,))
        self.generator_thread.daemon = True
        self.generator_thread.start()

    def stop_generation(self):
        """Stop the current text generation"""
        self.is_generating = False
        if hasattr(self, 'generator_thread') and self.generator_thread.is_alive():
            self.generator_thread.join(timeout=1.0)
        self.cleanup_generation()

    def save_to_db(self, role, content):
        """Save message to database"""
        add_message(role, content)

    def on_closing(self):
        """Handle window closing"""
        if self.is_generating:
            self.stop_generation()
        self.quit()


if __name__ == "__main__":
    app = Sidekick()
    app.mainloop()
