import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class PicnicApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Лабораторна робота №1: Задача про пікнік")
        self.geometry("950x600")

       
        self.left_frame = ctk.CTkFrame(self, width=320)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.lbl_title = ctk.CTkLabel(
            self.left_frame, 
            text="Вихідні дані для прийняття рішення\nв «Задачі про пікнік»", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.lbl_title.pack(padx=10, pady=10)

        self.lbl_prob = ctk.CTkLabel(self.left_frame, text="Імовірність дощу: 0.64", font=ctk.CTkFont(size=13))
        self.lbl_prob.pack(padx=10, pady=(5, 0))

        self.slider_prob = ctk.CTkSlider(self.left_frame, from_=0.0, to=1.0, number_of_steps=100, command=self.update_calculations)
        self.slider_prob.set(0.64)
        self.slider_prob.pack(padx=10, pady=(0, 15))

        self.lbl_util_title = ctk.CTkLabel(self.left_frame, text="Корисність результатів:", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_util_title.pack(padx=10, pady=5)

        self.entries = {}
        defaults = [
            ("вкрай погано (Дощ+Ліс):", "0"),
            ("погано (Дощ+Дім):", "2"),
            ("посередньо (Сухо+Дім):", "5"),
            ("чудово (Сухо+Ліс):", "8")
        ]

        for key, text, val in [
            ("v_bad", defaults[0][0], defaults[0][1]),
            ("bad", defaults[1][0], defaults[1][1]),
            ("med", defaults[2][0], defaults[2][1]),
            ("good", defaults[3][0], defaults[3][1])
        ]:
            frame_row = ctk.CTkFrame(self.left_frame, fg_color="transparent")
            frame_row.pack(fill="x", padx=10, pady=2)
            lbl = ctk.CTkLabel(frame_row, text=text, anchor="w", width=180)
            lbl.pack(side="left")
            entry = ctk.CTkEntry(frame_row, width=60)
            entry.insert(0, val)
            entry.pack(side="right")
            entry.bind("<KeyRelease>", lambda event: self.update_calculations())
            self.entries[key] = entry

        self.lbl_res_title = ctk.CTkLabel(self.left_frame, text="Очікувана корисність:", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_res_title.pack(padx=10, pady=(15, 5))

        self.lbl_u_forest = ctk.CTkLabel(self.left_frame, text="Ліс: 0.00", font=ctk.CTkFont(size=12))
        self.lbl_u_forest.pack(padx=10, pady=2)

        self.lbl_u_home = ctk.CTkLabel(self.left_frame, text="Дім: 0.00", font=ctk.CTkFont(size=12))
        self.lbl_u_home.pack(padx=10, pady=2)

        self.lbl_decision_title = ctk.CTkLabel(self.left_frame, text="Рішення:", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_decision_title.pack(padx=10, pady=(10, 2))

        self.lbl_decision = ctk.CTkLabel(self.left_frame, text="", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1f538d")
        self.lbl_decision.pack(padx=10, pady=5)

        self.fig, self.ax = plt.subplots(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

        self.update_calculations()

    def get_utilities(self):
        """ Зчитування користувацьких значень корисності """
        try:
            u_vbad = float(self.entries["v_bad"].get())
            u_bad = float(self.entries["bad"].get())
            u_med = float(self.entries["med"].get())
            u_good = float(self.entries["good"].get())
            return u_vbad, u_bad, u_med, u_good
        except ValueError:
            return 0.0, 2.0, 5.0, 8.0

    def update_calculations(self, *args):
        p_rain = round(self.slider_prob.get(), 2)
        p_dry = 1.0 - p_rain
        self.lbl_prob.configure(text=f"Імовірність дощу: {p_rain:.2f}")

        u_vbad, u_bad, u_med, u_good = self.get_utilities()

        u_forest = p_rain * u_vbad + p_dry * u_good
        u_home = p_rain * u_bad + p_dry * u_med

        self.lbl_u_forest.configure(text=f"Ліс: {u_forest:.2f}")
        self.lbl_u_home.configure(text=f"Дім: {u_home:.2f}")

        if u_forest > u_home:
            decision_text = "Ідемо в ліс! 🌲"
        elif u_home > u_forest:
            decision_text = "Сидимо вдома! 🏠"
        else:
            decision_text = "Рішення еквівалентні 🤷"

        self.lbl_decision.configure(text=decision_text)

        self.plot_graph(u_vbad, u_bad, u_med, u_good, p_rain)

    def plot_graph(self, u_vbad, u_bad, u_med, u_good, current_p):
        self.ax.clear()

        p_axis = [i / 100.0 for i in range(101)]
        u_forest_line = [p * u_vbad + (1 - p) * u_good for p in p_axis]
        u_home_line = [p * u_bad + (1 - p) * u_med for p in p_axis]

        self.ax.plot(p_axis, u_forest_line, label="ЛІС", color="magenta", linewidth=2)
        self.ax.plot(p_axis, u_home_line, label="ДІМ", color="navy", linewidth=2)

        self.ax.axvline(x=current_p, color="gray", linestyle="--", alpha=0.7)

        self.ax.set_title("Рішення про пікнік", fontsize=12, fontweight="bold")
        self.ax.set_xlabel("імовірність дощу")
        self.ax.set_ylabel("корисність")
        self.ax.set_xlim(0, 1)
        self.ax.grid(True, linestyle=":", alpha=0.6)
        self.ax.legend(loc="upper right")

        self.fig.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = PicnicApp()
    app.mainloop()