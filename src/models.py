from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Date, Time, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column( String(50), unique=True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(50), nullable=False)
    lastname: Mapped[str] = mapped_column( String(50), nullable=False)
    email: Mapped[str] = mapped_column( String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column( Boolean(), nullable=False, default=True) 

    user_favorite_people: Mapped[List["Peoplefavorite"]] = relationship(back_populates ="user", cascade="all, delete-orphan") 
    user_favorite_film: Mapped[List["Favoritefilm"]] = relationship(back_populates = "user", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "lastname": self.lastname,
            "is_active": self.is_active,
            # do not serialize the password, its a security breach
        }
class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstname: Mapped[str] = mapped_column(String (50), nullable=False)
    lastname: Mapped[str] = mapped_column(String(50), nullable=False)
    specie: Mapped[str] = mapped_column(String(50), nullable=False)
    created: Mapped[str] = mapped_column(String(100), nullable=False)
    

    favorites: Mapped [List["Peoplefavorite"]] = relationship(back_populates = "people", cascade = "all, delete-orphan")
    people_films: Mapped [List["Peoplefilm"]] = relationship (back_populates= "people" , cascade= "all, delete-orphan")
    
    def serialize(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "specie": self.specie,
            "created": self.created,
            # do not serialize the password, its a security breach
        }

class Film(db.Model):
    __tablename__ = "film"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    director: Mapped[str] = mapped_column(String(100),nullable=False)
    created: Mapped[str] = mapped_column(String(100), nullable=False)
    edited: Mapped[Date] = mapped_column( Date, nullable=False)
    release_date: Mapped[Date] = mapped_column( Date, nullable=False)
    
    
    films_favorites: Mapped [List["Favoritefilm"]] = relationship(back_populates = "film", cascade = "all, delete-orphan")
    films_people: Mapped [List["Peoplefilm"]] = relationship (back_populates="film", cascade= "all, delete-orphan" )
    film_planet: Mapped[List["Filmplanet"]]= relationship (back_populates="film", cascade= "all, delete-orphan")
    film_vehicle: Mapped[List["Filmvehicle"]]= relationship(back_populates="film", cascade="all, delete-orphan")


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "director": self.director,
            "created": self.created,
            "edited": self.edited,
            "release_date": self.release_date,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    diameter: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)
    surface_water: Mapped[str] = mapped_column(String(50), nullable=False)
    created: Mapped[str] = mapped_column(String(100), nullable=False)
    edited: Mapped [Date] = mapped_column(Date, nullable=False)

    planet_film: Mapped[List["Filmplanet"]]= relationship(back_populates="planet", cascade="all, delete-orphan")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "created": self.created,
            "edited": self.edited,
            # do not serialize the password, its a security breach
        }
    
class Vehicle(db.Model):
    __tablename__ = "vehicle"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    vehicles_class: Mapped[str] = mapped_column(String(50), nullable=False)
    created: Mapped[str] = mapped_column(String(100),nullable=False)
    edited: Mapped[Date] = mapped_column( Date, nullable=False)

    vehicle_film: Mapped[List["Filmvehicle"]]= relationship(back_populates="vehicle", cascade="all, delete-orphan")
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "vehicles_class": self.vehicles_class,
            "created": self.created
            # do not serialize the password, its a security breach
        }
    
class Peoplefavorite (db.Model):
    __tablename__ = "people_favorite"
    __table_args__ = (UniqueConstraint ("user_id", "people_id", name="uq_user_people"),)

    user_id : Mapped[int] = mapped_column(ForeignKey ("user.id"), primary_key=True, nullable=False )
    people_id: Mapped[int] = mapped_column(ForeignKey ("people.id"), primary_key=True, nullable=False)

    user: Mapped["User"] = relationship(back_populates ="user_favorite_people")
    people: Mapped ["People"] = relationship(back_populates = "favorites")

    def serialize(self):
        return {
            "user_id": self.user_id,
            "people_id": self.people_id
        }

class Favoritefilm (db.Model):
    __tablename__ = "favorite_film"
    __table_args__ = (UniqueConstraint ("user_id" , "film_id", name="uq_user_film"),)

    user_id: Mapped [int]= mapped_column(ForeignKey ("user.id"),primary_key=True, nullable=False, )
    film_id:  Mapped [int] = mapped_column(ForeignKey ("film.id"),primary_key=True,  nullable=False)

    user: Mapped ["User"] = relationship(back_populates = "user_favorite_film")
    film: Mapped ["Film"] = relationship(back_populates = "films_favorites")

    def serialize(self):
        return{
            "user_id": self.user_id,
            "film_id": self.film_id
        }
    
class Peoplefilm (db.Model):
        __tablename__= "peoplefilm"
        __table_args__ = (UniqueConstraint ("film_id" , "people_id", name="up_film_people"),)

        film_id: Mapped [int]= mapped_column(ForeignKey ("film.id"), primary_key=True, nullable=False, )
        people_id: Mapped [int]= mapped_column(ForeignKey("people.id"), primary_key=True, nullable=False,)

        film: Mapped["Film"]= relationship(back_populates= "films_people")
        people: Mapped["People"]= relationship(back_populates="people_films")

        def serialize(self):
            return{
                "film_id": self.film_id,
                "people_id": self.people_id
            }

class Filmplanet (db.Model):
    __tablename__="filmplanet"
    __table_args__= (UniqueConstraint ("film_id", "planet_id", name="up_film_planet"),)

    film_id: Mapped[int]= mapped_column(ForeignKey("film.id"), primary_key=True, nullable=False,)
    planet_id: Mapped[int]= mapped_column(ForeignKey("planet.id"), primary_key=True, nullable=False,)

    film: Mapped["Film"]= relationship(back_populates="film_planet")
    planet: Mapped["Planet"]= relationship(back_populates="planet_film")

    def serialize(self):
        return{
            "film_id": self.film_id,
            "planet_id": self.planet_id
        }
    
class Filmvehicle (db.Model):
    __tablename__="filmvehicle"
    __table_args__= (UniqueConstraint( "film_id", "vehicle_id", name="up_film_vehicle"),)

    film_id: Mapped[int]= mapped_column(ForeignKey("film.id"), primary_key=True, nullable=False,)
    vehicle_id: Mapped[int]= mapped_column(ForeignKey("vehicle.id"), primary_key=True, nullable=False)

    film: Mapped["Film"]= relationship(back_populates="film_vehicle")
    vehicle: Mapped["Vehicle"]= relationship(back_populates="vehicle_film")

    def serialize(self):
        return{
            "film_id": self.film_id,
            "vehicle_id": self.vehicle_id
        }
    

