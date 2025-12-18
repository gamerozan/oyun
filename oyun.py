
import tkinter as tk
from tkinter import messagebox
import os
import tempfile
import random
import winsound
import threading
import time

# ================= KORKU AYARLARI =================
WHISPERS = [
    "buradasın.",
    "nefesini duyuyorum.",
    "zamanın azalıyor.",
    "yanlış yapma.",
    "çok yaklaştım."
]

HEART_DELAY = 0.8  # kalp atışı aralığı
TIME_LIMIT = 10   # saniye
# ================================================

# Sahte dosyalar (yanlış cevaba ceza)
temp_dir = tempfile.mkdtemp()
files = []

for i in range(5):
    p = os.path.join(temp_dir, f"kurban_{i+1}.txt")
    with open(p, "w") as f:
        f.write("...")
    files.append(p)

# Sorular
questions = [
    ("Bu soruyu okuman gerekiyordu. (evet yaz)", "evet"),
    ("Bir şey yanlış hissettiriyor mu? (evet yaz)", "evet"),
    ("Az önce arkanda bir ses duydun mu? (hayır yaz)", "hayır"),
    ("Bu oyunu başlatmamalı mıydın? (evet yaz)", "evet"),
    ("Şu an zamanı kontrol ettin mi? (hayır yaz)", "hayır"),
    ("Kalp atışın hızlandı mı? (evet yaz)", "evet"),
    ("Soruların değiştiğini fark ettin mi? (evet yaz)", "evet"),
    ("Bu soruya cevap verme. (cevap verme)", ""),  # bilinçli tuzak
    ("Cevap verdin. Neden? (neden yaz)", "neden"),
    ("Bir şey eksik. (evet yaz)", "evet"),
    ("Ekran sana yakın mı? (evet yaz)", "evet"),
    ("Sessizlik ağırlaştı mı? (evet yaz)", "evet"),
    ("Yanlış yapmadın ama yine de ceza alacaksın. (tamam yaz)", "tamam"),
    ("Burada kalmak mı istiyorsun? (hayır yaz)", "hayır"),
    ("Bu bir oyun. Emin misin? (hayır yaz)", "hayır"),
    ("Bu soru daha önce var mıydı? (hayır yaz)", "hayır"),
    ("Kapatmak istiyorsan devam et. (devam yaz)", "devam"),
    ("Son soru değildi. (evet yaz)", "evet"),
    ("Artık geri yok. (evet yaz)", "evet"),
]

current_question = 0
time_left = TIME_LIMIT
running = True

# ================= KULLANICI ADI =================
user_name = input("Kullanıcı adını gir: ")

# ================= HTML CEVAP GÜNCELLEME =================
HTML_FILE = "answers.html"
answers_list = []

def update_html(answers):
    html_content = f"""
<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="UTF-8">
<title>Kullanıcı Cevapları</title>
<style>
  body {{ background-color: #1a1a1a; color: #f0f0f0; font-family: 'Courier New', monospace; padding: 30px; }}
  h1 {{ text-align: center; color: #ff5555; }}
  .container {{ display: flex; justify-content: space-around; gap: 20px; flex-wrap: wrap; }}
  .box {{ border: 3px solid #ff5555; background-color: #222; padding: 15px; width: 45%; height: 400px; overflow-y: scroll; border-radius: 12px; }}
  .box h2 {{ text-align: center; color: #ffbb55; margin-bottom: 10px; }}
  select {{ margin-bottom: 10px; padding: 5px; font-size: 16px; width: 100%; }}
  .entry {{ margin: 5px 0; padding: 3px; background-color: #111; border-radius: 5px; padding-left: 5px; }}
</style>
</head>
<body>

<h1>Kullanıcı Cevapları</h1>

<div class="container">
    <div class="box" id="all-box">
        <h2>Tüm Cevaplar</h2>
        <div id="all-answers"></div>
    </div>

    <div class="box" id="user-box">
        <h2>Kullanıcı Seç</h2>
        <select id="user-select" onchange="filterUser()">
            <option value="">--Kullanıcı Seç--</option>
        </select>
        <div id="user-answers"></div>
    </div>
</div>

<script>
    let allAnswers = {answers};

    function updateBoxes() {{
        const allBox = document.getElementById("all-answers");
        const userSelect = document.getElementById("user-select");
        allBox.innerHTML = "";
        let users = new Set();
        allAnswers.forEach(e => {{
            const div = document.createElement("div");
            div.className = "entry";
            div.textContent = e.user + ": " + e.answer;
            allBox.appendChild(div);
            users.add(e.user);
        }});
        userSelect.innerHTML = "<option value=''>--Kullanıcı Seç--</option>";
        users.forEach(u => {{
            const option = document.createElement("option");
            option.value = u;
            option.textContent = u;
            userSelect.appendChild(option);
        }});
        filterUser();
    }}

    function filterUser() {{
        const sel = document.getElementById("user-select").value;
        const userBox = document.getElementById("user-answers");
        userBox.innerHTML = "";
        if(sel === "") return;
        allAnswers.filter(e => e.user === sel).forEach(e => {{
            const div = document.createElement("div");
            div.className = "entry";
            div.textContent = e.answer;
            userBox.appendChild(div);
        }});
    }}

    updateBoxes();
    // setInterval(() => location.reload(), 2000); // test için kapalı
</script>

</body>
</html>
    """
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write(html_content)

# ================= SES =================
def heartbeat():
    while running:
        winsound.Beep(120, 200)
        time.sleep(HEART_DELAY)

# ================= ZAMAN =================
def countdown():
    global time_left
    while time_left > 0 and running:
        timer_label.config(text=f"ZAMAN: {time_left}")
        time.sleep(1)
        time_left -= 1

    if running:
        messagebox.showerror("ÇOK GEÇ", "ZAMAN DOLDU.")
        root.destroy()

# ================= EKRAN =================
def shake():
    for _ in range(10):
        root.geometry(f"+{random.randint(0,20)}+{random.randint(0,20)}")
        root.update()
        time.sleep(0.02)

def check_answer():
    global current_question, time_left
    
    answer = entry.get().strip().lower()
    
    # HTML için cevap kaydet
    answers_list.append({"user": user_name, "answer": answer})
    update_html(answers_list)
    
    label.config(text=random.choice(WHISPERS), fg="darkred")
    shake()

    correct = questions[current_question][1]
    if answer == correct:
        current_question += 1
        time_left = TIME_LIMIT
    else:
        if files:
            os.remove(files.pop())
        else:
            messagebox.showerror("SON", "ARTIK YOK.")
            root.destroy()
            return

    if current_question >= len(questions):
        messagebox.showwarning("…", "ŞİMDİLİK.")
        root.destroy()
        return

    question_label.config(text=questions[current_question][0])
    entry.delete(0, tk.END)

# ================= GUI =================
root = tk.Tk()
root.title(".")
root.geometry("900x600")  # test için tam ekran kapalı
root.configure(bg="#120000")

question_label = tk.Label(
    root, text=questions[0][0],
    font=("Arial", 30),
    fg="#aa0000", bg="#120000"
)
question_label.pack(pady=80)

timer_label = tk.Label(
    root, text="", font=("Arial", 20),
    fg="darkred", bg="#120000"
)
timer_label.pack()

entry = tk.Entry(
    root, font=("Arial", 24),
    bg="black", fg="red",
    insertbackground="red", justify="center"
)
entry.pack(pady=20)

button = tk.Button(
    root, text="CEVAPLA",
    font=("Arial", 20),
    bg="black", fg="red",
    command=check_answer
)
button.pack(pady=20)

label = tk.Label(
    root, text="",
    font=("Arial", 28),
    fg="darkred", bg="#120000"
)
label.pack(pady=40)

root.bind("<Escape>", lambda e: root.destroy())

# ================= THREADS =================
threading.Thread(target=heartbeat, daemon=True).start()
threading.Thread(target=countdown, daemon=True).start()

# Nefes alan arka plan
def breathing():
    colors = ["#120000", "#1a0000", "#220000", "#1a0000"]
    while running:
        for c in colors:
            root.configure(bg=c)
            time.sleep(0.8)

threading.Thread(target=breathing, daemon=True).start()

root.mainloop()
running = False
