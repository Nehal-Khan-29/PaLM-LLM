import tkinter as tk
from tkinter import ttk as ttk
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk,Image
import google.generativeai as palm
import webbrowser
import clipboard



def open_url1():
    webbrowser.open_new("https://aistudio.google.com/app/apikey")
def open_url2():
    webbrowser.open_new("https://ai.google.dev/palm_docs")


def api_page_func():
    global api_entry, api_page
    api_page = tk.Tk()
    api_page.geometry('400x200')
    api_page.title('PaLM LLM - API Key')
    api_page.config(bg='black')
    api_page.iconbitmap("Icon.ico")

    Label(api_page, text="Enter API Key", font=("italic_iv50", 12)).place(relx=0.5, rely=0.3, anchor=CENTER)
    api_entry = Entry(api_page)
    api_entry.place(relx=0.5, rely=0.4, anchor=CENTER, width=250)

    link_label = Label(api_page, text="Get API Key CLICK HERE", font=("italic_iv50", 10), bg='black',fg='blue', cursor="hand2")
    link_label.place(relx=0.5, rely=0.6, anchor=CENTER, height=20)
    link_label.bind("<Button-1>", lambda event: open_url1())    
    
    link_label = Label(api_page, text="Documentation: ai.google.dev/palm_docs", font=("italic_iv50", 10), bg='black',fg='blue', cursor="hand2")
    link_label.place(relx=0.5, rely=0.7, anchor=CENTER, height=20)
    link_label.bind("<Button-1>", lambda event: open_url2())  
    
    Button(api_page, text="Enter Key", font=("italic_iv50", 10), command=check_api_key).place(relx=0.5, rely=0.9, anchor=CENTER)
    
    screen_width = api_page.winfo_screenwidth()
    screen_height = api_page.winfo_screenheight()
    window_width = 400  
    window_height = 200
    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    api_page.geometry("+{}+{}".format(x, y))
    
    api_page.mainloop()


def check_api_key():
    api_key = api_entry.get()

    if not api_key:
        messagebox.showerror("Error", "Please enter API key.")
    else:
        try:
            palm.configure(api_key=api_key)
            models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
            if not models:
                messagebox.showerror("Error", "No models available.")
            else:
                api_page.destroy()
                prompt_page_func()
        except Exception as e:
            messagebox.showerror("Error", f"Invalid API key")


def prompt_page_func():
    global prompt_text_widget1,prompt_text_widget2

    prompt_page = tk.Tk()
    prompt_page.geometry('1000x700')
    prompt_page.title('PaLM LLM - Prompt Page')
    prompt_page.state('zoomed')
    prompt_page.iconbitmap("Icon.ico")
    prompt_pagepic=ImageTk.PhotoImage(Image.open("BG.png"))
    prompt_pagepicpanel=Label(prompt_page,image=prompt_pagepic)
    prompt_pagepicpanel.pack(side='top',fill='both',expand='yes')


    Label(prompt_page, text="Enter Prompt",bg='black',fg='white', font=("italic_iv50", 12)).place(relx=0.4, rely=0.07, anchor=CENTER)

    prompt_text_widget1 = Text(prompt_page, wrap=WORD, width=80, height=8.5, font=("italic_iv50", 10))
    prompt_text_widget1.place(relx=0.4, rely=0.21, anchor=CENTER)
    
    prompt_text_widget2 = Text(prompt_page, wrap=WORD, width=80, height=23,bg='black',fg='white', font=("italic_iv50", 10))
    prompt_text_widget2.place(relx=0.4, rely=0.61, anchor=CENTER)
    prompt_text_widget2.config(state=DISABLED)
    
    generate_button = Button(prompt_page, text="Generate Text", font=("italic_iv50", 12), command=generate_text)
    generate_button.place(relx=0.8, rely=0.4, anchor=CENTER)

    copy_button = Button(prompt_page, text="Copy Promt", font=("italic_iv50", 12), command=copy_text)
    copy_button.place(relx=0.8, rely=0.5, anchor=CENTER)
    
    copy_button = Button(prompt_page, text="Delete Promt", font=("italic_iv50", 12), command=clear_text)
    copy_button.place(relx=0.8, rely=0.6, anchor=CENTER)


    prompt_page.mainloop()


def generate_text():
    
    prompt_text = prompt_text_widget1.get("1.0", "end-1c")

    if not prompt_text.strip():
        messagebox.showerror("Error", "Please enter prompt text.")
    else:
        models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
        if not models:
            messagebox.showerror("Error", "No models available.")
        else:
            model = models[0].name
            completion = palm.generate_text(model=model, prompt=prompt_text, temperature=1)

            if completion.result:
                prompt_text_widget2.config(state=NORMAL)
                prompt_text_widget2.delete("1.0", END)
                generated_text = completion.result
                prompt_text_widget2.insert(END,generated_text)
                prompt_text_widget2.config(state=DISABLED)
                with open('Prompt_file.txt', 'a') as f:
                    prompt_text = "\n\n===================== NEW PROMT =====================\n\n" + prompt_text
                    f.write(prompt_text + '\n')
                    
                with open('Result_file.txt', 'a') as f:
                    result = "\n\n===================== NEW PROMT =====================\n\n" + completion.result
                    f.write(result + '\n')
    
            else:
                messagebox.showerror("Error", f"Error generating text")


def copy_text():
    text_to_copy = prompt_text_widget2.get("1.0", END)
    clipboard.copy(text_to_copy)
def clear_text():
    prompt_text_widget1.delete("1.0", END)
    prompt_text_widget2.config(state=NORMAL)
    prompt_text_widget2.delete("1.0", END)
    prompt_text_widget2.config(state=DISABLED)
    
   
icon = tk.Tk()
icon.title('PaLM LLM')
icon.iconbitmap("Icon.ico")
image = Image.open("Front.png")
tk_image = ImageTk.PhotoImage(image)
image_label = tk.Label(icon, image=tk_image)
image_label.pack()
icon.update()
screen_width = icon.winfo_screenwidth()
screen_height = icon.winfo_screenheight()
window_width = 432  
window_height = 171
x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)
icon.geometry("+{}+{}".format(x, y))
icon.after(2000, icon.destroy)
icon.mainloop()

api_page_func()

