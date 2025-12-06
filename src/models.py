from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    planets: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="user")
    people: Mapped[List["FavoritePeople"]] = relationship("FavoritePeople", back_populates="user")

    def serialize(self):
        return {"id": self.id, "email": self.email}


class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    species: Mapped[str] = mapped_column(String(40), nullable=False)

    favorites: Mapped[List["FavoritePeople"]] = relationship("FavoritePeople", back_populates="person")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "species": self.species,
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(40), nullable=False)
    rotation_period: Mapped[int] = mapped_column(Integer, nullable=False)
    gravity: Mapped[str] = mapped_column(String(40), nullable=False)
    terrain: Mapped[str] = mapped_column(String(40), nullable=False)

    favorites: Mapped[List["FavoritePlanet"]] = relationship("FavoritePlanet", back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "rotation_period": self.rotation_period,
            "gravity": self.gravity,
            "terrain": self.terrain,
        }


class FavoritePeople(db.Model):
    __tablename__ = "favorite_people"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    people_id: Mapped[int] = mapped_column(ForeignKey("people.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="people")
    person: Mapped["People"] = relationship("People", back_populates="favorites")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "people_id": self.people_id}


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="planets")
    planet: Mapped["Planet"] = relationship("Planet", back_populates="favorites")

    def serialize(self):
        return {"id": self.id, "user_id": self.user_id, "planet_id": self.planet_id}
