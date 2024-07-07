# MODELO
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, DeclarativeBase, Mapped
from hash_bcrypt import hash_password, check_password
from typing import List

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'usuario'
    
    idusuario = Column(Integer, primary_key=True)
    username = Column(String(50))
    password = Column(String(50))

    items: Mapped[List["Item"]] = relationship(back_populates="user")


class Item(Base):
    __tablename__ = 'item'
    
    iditem = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)
    usuario_idusuario = Column(Integer, ForeignKey('usuario.idusuario'))
    
    user: Mapped["User"] = relationship(back_populates="items")



engine = create_engine('mysql+pymysql://taven:D&vT0peirA@10.200.228.21/modelo-despensa')
if engine:
    print("Conexão realizada com sucesso")

    # criar a sessão
    Session = sessionmaker(bind=engine)
    session = Session()

    # Adicionar um novo usuário
    # new_password = '123'
    # new_password_hashed = hash_password(new_password)
    # new_user = User(username='teste', password=new_password_hashed)
    # session.add(new_user)
    # session.commit()

    # Adicionar um item
    new_item = Item(name='trigo', quantity=1, usuario_idusuario=5)
    session.add(new_item)
    session.commit()

    session.close()