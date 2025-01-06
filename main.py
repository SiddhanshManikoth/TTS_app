from tkinter import filedialog,PhotoImage
import PyPDF2
from pyht import Client
from dotenv import load_dotenv
from pyht.client import TTSOptions
from betterplaysound import playsound
import os
from PIL import Image, ImageTk
load_dotenv()


import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

window = tk.Tk()
window.title("TTS app")
window.geometry("300x400")
window.config(padx=50, pady=50)

pdf_image = Image.open("./image files/pdf.png")
resize_pdf_image = pdf_image.resize((50, 50))
pdf_img = ImageTk.PhotoImage(resize_pdf_image)
check_image =  Image.open("./image files/check.png")
resize_check_image = check_image.resize((50, 50))
check_img = ImageTk.PhotoImage(resize_check_image)
mp3_image =  Image.open("./image files/mp3_img.png")
resize_mp3_image = mp3_image.resize((50, 50))
mp3_img = ImageTk.PhotoImage(resize_mp3_image)
def play():
    playsound("./audio files/output_jenn.wav")

def pdf_to_text(pdf_path, output_txt):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize an empty string to store the text
        text = ''

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()

    # Write the extracted text to a text file
    with open(output_txt, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def select_PDF():
    filename = filedialog.askopenfilename(initialdir = "./pdf files",title = "Select file",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
    output_txt = './text files/output.txt'
    pdf_to_text(filename,output_txt)
    print("PDF converted to text successfully!")
    first_step_label.config(text="PDF converted to text successfully!")
    # audio genrator
    client = Client(
        user_id=os.getenv("PLAY_HT_USER_ID"),
        api_key=os.getenv("PLAY_HT_API_KEY"),
    )
    with open("./text files/output.txt") as text_file:
        options = TTSOptions(
            voice="s3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json")
        # Open a file to save the audio
        with open("./audio files/output_jenn.wav", "wb") as audio_file:
            for chunk in client.tts(text_file.read(), options, voice_engine='PlayDialog-http'):
                # Write the audio chunk to the file
                audio_file.write(chunk)

        print("Audio saved as output_jenn.wav")
        second_step_label.config(text="Audio saved as output_jenn.wav")
pdf_label = tk.Label(image=pdf_img)
pdf_label.image = pdf_img
pdf_label.grid(row = 0 ,column = 0)


b1 = ttk.Button(window, text="upload pdf", bootstyle=SUCCESS, command=select_PDF)
b1.grid(row = 1, column = 0  , padx=10 , pady= 10)

first_step_label = tk.Label(text="")
first_step_label.grid(row = 2, column = 0  , padx=10 , pady= 10)

second_step_label = tk.Label(text="")
second_step_label.grid(row = 3, column = 0  , padx=10 , pady= 10)

mp3_label = tk.Label(image=mp3_img)
mp3_label.image = mp3_img
mp3_label.grid(row = 4 ,column = 0)

b2 = ttk.Button(window, text="play audio", bootstyle=SUCCESS, command=play)
b2.grid(row = 5, column = 0  , padx=10 , pady= 10)


window.mainloop()







