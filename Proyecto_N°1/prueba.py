class Cuenta:
    def __init__(self,titular,numero_cuenta):
        self.titular = titular
        self.__numero_cuenta = numero_cuenta
        self.__saldo = 0
        self.tipo_cuenta = None

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}\nN°Cuenta: {self.__numero_cuenta}"

    def consultar_saldo(self):
        return self.__saldo

    def depositar(self, monto):
        try:
            if monto <= 0:
                raise ValueError("El monto debe ser positivo")
            
            self.__saldo += monto
            
        except ValueError as error:
            print(error)

    def girar(self, monto):
        if monto <= 0:
            print("El monto debe ser positivo")
            return
        
        if monto <= self.__saldo:
            self.__saldo -= monto
        
        else:
            print("Saldo insuficiente")
            return

    def modificar_saldo(self, monto):
        self.__saldo += monto

    def obtener_numero_cuenta(self):
        return self.__numero_cuenta
        

class Banco:
    def __init__(self, nombre, cuentas):
        self.nombre = nombre
        self.cuentas = cuentas

    def abrir_cuenta(self, cuenta):
        if self.buscar_cuentas(cuenta.obtener_numero_cuenta()) is not None:
            return
        
        self.cuentas.append(cuenta)

    def buscar_cuentas(self,numero_cuenta):
        for cuenta in self.cuentas:
            if cuenta.obtener_numero_cuenta() == numero_cuenta:
                return cuenta
            
        print("La cuenta no a sido encontrada")
        return None

    def transferir_cuenta(self,numero_origen,numero_destino,monto):
        if monto <= 0:
            print("El monto debe ser positivo")
            return

        if numero_origen == numero_destino:
            print("No puedes transferir a la misma cuenta")
            return
        
        cuenta_origen = self.buscar_cuentas(numero_origen)
        cuenta_destino = self.buscar_cuentas(numero_destino)

        if cuenta_origen is None or cuenta_destino is None:
            return

        if cuenta_origen.consultar_saldo() < monto:
            print("Error: saldo insuficiente")
            return

        cuenta_origen.girar(monto)
        cuenta_destino.depositar(monto)

    def mostrar_cuentas(self):
        cuentas_ordenadas = sorted(self.cuentas, key=lambda cuenta: cuenta.obtener_numero_cuenta())
        for cuenta in cuentas_ordenadas:
            print(cuenta.obtener_informacion_basica())

class Cuenta_ahorro(Cuenta):
    def __init__(self,titular, numero_cuenta,saldo_inicial, tasa_interes):
        super().__init__(titular, numero_cuenta)
        self.tipo_cuenta = "ahorro"
        self.tasa_interes = tasa_interes
        self.modificar_saldo(saldo_inicial)

    def aplicar_interes(self):
        #aplicar aumento de saldo
        saldo_actual = self.consultar_saldo()
        interes = saldo_actual * self.tasa_interes
        self.depositar(interes)

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}\nN° Cuenta: {self.obtener_numero_cuenta()}\nTipo: {self.tipo_cuenta}\nTasa de interés: {self.tasa_interes}"
    

class Cuenta_corriente(Cuenta):
    def __init__(self, titular, numero_cuenta, saldo_inicial,limite_giro):
        super().__init__(titular, numero_cuenta)
        self.tipo_cuenta = "corriente"
        self.limite_giro = limite_giro
        self.modificar_saldo(saldo_inicial)
        #monto de giro maximo
        
    def girar(self,monto):
        #hay que colocar un limete de giro puede salir negativo pero no se puede sobrepasar limite de giro
        if monto <= 0:
            print("El monto debe ser positivo")
            return
        
        if monto <= self.consultar_saldo() + self.limite_giro:
            self.modificar_saldo(-monto)

        else:
            print("Saldo insuficiente")
            return 

    def obtener_informacion_basica(self):
        return f"Titular: {self.titular}\nN° Cuenta: {self.obtener_numero_cuenta()}\nTipo: {self.tipo_cuenta}\nLímite giro: {self.limite_giro}"


cuenta1 = Cuenta_ahorro("Juan Perez", 1001, 50000, 0.05)
cuenta2 = Cuenta_corriente("Maria Gonzalez", 1002, 80000, 100000)

banco = Banco("Banco de Prueba", [])

banco.abrir_cuenta(cuenta1)
banco.abrir_cuenta(cuenta2)


print("cuenta banco")
banco.mostrar_cuentas()


print("\nsaldos\n")
print("Saldo Juan:", cuenta1.consultar_saldo())
print("Saldo Maria:", cuenta2.consultar_saldo())


print("\ndeposito\n")
cuenta1.depositar(20000)
print("Nuevo saldo Juan:", cuenta1.consultar_saldo())


print("\ngiro\n")
cuenta2.girar(30000)
print("Nuevo saldo Maria:", cuenta2.consultar_saldo())


print("\ninterese\n")
cuenta1.aplicar_interes()
print("Nuevo saldo Juan:", cuenta1.consultar_saldo())


print("\ntansferencia\n")
banco.transferir_cuenta(1001, 1002, 10000)

print("Saldo Juan:", cuenta1.consultar_saldo())
print("Saldo Maria:", cuenta2.consultar_saldo())