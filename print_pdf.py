import os

# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def print_pdf(user, kom, adr, dwys, dprzy, tresc, uzas, opis, dzak, dwyk, uzasz, akcepd, potw, zak):
    os.system('rm -rf /tmp/{}'.format(user))
    os.system('mkdir /tmp/{}'.format(user))
    _ttemplate = '''\\documentclass[11pt,a4paper]{article}\n\\usepackage{graphicx}\n\\usepackage{lipsum}\n\\usepackage{wrapfig}\n\\setlength{\\headheight}{12pt} \n\\setlength{\\textheight}{25cm}\n\\setlength{\\textwidth}{17cm}\n\\setlength{\\footskip}{10mm}\n\\setlength{\\oddsidemargin}{0mm}\n\\setlength{\\evensidemargin}{0mm}\n\\setlength{\\topmargin}{0mm}\n\\setlength{\\headsep}{10mm}\n\\usepackage{geometry}\n\\usepackage{tabularx, colortbl}\n\\usepackage{fancyhdr}\n\\usepackage[T1]{fontenc}\n\\usepackage[polish]{babel}\n\\usepackage[utf8]{inputenc}\n\\usepackage{lmodern}\n\\selectlanguage{polish}\n\\newgeometry{rmargin=1.5cm,lmargin=0.1cm,bmargin=1cm,tmargin=0.2cm}\n\n\n\n\\begin{document}\n\\begin{tabularx}{\\linewidth}{X}\n\\begin{center}\nZLECENIE WYKONANIA PRAC lub DOKONANIA ZAKUPU\n\\end{center}\n\\end{tabularx}\n\n\\begin{tabularx}{\\textwidth}{|X|X|X|X|}\n\\hline\n{\\scriptsize \\textbf{Komórka zlecająca:}}\\newline\n\\newline\n%s \\newline\n& {\\scriptsize \\textbf{Adresat:}}\\newline\n\\newline\n%s \\newline \n& {\\scriptsize \\textbf{Data wystawienia zlecenia:}}\\newline\n\\newline\n%s \\newline\n& {\\scriptsize \\textbf{Data przyjęcia zlecenia:}}\\newline\n\\newline\n%s \\newline\n\\\\ \\hline\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|}\n{\\footnotesize \\textbf{Treść zlecenia:}}\\newline\n\n%s  \n\n\\\\\n\\end{tabularx}\n\n\n\\begin{tabularx}{\\linewidth}{|X|}\n{\\footnotesize \\textbf{Uzasadnienie potrzeby realizacji zlecenia:}}\\newline\n\n%s  \n\n\\\\\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|}\n\n\\hspace{14.5cm} {\\scriptsize ......................................} \\newline .\n\\hspace{14.5cm} {\\scriptsize Podpis kierownika} \\newline .\n\\hspace{14.2cm} {\\scriptsize lub osoby upoważnionej}\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|}\n{\\tiny \\textbf{Uwaga!} W odniesieniu do artykułów o wymaganych parametrach technicznych (dotyczy również rozmiaru) prosimy o podanie tych parametrów}\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|}\n\\hline\n\\rowcolor[gray]{.7}\nWYPEŁNIA KOMÓRKA REALIZUJĄCA ZLECENIE:\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|}\n\\hline\n{\\footnotesize \\textbf{Opis wykonanych prac lub wniosek o zakup:}}\\newline\n\n%s  \n\n\\\\\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X|X|}\n\\hline\n{\\footnotesize \\textbf{Data i podpis osoby wnioskującej o zakup}} \\newline\n\n%s \\hspace{1cm} .....................................\n\n&\n{\\footnotesize \\textbf{Data i podpis osoby wykonującej zlecenie}} \\newline\n\n%s \\hspace{1cm} .....................................\n\n\n\\end{tabularx}\n\n\n\n\\begin{tabularx}{\\linewidth}{|X|}\n\\hline\n\n{\\footnotesize \\textbf{Uzasadnienie zakupu}}\\newline\n\n%s  \n\n\\end{tabularx}\n\n\\begin{tabularx}{\\linewidth}{|X X|}\n\n&  \n{\\footnotesize \\textbf{Akceptacja Dyrektora lub osoby upoważnionej}}\\newline\n\n%s \\hspace{1cm} .....................................\n\n\n\\\\ \n\\end{tabularx}\n\n\n\n\n\\begin{tabularx}{\\linewidth}{|X|X|}\n\\hline\n{\\footnotesize \\textbf{Zakończenie zlecenia}}\\newline\n\n%s \\hspace{1cm} ..................................... \\newline\n\n{\\scriptsize Data i podpis Kierownika komórki wystawiającej zlecenie }\n&\n{\\footnotesize \\textbf{Potwierdzenie wykonania zlecenia*}}\\newline\n\n%s \\hspace{1cm} ..................................... \\newline\n\n{\\scriptsize Data i podpis Kierownika komórki wystawiającej zlecenie }\n\\\\ \\hline\n\n\n\\end{tabularx}\n\\begin{center}\n{\\scriptsize SSz Zał. Nr1 do Zarządzenia Dyrektora Specjalistycznego Szpitala  nr 13/2008 z dnia 30.04.2008 obowiązujący od 1.05.2008}\n\\end{center}\n\\end{document}\n''' % (
    kom, adr, dwys, dprzy, tresc, uzas, opis, dzak, dwyk, uzasz, akcepd, potw, zak)

    _template = _ttemplate.decode('utf-8')
    with open('/tmp/template.tex', 'w') as file:
        file.write(_template)
        file.close()
        os.system('pdflatex -output-directory /tmp/{} /tmp/template.tex'.format(user))
        return 'Done'


def load():
    with open('/tmp/toprint.txt', 'r') as file:
        a = file.readlines()
        b = [i[:-1] for i in a]
        print(b)
        print_pdf('1',b[0]+' '+b[1],b[2],b[3],b[4],b[5],b[6],b[7],b[8],b[9],b[10],b[11],b[12],b[13])


load()