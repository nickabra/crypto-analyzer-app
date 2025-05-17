import customtkinter as ctk
import tkinter as tk
import tkinter.font as tkfont
from tkinter import ttk, messagebox, simpledialog, filedialog, PhotoImage
import requests
import time
import keyring
import os
import pandas as pd

SERVICE_NAME = 'CryptoAnalyzerApp'

# Tema dark di default
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CryptoAnalyzerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        default_font = tkfont.Font(family="Comic Sans MS", size=14)
        self.option_add("*Font", default_font)

        base = os.path.dirname(__file__)
        icon_path = os.path.join(base, "assets", "icon.ico")
        self.iconbitmap(icon_path)

        self.title("Crypto Analyzer")
        self.geometry("1000x700")
        self.cache = {}
        self.cache_timeout = 300  # 5 minuti
        self.api_key = None
        self.current_price = 0.0

        stored_key = keyring.get_password(SERVICE_NAME, 'api_key')
        if stored_key:
            self.api_key = stored_key
        else:
            dialog = APIKeyDialog(self)
            self.wait_window(dialog.win)  # Blocca finché la finestra è aperta
            if not dialog.api_key:
                messagebox.showerror("Errore", "API Key obbligatoria. L'app si chiuderà.")
                self.destroy()
                return
            self.api_key = dialog.api_key
            keyring.set_password(SERVICE_NAME, 'api_key', self.api_key)

        self.build_ui()
        self.update_all()
        self.update_countdown(300)

    def build_ui(self):
        # grid 2x2
        self.grid_columnconfigure((0,1), weight=1)
        self.grid_rowconfigure((0,1), weight=1)
        # Frame principale
        frame_price = ctk.CTkFrame(self)
        frame_price.grid(row=0, column=0, rowspan=2, padx=10, pady=10, sticky="nsew")
        frame_price.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(frame_price, text="Prezzo Attuale", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5,5))
        sub = ctk.CTkFrame(frame_price)
        sub.pack(pady=5)
        ctk.CTkLabel(sub, text="Simbolo:").pack(side=tk.LEFT)
        self.symbol_entry = ctk.CTkEntry(sub, width=80)
        self.symbol_entry.pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(sub, text="Carica", command=self.update_all).pack(side=tk.LEFT, padx=5)

        self.price_label = ctk.CTkLabel(frame_price, text="---", font=ctk.CTkFont(size=20))
        self.price_label.pack(pady=5)

        # Card: Percentuali e Supply
        frame_metrics = ctk.CTkFrame(self)
        frame_metrics.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_metrics, text="Metrica Crypto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5,5))
        self.metrics_tree = ttk.Treeview(frame_metrics, columns=("Valore",), show="tree headings")
        self.metrics_tree.heading("#0", text="Metrica")
        self.metrics_tree.heading("Valore", text="Valore")
        self.metrics_tree.tag_configure('positive', foreground='green')
        self.metrics_tree.tag_configure('negative', foreground='red')
        self.metrics_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Card: Top 50 Crypto
        frame_top50 = ctk.CTkFrame(self)
        frame_top50.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        ctk.CTkLabel(frame_top50, text="Top 50 Crypto", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(5,5))
        cols50 = ("Nome","Simbolo","Prezzo","%24h")
        self.top50_tree = ttk.Treeview(frame_top50, columns=cols50, show="headings")
        for c in cols50:
            self.top50_tree.heading(c, text=c)
        self.top50_tree.tag_configure('positive', foreground='green')
        self.top50_tree.tag_configure('negative', foreground='red')
        self.top50_tree.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

    def update_all(self):
        self.update_price()
        self.update_metrics()
        self.update_top50()

    def update_price(self):
        sym = self.symbol_entry.get().upper().strip()
        if not sym:
            return
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"symbol": sym}).json()
        price = r['data'][sym]['quote']['USD']['price']
        self.current_price = price
        self.price_label.configure(text=f"${price:,.2f}")

    def update_metrics(self):
        self.metrics_tree.delete(*self.metrics_tree.get_children())
        sym = self.symbol_entry.get().upper().strip()
        if not sym:
            return
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"symbol": sym}).json()
        data = r['data'][sym]['quote']['USD']
        parent = self.metrics_tree.insert('', 'end', text="Andamento Mercato", open=True)
        for period in ['percent_change_24h','percent_change_30d','percent_change_60d','percent_change_90d']:
            val = data.get(period, 0)
            tag = 'positive' if val > 0 else 'negative' if val < 0 else ''
            symb = '▲' if val > 0 else '▼' if val < 0 else ''
            self.metrics_tree.insert(parent, 'end', text=f"Var % ({period[-3:]})", values=(f"{val:.2f}% {symb}"), tags=(tag,))
        sup = self.metrics_tree.insert('', 'end', text="Supply", open=True)
        cs = r['data'][sym]['circulating_supply']
        ts = r['data'][sym]['total_supply'] or 0
        ms = r['data'][sym].get('max_supply')
        self.metrics_tree.insert(sup, 'end', text="Circolante", values=(f"{cs:,}",))
        self.metrics_tree.insert(sup, 'end', text="Totale", values=(f"{ts:,}",))
        self.metrics_tree.insert(sup, 'end', text="Massima", values=(f"{int(ms):,}" if ms else "Non definita",))
        self.metrics_tree.insert(sup, 'end', text="Ultimo Agg.", values=(data['last_updated'][:19],))
        df = pd.DataFrame([{ 'Simbolo': sym,
                              '%24h': data['percent_change_24h'],
                              '%30d': data['percent_change_30d'],
                              '%60d': data['percent_change_60d'],
                              '%90d': data['percent_change_90d'],
                              'Circolante': cs,
                              'Totale': ts,
                              'MaxSupply': ms or 0,
                              'Timestamp': data['last_updated'][:19]}])
        df.to_csv(f"export_{sym}.csv", index=False)

    def update_top50(self):
        self.top50_tree.delete(*self.top50_tree.get_children())
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
        r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"limit":50, "sort":"market_cap"}).json()
        for c in r['data']:
            pct = c['quote']['USD']['percent_change_24h']
            tag = 'positive' if pct > 0 else 'negative' if pct < 0 else ''
            item = self.top50_tree.insert('', 'end', values=(c['name'], c['symbol'], f"${c['quote']['USD']['price']:,.2f}", f"{pct:.2f}%"))
            self.top50_tree.item(item, tags=(tag,))

    def calculate_value(self):
        try:
            qty = float(self.qty_entry.get())
            result = qty * self.current_price
            self.calc_result.configure(text=f"${result:,.2f}")
        except:
            self.calc_result.configure(text="Err")

    def update_countdown(self, sec):
        if sec > 0:
            self.after(1000, lambda: self.update_countdown(sec-1))
        else:
            self.update_all()
            self.update_countdown(300)

class APIKeyDialog:
    def __init__(self, parent):
        # Creo una Toplevel nativa
        self.win = tk.Toplevel(parent)
        self.win.title("Inserisci API Key")
        self.win.geometry("420x180")
        self.win.transient(parent)
        self.win.grab_set()
        self.win.resizable(False, False)

        ico = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
        if os.path.exists(ico):
            self.win.iconbitmap(ico)

        bg_light  = "#f0f0f0"
        frame_bg  = "#ffffff"
        text_dark = "#000000"
        btn_bg    = "#e0e0e0"
        btn_fg    = "#333333"

        self.win.configure(bg=bg_light)

        frame = ctk.CTkFrame(master=self.win,
                             fg_color=frame_bg,
                             corner_radius=8)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        ctk.CTkLabel(frame,
                     text="Inserisci la tua API Key CoinMarketCap:",
                     text_color=text_dark,
                     font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(0,10))

        self.entry = ctk.CTkEntry(frame,
                                  fg_color="white",
                                  placeholder_text="API Key",
                                  placeholder_text_color="#888888",
                                  text_color=text_dark,
                                  border_width=1,
                                  corner_radius=4)
        self.entry.pack(pady=(0,5), fill="x")

        btn_frame = ctk.CTkFrame(master=frame,
                                 fg_color=frame_bg,
                                 corner_radius=0)
        btn_frame.pack(fill="x", pady=(0,5))

        ctk.CTkButton(btn_frame,
                      text="Conferma",
                      fg_color=btn_bg,
                      hover_color="#d0d0d0",
                      text_color=btn_fg,
                      command=self._on_confirm).pack(side="left", expand=True, padx=10, pady=5)

        ctk.CTkButton(btn_frame,
                      text="Annulla",
                      fg_color=btn_bg,
                      hover_color="#d0d0d0",
                      text_color=btn_fg,
                      command=self._on_cancel).pack(side="right", expand=True, padx=10, pady=5)

        self.api_key = None
        self.win.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _on_confirm(self):
        key = self.entry.get().strip()
        if key:
            self.api_key = key
        self.win.destroy()

    def _on_cancel(self):
        self.api_key = None
        self.win.destroy()

if __name__ == '__main__':
    app = CryptoAnalyzerApp()
    app.mainloop()