import sys

if sys.version_info.major < 3:
    reload(sys)
sys.setdefaultencoding('utf8')

def get_headers():
    with open('/var/www/FlaskApp/FlaskApp/config_files/typy_zlecen.config', 'r') as file:
        all_lines = [ i.decode('utf-8') for i in file.readlines() if i[0] != '\n' ]
        return all_lines

def get_incidents():
    with open('/var/www/FlaskApp/FlaskApp/config_files/incydenty.config', 'r') as file:
        all_lines = file.readlines()
        _all_lines = [ i for i in all_lines if (i[0]!='#' and i[0]!='\n') ].reverse()
        temp = []
        c = []
        a = 0
        b = 0
        for lines in all_lines:
            if lines[0] != '#' and lines[0] != '\n':
                if lines[0] == ' ':
                    c.append([lines, str(b)])
                    b += 1
                else:
                    temp.append([[lines, str(a)], c])
                    c = []
                    a += 1
                    b = 0
        return temp
