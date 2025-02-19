import time
import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image, ImageTk
import pygame
import threading
import os

import cv2



#cap.release()
#cv2.destroyAllWindows()


from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Standard-Audio-Gerät abrufen
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# Lautstärke auf 0% setzen
volume.SetMasterVolumeLevelScalar(1, None) #change to 1 to troll your friends


# Initialisiere pygame für die Audio-Wiedergabe
pygame.mixer.init()
angenommen = False
muted = False

# Datei-Pfade
klingelton_path = "john_pork_is_calling.mp3"
anruf_sound_path = "answer.mp3"  # Sound nach Annahme
bild_path = "jpcallintypavibs.jpeg"  # Hintergrundbild
icon_path = "photoicon.png"  # App-Icon

def play_ringtone():
    pygame.mixer.music.load(klingelton_path)
    pygame.mixer.music.play(-1)

def stop_ringtone():
    pygame.mixer.music.stop()

def play_answer_sound():
    if os.path.exists(anruf_sound_path):
        pygame.mixer.music.load(anruf_sound_path)
        pygame.mixer.music.play(-1)
    else:
        print("Fehler: Datei 'answer.mp3' nicht gefunden!")

def start_timer():
    start_time = time.time()
    def update_timer():
        while angenommen:
            elapsed_time = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            timer_label.configure(text=f"Dauer: {minutes:02}:{seconds:02}")
            time.sleep(1)
    threading.Thread(target=update_timer, daemon=True).start()

def accept_call():
    global angenommen
    angenommen = True
    stop_ringtone()
    play_answer_sound()
    info_label.configure(text="Anruf angenommen!", fg_color="green")
    accept_button.place_forget()
    decline_button.place_forget()
    timer_label.place(relx=0.5, rely=0.05, anchor="center")  # Timer oben in der Mitte
    end_call_button.place(relx=0.5, rely=0.85, anchor="center")  # Ende-Call Button unten in der Mitte
    mute_button.place(relx=0.23, rely=0.87, anchor="center")  # Mute-Button links
    volume_button.place(relx=0.8, rely=0.75, anchor="center")  # Lautstärke-Button rechts
    video_button.place(relx=0.23, rely=0.80, anchor="center")  # Video-Button in der Mitte etwas höher

    info_label.after(2000, info_label.place_forget)
    info_label.configure(text="Anruf angenommen!")
    start_timer()

def decline_call():
    global angenommen
    stop_ringtone()
    if not angenommen:
        info_label.configure(text="Anruf abgelehnt!", fg_color="red")
        app.after(2000, app.destroy)
    else:
        end_call()

def end_call():
    global angenommen
    angenommen = False
    timer_label.place_forget()
    end_call_button.place_forget()
    mute_button.place_forget()
    volume_button.place_forget()
    video_button.place_forget()
    info_label.configure(text="Anruf beendet!", fg_color="red")
    app.after(2000, app.destroy)

def toggle_mute():
    global muted
    muted = not muted
    if muted:
        pygame.mixer.music.set_volume(0.0)
        mute_button.configure(text="Unmute")
    else:
        pygame.mixer.music.set_volume(1.0)
        mute_button.configure(text="Mute")



# Hauptanwendungsfenster erstellen
app = ctk.CTk()
app.title("Incoming Call...")
app.geometry("500x700")
app.resizable(False, False)

icon_image = Image.open(icon_path).resize((32, 32))
icon = ImageTk.PhotoImage(icon_image)
app.iconphoto(False, icon)

image = Image.open(bild_path).resize((500, 700))
john_pork_image = CTkImage(light_image=image, size=(500, 700))
image_label = ctk.CTkLabel(app, image=john_pork_image, text="")
image_label.place(x=0, y=0, relwidth=1, relheight=1)

info_label = ctk.CTkLabel(app, text="Eingehender Anruf von John Pork...", font=("Arial", 18, "bold"))
info_label.place(relx=0.5, rely=0.1, anchor="center")

accept_button = ctk.CTkButton(app, text="Annehmen", command=accept_call, fg_color="green", text_color="white", width=170, height=80)
accept_button.place(relx=0.3, rely=0.85, anchor="center")

decline_button = ctk.CTkButton(app, text="Ablehnen", command=decline_call, fg_color="red", text_color="white", width=170, height=80)
decline_button.place(relx=0.7, rely=0.85, anchor="center")

timer_label = ctk.CTkLabel(app, text="Dauer: 00:00", font=("Arial", 16))

def toggle_video():
    app.destroy()
    video_path = "John pork gets rizzed by the cops.mp4"
    cap = cv2.VideoCapture(video_path)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Video", frame)
        
        # Press 'q' to quit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

end_call_button = ctk.CTkButton(app, text="Auflegen", command=end_call, fg_color="red", text_color="white", width=170, height=80)
mute_button = ctk.CTkButton(app, text="Mute", command=toggle_mute, fg_color="gray", text_color="white", width=100, height=50)
volume_button = ctk.CTkButton(app, text="Lautstärke", fg_color="blue", text_color="white", width=100, height=50)
video_button = ctk.CTkButton(app, text="Video", command=toggle_video, fg_color="purple", text_color="white", width=100, height=50)





threading.Thread(target=play_ringtone, daemon=True).start()
app.mainloop()
