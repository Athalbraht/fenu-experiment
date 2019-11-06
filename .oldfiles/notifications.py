##################################
# This file is a part of         #
# HelpDesk project               #
##################################

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

        temp = []
        c = []
        a = 0
        b = 0
        for lines in all_lines[::-1]:
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

def get_branches():
    import db_func as db
    _branches = db.get_info('branch', 'users', '0','0')
    branches = []
    for branch in _branches:
        branches.append(branch[0])
    all_branches = list(set(branches))
    return all_branches

def load_branches():
    with open('/var/www/FlaskApp/FlaskApp/config_files/branches.data') as file:
        branches = file.readlines()
        _branches = [ i[:-1] for i in branches ]
        return _branches


def decode_headers():
    headers = get_headers()
    inc = get_incidents()
    j = zip(headers, range(1, len(headers) + 1))
    incidents = []
    for i in inc:
        if len(i[1]) == 0:
            incidents.append(('0'+str(i[0][1]), i[0][0] ))
        else:
            for j in i[1]:
                incidents.append(('0'+str(i[0][1])+str(j[1]),str(i[0][0])+' '+str(j[0])))
    print headers
    print incidents
