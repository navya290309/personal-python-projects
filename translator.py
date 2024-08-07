#copy the code and paste it in you compiler or you can download the raw file by clicking the download symbol in top right corner
#make sure you have downloaded googletrans==3.1.0a0 pyperclip gTTS pygame 
#to avoid any error use : pip install googletrans==3.1.0a0 pyperclip gTTS pygame

import tkinter as tk
from tkinter import ttk
from googletrans import Translator, LANGUAGES
import pyperclip
from gtts import gTTS
import pygame
import os
import tempfile

LANGUAGE_TO_CODE = {v: k for k, v in LANGUAGES.items()}

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    src_lang = src_lang_var.get()
    dest_lang = dest_lang_var.get()
    
    translator = Translator()
    translated = translator.translate(text, src=src_lang, dest=dest_lang)
    
    output_text.config(state='normal')  # Temporarily enable the widget
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, translated.text)
    output_text.config(state='disabled')  # Disable the widget again

def swap_languages():
    src_lang = src_lang_var.get()
    dest_lang = dest_lang_var.get()
    
    src_lang_var.set(dest_lang)
    dest_lang_var.set(src_lang)

    translated_text = output_text.get("1.0", tk.END).strip()
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, translated_text)

    output_text.config(state='normal')  # Temporarily enable the widget
    output_text.delete("1.0", tk.END)
    output_text.config(state='disabled')  # Disable the widget again

def search_language(event, combobox):
    value = event.widget.get()
    if value == '':
        combobox['values'] = list(LANGUAGES.values())
    else:
        data = []
        for item in LANGUAGES.values():
            if value.lower() in item.lower():
                data.append(item)
        combobox['values'] = data

def copy_translation():
    translated_text = output_text.get("1.0", tk.END).strip()
    pyperclip.copy(translated_text)

def paste_to_input():
    clipboard_text = pyperclip.paste()
    input_text.delete("1.0", tk.END)
    input_text.insert(tk.END, clipboard_text)

def play_translated_audio():
    translated_text = output_text.get("1.0", tk.END).strip()
    dest_lang_full = dest_lang_var.get()
    
    if translated_text:
        # Get the language code from the full language name
        lang_code = LANGUAGE_TO_CODE.get(dest_lang_full, 'en')
        
        try:
            tts = gTTS(text=translated_text, lang=lang_code)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tf:
                temp_file = tf.name
            
            tts.save(temp_file)
            
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file)
            pygame.mixer.music.play()
            
            # Wait for the audio to finish playing
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            
            pygame.mixer.quit()
            os.remove(temp_file)
        except ValueError as e:
            print(f"Error: {e}. Using English as fallback.")
            # Fallback to English if the language is not supported
            tts = gTTS(text=translated_text, lang='en')
            # ... (rest of the code remains the same)

# Create the main window
root = tk.Tk()
root.title("Language Translator")
root.geometry("600x550")
root.configure(bg='#E6F3FF')

# Create and place widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
frame.configure(style='TFrame')

# Create a style
style = ttk.Style()
style.configure('TFrame', background='#E6F3FF')
style.configure('TLabel', background='#E6F3FF')
style.configure('TButton', background='#E6F3FF')

# Input text area
input_label = ttk.Label(frame, text="Enter text to translate:")
input_label.grid(row=0, column=0, columnspan=2, sticky=tk.W)
input_text = tk.Text(frame, height=10, width=60)
input_text.grid(row=1, column=0, columnspan=2)

# Paste button
paste_button = ttk.Button(frame, text="Paste", command=paste_to_input)
paste_button.grid(row=0, column=2, sticky=tk.E)

# Source language dropdown
src_lang_label = ttk.Label(frame, text="From:")
src_lang_label.grid(row=2, column=0, sticky=tk.W)
src_lang_var = tk.StringVar()
src_lang_dropdown = ttk.Combobox(frame, textvariable=src_lang_var, values=list(LANGUAGES.values()))
src_lang_dropdown.grid(row=2, column=1, sticky=(tk.W, tk.E))
src_lang_dropdown.set("auto")
src_lang_dropdown.bind('<KeyRelease>', lambda event: search_language(event, src_lang_dropdown))

# Swap button
swap_button = ttk.Button(frame, text="Swap Languages", command=swap_languages)
swap_button.grid(row=2, column=2, rowspan=2, padx=(5, 0), pady=5)

# Destination language dropdown
dest_lang_label = ttk.Label(frame, text="To:")
dest_lang_label.grid(row=3, column=0, sticky=tk.W)
dest_lang_var = tk.StringVar()
dest_lang_dropdown = ttk.Combobox(frame, textvariable=dest_lang_var, values=list(LANGUAGES.values()))
dest_lang_dropdown.grid(row=3, column=1, sticky=(tk.W, tk.E))
dest_lang_dropdown.set("english")
dest_lang_dropdown.bind('<KeyRelease>', lambda event: search_language(event, dest_lang_dropdown))

# Translate button
translate_button = ttk.Button(frame, text="Translate", command=translate_text)
translate_button.grid(row=4, column=0, columnspan=3, pady=(10, 0))

# Output text area
output_label = ttk.Label(frame, text="Translation:")
output_label.grid(row=5, column=0, columnspan=2, sticky=tk.W)
output_text = tk.Text(frame, height=10, width=60, state='disabled')
output_text.grid(row=6, column=0, columnspan=2)

# Copy button
copy_button = ttk.Button(frame, text="Copy", command=copy_translation)
copy_button.grid(row=5, column=2, sticky=tk.E)

# Play button
play_button = ttk.Button(frame, text="Play", command=play_translated_audio)
play_button.grid(row=6, column=2, sticky=(tk.N, tk.E))

# Configure grid to expand with window
root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(6, weight=1)

# Start the GUI event loop
root.mainloop()
