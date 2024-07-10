import csv
import os
from time import strftime
import glob


def validare_cnp(cnp):
    erori_cnp = []
    ok_cnp = 0
    if len(cnp) != 13:
        erori_cnp.append("CNP-ul trebuie să aibă 13 caractere!")
        ok_cnp = 1
    elif cnp[0] not in '12345678':
        erori_cnp.append("CNP-ul nu trebuie să înceapă cu 0 sau 9!")
        ok_cnp = 1
    elif cnp == " ":
        erori_cnp.append("CNP-ul este gol!")
        ok_cnp = 1
    elif cnp.isalpha():
        erori_cnp.append("CNP-ul nu are litere!")
        ok_cnp = 1
    else:
        valoare_ct = [2, 7, 9, 1, 4, 6, 3, 5, 8, 2, 7, 9]
        suma = sum(int(cnp[i]) * valoare_ct[i] for i in range(12))
        cifra_control = suma % 11
        if cifra_control == 10:
            cifra_control = 1
        if cifra_control != int(cnp[12]):
            erori_cnp.append("Ultima cifră a CNP-ului nu este corectă!")
            ok_cnp = 1
    return ok_cnp, erori_cnp


def validare_nume_prenume(nume, prenume):
    erori_nume_prenume = []
    car_interzise = set("@/+=?!;<>#$&*()%~':[]{}")
    ok_nume_prenume = 0
    if any(char in car_interzise for char in nume):
        erori_nume_prenume.append("Numele are caractere interzise!")
        ok_nume_prenume = 1
    if any(char in car_interzise for char in prenume):
        erori_nume_prenume.append("Prenumele are caractere interzise!")
        ok_nume_prenume = 1
    if any(i.isdigit() for i in nume):
        erori_nume_prenume.append("Numele nu trebuie să conțină cifre!")
        ok_nume_prenume = 1
    if any(j.isdigit() for j in prenume):
        erori_nume_prenume.append("Prenumele nu trebuie să conțină cifre!")
        ok_nume_prenume = 1
    if nume == " ":
        erori_nume_prenume.append("Numele este gol!")
        ok_nume_prenume = 1
    if prenume == " ":
        erori_nume_prenume.append("Prenumele este gol!")
        ok_nume_prenume = 1
    return ok_nume_prenume, erori_nume_prenume


def open_csv(filename):
    if os.name == 'nt':
        os.startfile(filename)
    else:
        os.system(filename)


def open_txt(filename):
    if os.name == 'nt':
        os.startfile(filename)
    else:
        os.system(filename)


def getId():
    all_files = glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.[ct][sx][tv]")
    max_id = 0
    for filename in all_files:
        with open(filename, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)
            id_uri = [int(row[0]) for row in reader if row[0].isdigit()]
            if id_uri:
                max_id = max(max_id, max(id_uri))
    return max_id + 1


def stergere_cnp_txt(cnpsters):
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.txt"):
        with open(filename, "r") as filetxt:
            lines = filetxt.readlines()
        with open(filename, "w") as filetxt:
            for line in lines:
                linie = line.split(',')
                if len(linie) > 3 and linie[3].strip() == cnpsters:
                    print(line.rstrip(), "a fost șters din fisierul", filename)
                else:
                    filetxt.write(line)


def stergere_cnp_csv(cnpsters):
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.csv"):
        with open(filename, "r") as filecsv:
            lines = filecsv.readlines()
        with open(filename, "w") as filecsv:
            for line in lines:
                linie = line.split(',')
                if len(linie) > 3 and linie[3].strip() == cnpsters:
                    print(line.rstrip(), "a fost șters din fisierul", filename)
                else:
                    filecsv.write(line)


def stergere_csv(idsters):
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.csv"):
        with open(filename, "r") as filecsv:
            lines = filecsv.readlines()
        with open(filename, "w") as filecsv:
            for line in lines:
                linie = line.split(',')
                if linie[0] == idsters:
                    print(line.rstrip(), "a fost șters din fisierul", filename)
                else:
                    filecsv.write(line)


def stergere_txt(idsters):
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.txt"):
        with open(filename, "r") as filetxt:
            lines = filetxt.readlines()
        with open(filename, "w") as filetxt:
            for line in lines:
                linie = line.split(',')
                if linie[0] == idsters:
                    print(line.rstrip(), "a fost șters din fisierul", filename)
                else:
                    filetxt.write(line)


def elimina_duplicate():
    cnp_set = set()
    duplicate_list = []
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.csv"):
        with open(filename, "r") as filecsv:
            reader = csv.reader(filecsv)
            lines = list(reader)
        with open(filename, "w", newline='') as filecsv:
            writer = csv.writer(filecsv)
            for line in lines:
                if line[0] == 'ID': 
                    writer.writerow(line)
                elif line[3] in cnp_set:
                    duplicate_list.append(line)
                else:
                    cnp_set.add(line[3])
                    writer.writerow(line)
    for filename in glob.glob("C:/Users/Mihai/Gestionare Cursanti/*.txt"):
        with open(filename, "r") as filetxt:
            lines = filetxt.readlines()
        with open(filename, "w") as filetxt:
            for line in lines:
                linie = line.split(',')
                if linie[0] == 'ID': 
                    filetxt.write(line)
                elif linie[3].strip() in cnp_set:
                    duplicate_list.append(linie)
                else:
                    cnp_set.add(linie[3].strip())
                    filetxt.write(line)
    return duplicate_list


def cursanti_inregistrare():
    while True:
        nume = input("Adăugați numele:\n")
        prenume = input("Adăugați prenumele:\n")
        cnp = input("Adăugați CNP-ul:\n")
        ok1, erori_cnp = validare_cnp(cnp)
        ok2, erori_nume_prenume = validare_nume_prenume(nume, prenume)
        if ok1 == 0 and ok2 == 0:
            data = {
                'NUME': nume,
                'PRENUME': prenume,
                'CNP': cnp
            }
            fisier = input("Ce fel de fișier doriți?\nTXT sau CSV?\n")
            filename = "C:/Users/Mihai/Gestionare Cursanti/" + strftime("%Y-%m-%d %H-%M") + f".{fisier.lower()}"
            ID = getId()
            if fisier.lower() == "csv":
                lista = [ID] + list(data.values())
                file_exists = os.path.isfile(filename)
                with open(filename, 'a', newline='') as file:
                    writer = csv.writer(file)
                    if not file_exists:
                        writer.writerow(['ID', 'NUME', 'PRENUME', 'CNP'])
                    writer.writerow(lista)
                    open_csv(filename)
            elif fisier.lower() == "txt":
                with open(filename, 'a') as file:
                    if os.path.getsize(filename) == 0:
                        file.write('ID, NUME, PRENUME, CNP\n')
                    file.write(f"{ID}, {nume}, {prenume}, {cnp}\n")
                    open_txt(filename)

            print("Datele au fost adăugate!")
            stergere = input("Doriți să ștergeți un anumit ID sau CNP?\nID/CNP/N\n")

            if stergere.lower() == "id":
                tip_stergere = input("Din ce fel de fișier doriți să ștergeți?\nCSV sau TXT?\n")
                if tip_stergere.lower() == "csv":
                    idsters = input("Ce ID doriți să ștergeți?:\n")
                    stergere_csv(idsters)
                    open_csv(filename)
                elif tip_stergere.lower() == "txt":
                    idsters = input("Ce ID doriți să ștergeți?:\n")
                    stergere_txt(idsters)
            elif stergere.lower() == "cnp":
                tip_stergere = input("Din ce fel de fișier doriți să ștergeți?\nCSV sau TXT?\n")
                if tip_stergere.lower() == "csv":
                    cnpsters = input("Ce CNP doriți să ștergeți?:\n")
                    stergere_cnp_csv(cnpsters)
                elif tip_stergere.lower() == "txt":
                    cnpsters = input("Ce CNP doriți să ștergeți?:\n")
                    stergere_cnp_txt(cnpsters)
            din_nou = input("Doriți să încercați din nou să înregistrați un cursant?\nY/N\n")
            if din_nou.lower() != "y":
                break
        else:
            print("Datele introduse nu sunt valide!")
            for i in erori_cnp:
                print(i)
            for i in erori_nume_prenume:
                print(i)
            din_nou = input("Doriți să încercați din nou să înregistrați un cursant?\nY/N\n")
            if din_nou.lower() != "y":
                break


if __name__ == "__main__":
    cursanti_inregistrare()
    duplicate_list = elimina_duplicate()
    print("Duplicatele gasite sunt:")
    for dup in duplicate_list:
        print(dup)
