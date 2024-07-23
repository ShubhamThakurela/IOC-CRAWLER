from .paths import KEYFILE_PATH


class LoginConfig(object):
    def __init__(self):
        self.jwt_key = None
        self.load_keyfile()

    def load_keyfile(self):
        path = KEYFILE_PATH
        with open(path, "r") as f:
            self.jwt_key = f.readline()

    def get_jwt_key(self):
        return self.jwt_key
