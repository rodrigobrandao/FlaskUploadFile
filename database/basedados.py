from sqlalchemy import create_engine, DateTime, Column, Integer, String, LargeBinary, BLOB,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Usuario(Base):
        __tablename__ = "tbUsuario"
        id = Column("Id", Integer, autoincrement=True, primary_key=True)
        nome = Column('Nome', String(40))
        email = Column('Email', String(4))
        criadoEm = Column("CriadoEm", DateTime, default=datetime.now)

class Release(Base):
        __tablename__ = "tbRelease"
        id = Column("Id", Integer, autoincrement=True, primary_key=True)
        titulo = Column('Titulo', String(40))
        user_id = Column(Integer, ForeignKey('tbUsuario.Id'))

class ReleaseDetalhe(Base):
        __tablename__ = "tbReleaseDetalhe"
        id = Column("Id", Integer, primary_key=True)
        titulo = Column('Titulo', String(40))
        area = Column('Area', String)
        time = Column('Time', String)
        descricao = Column('Descricao', String)
        image01 = Column(LargeBinary)
        image02 = Column(LargeBinary)
        releaase_id = Column(Integer, ForeignKey('tbRelease.Id'))
        
def getSession():

        engine = create_engine('sqlite:///BaseSample.db', echo=False)
        Base.metadata.create_all(bind=engine)
        Session = sessionmaker(bind=engine)

        session = Session()
        return session

def __initDataTables():
        session = getSession()
        session.query(ReleaseDetalhe).delete()
        session.query(Release).delete()
        session.query(Usuario).delete()
        session.commit()

        user = Usuario()
        user.nome = "Rodrigo Brandao"
        user.email = "rodrigo.brandao@gmail.com"
        session.add(user)

        user = Usuario()
        user.nome = "Fabiana Mazurega"
        user.email = "fafa.mazurega@gmail.com"
        session.add(user)

        user = Usuario()
        user.nome = "Joaquim Duarte Brandão"
        user.email = "joaquimd.brandao@gmail.com"
        session.add(user)

        release = Release()
        release.titulo = "Release 4.50"
        release.user_id = 1
        session.add(release)

        #releaseDet = ReleaseDetalhe()
        #releaseDet.id = 1
        #releaseDet.titulo = "Entrega 01"
        #releaseDet.area = "Alpha"
        #releaseDet.time = "Heats"
        #releaseDet.releaase_id = release.id
        #session.add(releaseDet)

        session.commit()
        session.close()

def getRelease(id):

        session = getSession()
        release = session.query(Release).filter(Release.id == id).first()
        entregas = session.query(ReleaseDetalhe).filter(Release.id == id).all()
        return release, entregas

def deleteEntregavel(idEntregavel):

        session = getSession()
        entrega = session.query(ReleaseDetalhe).filter(ReleaseDetalhe.id == idEntregavel).first()
        session.delete(entrega)
        session.commit()


def getUsuarios():

        session = getSession()
        users = session.query(Usuario).all()
        
        return users

def __runQuerys():
        
        session = getSession()
        users = session.query(Usuario).all()
        for user in users:
                print(f"{user.id} | {user.nome} | {user.email} | {user.criadoEm}")

        releases = session.query(Release).all()
        for release in releases:
                print(f"{release.id} | {release.titulo} | {release.user_id} ")

        releasesDet = session.query(ReleaseDetalhe).all()
        for r in releasesDet:
                print(f"{r.titulo} | {r.area} | {r.time} ")

        session.close()

#__initDataTables()
#__runQuerys()