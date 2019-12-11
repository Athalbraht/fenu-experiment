#extensions.py

import os

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

def exp_imgs(folder):
	_exp_images = ["bina{}.jpg".format(i) for i in range(1,7)]
	_exp_images2 = ["hbina{}.jpg".format(i) for i in range(1,4)]
	_exp_images2.append("logo.png")
	exp_img = list(map(lambda x: os.path.join(folder, x), _exp_images+_exp_images2))
	return exp_img
