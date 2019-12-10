# models.py

def check_password(passwd):
    if passwd == "changeme":
        return "Correct password", True
    else:
        return "Wrong password. Try again.", False

def get_var(session):
	var = {
				"status":session["status"],
				"guest":session["guest"],
				"login":session["logged_in"],
				"admin":session["admin"],
				}
	return var
