# from api.model import Files, Links, Payments
# import secrets
# from api.extensions import db
#
#
# class aws_service:
#     def __init__(self):
#         pass
#
#     @staticmethod
#     def CreateLink(user):
#         try:
#             token = secrets.token_urlsafe()
#             new_link = Links(link_name=token, id_user=user)
#             db.session.add(new_link)
#             db.session.commit()
#             print(f"id: {new_link.id_link}")
#             print(f"link object : {new_link}")
#             print(f"link created successfully => {user}: {token}")
#             return new_link.id_link, token
#         except Exception as e:
#             raise e
#
#     @staticmethod
#     def StoreFile(id_link, file_name, id_user):
#         try:
#             new_file = Files(file_name=file_name, id_link=id_link, id_user=id_user)
#             db.session.add(new_file)
#             db.session.commit()
#
#             print(f"file stored successfully => {file_name} : {id_link} - {id_user}")
#         except Exception as e:
#             raise e
#
#     @staticmethod
#     def getFileName(link):
#         try:
#             res = Links.query.filter_by(link_name=link).with_entities(Links.id_link).first()
#             if res:
#                 print(f"test res id: {res.id_link}")
#                 file = Files.query.filter_by(id_link=res.id_link).first()
#                 print(file)
#                 return file
#             return None
#         except Exception as e:
#             print(e)
#             raise e
#
