import time
import customtkinter as ctk
from PIL import Image, ImageTk
import pygame
import threading
import os

# Initialisiere pygame für die Audio-Wiedergabe
pygame.mixer.init()
angenommen = False
# Datei-Pfade
klingelton_path = "ringtone.mp3"  # Ersetze durch den Pfad deines Klingeltons
anruf_sound_path = "answer.mp3"  # Ersetze durch den Pfad des Sounds nach Annahme
bild_path = "jpcallintypavibs.jpeg"  # Bild von John Pork
icon_path = "photoicon.png"  # Icon für den Anruf

# Funktion zum Abspielen des Klingeltons
def play_ringtone():
    pygame.mixer.music.load(klingelton_path)
    pygame.mixer.music.play(-1)  # Wiederhole den Klingelton unendlich oft

# Funktion zum Stoppen des Klingeltons
def stop_ringtone():
    pygame.mixer.music.stop()

# Funktion zum Abspielen des Sounds nach Annahme
def play_answer_sound():
    pygame.mixer.music.load(anruf_sound_path)
    pygame.mixer.music.play()

# Timer-Funktion
def start_timer():
    start_time = time.time()

    def update_timer():
        while angenommen:
            timer_label.place(relx=0.5, rely=0.1, anchor="center")
            info_label.place_forget()
            elapsed_time = int(time.time() - start_time)
            minutes, seconds = divmod(elapsed_time, 60)
            timer_label.configure(text=f"Dauer: {minutes:02}:{seconds:02}")
            time.sleep(1)

    threading.Thread(target=update_timer, daemon=True).start()





# Funktion, wenn der Anruf angenommen wird
def accept_call():
    global angenommen
    angenommen = True
    #stop_ringtone()
    #play_answer_sound()
    info_label.configure(text="Anruf angenommen!", bg_color="green")
    start_timer()

# Funktion, wenn der Anruf abgelehnt wird
def decline_call():
    global angenommen
    stop_ringtone()
    if not angenommen:
        info_label.configure(text="Anruf abgelehnt!", bg_color="red")
        app.after(2000, app.destroy)  # Schließt die Anwendung nach 2 Sekunden
    else:
        timer_label.destroy()
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        info_label.configure(text="Anruf beendet!", bg_color="red")
        app.after(2000, app.destroy)  # Schließt die Anwendung nach 2 Sekunden

# Hauptanwendungsfenster erstellen
app = ctk.CTk()
app.title("Incoming Call...")
app.geometry("500x700")
app.resizable(False, False)  # Fenstergröße nicht anpassbar

#app.iconpath = ImageTk.PhotoImage(file=os.path.join("assets","photoicon.png"))
#app.wm_iconbitmap()
#app.iconphoto(False, app.iconpath)


# Setze das Fenster-Icon
icon_image = Image.open(icon_path).resize((32, 32))
icon = ImageTk.PhotoImage(icon_image)
app.iconphoto(False, icon)

# Benutzeroberfläche gestalten
# Hintergrundbild laden
image = Image.open(bild_path).resize((500, 700))
john_pork_image = ImageTk.PhotoImage(image)

# Bildanzeige (Hintergrund)
image_label = ctk.CTkLabel(app, image=john_pork_image, text="")
image_label.place(x=0, y=0, relwidth=1, relheight=1)

# Overlay-Elemente (Text und Buttons)
info_label = ctk.CTkLabel(app, text="Eingehender Anruf von John Pork...", font=("Arial", 18, "bold"))
info_label.place(relx=0.5, rely=0.1, anchor="center")

accept_button = ctk.CTkButton(app, text="Annehmen", command=accept_call, fg_color="green", text_color="white", width=170, height=80)
accept_button.place(relx=0.3, rely=0.85, anchor="center")

decline_button = ctk.CTkButton(app, text="Ablehnen", command=decline_call, fg_color="red", text_color="white", width=170, height=80)
decline_button.place(relx=0.7, rely=0.85, anchor="center")

# Timer-Anzeige
timer_label = ctk.CTkLabel(app, text="Dauer: 00:00", font=("Arial", 16))


# Starte den Klingelton in einem separaten Thread, um die GUI nicht zu blockieren
threading.Thread(target=play_ringtone, daemon=True).start()

# Hauptloop starten
app.mainloop()
