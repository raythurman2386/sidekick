import os
import threading
import json
from tkinter import messagebox, scrolledtext, END
import customtkinter as ctk
from PIL import Image, ImageTk

from src.config.logging_config import CURRENT_LOGGING_CONFIG
from src.db.database import init_db, add_message
from src.utils.logger import setup_logger
from src.utils.ollama import generate_chat_completion, list_models, install_model

logger = setup_logger(
    "sidekick",
    log_level=CURRENT_LOGGING_CONFIG["log_level"],
    log_dir=CURRENT_LOGGING_CONFIG["log_dir"],
)


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Settings")
        self.geometry("600x500")

        # Make window modal
        self.transient(parent)
        self.grab_set()

        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Initialize state
        self.installing = False

        self.create_widgets()

        # Center the window
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - self.winfo_width()) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{x}+{y}")

        # Bind close event
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        # Fonts
        title_font = ctk.CTkFont(family="Roboto", size=24, weight="bold")
        section_font = ctk.CTkFont(family="Roboto", size=16, weight="bold")
        default_font = ctk.CTkFont(family="Roboto", size=13)

        # Main container
        container = ctk.CTkFrame(self)
        container.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        container.grid_columnconfigure(0, weight=1)

        # Title
        title_label = ctk.CTkLabel(container, text="Sidekick Settings", font=title_font)
        title_label.grid(row=0, column=0, pady=(0, 20), sticky="w")

        # Model Installation Section
        install_frame = ctk.CTkFrame(container)
        install_frame.grid(row=1, column=0, pady=(0, 20), sticky="ew")
        install_frame.grid_columnconfigure(1, weight=1)

        # Section header with icon
        header_frame = ctk.CTkFrame(install_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=3, pady=(15, 20), padx=15, sticky="w")

        ctk.CTkLabel(header_frame, text="⬇️", font=("Segoe UI Emoji", 16)).grid(
            row=0, column=0, padx=(0, 10)
        )
        ctk.CTkLabel(header_frame, text="Install New Model", font=section_font).grid(
            row=0, column=1
        )

        # Model entry and install button
        ctk.CTkLabel(install_frame, text="Model Name:", font=default_font).grid(
            row=1, column=0, padx=(15, 10), pady=(0, 5), sticky="w"
        )
        self.model_entry = ctk.CTkEntry(
            install_frame, font=default_font, placeholder_text="e.g., phi:latest", height=32
        )
        self.model_entry.grid(row=1, column=1, padx=(0, 10), pady=(0, 5), sticky="ew")

        self.install_button = ctk.CTkButton(
            install_frame,
            text="Install Model",
            font=default_font,
            command=self.install_model,
            height=32,
            width=120,
        )
        self.install_button.grid(row=1, column=2, padx=(0, 15), pady=(0, 5))

        self.progress_label = ctk.CTkLabel(install_frame, text="", font=default_font)
        self.progress_label.grid(row=2, column=0, columnspan=3, padx=15, pady=(5, 15), sticky="w")

        # Model Settings Section
        settings_frame = ctk.CTkFrame(container)
        settings_frame.grid(row=2, column=0, pady=(0, 20), sticky="ew")
        settings_frame.grid_columnconfigure(1, weight=1)

        # Section header with icon
        header_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        header_frame.grid(row=0, column=0, columnspan=2, pady=(15, 20), padx=15, sticky="w")

        ctk.CTkLabel(header_frame, text="⚙️", font=("Segoe UI Emoji", 16)).grid(
            row=0, column=0, padx=(0, 10)
        )
        ctk.CTkLabel(header_frame, text="Model Configuration", font=section_font).grid(
            row=0, column=1
        )

        # Active model selection
        ctk.CTkLabel(settings_frame, text="Active Model:", font=default_font).grid(
            row=1, column=0, padx=(15, 10), pady=(0, 15), sticky="w"
        )
        self.model_dropdown = ctk.CTkComboBox(
            settings_frame,
            values=self.parent.available_models,
            font=default_font,
            height=32,
            width=250,
            dropdown_font=default_font,
        )
        self.model_dropdown.set(self.parent.model_dropdown.get())
        self.model_dropdown.grid(row=1, column=1, padx=(0, 15), pady=(0, 15), sticky="ew")

        # Temperature control
        ctk.CTkLabel(settings_frame, text="Temperature:", font=default_font).grid(
            row=2, column=0, padx=(15, 10), pady=(0, 15), sticky="w"
        )

        temp_control_frame = ctk.CTkFrame(settings_frame)
        temp_control_frame.grid(row=2, column=1, padx=(0, 15), pady=(0, 15), sticky="ew")
        temp_control_frame.grid_columnconfigure(0, weight=1)

        self.temp_slider = ctk.CTkSlider(temp_control_frame, from_=0, to=1, number_of_steps=100)
        self.temp_slider.set(self.parent.temp_slider.get())
        self.temp_slider.grid(row=0, column=0, padx=(0, 10), sticky="ew")

        self.temp_value_label = ctk.CTkLabel(
            temp_control_frame,
            text=f"{self.parent.temp_slider.get():.1f}",
            font=default_font,
            width=40,
        )
        self.temp_value_label.grid(row=0, column=1)
        self.temp_slider.configure(command=self.update_temp_label)

        # Save button at the bottom
        self.save_button = ctk.CTkButton(
            container,
            text="Save Changes",
            font=default_font,
            command=self.save_and_close,
            height=36,
            width=160,
        )
        self.save_button.grid(row=3, column=0, pady=(10, 0), sticky="ew")

    def update_temp_label(self, value):
        self.temp_value_label.configure(text=f"{float(value):.1f}")

    def install_model(self):
        if self.installing:
            logger.debug("Model installation already in progress")
            return

        model_name = self.model_entry.get().strip()
        if not model_name:
            logger.warning("Attempted to install model with empty name")
            messagebox.showerror("Error", "Please enter a model name")
            return

        def update_progress(status):
            logger.info(f"Model installation progress: {status}")
            self.progress_label.configure(text=status)

        def install_thread():
            self.installing = True
            logger.info(f"Starting installation of model: {model_name}")
            self.install_button.configure(state="disabled")
            self.model_entry.configure(state="disabled")
            self.save_button.configure(state="disabled")

            success = install_model(model_name, update_progress)

            self.installing = False
            self.install_button.configure(state="normal")
            self.model_entry.configure(state="normal")
            self.save_button.configure(state="normal")

            if success:
                logger.info(f"Successfully installed model: {model_name}")
                self.progress_label.configure(text=f"Successfully installed {model_name}")
                self.model_entry.delete(0, END)
                # Refresh the model list in the main thread
                self.after(0, self.parent.refresh_model_list)
                self.after(0, self.refresh_model_dropdown)
            else:
                logger.error(f"Failed to install model: {model_name}")
                self.progress_label.configure(text="Installation failed")

        thread = threading.Thread(target=install_thread)
        thread.start()

    def refresh_model_dropdown(self):
        current_model = self.model_dropdown.get()
        self.model_dropdown.configure(values=self.parent.available_models)
        if current_model in self.parent.available_models:
            self.model_dropdown.set(current_model)
        else:
            self.model_dropdown.set(self.parent.available_models[0])

    def save_and_close(self):
        if not self.installing:
            self.parent.model_dropdown.set(self.model_dropdown.get())
            self.parent.temp_slider.set(self.temp_slider.get())
            self.destroy()

    def on_close(self):
        if not self.installing:
            self.destroy()


class Sidekick(ctk.CTk):
    def __init__(self):
        super().__init__()
        logger.info("Initializing Sidekick AI Assistant")
        base_path = os.path.dirname(os.path.abspath(__file__))
        logo_path = os.path.join(base_path, "images/sidekick.png")

        self.title("Sidekick AI Assistant")
        self.geometry("900x700")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.db = init_db()
        self.full_response = ""
        self.is_generating = False
        self.settings_window = None

        self.logo = Image.open(logo_path)
        self.logo_img = ImageTk.PhotoImage(self.logo)
        self.iconphoto(True, self.logo_img)

        # Initialize model settings
        self.available_models = list_models() or ["deepseek-r1:latest"]
        logger.info(f"Available models: {self.available_models}")
        self.model_dropdown = ctk.CTkComboBox(self, values=self.available_models)
        self.model_dropdown.set(self.available_models[0])
        self.temp_slider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=100)
        self.temp_slider.set(0.4)

        self.create_widgets()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        # Configure fonts
        title_font = ctk.CTkFont(family="Roboto", size=24, weight="bold")
        default_font = ctk.CTkFont(family="Roboto", size=13)
        text_area_font = ctk.CTkFont(family="Roboto", size=14)

        # Title and Settings Bar
        top_frame = ctk.CTkFrame(self)
        top_frame.grid(row=0, column=0, padx=20, pady=(20, 0), sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)

        # Title with logo
        title_label = ctk.CTkLabel(top_frame, text="Sidekick AI Assistant", font=title_font)
        title_label.grid(row=0, column=0, sticky="w", padx=10)

        # Settings button
        settings_button = ctk.CTkButton(
            top_frame,
            text="⚙️ Settings",
            font=default_font,
            command=self.open_settings,
            width=120,
            height=32,
        )
        settings_button.grid(row=0, column=1, padx=10)

        # Input Section
        input_frame = ctk.CTkFrame(self)
        input_frame.grid(row=1, column=0, padx=20, pady=20, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        # Prompt entry with label
        prompt_label = ctk.CTkLabel(input_frame, text="Your Message:", font=default_font)
        prompt_label.grid(row=0, column=0, padx=(15, 10), sticky="w")

        self.prompt_entry = ctk.CTkEntry(input_frame, font=default_font, height=35)
        self.prompt_entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")
        self.prompt_entry.bind("<Return>", self.generate_text)

        # Button frame
        button_frame = ctk.CTkFrame(input_frame)
        button_frame.grid(row=0, column=2, padx=(0, 15))

        # Generate button
        self.generate_button = ctk.CTkButton(
            button_frame,
            text="Send Message",
            command=self.generate_text,
            font=default_font,
            width=120,
            height=32,
        )
        self.generate_button.grid(row=0, column=0, padx=(0, 10))

        # Stop button
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop",
            command=self.stop_generation,
            font=default_font,
            width=80,
            height=32,
            state="disabled",
            fg_color="#E74C3C",
            hover_color="#C0392B",
        )
        self.stop_button.grid(row=0, column=1)

        # Chat Area
        chat_frame = ctk.CTkFrame(self)
        chat_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)

        self.text_area = scrolledtext.ScrolledText(
            chat_frame, wrap="word", font=text_area_font, borderwidth=0, highlightthickness=0
        )
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    def open_settings(self):
        logger.debug("Opening settings window")
        if self.settings_window is None or not ctk.CTkToplevel.winfo_exists(self.settings_window):
            self.settings_window = SettingsWindow(self)
        else:
            self.settings_window.focus()

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
                messages, self.model_dropdown.get(), self.temp_slider.get()
            )

            for line in response.iter_lines():
                if not self.is_generating:
                    break
                if line:
                    try:
                        decoded_line = line.decode("utf-8")
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
        if self.is_generating:
            logger.info("Stopping text generation")
            self.is_generating = False
            return

        prompt = self.prompt_entry.get().strip()
        if not prompt:
            logger.warning("Attempted to generate text with empty prompt")
            return

        self.is_generating = True
        self.generate_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.prompt_entry.delete(0, END)

        logger.info(f"Starting text generation with model: {self.model_dropdown.get()}")
        
        def generate():
            try:
                response_generator = generate_chat_completion(
                    [{"role": "user", "content": prompt}],
                    self.model_dropdown.get(),
                    self.temp_slider.get()
                )

                self.text_area.insert(END, f"\nYou: {prompt}\nAssistant: ")
                self.text_area.see(END)

                full_response = ""
                for chunk in response_generator:
                    if not self.is_generating:
                        logger.info("Text generation stopped by user")
                        break
                    
                    if chunk:
                        # Update UI with the new chunk
                        self.text_area.insert(END, chunk)
                        self.text_area.see(END)
                        full_response += chunk

                if self.is_generating:  # Only save if not stopped
                    logger.debug("Saving conversation to database")
                    add_message("user", prompt)
                    add_message("assistant", full_response)

            except Exception as e:
                logger.error(f"Error during text generation: {str(e)}", exc_info=True)
                self.text_area.insert(END, f"\nError: {str(e)}\n")
                self.text_area.see(END)
            finally:
                self.is_generating = False
                self.generate_button.configure(state="normal")
                self.stop_button.configure(state="disabled")

        thread = threading.Thread(target=generate)
        thread.start()

    def refresh_model_list(self):
        """Refresh the list of available models in the dropdown"""
        logger.debug("Refreshing model list")
        self.available_models = list_models() or ["deepseek-r1:latest"]
        self.model_dropdown.configure(values=self.available_models)
        
        # Keep the current selection if it still exists, otherwise select the first model
        current_model = self.model_dropdown.get()
        if current_model not in self.available_models:
            logger.info(f"Previously selected model {current_model} no longer available, switching to {self.available_models[0]}")
            self.model_dropdown.set(self.available_models[0])
            
        # Update settings window if it's open
        if self.settings_window and ctk.CTkToplevel.winfo_exists(self.settings_window):
            self.settings_window.refresh_model_dropdown()

    def stop_generation(self):
        """Stop the current text generation"""
        self.is_generating = False
        if hasattr(self, "generator_thread") and self.generator_thread.is_alive():
            self.generator_thread.join(timeout=1.0)
        self.cleanup_generation()

    def save_to_db(self, role, content):
        """Save message to database"""
        add_message(role, content)

    def on_closing(self):
        logger.info("Shutting down Sidekick AI Assistant")
        self.destroy()


if __name__ == "__main__":
    app = Sidekick()
    app.mainloop()
