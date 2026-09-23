class usuario:
    def __init__(self, username: str, email: str, edad: int):
        self.__username = username
        self.email = email
        self.edad = edad
        
    @property    
    def username(self) -> str:
        return self.__username
        
    @property
    def email(self) -> str:
        return self.__email
    
    @email.setter
    def email(self, nuevo_email: str) -> str:
        if "@" not in nuevo_email or "." not in nuevo_email:
            raise ValueError("El Correo debe contener caracteres Validos como '@' y '.' ")
        self.__email = nuevo_email
        
    @property
    def edad(self) -> int:
        return self.__edad
        
    @edad.setter
    def edad(self, nueva_edad: int):
        if nueva_edad < 18:
            raise ValueError("El usuario debe ser mayor de 18 años")
        self.__edad = nueva_edad
        
        
    def __str__(self):
        return f"Usuario: {self.__username}, Email: {self.__email}, Edad: {self.__edad}"
    
    def __repr__(self) -> str:    
        return f"Usuario: {self.__username}, Email: {self.__email}, Edad: {self.__edad}"
         