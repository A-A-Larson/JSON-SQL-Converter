import json


class User:
    def __init__(self, id, first_name, last_name, age, city, phone_number):
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__age = age
        self.__city = city
        self.__phone_number = phone_number

    # getters
    def getID(self):
        return self.__id

    def getFirstName(self):
        return self.__first_name

    def getLastName(self):
        return self.__last_name

    def getAge(self):
        return self.__age

    def getCity(self):
        return self.__city

    def getPhoneNumber(self):
        return self.__phone_number

    # setters
    def setID(self, id):
        self.__id = id

    def setFirstName(self, first_name):
        self.__first_name = first_name

    def setLastName(self, last_name):
        self.__last_name = last_name

    def setAge(self, age):
        self.__age = age

    def setCity(self, city):
        self.__city = city

    def setPhoneNumber(self, phone_number):
        self.__phone_number = phone_number

    def __str__(self):
        return print("User ID:", str(self.__id), "\n" +
                     self.__first_name, self.__last_name, "\n" +
                     self.__city, "\n" +
                     str(self.__age), "\n" +
                     self.__phone_number, "\n" +
                     "----------")

    def __dict__(self):
        return {"id": self.__id, "first_name": self.__first_name, "last_name": self.__last_name, "age": self.__age,
                "city": self.__city, "phone_number": self.__phone_number}

    def age_in_range(self, min: int, max: int):
        if max >= self.__age >= min:
            return True
        else:
            return False

    def id_in_range(self, min: int, max: int):
        if max >= self.__id >= min:
            return True
        else:
            return False
