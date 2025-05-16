import tkinter as tk
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox, simpledialog, filedialog
import requests
import time
import keyring
import pandas as pd

SERVICE_NAME = 'CryptoAnalyzerApp'

class CryptoAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Crypto Analyzer")
        self.cache = {}
        self.cache_timeout = 300
        self.api_key = None
        self.watchlist = []

        stored_key = keyring.get_password(SERVICE_NAME, 'api_key')
        if stored_key:
            self.api_key = stored_key
        else:
            new_key = simpledialog.askstring("API Key Mancante", "Inserisci la tua API Key CoinMarketCap:")
            if not new_key:
                messagebox.showerror("Errore", "API Key obbligatoria. L'app si chiuderà.")
                root.destroy()
                return
            self.api_key = new_key.strip()
            keyring.set_password(SERVICE_NAME, 'api_key', self.api_key)

        self.build_ui()

    def build_ui(self):
        # Main layout
        main = tb.Frame(self.root, padding=10)
        main.pack(expand=YES, fill=BOTH)
        main.columnconfigure(0, weight=1)
        main.columnconfigure(1, weight=2)
        main.rowconfigure(0, weight=1)
        main.rowconfigure(1, weight=0)

        # Watchlist
        watch_frame = tb.Labelframe(main, text="Watchlist")
        watch_frame.grid(row=0, column=0, sticky=NSEW, padx=5, pady=5)
        watch_frame.columnconfigure(0, weight=1)
        watch_frame.rowconfigure(1, weight=1)

        ctrl = tb.Frame(watch_frame)
        ctrl.grid(row=0, column=0, sticky=EW, pady=5)
        self.sym_entry = tb.Entry(ctrl)
        self.sym_entry.pack(side=LEFT, expand=YES, fill=X)
        tb.Button(ctrl, text="Aggiungi", bootstyle="success", command=self.add_symbol).pack(side=LEFT, padx=2)
        tb.Button(ctrl, text="Rimuovi", bootstyle="danger", command=self.remove_symbol).pack(side=LEFT, padx=2)
        tb.Button(ctrl, text="Esporta CSV", bootstyle="info", command=self.export_csv).pack(side=LEFT, padx=2)

        cols = ("Simbolo","Prezzo","%24h")
        self.watch_tree = tb.Treeview(watch_frame, columns=cols, show="headings")
        for c in cols:
            self.watch_tree.heading(c, text=c)
        self.watch_tree.grid(row=1, column=0, sticky=NSEW)

        # Details
        detail_frame = tb.Labelframe(main, text="Dettagli Crypto")
        detail_frame.grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)
        detail_frame.columnconfigure(0, weight=1)
        detail_frame.rowconfigure(1, weight=1)

        bf = tb.Frame(detail_frame)
        bf.grid(row=0, column=0, columnspan=3, sticky=EW, pady=5)
        tb.Label(bf, text="Simbolo:").pack(side=LEFT)
        self.detail_entry = tb.Entry(bf)
        self.detail_entry.pack(side=LEFT, padx=5)
        tb.Button(bf, text="Analizza", bootstyle="primary", command=self.fetch_crypto_data).pack(side=LEFT)
        tb.Button(bf, text="Aggiorna Dati", bootstyle="secondary", command=self.refresh_data).pack(side=LEFT, padx=5)
        self.spinner = tb.Progressbar(bf, bootstyle="warning", mode="indeterminate", length=100)
        self.spinner.pack(side=LEFT, padx=5)

        self.detail_tree = tb.Treeview(detail_frame, columns=("Valore",), show="tree headings")
        self.detail_tree.heading("#0", text="Metrica")
        self.detail_tree.heading("Valore", text="Valore")
        self.detail_tree.column("#0", width=250)
        self.detail_tree.column("Valore", width=150, anchor=E)
        self.detail_tree.grid(row=1, column=0, columnspan=3, sticky=NSEW, pady=5)
        self.detail_tree.tag_configure('positive', foreground='green')
        self.detail_tree.tag_configure('negative', foreground='red')

        cf = tb.Frame(detail_frame)
        cf.grid(row=2, column=0, columnspan=3, sticky=EW, pady=5)
        tb.Label(cf, text="Quantità:").pack(side=LEFT)
        self.quantity_entry = tb.Entry(cf, width=10)
        self.quantity_entry.pack(side=LEFT, padx=5)
        tb.Button(cf, text="Calcola", bootstyle="info", command=self.calculate_value).pack(side=LEFT)
        self.result_label = tb.Label(cf, text="")
        self.result_label.pack(side=LEFT, padx=10)

        # Theme toggle at bottom-left
        self.toggle_btn = tb.Button(main, text="Light Theme", bootstyle="secondary", command=self.toggle_theme)
        self.toggle_btn.grid(row=1, column=0, sticky=W, padx=5, pady=5)

    def toggle_theme(self):
        style = self.root.style
        current = style.theme.name
        new = 'flatly' if current == 'darkly' else 'darkly'
        style.theme_use(new)
        self.toggle_btn.config(text='Dark Theme' if new == 'darkly' else 'Light Theme')

    def add_symbol(self):
        sym = self.sym_entry.get().upper().strip()
        if sym and sym not in self.watchlist:
            self.watchlist.append(sym)
            self.sym_entry.delete(0, tk.END)
            self.update_watchlist()

    def remove_symbol(self):
        for i in self.watch_tree.selection():
            sym = self.watch_tree.item(i, 'values')[0]
            if sym in self.watchlist:
                self.watchlist.remove(sym)
        self.update_watchlist()

    def update_watchlist(self):
        self.watch_tree.delete(*self.watch_tree.get_children())
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        for sym in self.watchlist:
            try:
                r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"symbol": sym}).json()
                d = r['data'][sym]['quote']['USD']
                price = f"${d['price']:,.2f}"
                ch = f"{d['percent_change_24h']:.2f}%"
                self.watch_tree.insert('', tk.END, values=(sym, price, ch))
            except:
                self.watch_tree.insert('', tk.END, values=(sym, 'Err', 'Err'))

    def export_csv(self):
        if not self.watchlist:
            messagebox.showwarning("Warning", "Watchlist vuota.")
            return
        rows = []
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        for sym in self.watchlist:
            try:
                r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"symbol": sym}).json()
                q = r['data'][sym]['quote']['USD']
                rows.append({'Simbolo': sym, 'Prezzo': q['price'], '%24h': q['percent_change_24h'], 'Vol24h': q['volume_24h']})
            except:
                continue
        df = pd.DataFrame(rows)
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV', '*.csv')])
        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Esporta CSV", f"Esportato in {path}")

    def fetch_crypto_data(self):
        sym = self.detail_entry.get().upper().strip()
        if not sym:
            messagebox.showerror("Errore", "Inserisci un simbolo.")
            return
        self.spinner.start()
        self.root.update()
        now = time.time()
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        if sym in self.cache and now - self.cache[sym][0] < self.cache_timeout:
            entry = self.cache[sym][1]
        else:
            r = requests.get(url, headers={"X-CMC_PRO_API_KEY": self.api_key}, params={"symbol": sym}).json()
            entry = r['data'][sym]
            self.cache[sym] = (now, entry)
        self.show_details(entry)
        self.spinner.stop()

    def show_details(self, entry):
        d = entry['quote']['USD']
        self.detail_tree.delete(*self.detail_tree.get_children())
        m = self.detail_tree.insert('', 'end', text='Mercato', open=True)
        for lbl, val in [('Prezzo', f"${d['price']:,.2f}"), ('Vol24h', f"${d['volume_24h']:,.0f}")]:
            self.detail_tree.insert(m, 'end', text=lbl, values=(val,))
        for p in ['percent_change_1h', 'percent_change_24h', 'percent_change_30d', 'percent_change_60d', 'percent_change_90d']:
            v = d.get(p)
            tag = 'positive' if v > 0 else 'negative' if v < 0 else ''
            sym = '▲' if v > 0 else '▼' if v < 0 else ''
            self.detail_tree.insert(m, 'end', text=f"Var%({p[-3:]})", values=(f"{v:.2f}% {sym}" if v is not None else 'N/A',), tags=(tag,))
        s = self.detail_tree.insert('', 'end', text='Supply', open=True)
        for lbl, key in [('Circolante', 'circulating_supply'), ('Totale', 'total_supply')]:
            self.detail_tree.insert(s, 'end', text=lbl, values=(f"{entry[key]:,.0f} {entry['symbol']}",))
        ms = entry.get('max_supply')
        self.detail_tree.insert(s, 'end', text='Massima', values=(f"{ms:,.0f} {entry['symbol']}" if ms else 'Non definita',))
        self.detail_tree.insert(s, 'end', text='UltAgg', values=(d['last_updated'][:19],))

    def calculate_value(self):
        try:
            amt = float(self.quantity_entry.get())
            sym = self.detail_entry.get().upper()
            price = self.cache[sym][1]['quote']['USD']['price']
            self.result_label.config(text=f"{amt} {sym} = ${amt*price:,.2f}")
        except:
            messagebox.showerror("Errore", "Quantità non valida.")

    def refresh_data(self):
        self.fetch_crypto_data()

if __name__ == '__main__':
    app = tb.Window(themename='darkly')
    CryptoAnalyzerApp(app)
    app.mainloop()