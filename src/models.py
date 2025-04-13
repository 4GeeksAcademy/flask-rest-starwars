from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

db = SQLAlchemy()

# Modelo de Usuario
class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    subscription_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(
        Boolean(), nullable=False, default=True)

    # Relaciones con favoritos
    favorite_planets = relationship(
        "FavoritePlanet", back_populates="user", cascade="all, delete-orphan")
    favorite_characters = relationship(
        "FavoriteCharacter", back_populates="user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "subscription_date": self.subscription_date.isoformat() if self.subscription_date else None,
            "is_active": self.is_active
        }


# Modelo de Planeta
class Planet(db.Model):
    __tablename__ = 'planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    climate: Mapped[str] = mapped_column(String(100))
    terrain: Mapped[str] = mapped_column(String(100))
    population: Mapped[int] = mapped_column(Integer)

    # Relación con los usuarios que marcan este planeta como favorito
    favorite_by_users = relationship(
        "FavoritePlanet", back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population
        }


# Modelo de Personaje
class Character(db.Model):
    __tablename__ = 'characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    gender: Mapped[str] = mapped_column(String(20))
    birth_year: Mapped[str] = mapped_column(String(10))
    height: Mapped[float] = mapped_column(Float, nullable=True)
    mass: Mapped[float] = mapped_column(Float, nullable=True)
    # Relación opcional al planeta natal
    home_planet_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=True)
    home_planet = relationship("Planet")

    # Relación con los usuarios que marcan este personaje como favorito
    favorite_by_users = relationship(
        "FavoriteCharacter", back_populates="character", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "home_planet": self.home_planet.serialize() if self.home_planet else None
        }


# Modelo para relacionar Usuario y Planet (favoritos)
class FavoritePlanet(db.Model):
    __tablename__ = 'favorite_planets'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    planet_id: Mapped[int] = mapped_column(
        ForeignKey('planets.id'), nullable=False)

    user = relationship("User", back_populates="favorite_planets")
    planet = relationship("Planet", back_populates="favorite_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet": self.planet.serialize() if self.planet else None
        }


# Modelo para relacionar Usuario y Character (favoritos)
class FavoriteCharacter(db.Model):
    __tablename__ = 'favorite_characters'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    character_id: Mapped[int] = mapped_column(
        ForeignKey('characters.id'), nullable=False)

    user = relationship("User", back_populates="favorite_characters")
    character = relationship("Character", back_populates="favorite_by_users")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character": self.character.serialize() if self.character else None
        }
