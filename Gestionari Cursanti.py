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


def cursanti_inregistrare():
    nume = input("Adaugati numele:\n")
    prenume = input("Adaugati prenumele:\n")
    cnp = input("Adaugati CNP-ul:\n")
    ok1, erori_cnp = validare_cnp(cnp)
    ok2, erori_nume_prenume = validare_nume_prenume(nume, prenume)
    if ok1 == 0 and ok2 == 0:  # ok = 0 => datele sunt valide
        data = {
            'NUME': nume,
            'PRENUME': prenume,
            'CNP': cnp
        }
        lista = list(data.values())  # adaugam in lista din dictionar doar valorile, nu si cheile

        fisier = input("Ce fel de fisier doriti:\nCSV sau TXT?")
        if fisier == "CSV":
            file_exists = os.path.isfile('datafinal.csv')
            with open('datafinal.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:  # pentru a adauga in fisier coloanele nume, prenume si cnp daca fisierul nu exista
                    # sau este gol
                    writer.writerow(['NUME', 'PRENUME', 'CNP'])
                writer.writerow(lista)
                open_csv()

        elif fisier == "TXT":
            with open('datafinal.txt', 'a') as file:
                if os.path.getsize('datafinal.txt') == 0:  # daca fisierul este gol
                    file.write('NUME, PRENUME, CNP\n')
                file.write(f"{nume}, {prenume}, {cnp}\n")
                open_txt()
        print("Datele au fost adaugate!")
    else:
        print("Datele introduse nu sunt valide!")
        for i in erori_cnp:
            print(i)
        for i in erori_nume_prenume:
            print(i)


cursanti_inregistrare()
