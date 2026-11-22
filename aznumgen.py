import math
import random
from datetime import date
import tkinter as tk
from pathlib import Path
from tkinter import ttk, filedialog
from PIL import Image, ImageDraw, ImageFont, ImageTk

S = 4  # pixels per mm when rendering
PREVIEW = 1.5  # pixels per mm on screen

REGIONS = {
    "01": "Abşeron", "02": "Ağdam", "03": "Ağdaş", "04": "Ağcabədi", "05": "Ağstafa",
    "06": "Ağsu", "07": "Astara", "08": "Balakən", "09": "Bərdə", "10": "Bakı",
    "11": "Beyləqan", "12": "Biləsuvar", "14": "Cəbrayıl", "15": "Cəlilabad", "16": "Daşkəsən",
    "17": "Şabran", "18": "Şirvan", "19": "Füzuli", "20": "Gəncə", "21": "Gədəbəy",
    "22": "Goranboy", "23": "Göyçay", "24": "Hacıqabul", "25": "Göygöl", "26": "Xankəndi",
    "27": "Xaçmaz", "28": "Xocavənd", "29": "Xızı", "30": "İmişli", "31": "İsmayıllı",
    "32": "Kəlbəcər", "33": "Kürdəmir", "34": "Qax", "35": "Qazax", "36": "Qəbələ",
    "37": "Qobustan", "38": "Qusar", "39": "Qubadlı", "40": "Quba", "41": "Laçın",
    "42": "Lənkəran", "43": "Lerik", "44": "Masallı", "45": "Mingəçevir", "46": "Naftalan",
    "47": "Neftçala", "48": "Oğuz", "49": "Saatlı", "50": "Sumqayıt", "51": "Samux",
    "52": "Salyan", "53": "Siyəzən", "54": "Sabirabad", "55": "Şəki", "56": "Şamaxı",
    "57": "Şəmkir", "58": "Şuşa", "59": "Tərtər", "60": "Tovuz", "61": "Ucar",
    "62": "Zaqatala", "63": "Zərdab", "64": "Zəngilan", "65": "Yardımlı", "66": "Yevlax",
    "67": "Babək", "68": "Şərur", "69": "Ordubad", "70": "Naxçıvan", "71": "Şahbuz",
    "72": "Culfa", "73": "Sədərək", "74": "Kəngərli", "75": "Naxçıvan", "77": "Bakı",
    "85": "Naxçıvan MR", "88": "Bakı", "90": "Bakı", "99": "Ölkə üzrə",
}

LETTERS = "ABCDEFGHJKLMNOPRSTUVXYZ"  # AZS 599-2015, Şəkil 18/19: no I, Q, W

COLORS = {
    "white": ((255, 255, 255), (0, 0, 0)),
    "blue": ((30, 152, 213), (255, 255, 255)),
    "red": ((228, 50, 45), (255, 255, 255)),
}
FLAG_BLUE, FLAG_RED, FLAG_GREEN = (0, 181, 226), (239, 51, 64), (80, 158, 47)
TRANSIT_GREEN = (0, 160, 80)


def row(y, size, *items):
    return [(kind, x, y, size) for kind, x in items]


# slot kinds: r = region digit, y = year digit, d = digit, l = letter, - = dash, any capital = fixed letter
PLATES = {
    "Standart": dict(
        size=(520, 110), color="white", flag=(25, 17), tag=(16, 49, True),
        slots=row(16.5, 77, ("r", 89), ("r", 141), ("-", 194), ("l", 218), ("l", 270), ("-", 323),
                  ("d", 346), ("d", 398), ("d", 450))),
    "Sərnişin daşıma (göy)": dict(
        size=(520, 110), color="blue", flag=(25, 17), tag=(16, 49, True),
        slots=row(16.5, 77, ("r", 89), ("r", 141), ("-", 194), ("T", 218), ("l", 270), ("-", 323),
                  ("d", 346), ("d", 398), ("d", 450))),
    "Tranzit": dict(
        size=(520, 110), color="white", transit=True,
        slots=row(16.5, 77, ("l", 30), ("l", 82), ("d", 134), ("d", 186), ("d", 238))
        + row(43.5, 50, ("y", 416), ("y", 453))),
    "Fəxri konsul": dict(
        size=(520, 110), color="red", tag=(16, 49, True),
        slots=row(16.5, 77, ("d", 90), ("d", 142), ("d", 194), ("F", 246), ("K", 298),
                  ("d", 350), ("d", 402), ("d", 454))),
    "Diplomatik (D)": dict(
        size=(520, 110), color="red", tag=(16, 49, True),
        slots=row(16.5, 77, ("d", 90), ("d", 142), ("d", 194), ("D", 263), ("d", 332), ("d", 384), ("d", 436))),
    "Diplomatik (T)": dict(
        size=(520, 110), color="red", tag=(16, 49, True),
        slots=row(16.5, 77, ("d", 90), ("d", 142), ("d", 194), ("T", 263), ("d", 332), ("d", 384), ("d", 436))),
    "Hərbi": dict(
        size=(520, 110), color="white", flag=(25, 17), tag=(16, 49, True),
        slots=row(16.5, 77, ("l", 113), ("d", 195), ("d", 247), ("d", 299), ("l", 381), ("l", 433))),
    "II tip (280×200)": dict(
        size=(280, 200), color="white", flag=(25, 17), tag=(16, 50, True),
        slots=row(15, 77, ("r", 123), ("r", 175))
        + row(106, 77, ("l", 13.5), ("l", 65.5), ("d", 117.5), ("d", 169.5), ("d", 221.5))),
    "II tip hərbi": dict(
        size=(280, 200), color="white", flag=(25, 17), tag=(16, 50, True),
        slots=row(106, 77, ("l", 28), ("d", 110), ("d", 162), ("d", 214)) + row(15, 77, ("l", 123), ("l", 175))),
    "III tip (300×150)": dict(
        size=(300, 150), color="white", flag=(17, 17), az=(18, 50), tag=(225, 19, False),
        slots=row(17, 50, ("r", 115), ("r", 152))
        + row(83, 50, ("l", 41), ("l", 85), ("d", 145), ("d", 182), ("d", 219))),
    "III tip fəxri konsul": dict(
        size=(300, 150), color="red", az=(18, 50), tag=(225, 19, False),
        slots=row(17, 50, ("d", 98), ("d", 135), ("d", 172))
        + row(83, 50, ("F", 73), ("K", 117), ("d", 169), ("d", 206), ("d", 243))),
    "III tip diplomatik (D)": dict(
        size=(300, 150), color="red", az=(18, 50), tag=(225, 19, False),
        slots=row(17, 50, ("d", 98), ("d", 135), ("d", 172))
        + row(83, 50, ("D", 73), ("d", 133), ("d", 170), ("d", 207))),
    "III tip diplomatik (T)": dict(
        size=(300, 150), color="red", az=(18, 50), tag=(225, 19, False),
        slots=row(17, 50, ("d", 98), ("d", 135), ("d", 172))
        + row(83, 50, ("T", 73), ("d", 133), ("d", 170), ("d", 207))),
    "III tip hərbi": dict(
        size=(300, 150), color="white", flag=(17, 17), az=(18, 50), tag=(225, 19, False),
        slots=row(83, 50, ("l", 70), ("d", 129), ("d", 166), ("d", 203)) + row(17, 50, ("l", 96), ("l", 139))),
    "IV tip motosiklet (260×150)": dict(
        size=(260, 150), color="white", flag=(17, 17), az=(18, 50), tag=(185, 19, False),
        slots=row(17, 50, ("r", 97), ("r", 134)) + row(83, 50, ("l", 71), ("d", 131), ("d", 168), ("d", 205))),
}


def mm(v):
    return int(round(v * S))


def load_font(filename):
    here = Path(__file__).resolve().parent
    for path in (here / filename, here / "AZPlate.otf"):
        if path.exists():
            return ImageFont.truetype(str(path), mm(100))
    for name in ("bahnschrift.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            font = ImageFont.truetype(name, mm(100))
            if name == "bahnschrift.ttf":
                try:
                    font.set_variation_by_name("SemiBold SemiCondensed")
                except Exception:
                    pass
            return font
        except OSError:
            continue
    return ImageFont.load_default(mm(100))


FONT77 = load_font("AZPlate.otf")
FONT50 = load_font("AZPlate50.otf")


def paste_text(img, text, color, box, font, stretch=False):
    x, y, w, h = (mm(v) for v in box)
    layer = Image.new("L", (mm(100) * (len(text) + 1), mm(160)), 0)
    ImageDraw.Draw(layer).text((mm(20), mm(20)), text, font=font, fill=255)
    layer = layer.crop(layer.getbbox())
    lw, lh = layer.size
    new_w = w if stretch else min(int(lw * h / lh), w)
    layer = layer.resize((new_w, h), Image.LANCZOS)
    img.paste(Image.new("RGBA", layer.size, color), (x + (w - new_w) // 2, y), layer)


def draw_flag(d, x, y, w, h):
    s = h / 3
    d.rectangle([x, y, x + w, y + s], fill=FLAG_BLUE)
    d.rectangle([x, y + s, x + w, y + 2 * s], fill=FLAG_RED)
    d.rectangle([x, y + 2 * s, x + w, y + h], fill=FLAG_GREEN)
    cx, cy = x + w / 2, y + h / 2
    r1, r2 = 0.15 * h, 0.125 * h
    d.ellipse([cx - 0.04 * h - r1, cy - r1, cx - 0.04 * h + r1, cy + r1], fill="white")
    d.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=FLAG_RED)
    sx, ro, ri = cx + 0.12 * h, 0.075 * h, 0.034 * h
    pts = []
    for i in range(16):
        a = -math.pi / 2 + i * math.pi / 8
        r = ro if i % 2 == 0 else ri
        pts.append((sx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill="white")


def render_plate(kind, chars, dashes=True):
    p = PLATES[kind]
    W, H = p["size"]
    bg, fg = COLORS[p["color"]]
    img = Image.new("RGBA", (mm(W), mm(H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if p["color"] == "white":
        d.rounded_rectangle([0, 0, mm(W) - 1, mm(H) - 1], radius=mm(13), fill=bg)
        if p.get("transit"):
            d.rectangle([mm(308), 0, mm(378), mm(H)], fill=TRANSIT_GREEN)
        d.rounded_rectangle([mm(1), mm(1), mm(W - 1), mm(H - 1)], radius=mm(12), outline=fg, width=mm(4.5))
    else:
        d.rounded_rectangle([0, 0, mm(W) - 1, mm(H) - 1], radius=mm(13), fill=fg)
        d.rounded_rectangle([mm(2.5), mm(2.5), mm(W - 2.5), mm(H - 2.5)], radius=mm(11), fill=bg)

    if p.get("transit"):
        black = (0, 0, 0)
        paste_text(img, "AZ", black, (313, 21, 60, 30), FONT77)
        d.rectangle([mm(315), mm(54), mm(371), mm(56.5)], fill=black)
        paste_text(img, "TR", black, (313, 59.5, 60, 30), FONT77)

    if "flag" in p:
        fx, fy = p["flag"]
        if p["color"] != "white":
            d.rectangle([mm(fx - 1), mm(fy - 1), mm(fx + 43), mm(fy + 22)], fill="white")
        draw_flag(d, mm(fx), mm(fy), mm(42), mm(21))

    if "tag" in p:
        tx, ty, with_az = p["tag"]
        d.rounded_rectangle([mm(tx), mm(ty), mm(tx + 58), mm(ty + 44)], radius=mm(7),
                            fill="white", outline=(0, 0, 0), width=mm(0.8))
        d.rounded_rectangle([mm(tx + 5), mm(ty + 5), mm(tx + 53), mm(ty + 39)], radius=mm(3),
                            outline=(0, 0, 0), width=mm(0.8))
        if with_az:
            paste_text(img, "AZ", (0, 0, 0), (tx + 9, ty + 9.5, 40, 25), FONT77, stretch=True)

    if "az" in p:
        ax, ay = p["az"]
        paste_text(img, "AZ", fg, (ax, ay, 40, 25), FONT77, stretch=True)

    for (slot, x, y, size), ch in zip(p["slots"], chars):
        if slot == "-":
            if dashes:
                d.rectangle([mm(x), mm(y + 34.5), mm(x + 15), mm(y + 44.5)], fill=fg)
            continue
        if size == 77:
            paste_text(img, ch, fg, (x, y, 45, 77), FONT77)
        else:
            paste_text(img, ch, fg, (x, y, 29 if ch.isdigit() else 36, 50), FONT50)
    return img


def parse(kind, raw):
    chars = [c for c in raw.upper() if c.isalnum()]
    i, out = 0, []
    for slot, *_ in PLATES[kind]["slots"]:
        if slot == "-":
            out.append("-")
        elif slot in "rydl":
            ok = str.isdigit if slot in "ryd" else (lambda c: c in LETTERS)
            while i < len(chars) and not ok(chars[i]):
                i += 1
            out.append(chars[i] if i < len(chars) else ("0" if slot in "ryd" else "A"))
            i += 1
        else:
            if i < len(chars) and chars[i] == slot:
                i += 1
            out.append(slot)
    return out


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Azərbaycan nömrə generatoru")
        self.resizable(False, False)

        self.kind = tk.StringVar(value="Standart")
        self.number = tk.StringVar()
        self.dashes = tk.BooleanVar(value=True)
        self.plate = None

        self.preview = ttk.Label(self, padding=15)
        self.preview.pack()

        self.info = ttk.Label(self, font=("Segoe UI", 11))
        self.info.pack()

        form = ttk.Frame(self, padding=15)
        form.pack()
        ttk.Label(form, text="Növ:").grid(row=0, column=0, sticky="w")
        ttk.Combobox(form, textvariable=self.kind, values=list(PLATES), state="readonly",
                     width=30).grid(row=0, column=1, sticky="w", pady=3)
        ttk.Label(form, text="Nömrə:").grid(row=1, column=0, sticky="w")
        ttk.Entry(form, textvariable=self.number, width=20).grid(row=1, column=1, sticky="w", pady=3)
        self.dash_check = ttk.Checkbutton(form, text="Defislərlə", variable=self.dashes)
        self.dash_check.grid(row=2, column=1, sticky="w", pady=3)

        buttons = ttk.Frame(self, padding=(15, 0, 15, 15))
        buttons.pack()
        ttk.Button(buttons, text="Təsadüfi", command=self.randomize).pack(side="left", padx=5)
        ttk.Button(buttons, text="PNG saxla", command=self.save).pack(side="left", padx=5)

        self.kind.trace_add("write", lambda *a: self.randomize())
        self.number.trace_add("write", lambda *a: self.draw())
        self.dashes.trace_add("write", lambda *a: self.draw())
        self.randomize()

    def randomize(self):
        region = iter(random.choice(list(REGIONS)))
        year = iter(f"{date.today().year % 100:02}")
        out = []
        for slot, *_ in PLATES[self.kind.get()]["slots"]:
            if slot == "r":
                out.append(next(region))
            elif slot == "y":
                out.append(next(year))
            elif slot == "d":
                out.append(random.choice("0123456789"))
            elif slot == "l":
                out.append(random.choice(LETTERS))
            else:
                out.append(slot)
        self.number.set("".join(out))

    def chars(self):
        return parse(self.kind.get(), self.number.get())

    def text(self):
        return "".join(c for c in self.chars() if c != "-" or self.dashes.get())

    def draw(self):
        kind, chars = self.kind.get(), self.chars()
        has_dash = "-" in chars
        self.dash_check.config(state="normal" if has_dash else "disabled")
        self.plate = render_plate(kind, chars, self.dashes.get())
        W, H = PLATES[kind]["size"]
        small = self.plate.resize((int(W * PREVIEW), int(H * PREVIEW)), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(small)
        self.preview.config(image=self.photo)
        slots = PLATES[kind]["slots"]
        region = "".join(c for (slot, *_), c in zip(slots, chars) if slot == "r")
        year = "".join(c for (slot, *_), c in zip(slots, chars) if slot == "y")
        text = self.text()
        if region:
            text += f"   •   {REGIONS.get(region, '?')}"
        if year:
            text += f"   •   İl: 20{year}"
        self.info.config(text=text)

    def save(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", initialfile=f"{self.text()}.png",
                                            filetypes=[("PNG image", "*.png")])
        if path:
            self.plate.save(path)


if __name__ == "__main__":
    App().mainloop()
