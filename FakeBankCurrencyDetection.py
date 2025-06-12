import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR
import tensorflow as tf
tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

import tkinter as tk
from tkinter import Label, Frame, Canvas, Button, filedialog, messagebox, font as tkfont, simpledialog
from PIL import Image, ImageTk, ImageSequence
import requests
from io import BytesIO
import numpy as np
import cv2
import imutils
from keras.models import model_from_json, Sequential
from keras.layers import Convolution2D, MaxPooling2D, Flatten, Dense, Activation, BatchNormalization
import pyttsx3
import random
from twilio.rest import Client

# Twilio configuration
TWILIO_ACCOUNT_SID = ''
TWILIO_AUTH_TOKEN = ''
TWILIO_PHONE_NUMBER = ''
USER_PHONE_NUMBER = ''

# Initialize text-to-speech engine globally
engine = pyttsx3.init()

# Configure voice settings
def configure_voice():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty('rate', 150)

configure_voice()

# Speak message
def speak_message(message):
    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print("Voice error:", e)

# Load and convert image URL to icon
def get_window_icon():
    try:
        response = requests.get("https://cdn.gamma.app/zd5t1lpzqcyw71a/generated-images/77d5CUNucwVjCN5xwE5UP.png")
        img_data = BytesIO(response.content)
        pil_image = Image.open(img_data).resize((64, 64))
        return ImageTk.PhotoImage(pil_image)
    except Exception as e:
        print("Failed to load icon:", e)
        return None

# Custom error box
def custom_error_box(title, message):
    error_win = tk.Toplevel()
    error_win.title(title)
    error_win.geometry("500x200")
    error_win.resizable(False, False)
    error_win.grab_set()

    icon = get_window_icon()
    if icon:
        error_win.iconphoto(False, icon)

    tk.Label(error_win, text=title, font=('Arial', 16, 'bold'), fg='red').pack(pady=(20, 5))
    tk.Label(error_win, text=message, font=('Arial', 13), wraplength=450).pack(pady=(0, 20))
    tk.Button(error_win, text="OK", font=('Arial', 12), command=error_win.destroy).pack()
    error_win.bind('<Return>', lambda e: error_win.destroy())
    error_win.wait_window()

# Send OTP
def send_otp_via_twilio(phone_number, otp):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f'[Created By Arshad Wasib Shaik] Your OTP is: {otp}',
            from_=TWILIO_PHONE_NUMBER,
            to=phone_number
        )
        print(f"OTP sent to {phone_number}")
    except Exception as e:
        print(f"Failed to send OTP: {e}")
        custom_error_box("Error", "Failed to send OTP. Please check your Twilio configuration.")
        exit()

# Generate OTP
def generate_otp():
    return str(random.randint(1000, 9999))

# Maximized dialog input (centered layout) with black background
def maximized_askstring(title, prompt):
    dialog = tk.Toplevel()
    dialog.title(title)
    dialog.state('zoomed')
    dialog.configure(bg='black')  # Set background color to black
    dialog.grab_set()

    icon = get_window_icon()
    if icon:
        dialog.iconphoto(False, icon)

    outer_frame = tk.Frame(dialog)  
    outer_frame.place(relx=0.5, rely=0.5, anchor='center')

    prompt_label = tk.Label(
        outer_frame,
        text=prompt,
        font=('Arial', 20),
        fg='black'  
    )
    prompt_label.pack(pady=(0, 30))

    entry_var = tk.StringVar()
    entry = tk.Entry(outer_frame, textvariable=entry_var, font=('Arial', 18))
    entry.pack(pady=10, ipadx=10, ipady=10)
    entry.focus_set()

    result = {'value': None}

    def on_ok():
        result['value'] = entry_var.get()
        dialog.destroy()

    def on_cancel():
        dialog.destroy()

    button_frame = tk.Frame(outer_frame, bg='white')
    button_frame.pack(pady=20)

    ok_button = tk.Button(button_frame, text="OK", command=on_ok, font=('Arial', 16), width=10, bg='lime', fg='white')
    ok_button.pack(side='left', padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=on_cancel, font=('Arial', 16), width=10, bg='red', fg='white')
    cancel_button.pack(side='left', padx=10)

    dialog.bind('<Return>', lambda e: on_ok())
    dialog.bind('<Escape>', lambda e: on_cancel())

    dialog.wait_window()
    return result['value']


# Authentication process
def run_authentication():
    auth_root = tk.Tk()
    auth_root.withdraw()

    user_name = maximized_askstring("Authentication with Twilio API", "What's your name?")
    print(user_name)
    if user_name:
        otp = generate_otp()
        send_otp_via_twilio(USER_PHONE_NUMBER, otp)
        entered_otp = maximized_askstring("OTP Verification", f"Hi {user_name}, enter the OTP sent to your phone")
        print(f"One Time Passcode was created by Arshad Shaik {otp} ")
        if entered_otp == otp:
            speak_message(f"Welcome {user_name}, authentication successful.")
            print(f"Welcome {user_name}, Authentication Successful.....")
            auth_root.destroy()
            run_preloader()
        else:
            custom_error_box("Authentication Failed", "Incorrect OTP. Exiting application.")
            auth_root.destroy()
            exit()
    else:
        custom_error_box("Authentication Failed", "Name not entered. Exiting application.")
        auth_root.destroy()
        exit()

# === Preloader ===
def run_preloader():
    # Create the main Tkinter window
    global main
    main = tk.Tk()
    main.title("Loading The Fake Bank Currency Detection Application...")
    main.state('zoomed')  # Maximized (not fullscreen) for preloader

    # Set window icon
    icon_response = requests.get('https://cdn.gamma.app/zd5t1lpzqcyw71a/generated-images/77d5CUNucwVjCN5xwE5UP.png')
    icon_data = icon_response.content
    icon_img = Image.open(BytesIO(icon_data))
    icon_photo = ImageTk.PhotoImage(icon_img)
    main.tk.call('wm', 'iconphoto', main._w, icon_photo)

    # This Image Links Will Be Dynamically Loaded From The Google
    response = requests.get('https://i.pinimg.com/originals/b1/3a/d5/b13ad59867aa8ade2e9e2194afd75402.gif')
    img_data = response.content
    img = Image.open(BytesIO(img_data))

    # Get original dimensions of the first frame
    first_frame = next(ImageSequence.Iterator(img))
    original_width, original_height = first_frame.size

    # Create frames without resizing
    frames = [ImageTk.PhotoImage(frame.copy()) 
              for frame in ImageSequence.Iterator(img)]

    main['bg'] = 'black'
    preloader_label = Label(main, bg='black')
    preloader_label.place(relx=0.5, rely=0.5, anchor='center')

    stop_animation = [False]
    def animate(index):
        if stop_animation[0] or not preloader_label.winfo_exists():
            return
        frame = frames[index]
        try:
            preloader_label.configure(image=frame)
            main.after(100, lambda: animate((index + 1) % len(frames)))
        except tk.TclError:
            pass

    def safe_load_main_app():
        stop_animation[0] = True
        load_main_app()

    animate(0)
    # Schedule voice message after 10 seconds
    main.after(10000, lambda: speak_message("Hi, Arshad ShaiK, It's Almost Ready, to Launch, The Fake Bank Currency Detection Application with, Twilio API, and voice assistant"))
    # Schedule main app load after 30 seconds
    main.after(30000, safe_load_main_app)
    main.mainloop()

# === Main App ===
def load_main_app():
    for widget in main.winfo_children():
        widget.destroy()

    main.title("EVALUATION OF DEEP LEARNING ALGORITHMS FOR THE DETECTION OF FAKE BANK CURRENCY WITH TWILIO API AND VOICE ASSISTANT")
    main.attributes("-fullscreen", True)  # Fullscreen for main app
    
    def set_background_image():
        try:
            response = requests.get("https://i.postimg.cc/3RY19cz4/Fake-Bank-Currency-Image.png")  # Update with direct image link
            img_data = response.content
            bg_image = Image.open(BytesIO(img_data))

            def resize_background(event=None):
                width = main.winfo_width()
                height = main.winfo_height()
                if width > 1 and height > 1:
                    resized = bg_image.resize((width, height), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(resized)
                    bg_label.config(image=photo)
                    bg_label.image = photo

            bg_label = Label(main)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            main.bind("<Configure>", resize_background)
            main.after(100, resize_background)

        except Exception as e:
            print("Background load failed:", e)
            main.config(bg='navyblue')

    def set_window_icon():
        try:
            response = requests.get("https://cdn.gamma.app/zd5t1lpzqcyw71a/generated-images/77d5CUNucwVjCN5xwE5UP.png")
            img_data = response.content
            icon = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))
            main.tk.call('wm', 'iconphoto', main._w, icon)
        except Exception as e:
            print("Icon set failed:", e)

    set_background_image()
    set_window_icon()

    # Title Animation
    title_frame = Frame(main, bg='white', height=70)
    title_frame.pack(fill='x', pady=8)

    canvas = Canvas(title_frame, bg='white', highlightthickness=0, height=70)
    canvas.pack(fill='both', expand=True)

    text = "EVALUATION OF DEEP LEARNING ALGORITHMS FOR THE DETECTION OF FAKE BANK CURRENCIES WITH TWILIO API AND VOICE ASSISTANT"
    font = ('times', 16, 'bold')
    text_width = tkfont.Font(family='times', size=16, weight='bold').measure(text)

    title_x = 900
    animation_speed = 2
    colors = ['red', 'green', 'blue', 'pink', 'black', 'lime', 'skyblue']
    color_index = 0
    title_text = canvas.create_text(title_x, 35, text=text, fill='green', font=font, anchor='w')

    def animate_title():
        nonlocal title_x, color_index
        canvas.coords(title_text, title_x, 35)
        canvas.itemconfig(title_text, fill=colors[color_index])
        color_index = (color_index + 1) % len(colors)
        title_x -= animation_speed
        if title_x < -text_width:
            title_x = 900
        main.after_idle(lambda: main.after(75, animate_title))

    animate_title()

    # === Functional Code ===
    def get_pixel(img, center, x, y):
        try:
            return 1 if img[x][y] >= center else 0
        except:
            return 0

    def lbp_calculated_pixel(img, x, y):
        center = img[x][y]
        val_ar = [
            get_pixel(img, center, x-1, y+1),
            get_pixel(img, center, x, y+1),
            get_pixel(img, center, x+1, y+1),
            get_pixel(img, center, x+1, y),
            get_pixel(img, center, x+1, y-1),
            get_pixel(img, center, x, y-1),
            get_pixel(img, center, x-1, y-1),
            get_pixel(img, center, x-1, y)
        ]
        power_val = [1, 2, 4, 8, 16, 32, 64, 128]
        return sum([val_ar[i] * power_val[i] for i in range(8)])

    def upload():
        speak_message("Uploading, Test Image")
        print("Uploading, Test Image")
        global filename
        filename = filedialog.askopenfilename(initialdir="testimages")
        if filename:
            messagebox.showinfo("File Information", "Image File Loaded Successfully")

    def generateModel():
        speak_message("Generating, Image, Train & Test Model")
        print("Generating, Image, Train & Test Model")
        global loaded_model
        if os.path.exists('model.json'):
            with open('model.json', "r") as json_file:
                loaded_model = model_from_json(json_file.read())
            loaded_model.load_weights("model_weights.h5")
            print(loaded_model.summary())
            messagebox.showinfo("CNN Model Generated", "Model Loaded Successfully")
        else:
            classifier = Sequential()
            classifier.add(Convolution2D(32, (3, 3), input_shape=(48, 48, 1)))
            classifier.add(BatchNormalization())
            classifier.add(Activation("relu"))
            classifier.add(Convolution2D(32, (3, 3)))
            classifier.add(BatchNormalization())
            classifier.add(Activation("relu"))
            classifier.add(MaxPooling2D(pool_size=(2, 2)))
            classifier.add(Flatten())
            classifier.add(Dense(128))
            classifier.add(BatchNormalization())
            classifier.add(Activation("relu"))
            classifier.add(Dense(2))
            classifier.add(BatchNormalization())
            classifier.add(Activation("softmax"))
            classifier.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

            files, labels = [], []
            for label_dir, label_vec in [('Fake', [1, 0]), ('Real', [0, 1])]:
                path = f'LBP/train/{label_dir}'
                for root, _, filenames in os.walk(path):
                    for file in filenames:
                        files.append(os.path.join(root, file))
                        labels.append(label_vec)

            X = np.ndarray((len(files), 48, 48, 1), dtype=np.float32)
            Y = np.array(labels, dtype=np.float32)
            for i, file in enumerate(files):
                img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
                img = cv2.resize(img, (48, 48)).reshape(48, 48, 1)
                X[i] = img

            classifier.fit(X, Y, epochs=10)
            classifier.save_weights('model_weights.h5')
            with open("model.json", "w") as json_file:
                json_file.write(classifier.to_json())
            messagebox.showinfo("Model", "Trained and Saved")
            loaded_model = classifier

    def classify():
        speak_message("Classifying, Picture In Image")
        print("Classifying, Picture In Image")
        img_bgr = cv2.imread(filename)
        name = os.path.basename(filename)
        h, w, _ = img_bgr.shape
        img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
        img_lbp = np.zeros((h, w, 3), np.uint8)
        for i in range(h):
            for j in range(w):
                pixel = lbp_calculated_pixel(img_gray, i, j)
                img_lbp[i, j] = (pixel, pixel, pixel)

        lbp_path = f'testimages/lbp_{name}'
        cv2.imwrite(lbp_path, img_lbp)

        img = cv2.imread(lbp_path, cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (48, 48)).reshape(1, 48, 48, 1)
        preds = loaded_model.predict(img)
        predict = np.argmax(preds)
        msg = "Image Contains, Fake Currency, RBI, Will Caught You!!!" if predict == 1 else "Image Contains, Real Currency, Deposited, In Bank :)!"

        # Speak the classification result
        speak_message(msg)

        output = imutils.resize(cv2.imread(filename), width=850)
        cv2.putText(output, msg, (50, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

        cv2.imshow("Result", output)

        lbp_output = imutils.resize(cv2.imread(lbp_path), width=850)
        cv2.imshow("LBP Image", lbp_output)
        os.remove(lbp_path)
        cv2.waitKey(0)

    def close_app():
        speak_message("Exiting, The Application, © 2025, ARSHAD WASIB, SHAIK | All Rights Reserved")
        print("Exiting, The Application, © 2025, ARSHAD WASIB, SHAIK | All Rights Reserved")
        main.destroy()

    speak_message("Welcome To, Fake Bank Currency Detection Application with, Twilio API, and, voice assistant")
    font1 = ('times', 14, 'bold')
    Button(main, text="Generate Image Train & Test Model", command=generateModel, font=font1).place(x=200, y=150)
    Button(main, text="Upload Test Image", command=upload, font=font1).place(x=200, y=200)
    Button(main, text="Classify Picture In Image", command=classify, font=font1).place(x=200, y=250)
    Button(main, text="Exit The Application", command=close_app, font=font1).place(x=200, y=300)

    # Add footer with copyright information
    footer_font = ('Times', 16, 'bold')
    footer_label = Label(main,
                         text="© 2025 | ARSHAD WASIB SHAIK | All Rights Reserved. ",
                         font=footer_font,
                         fg='white',
                         bg=main['bg'],  # Match main window background
                         bd=0,  # No border
                         highlightthickness=0)  # No focus highlight
    footer_label.pack(side='bottom', pady=10)

# Start the application with authentication
if __name__ == "__main__":
    run_authentication()



