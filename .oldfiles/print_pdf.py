import os
import subprocess as sp
# encoding=utf8
import sys
if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')


def fixed_pdf(user, kom, adr, dwys, dprzy, tresc, uzas, opis, dzak, dwyk, uzasz, akcepd, potw, zak):
    os.system('rm /var/FlaskApp/FlaskApp/static/temp.tex')
    try:
        file = open('/var/www/FlaskApp/FlaskApp/static/template.tex','r')
        lines = file.read()
        file.close()
        new_template = lines % (kom, adr, dwys, dprzy, tresc, uzas, opis, dzak, dwyk, uzasz, akcepd, potw, zak)

        saved_file = open('/var/www/FlaskApp/FlaskApp/static/temp.tex','w')
        saved_file.write(new_template)
        saved_file.close()

        comp = ['pdflatex','-interaction=nonstopmode', '-output-directory', '/var/www/FlaskApp/FlaskApp/static', '/var/www/FlaskApp/FlaskApp/static/temp.tex']

        compiled = sp.Popen(comp)

        return 'Compileted'
    except Exception as e:
        return str(e)
    finally:
        return None


