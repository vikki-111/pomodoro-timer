import customtkinter as ctk
from CTkMessagebox import CTkMessagebox as ctkmsg
from plyer import notification as notify
from pygame import mixer, time

class PomodoroTimer:
    def __init__(self, main_window):
        self.root = main_window
        self.sound = mixer.Sound('alarm.wav')
        self.minutes = 0
        self.initial_minutes = 0
        self.seconds = 0
        self.isRunning = False
        self.label = None
        self.start_btn = None
        self.reset_btn = None
        self.delete_btn = None
        self.pause_btn = None
        self.resume_btn = None
        self.add_minute_btn = None
        self.mute_btn = None
        self.unmute_btn = None
        self.breakLabel = None
        self.break_flag = -1
        self.break_minutes = 0
        self.muteFlag = False

        self.new_timer = ctk.CTkButton(self.root, text="New Timer", command=self.set_timer, width=100)
        self.new_timer.place(x=350, y=100)

    def set_timer(self):
        try:
            if self.label: self.label.destroy()
            self.minutes = int(ctk.CTkInputDialog(title="New timer", text="Enter the time in minutes:").get_input())
            self.initial_minutes = self.minutes
            self.seconds = 0

            self.label = ctk.CTkLabel(self.root, text=f"{self.minutes}:00", font=("Inter", 40))
            self.label.pack(pady=20)

            self.start_btn = ctk.CTkButton(self.root, text="Start Timer", command=self.start_timer, width=70)
            self.start_btn.place(x=200, y=350)

            self.reset_btn = ctk.CTkButton(self.root, text="Reset Timer", command=self.reset_timer, width=70)
            self.reset_btn.place(x=350, y=350)

            self.delete_btn = ctk.CTkButton(self.root, text="Delete Timer", command=self.delete_timer, width=70, fg_color='red')
            self.delete_btn.place(x=490, y=350)

            self.new_timer.destroy()
            self.break_flag = -1
        except ValueError:
            ctkmsg(title="Bruh", message="Enter a valid number!")
        except TypeError:
            pass

    def start_timer(self):
        self.isRunning = True
        if self.start_btn: self.start_btn.destroy()

        self.add_minute_btn = ctk.CTkButton(self.root, text="+1", command=self.add_minute, width=30, fg_color='black')
        self.add_minute_btn.place(x=550, y=130)

        self.pause_btn = ctk.CTkButton(self.root, text="Pause", command=self.pause, width=70)
        self.pause_btn.place(x=200, y=350)

        self.mute_btn = ctk.CTkButton(self.root, text="Mute alarm", command=self.mute, width=70, fg_color='black')
        self.mute_btn.place(x=550, y=160)

        self.update_time()

    def update_time(self):
        if not self.isRunning: return

        if self.break_flag == 1:
            if not self.breakLabel:
                self.breakLabel = ctk.CTkLabel(self.root, text="Break time! 2 mins...")
                self.breakLabel.place(x=320, y=40)
            self.break_minutes += 1
            if self.break_minutes >= 2:
                self.break_flag = -1
                self.break_minutes = 0
                self.breakLabel.destroy()
                self.breakLabel = None
            self.root.after(60000, self.update_time)
            return

        if self.seconds > 0:
            self.seconds -= 1
        elif self.minutes > 0:
            self.minutes -= 1
            self.seconds = 59
            self.break_flag += 1
        else:
            self.timer_done()
            return

        self.update_label()
        self.root.after(1000, self.update_time)

    def update_label(self):
        if self.label: self.label.destroy()
        time_str = f"{self.minutes}:{self.seconds:02d}"
        self.label = ctk.CTkLabel(self.root, text=time_str, font=("Inter", 40))
        self.label.pack(pady=20)

    def timer_done(self):
        if not self.muteFlag:
            self.sound.play(loops=3)
            time.delay(5000)
            self.sound.stop()

        for widget in self.root.winfo_children():
            widget.destroy()

        self.label = ctk.CTkLabel(self.root, text=f"Your {self.initial_minutes}-minute timer has ended!")
        self.label.place(x=300, y=30)

        self.new_timer = ctk.CTkButton(self.root, text="New Timer", command=self.set_timer, width=100)
        self.new_timer.place(x=350, y=100)

        notify.notify(title="Timer Complete!", message="Your pomodoro timer is up!", timeout=5)

    def reset_timer(self):
        self.isRunning = False
        self.break_flag = -1
        self.break_minutes = 0

        if self.label: self.label.destroy()
        if self.pause_btn: self.pause_btn.destroy()
        if self.add_minute_btn: self.add_minute_btn.destroy()
        if self.mute_btn: self.mute_btn.destroy()
        if self.unmute_btn: self.unmute_btn.destroy()

        self.start_btn = ctk.CTkButton(self.root, text="Start", command=self.start_timer, width=70)
        self.start_btn.place(x=200, y=350)

        self.minutes = self.initial_minutes
        self.seconds = 0

        self.label = ctk.CTkLabel(self.root, text=f"{self.minutes}:00", font=("Inter", 40))
        self.label.pack(pady=20)

    def delete_timer(self):
        self.isRunning = False
        for widget in self.root.winfo_children():
            widget.destroy()

        self.new_timer = ctk.CTkButton(self.root, text="New Timer", command=self.set_timer, width=100)
        self.new_timer.place(x=350, y=100)
        self.seconds = 0

    def pause(self):
        self.isRunning = False
        if self.pause_btn: self.pause_btn.destroy()
        self.resume_btn = ctk.CTkButton(self.root, text="Resume", command=self.resume, width=70)
        self.resume_btn.place(x=200, y=350)

    def resume(self):
        self.isRunning = True
        if self.resume_btn: self.resume_btn.destroy()
        self.pause_btn = ctk.CTkButton(self.root, text="Pause", command=self.pause, width=70)
        self.pause_btn.place(x=200, y=350)
        self.update_time()

    def add_minute(self):
        self.minutes += 1
        self.update_label()

    def mute(self):
        self.muteFlag = True
        if self.mute_btn: self.mute_btn.destroy()
        self.unmute_btn = ctk.CTkButton(self.root, text="Unmute alarm", command=self.unmute, width=70, fg_color='black')
        self.unmute_btn.place(x=550, y=160)

    def unmute(self):
        self.muteFlag = False
        if self.unmute_btn: self.unmute_btn.destroy()
        self.mute_btn = ctk.CTkButton(self.root, text="Mute alarm", command=self.mute, width=70, fg_color='black')
        self.mute_btn.place(x=550, y=160)

# UI Initialization
mixer.init()
main_window = ctk.CTk()
ctk.set_default_color_theme('blue')
ctk.set_appearance_mode('dark')
main_window.geometry("800x600")
main_window.title("Pomodoro Timer")
ptimer = PomodoroTimer(main_window)
main_window.mainloop()
