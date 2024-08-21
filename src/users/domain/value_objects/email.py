import re


class Email:
    email: str

    def __init__(self):
        regex = r"^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$"
        if re.match(regex, self.email) is None:
            return TypeError("El email introducido no es válido")
        else:
            pass
