class User:
    def __init__(self, id, username, is_admin):
        self.id = id
        self.username = username
        self.is_admin = bool(is_admin)

    def __repr__(self):
        return f"<User {self.username} {'(Admin)' if self.is_admin else ''}>"


class Kategorie:
    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color  # HEX-String wie #RRGGBB

    def __repr__(self):
        return f"<Kategorie {self.name} ({self.color})>"


class Brief:
    def __init__(self, id, datum_erhalt, datum_verarbeitet, datum_frist,
                 typ, absender_empfaenger, betreff, notizen,
                 erledigt, user_id, kategorie_id):
        self.id = id
        self.datum_erhalt = datum_erhalt
        self.datum_verarbeitet = datum_verarbeitet
        self.datum_frist = datum_frist
        self.typ = typ
        self.absender_empfaenger = absender_empfaenger
        self.betreff = betreff
        self.notizen = notizen
        self.erledigt = bool(erledigt)
        self.user_id = user_id
        self.kategorie_id = kategorie_id

    def __repr__(self):
        return f"<Brief {self.betreff} ({'Erledigt' if self.erledigt else 'Offen'})>"
