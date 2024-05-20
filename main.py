import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet


# Funzione per la crittografia di un file
def crittografa_file():
    # Acquisire i file di input e output dall'utente
    file_da_criptare = filedialog.askopenfilename()
    if not file_da_criptare:
        return
    file_crittografato = filedialog.asksaveasfilename()
    if not file_crittografato:
        return

    # Acquisire la chiave di crittografia dall'utente
    chiave = get_chiave()
    if not chiave:
        return

    # Crittografare il file
    try:
        crittografa_con_chiave(file_da_criptare, file_crittografato, chiave)
        messagebox.showinfo("Successo", "File crittografato con successo!")
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile crittografare il file: {e}")


# Funzione per la decrittazione di un file
def decrittografa_file():
    # Acquisire i file di input e output dall'utente
    file_crittografato = filedialog.askopenfilename()
    if not file_crittografato:
        return
    file_decrittografato = filedialog.asksaveasfilename()
    if not file_decrittografato:
        return

    # Acquisire la chiave di decrittazione dall'utente
    chiave = get_chiave()
    if not chiave:
        return

    # Decrittografare il file
    try:
        decrittografa_con_chiave(file_crittografato, file_decrittografato, chiave)
        messagebox.showinfo("Successo", "File decrittografato con successo!")
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile decrittografare il file: {e}")


# Funzione per la gestione delle chiavi
def gestisci_chiavi():
    opzione = messagebox.askquestion(
        "Gestisci Chiavi", "Vuoi generare una nuova chiave?"
    )
    if opzione == "yes":
        chiave = Fernet.generate_key()
        with open("chiave.key", "wb") as chiave_file:
            chiave_file.write(chiave)
        messagebox.showinfo(
            "Chiave Generata",
            "Una nuova chiave è stata generata e salvata come 'chiave.key'.",
        )


# Funzioni ausiliare per la crittografia e la decrittazione
def crittografa_con_chiave(file_in, file_out, chiave):
    fernet = Fernet(chiave)
    with open(file_in, "rb") as f:
        dati = f.read()
    dati_crittografati = fernet.encrypt(dati)
    with open(file_out, "wb") as f:
        f.write(dati_crittografati)


def decrittografa_con_chiave(file_in, file_out, chiave):
    fernet = Fernet(chiave)
    with open(file_in, "rb") as f:
        dati_crittografati = f.read()
    dati_decrittografati = fernet.decrypt(dati_crittografati)
    with open(file_out, "wb") as f:
        f.write(dati_decrittografati)


# Funzione per l'acquisizione della chiave dall'utente
def get_chiave():
    chiave_file = filedialog.askopenfilename(
        title="Seleziona il file della chiave",
        filetypes=(("Key files", "*.key"), ("All files", "*.*")),
    )
    if not chiave_file:
        return None
    try:
        with open(chiave_file, "rb") as f:
            chiave = f.read()
        return chiave
    except Exception as e:
        messagebox.showerror("Errore", f"Impossibile leggere la chiave: {e}")
        return None


# Creare l'interfaccia grafica con Tkinter
root = tk.Tk()
root.title("Crittografia e Decrittazione File")

# Creare pulsanti per la crittografia, decrittazione e gestione delle chiavi
btn_crittografa = tk.Button(root, text="Crittografa File", command=crittografa_file)
btn_crittografa.pack(pady=10)

btn_decrittografa = tk.Button(
    root, text="Decrittografa File", command=decrittografa_file
)
btn_decrittografa.pack(pady=10)

btn_gestisci_chiavi = tk.Button(root, text="Gestisci Chiavi", command=gestisci_chiavi)
btn_gestisci_chiavi.pack(pady=10)

# Eseguire il main loop di Tkinter
root.mainloop()
