import tkinter as tk
import random

# =====================
# AYARLAR
# =====================
PY_COUNT = 100          # SAKIN 30 YAPMA – önce bunu çalıştır
WIN_W = 260
WIN_H = 80
UPDATE_MS = 100

TEXT = "ÇALIŞIYOR 😎"

# =====================
# ANA TK
# =====================
root = tk.Tk()
root.title("Kontrol Penceresi")
root.geometry("300x100")

info = tk.Label(
    root,
    text="ESC = ÇIKIŞ\nPencereler hareket ediyor",
    font=("Arial", 10)
)
info.pack(expand=True)

screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()

windows = []

# =====================
# HAREKETLİ PENCERE
# =====================
class MovingWindow:
    def __init__(self):
        self.win = tk.Toplevel(root)
        self.win.geometry(f"{WIN_W}x{WIN_H}")

        self.label = tk.Label(
            self.win,
            text=TEXT,
            font=("Arial", 12, "bold"),
            fg="white"
        )
        self.label.pack(expand=True, fill="both")

        self.x = random.randint(0, screen_w - WIN_W)
        self.y = random.randint(0, screen_h - WIN_H)
        self.dx = random.choice([-4, 4])
        self.dy = random.choice([-4, 4])

        self.update()

    def update(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= screen_w - WIN_W:
            self.dx *= -10
        if self.y <= 0 or self.y >= screen_h - WIN_H:
            self.dy *= -10

        color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.win.configure(bg=color)
        self.label.configure(bg=color)

        self.win.geometry(f"{WIN_W}x{WIN_H}+{self.x}+{self.y}")
        self.win.after(UPDATE_MS, self.update)

# =====================
# ÇIKIŞ
# =====================
def quit_all(event=None):
    root.destroy()

root.bind("<Escape>", quit_all)

# =====================
# BAŞLAT
# =====================
for _ in range(PY_COUNT):
    windows.append(MovingWindow())

root.mainloop()
