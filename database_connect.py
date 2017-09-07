import MySQLdb

def connection():
    conn = MySQLdb.connect(host="localhost",
                           user = "root",
                           passwd = "3y0q5rZkn",
                           db = "helpdesk")
    c = conn.cursor()
    return c, conn