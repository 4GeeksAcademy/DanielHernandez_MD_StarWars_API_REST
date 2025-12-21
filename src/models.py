from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[int] = mapped_column(nullable=False)

    Favorites: Mapped[List["Favorites"]] = relationship(back_populates = "User")


class People(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    surname: Mapped[str] = mapped_column(nullable=False)
    birth_year: Mapped[str] = mapped_column(nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    films: Mapped[str] = mapped_column(nullable=False)
    planets: Mapped[str] = mapped_column(nullable=False)
    homeWorld: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[str] = mapped_column(nullable=False)
    skin_color: Mapped[str] = mapped_column(nullable=False)
    eye_color: Mapped[str] = mapped_column(nullable=False)
    hair_color: Mapped[str] = mapped_column(nullable=False)
    species: Mapped[str] = mapped_column(nullable=False)
    vehicles: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[int] = mapped_column(nullable=False)

    FavoritePeople: Mapped[List["FavoritePeople"]] = relationship(back_populates="People")

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    diameter: Mapped[int] = mapped_column(nullable=False)
    rotation_period: Mapped[str] = mapped_column(nullable=False)
    orbital_period: Mapped[str] = mapped_column(nullable=False)
    climate: Mapped[str] = mapped_column(nullable=False)
    terrain: Mapped[str] = mapped_column(nullable=False)
    surface: Mapped[str] = mapped_column(nullable=False)
    residents: Mapped[str] = mapped_column(nullable=False)
    films: Mapped[str] = mapped_column(nullable=False)
    url: Mapped[str] = mapped_column(nullable=False)
    date_created: Mapped[int] = mapped_column(nullable=False)

    FavoritePlanet: Mapped[List["FavoritePlanet"]] = relationship(back_populates="Planet")
    

    
class Favorites(db.Model):
    id: Mapped[int] = mapped_column(primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
    User: Mapped["User"] = relationship(back_populates="Favorites")

class FavoritePlanet(Favorites):
    id: Mapped[int] = mapped_column(primary_key = True)
    planet: Mapped[int] = mapped_column(ForeignKey("Planet.id"))
    Planet: Mapped["Planet"] = relationship(back_populates="FavoritePlanet")

class FavoritePeople(Favorites):
    id: Mapped[int] = mapped_column(primary_key = True)
    people: Mapped[int] = mapped_column(ForeignKey("People.id"))
    People: Mapped["People"] = relationship(back_populates="FavoritePeople")