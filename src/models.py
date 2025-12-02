from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    planets: Mapped[List["FavoritePlanet"]] = relationship()
    characters: Mapped[List["FavoriteCharacter"]] = relationship()

    def serialize(self):
        return {"id": self.id, "email": self.email}


class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    gender: Mapped[str] = mapped_column(String(40), nullable=False)
    hair_color: Mapped[str] = mapped_column(String(120), nullable=False)
    species: Mapped[str] = mapped_column(String(40), nullable=False)
    favorites: Mapped[List["FavoriteCharacter"]
                      ] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "species": self.species,
        }


class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[str] = mapped_column(String(40), nullable=False)
    rotation_period: Mapped[int] = mapped_column(Integer, nullable=False)
    gravity: Mapped[str] = mapped_column(String(40), nullable=False)
    terrain: Mapped[str] = mapped_column(String(40), nullable=False)
    favorites: Mapped[List["FavoritePlanet"]
                      ] = relationship(back_populates="planet")


class FavoriteCharacter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    character_id: Mapped[int] = mapped_column(
        ForeignKey("character.id"), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    character: Mapped["Character"] = relationship(back_populates="favorites")

    def serialize(self):
        return {"character_name": self.character.name}


class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey("planet.id"), nullable=True)
    planet: Mapped["Planet"] = relationship(back_populates="favorites")

    def serialize(self):
        return {"planet_name": self.planet.name}
