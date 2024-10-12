"""from ..extensions import db


class contact_service:
    @staticmethod
    def saveContact(contact):
        try:
            db.session.add(contact)
            db.session.commit()
            print("contact commit success")
        except Exception as e:
            raise e
"""