import database.basedados
from database.basedados import Usuario

session = database.basedados.getSession()
users = session.query(Usuario).all()
for user in users:
        print(f"{user.id} | {user.nome} | {user.email} | {user.criadoEm}")
