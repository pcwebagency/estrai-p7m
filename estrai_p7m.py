"""
estrai_p7m.py — Estrae i PDF da file .pdf.p7m in modo ricorsivo o singolo.

Dipendenza: asn1crypto  (inclusa nell'app da PyInstaller)
Nessun tool esterno richiesto (openssl non necessario).

Autore: Ing. Carmine Palermo
"""

import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext, ttk

import asn1crypto.cms as cms


def find_p7m_files(root: Path) -> list[Path]:
    return sorted(root.rglob("*.p7m"))


def dest_path(src: Path) -> Path:
    """
    doc.pdf.p7m      → doc.pdf
    doc.pdf.p7m.p7m  → doc.pdf.p7m  (estratto al passaggio successivo)
    """
    return src.with_suffix("")


def extract_p7m(src: Path) -> tuple[bool, str]:
    try:
        raw = src.read_bytes()
        ci = cms.ContentInfo.load(raw)
        payload = bytes(ci["content"]["encap_content_info"]["content"])
        dest = dest_path(src)
        dest.write_bytes(payload)
        return True, str(dest)
    except Exception as e:
        return False, str(e)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Estrai da P7M")
        self.resizable(True, True)
        self.minsize(660, 500)
        self._build_menu()
        self._build_ui()

    def _build_menu(self):
        menubar = tk.Menu(self)

        # Su Mac il menu "Info" va nella barra di sistema; su Windows appare nella finestra
        info_menu = tk.Menu(menubar, tearoff=0)
        info_menu.add_command(label="Credits", command=self._show_credits)
        menubar.add_cascade(label="Info", menu=info_menu)

        self.config(menu=menubar)

    def _show_credits(self):
        win = tk.Toplevel(self)
        win.title("Credits")
        win.resizable(False, False)
        win.grab_set()

        pad = 28
        tk.Label(win, text="Estrai da P7M", font=("Helvetica", 15, "bold")).pack(pady=(pad, 4))
        tk.Label(win, text="Versione 1.0  —  2026", font=("Helvetica", 10)).pack()
        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=pad, pady=14)
        tk.Label(win, text="Sviluppato da", font=("Helvetica", 10, "italic"), fg="#888888").pack()
        tk.Label(win, text="Ing. Carmine Palermo", font=("Helvetica", 13, "bold")).pack(pady=(2, 14))
        tk.Label(
            win,
            text="Estrazione documenti firmati digitalmente\n(formato CAdES .p7m)\nsenza dipendenze esterne.",
            font=("Helvetica", 10),
            justify="center",
            fg="#555555",
        ).pack(padx=pad)
        import webbrowser
        lnk = tk.Label(
            win, text="www.pcwebagency.it",
            font=("Helvetica", 10, "underline"),
            fg="#0066cc", cursor="hand2",
        )
        lnk.pack(pady=(10, 0))
        lnk.bind("<Button-1>", lambda e: webbrowser.open("https://www.pcwebagency.it"))
        ttk.Separator(win, orient="horizontal").pack(fill="x", padx=pad, pady=14)
        tk.Button(win, text="Chiudi", width=12, command=win.destroy).pack(pady=(0, pad))

        # Centra la finestra
        win.update_idletasks()
        x = self.winfo_x() + (self.winfo_width() - win.winfo_width()) // 2
        y = self.winfo_y() + (self.winfo_height() - win.winfo_height()) // 2
        win.geometry(f"+{x}+{y}")

    def _build_ui(self):
        pad = {"padx": 10, "pady": 4}

        # --- Notebook: Cartella / Singolo file ---
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="x", padx=10, pady=8)

        tab_folder = tk.Frame(self.notebook)
        self.notebook.add(tab_folder, text="  Cartella (ricorsivo)  ")

        tk.Label(tab_folder, text="Cartella:").pack(side="left", padx=(8, 2), pady=6)
        self.var_folder = tk.StringVar()
        tk.Entry(tab_folder, textvariable=self.var_folder, width=55).pack(
            side="left", padx=4, expand=True, fill="x"
        )
        tk.Button(tab_folder, text="Sfoglia…", command=self._browse_folder).pack(
            side="left", padx=(0, 8), pady=6
        )

        tab_file = tk.Frame(self.notebook)
        self.notebook.add(tab_file, text="  Singolo file  ")

        tk.Label(tab_file, text="File .p7m:").pack(side="left", padx=(8, 2), pady=6)
        self.var_file = tk.StringVar()
        tk.Entry(tab_file, textvariable=self.var_file, width=55).pack(
            side="left", padx=4, expand=True, fill="x"
        )
        tk.Button(tab_file, text="Sfoglia…", command=self._browse_file).pack(
            side="left", padx=(0, 8), pady=6
        )

        # --- Opzioni ---
        frm_opts = tk.Frame(self)
        frm_opts.pack(fill="x", **pad)
        self.var_overwrite = tk.BooleanVar(value=False)
        tk.Checkbutton(
            frm_opts, text="Sovrascrivi file PDF già esistenti",
            variable=self.var_overwrite,
        ).pack(side="left")

        # --- Barra avanzamento ---
        self.progress = ttk.Progressbar(self, mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=2)

        self.lbl_status = tk.Label(self, text="Pronto.", anchor="w")
        self.lbl_status.pack(fill="x", padx=10)

        # --- Log ---
        self.log = scrolledtext.ScrolledText(
            self, state="disabled", font=("Courier", 10), wrap="none"
        )
        self.log.pack(fill="both", expand=True, padx=10, pady=5)

        self.log.tag_config("ok",   foreground="#00cc44")
        self.log.tag_config("skip", foreground="#cccc00")
        self.log.tag_config("err",  foreground="#ff4444")
        self.log.tag_config("info", foreground="#ffffff")

        # --- Bottoni ---
        frm_btn = tk.Frame(self)
        frm_btn.pack(fill="x", padx=10, pady=8)

        self.btn_start = tk.Button(
            frm_btn, text="Avvia estrazione", width=20,
            bg="#007700", fg="white", command=self._start,
        )
        self.btn_start.pack(side="left", padx=4)

        tk.Button(frm_btn, text="Pulisci log", command=self._clear_log).pack(
            side="left", padx=4
        )

    # ------------------------------------------------------------------
    def _browse_folder(self):
        folder = filedialog.askdirectory(title="Seleziona la cartella principale")
        if folder:
            self.var_folder.set(folder)

    def _browse_file(self):
        path = filedialog.askopenfilename(
            title="Seleziona file .p7m",
            filetypes=[("File P7M firmati", "*.p7m"), ("Tutti i file", "*.*")],
        )
        if path:
            self.var_file.set(path)

    def _clear_log(self):
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def _log(self, msg: str, tag: str = ""):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n", tag)
        self.log.see("end")
        self.log.configure(state="disabled")

    def _set_status(self, msg: str):
        self.lbl_status.config(text=msg)

    # ------------------------------------------------------------------
    def _start(self):
        tab = self.notebook.index(self.notebook.select())

        if tab == 0:
            folder = self.var_folder.get().strip()
            if not folder:
                messagebox.showwarning("Attenzione", "Seleziona prima una cartella.")
                return
            root = Path(folder)
            if not root.is_dir():
                messagebox.showerror("Errore", f"Cartella non trovata:\n{folder}")
                return
            self.btn_start.config(state="disabled")
            threading.Thread(target=self._run_folder, args=(root,), daemon=True).start()
        else:
            fpath = self.var_file.get().strip()
            if not fpath:
                messagebox.showwarning("Attenzione", "Seleziona prima un file .p7m.")
                return
            p = Path(fpath)
            if not p.is_file():
                messagebox.showerror("Errore", f"File non trovato:\n{fpath}")
                return
            if not p.name.endswith(".p7m"):
                messagebox.showerror("Errore", "Il file selezionato non ha estensione .p7m")
                return
            self.btn_start.config(state="disabled")
            threading.Thread(target=self._run_single, args=(p,), daemon=True).start()

    # ------------------------------------------------------------------
    def _run_single(self, p7m: Path):
        overwrite = self.var_overwrite.get()
        dest = dest_path(p7m)

        self._log(f"File: {p7m}", "info")
        self.progress["maximum"] = 1
        self.progress["value"] = 0

        if dest.exists() and not overwrite:
            self._log(f"[SKIP]  {p7m.name}  (PDF già esistente)", "skip")
            self._set_status("Saltato — file già esistente.")
        else:
            success, detail = extract_p7m(p7m)
            if success:
                self._log(f"[OK]    {p7m.name}  →  {dest.name}", "ok")
                self._set_status(f"Estratto: {dest.name}")
            else:
                self._log(f"[ERR]   {p7m.name}  —  {detail}", "err")
                self._set_status("Errore durante l'estrazione.")

        self.progress["value"] = 1
        self.btn_start.config(state="normal")

    # ------------------------------------------------------------------
    def _run_folder(self, root: Path):
        overwrite = self.var_overwrite.get()

        self._log(f"Scansione in corso: {root}", "info")

        ok = skip = err = 0
        processed: set[Path] = set()
        pass_num = 0

        while True:
            files = [f for f in find_p7m_files(root) if f not in processed]
            if not files:
                break

            pass_num += 1
            if pass_num > 1:
                self._log(f"Passaggio {pass_num}: trovati {len(files)} .p7m annidati", "info")
            else:
                self._log(f"Trovati {len(files)} file .p7m", "info")

            self.progress["maximum"] = len(files)
            self.progress["value"] = 0

            for i, p7m in enumerate(files, 1):
                dest = dest_path(p7m)
                rel = p7m.relative_to(root)
                processed.add(p7m)

                if dest.exists() and not overwrite:
                    self._log(f"[SKIP]  {rel}", "skip")
                    skip += 1
                else:
                    success, detail = extract_p7m(p7m)
                    if success:
                        self._log(f"[OK]    {rel}  →  {dest.name}", "ok")
                        ok += 1
                    else:
                        self._log(f"[ERR]   {rel}  —  {detail}", "err")
                        err += 1

                self.progress["value"] = i
                self._set_status(
                    f"Passaggio {pass_num} — {i}/{len(files)}  OK:{ok}  Skip:{skip}  Errori:{err}"
                )

        if ok == 0 and skip == 0 and err == 0:
            self._log("Nessun file .p7m trovato.", "skip")
            self._set_status("Nessun file trovato.")
        else:
            summary = f"Completato.  Estratti: {ok}  |  Saltati: {skip}  |  Errori: {err}"
            self._log("─" * 60, "info")
            self._log(summary, "info")
            self._set_status(summary)

        self.btn_start.config(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()
