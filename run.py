from App import app
import config

from hyperdash import Experiment

exp = Experiment("fenu-exp.pl:h235")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="8000")
