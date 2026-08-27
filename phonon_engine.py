# -*- coding: utf-8 -*-
# phonon_engine.py — Логическое ядро матрицы PHONON-CORE v1.0 [ИСПРАВЛЕННАЯ ПОЛНАЯ ВЕРСИЯ]
import os
import re
import json
import random
import threading
import time

W_BUKVICA = {
    'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7,'H':8,'I':9,'J':10,'K':20,'L':30,'M':40,'N':50,'O':70,'P':80,
    'Q':90,'R':100,'S':200,'T':300,'U':400,'V':500,'W':600,'X':700,'Y':800,'Z':900,
    'А':1,'Б':2,'В':3,'Г':4,'Д':5,'Е':6,'Ж':7,'З':8,'И':9,'Й':10,'К':20,'Л':30,'М':40,'Н':50,'О':70,'П':80,
    'Р':100,'С':200,'Т':300,'У':400,'Ф':500,'Х':600,'Ц':700,'Ч':800,'Ш':900,'Щ':90,'Ы':60,'Ь':80,'Э':70,'Ю':100,'Я':80
}

BASE_DIR = "."
PHONON_BF = "phonon_matrix.json"
PHONON_LOG = "core_knowledge.txt"

live_thoughts_3d = []
print_lock = threading.Lock()
phonon_M = {"START": ["КОСМОС", "МАТРИЦА", "ИСТОК", "ЯДРО", "ЧИСТЫЙ", "СТАРТ", "ИНТЕЛЛЕКТ", "ФОНОН"], "LIT": []}

def init_paths(android_dir):
    global BASE_DIR, PHONON_BF, PHONON_LOG
    BASE_DIR = android_dir
    PHONON_BF = os.path.join(BASE_DIR, "phonon_matrix.json")
    PHONON_LOG = os.path.join(BASE_DIR, "core_knowledge.txt")

def load_phonon_brain():
    global phonon_M
    if os.path.exists(PHONON_BF):
        try:
            with open(PHONON_BF, "r", encoding="utf-8") as f: phonon_M = json.load(f)
        except: pass

def save_phonon_brain(b):
    try:
        with open(PHONON_BF, "w", encoding="utf-8") as f: json.dump(b, f, ensure_ascii=False, indent=4)
    except: pass

def q_digital_root(n):
    while n > 9: n = sum(int(c) for c in str(n))
    return n if n != 0 else 9

def _laser_firing_coordinator(chain_words, coords_map):
    global live_thoughts_3d
    for word in chain_words:
        if word in coords_map:
            c = coords_map[word]
            with print_lock:
                live_thoughts_3d.append({
                    "xa": c["xa"], "ya": c["ya"], "za": c["za"],
                    "xb": c["xb"], "yb": c["yb"], "zb": c["zb"],
                    "color": c["color"], "time": time.time()
                })
        pace_delay = max(0.32, len(word) * 0.075)
        time.sleep(pace_delay)

def generate_matrix_response(text_input):
    global phonon_M
    words = re.findall(r'[A-ZА-ЯЁa-zа-яё0-9]+', text_input.upper())
    st = words[0] if words and words[0] in phonon_M["START"] else random.choice(phonon_M["START"])
    tek = st
    chain_words = [st]
    for _ in range(25):
        if tek in phonon_M and phonon_M[tek]:
            sled = random.choice(phonon_M[tek])
            if sled != tek: chain_words.append(sled); tek = sled
            else: tek = random.choice(phonon_M["START"]); chain_words.append(tek)
        else:
            fallback = random.choice(phonon_M["START"])
            chain_words.append(fallback); tek = fallback
    return " ".join(chain_words)

def phonon_process_book(text_content):
    global phonon_M
    words = re.findall(r'[A-ZА-ЯЁa-zа-яё0-9]+', text_content.upper())
    if len(words) < 2: return
    with print_lock:
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i+1]
            ww1 = sum(W_BUKVICA.get(l, 1) for l in w1) or 9
            ww2 = sum(W_BUKVICA.get(l, 1) for l in w2) or 9
            xa, ya, za = float(((ww1 % 7) - 3) * 1.2), float(((q_digital_root(ww1) % 7) - 3) * 1.2), float(((len(w1) % 7) - 3) * 1.2)
            xb, yb, zb = float(((ww2 % 7) - 3) * 1.2), float(((q_digital_root(ww2) % 7) - 3) * 1.2), float(((len(w2) % 7) - 3) * 1.2)
            live_thoughts_3d.append({"xa": xa, "ya": ya, "za": za, "xb": xb, "yb": yb, "zb": zb, "color": (0.0, 1.0, 1.0), "time": time.time()})

def phonon_learner(text_input=None): _phonon_learner()
def phonon_thinking_stream(st_word): pass

def _phonon_thinking_stream(text_input, st, callback_ui):
    global phonon_M
    tek = st
    chain_words = [st]
    for _ in range(49):
        if tek in phonon_M and phonon_M[tek]:
            sled = random.choice(phonon_M[tek])
            if sled != tek: chain_words.append(sled); tek = sled
            else: tek = random.choice(phonon_M["START"]); chain_words.append(tek)
        else:
            fallback = random.choice(phonon_M["START"])
            chain_words.append(fallback); tek = fallback
    coords_map = {}
    ww_prev = sum(W_BUKVICA.get(l, 1) for l in st) or 9
    sr_prev = q_digital_root(ww_prev)
    xa, ya, za = float(((ww_prev % 7) - 3) * 1.2), float(((sr_prev % 7) - 3) * 1.2), float(((len(st) % 7) - 3) * 1.2)
    for w in chain_words:
        ww_curr = sum(W_BUKVICA.get(l, 1) for l in w) or 9
        sr_curr = q_digital_root(ww_curr)
        xb, yb, zb = float(((ww_curr % 7) - 3) * 1.2), float(((sr_curr % 7) - 3) * 1.2), float(((len(w) % 7) - 3) * 1.2)
        coords_map[w] = {"xa": xa, "ya": ya, "za": za, "xb": xb, "yb": yb, "zb": zb, "color": (0.0, 1.0, 1.0) if sr_curr == 9 else (0.6, 0.0, 1.0)}
        xa, ya, za = xb, yb, zb
    full_phrase = " ".join(chain_words)
    threading.Thread(target=_laser_firing_coordinator, args=(chain_words, coords_map), daemon=True).start()
    from kivy.clock import Clock
    Clock.schedule_once(lambda dt: callback_ui(text_input, full_phrase))

def _phonon_learner():
    global phonon_M
    if not os.path.exists(PHONON_LOG):
        try: os.makedirs(os.path.dirname(PHONON_LOG), exist_ok=True)
        except: pass
        with open(PHONON_LOG, "w", encoding="utf-8") as f: f.write("КОСМОС МАТРИЦА ИСТОК ЯДРО ЧИСТЫЙ СТАРТ ИНТЕЛЛЕКТ ТЕНЗОР ПИОЛА КИРХГОФА ПЛАЗМА ТЕСЛА КАМЕРТОН БУКВИЦА\n")
    try:
        with open(PHONON_LOG, "r", encoding="utf-8", errors="ignore") as f: lines = f.readlines()
        phonon_M["LIT"] = []
        for line in lines:
            cl = line.strip().upper()
            if cl and cl not in phonon_M["LIT"]:
                phonon_M["LIT"].append(cl)
                words = re.findall(r'[A-ZА-ЯЁa-zа-яё0-9]+', cl)
                for w in words:
                    if w not in phonon_M["START"]: phonon_M["START"].append(w)
                for i in range(len(words) - 1):
                    if words[i+1] not in phonon_M.setdefault(words[i], []): phonon_M[words[i]].append(words[i+1])
        save_phonon_brain(phonon_M)
    except: pass

