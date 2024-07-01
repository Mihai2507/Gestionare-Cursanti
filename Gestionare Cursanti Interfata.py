import csv
import os
import tkinter as tk


def validare_cnp(cnp):
    erori_cnp = []
    ok_cnp = 0
    if len(cnp) != 13:  # lungimea CNP-ului
        erori_cnp.append("CNP-ul trebuie să aiba 13 caractere!")
        ok_cnp = 1
    elif cnp[0] not in '12345678':  # începutul CNP-ului
        erori_cnp.append("CNP-ul nu trebuie sa inceapa cu 0 sau 9!")
        ok_cnp = 1
    else:
        valoare_ct = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]  # valoarea constanta cu care se inmultește CNP-ul
        suma = sum(int(cnp[i]) * valoare_ct[i] for i in range(12))
        cifra_control = suma % 11  # formula dupa care calculam ultima cifra a CNP-ului
        if cifra_control == 10:
            cifra_control = 1
        if cifra_control != int(cnp[12]):
            erori_cnp.append("Ultima cifra a CNP-ului nu este corecta!")
            ok_cnp = 1
    return ok_cnp, erori_cnp


def validare_nume_prenume(nume, prenume):
    erori_nume_prenume = []
    car_interzise = set("@/+=?!;<>#$&*()%~")
    ok_nume_prenume = 0
    if any(char in car_interzise for char in nume):
        erori_nume_prenume.append("Numele are caractere interzise!")
        ok_nume_prenume = 1
    if any(char in car_interzise for char in prenume):
        erori_nume_prenume.append("Prenumele are caractere interzise!")
        ok_nume_prenume = 1
    for i in nume:
        if i.isdigit():
            erori_nume_prenume.append("Numele nu trebuie sa contina cifre!")
            ok_nume_prenume = 1
            break
    for j in prenume:
        if j.isdigit():
            erori_nume_prenume.append("Prenumele nu trebuie sa contina cifre!")
            ok_nume_prenume = 1
            break
    return ok_nume_prenume, erori_nume_prenume


def open_csv():  # pentru a deschide fisierul excel daca avem o inregistrare cu succes
    if os.name == 'nt':  # pt windows
        os.startfile('datafinal.csv')
    else:  # pt linux
        os.system('open datafinal.csv')


def open_txt():  # pentru a deschide fisierul text daca avem o inregistrare cu succes
    if os.name == 'nt':
        os.startfile('datafinal.txt')
    else:
        os.system('open datafinal.txt')


def cursanti_inregistrare(event=None):
    nume = entry_nume.get()
    prenume = entry_prenume.get()
    cnp = entry_cnp.get()
    ok1, erori_cnp = validare_cnp(cnp)
    ok2, erori_nume_prenume = validare_nume_prenume(nume, prenume)

    if ok1 == 0 and ok2 == 0:  # ok = 0 => datele sunt valide
        data = {
            'NUME': nume,
            'PRENUME': prenume,
            'CNP': cnp
        }
        lista = list(data.values())  # adaugam in lista din dictionar doar valorile, nu si cheile

        # Save data to CSV
        file_exists = os.path.isfile('datafinal.csv')
        with open('datafinal.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:  # pentru a adauga in fisier coloanele nume, prenume si cnp daca fisierul nu exista
                # sau este gol
                writer.writerow(['NUME', 'PRENUME', 'CNP'])
            writer.writerow(lista)

        # Save data to TXT
        with open('datafinal.txt', 'a') as file:
            if os.path.getsize('datafinal.txt') == 0:  # daca fisierul este gol
                file.write('NUME, PRENUME, CNP\n')
            file.write(f"{nume}, {prenume}, {cnp}\n")

        eroare.set("Datele au fost adaugate!")
        label_erori_cnp.config(text="")
        label_erori_nume_prenume.config(text="")

        # Show appropriate buttons based on the format
        if var_format.get() == 'csv':
            open_csv()
        elif var_format.get() == 'txt':
            open_txt()
    else:
        eroare.set("Datele introduse nu sunt valide!")
        label_erori_cnp.config(text="\n".join(erori_cnp))  # ne arata fiecare eroare pe cate o linie
        label_erori_nume_prenume.config(text="\n".join(erori_nume_prenume))


root = tk.Tk()
root.title("Inregistrare cursant")  # titlul interfetei

label_nume = tk.Label(root, text="Nume:", font=("Helvetica", 12))
label_nume.grid(row=0, column=0, padx=10, pady=10)  # unde asezam
entry_nume = tk.Entry(root)  # "chenarul" unde scriem numele
entry_nume.grid(row=0, column=1, padx=10, pady=10)

label_prenume = tk.Label(root, text="Prenume:", font=("Helvetica", 12))
label_prenume.grid(row=1, column=0, padx=10, pady=10)
entry_prenume = tk.Entry(root)
entry_prenume.grid(row=1, column=1, padx=10, pady=10)  # "chenarul" unde scriem prenumele

label_cnp = tk.Label(root, text="CNP:", font=("Helvetica", 12))
label_cnp.grid(row=2, column=0, padx=10, pady=10)
entry_cnp = tk.Entry(root)
entry_cnp.grid(row=2, column=1, padx=10, pady=10)  # "chenarul" unde scriem cnp-ul

var_format = tk.StringVar(value="csv")
label_format = tk.Label(root, text="Selecteaza formatul:", font=("Helvetica", 12))
label_format.grid(row=3, column=0, padx=10, pady=10)

radio_csv = tk.Radiobutton(root, text="CSV", variable=var_format, value="csv", font=("Helvetica", 12))
radio_csv.grid(row=3, column=1, padx=10, pady=10)
radio_txt = tk.Radiobutton(root, text="TXT", variable=var_format, value="txt", font=("Helvetica", 12))
radio_txt.grid(row=4, column=1, padx=10, pady=10)

eroare = tk.StringVar()
label_eroare = tk.Label(root, textvariable=eroare, fg="red", font=("Helvetica", 12))
label_eroare.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

button_adauga = tk.Button(root, text="Adauga inregistrare", fg="blue", command=cursanti_inregistrare,
                          font=("Helvetica", 12))
button_adauga.grid(row=6, column=0, columnspan=2, padx=10, pady=10)  # butonul de adaugare


root.bind("<Return>", cursanti_inregistrare)  # putem apasa si enter

label_erori_cnp = tk.Label(root, fg="red", font=("Helvetica", 12))
label_erori_cnp.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# avem erorile in caz ca nu este ok inregistrarea
label_erori_nume_prenume = tk.Label(root, fg="red", font=("Helvetica", 12))
label_erori_nume_prenume.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

iconita = tk.PhotoImage(file="C:/Users/Mihai/Desktop/snake.png")
root.iconphoto(True, iconita)

root.mainloop()
