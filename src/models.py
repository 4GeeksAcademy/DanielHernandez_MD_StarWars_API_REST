from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
import enum

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(20), nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable = False)
    date_created: Mapped[int] = mapped_column(nullable=False)
    
    favorite_people: Mapped[list['FavoritePeople']] = relationship(back_populates='user')
    favorite_starships: Mapped[list['FavoriteStarships']] = relationship(back_populates='user')
    favorite_planets: Mapped[list['FavoritePlanets']] = relationship(back_populates='user')
    

class GenderEnum(enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    DROID = 'droid'

class People(db.Model):
    __tablename__ = 'people'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    gender: Mapped[GenderEnum] = mapped_column(db.Enum(GenderEnum), nullable= False)
    height: Mapped[int] = mapped_column(Integer, nullable=False)
    favorite_by: Mapped[List['FavoritePeople']] = relationship(back_populates='people')

class Starship(db.Model):
    __tablename__ = 'starship'
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(50), nullable= False)
    cost_in_credits: Mapped[int] = mapped_column(Integer, nullable= False)
    speed: Mapped[int] = mapped_column(Integer, nullable= False)
    favorite_by: Mapped[list['FavoriteStarships']] = relationship(back_populates='starship')   

class Planet(db.Model):
    __tablename__ = 'planet'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50),nullable=False)
    size: Mapped[int] = mapped_column(Integer,nullable=False)
    population: Mapped[int] = mapped_column(Integer,nullable=False)
    climate: Mapped[str] = mapped_column(String(100), nullable= False)
    favorite_by: Mapped[List['FavoritePlanets']] = relationship(back_populates='planet')

class FavoritePeople(db.Model):
    __tablename__ = 'favorite_people'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorite_people')   
    people_id: Mapped[int] = mapped_column(ForeignKey('people.id'))
    people: Mapped['People'] = relationship(back_populates='favorite_by')   

class FavoriteStarships(db.Model):
    __tablename__ = 'favorite_starships'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates = 'favorite_starships')
    starship_id: Mapped[int] = mapped_column(ForeignKey('starship.id'))
    starship: Mapped['Starship'] = relationship(back_populates='favorite_by')

class FavoritePlanets(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    user: Mapped['User'] = relationship(back_populates='favorite_planets') 
    planet_id: Mapped[int] = mapped_column(ForeignKey('planet.id'))
    planet: Mapped['Planet'] = relationship(back_populates= 'favorite_by')
