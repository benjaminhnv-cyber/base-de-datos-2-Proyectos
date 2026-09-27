def preprocesar_cuentas(cuentas):
    #lista de cuentas validas  y las cuentas ya usadas
    cuenta_validas = []
    numero_usado = set()

    for cuenta in cuentas:
        #Verificacion de los campos de la cuenta
        campos_obigatorio = ['titular', 'numero_cuenta', 'saldo_inicial', 'tipo']
        if not all(campo in cuenta for campo in campos_obigatorio):
            continue
        
        #En esta seccion se limpia el titular
        titular = cuenta['titular']
        if not isinstance(titular, str) or not titular.strip():
            continue
        titular_limpio = titular.strip().title()

        #Validacion de cuenta
        try:
            numero_cuenta = int(str(cuenta['numero_cuenta']).strip())
        except (ValueError, TypeError):
            continue

        if numero_cuenta in numero_usado:
            continue

        #Validacion saldo
        try: 
            saldo = int(cuenta['saldo_inicial'])
            if saldo < 0:
                continue
        except (ValueError, TypeError):
            continue

        #verificacion de cuenta ahorro o corriente
        tipo = str(cuenta['tipo']).strip().lower()
        if tipo not in ['ahorro','corriente']:
            continue

        #cuenta porcesada
        cuenta_procesada = {"titular": titular_limpio, "numero_cuenta": numero_cuenta,"saldo_inicial": saldo,"tipo": tipo}

        # esta parte de la seccion tipo «ahorro», si el campo no está presente o contieneun valor no válido (por ejemplo, una cadena de caracteres que no puede convertirsea número o un valor negativo), se deberá asignar el valor por defecto 0.5.
        if tipo == 'ahorro':
                    tasa_defecto = 0.5
                    if 'tasa_interes' in cuenta:
                        try:
                            tasa = float(cuenta['tasa_interes'])
                            cuenta_procesada['tasa_interes'] = tasa if tasa >= 0 else tasa_defecto
                        except (ValueError, TypeError):
                            cuenta_procesada['tasa_interes'] = tasa_defecto
                    else:
                        cuenta_procesada['tasa_interes'] = tasa_defecto

        #limite de giro para cuenta tipo corriente
        if tipo == 'corriente':
            limite_defecto = 100000

            if 'limite_giro' in cuenta:
                try:
                    limite = int(cuenta['limite_giro'])
                    cuenta_procesada['limite_giro'] = limite if limite >= 0 else limite_defecto
                except (ValueError, TypeError):
                    cuenta_procesada['limite_giro'] = limite_defecto
                    
            else:
                cuenta_procesada['limite_giro'] = limite_defecto

        numero_usado.add(numero_cuenta)
        cuenta_validas.append(cuenta_procesada)


    return cuenta_validas

cuentas_prueba = [
    # 1. Válida
    {
        "titular": "juan perez",
        "numero_cuenta": "1001",
        "saldo_inicial": 50000,
        "tipo": "ahorro",
        "tasa_interes": 0.8
    },

    # 2. Válida
    {
        "titular": "maria gonzalez",
        "numero_cuenta": 1002,
        "saldo_inicial": 75000,
        "tipo": "corriente",
        "limite_giro": 150000
    },

    # 3. Falta titular
    {
        "numero_cuenta": 1003,
        "saldo_inicial": 30000,
        "tipo": "ahorro"
    },

    # 4. Falta numero_cuenta
    {
        "titular": "pedro ramirez",
        "saldo_inicial": 40000,
        "tipo": "ahorro"
    },

    # 5. Falta saldo_inicial
    {
        "titular": "ana torres",
        "numero_cuenta": 1005,
        "tipo": "corriente"
    },

    # 6. Falta tipo
    {
        "titular": "carlos rojas",
        "numero_cuenta": 1006,
        "saldo_inicial": 25000
    },

    # 7. Numero de cuenta duplicado
    {
        "titular": "lucas muñoz",
        "numero_cuenta": 1001,
        "saldo_inicial": 90000,
        "tipo": "ahorro"
    },

    # 8. Saldo negativo
    {
        "titular": "sofia castro",
        "numero_cuenta": 1008,
        "saldo_inicial": -5000,
        "tipo": "ahorro"
    },

    # 9. Saldo inválido
    {
        "titular": "diego silva",
        "numero_cuenta": 1009,
        "saldo_inicial": "abc",
        "tipo": "corriente"
    },

    # 10. Tipo de cuenta desconocido
    {
        "titular": "camila flores",
        "numero_cuenta": 1010,
        "saldo_inicial": 50000,
        "tipo": "inversion"
    },

    # 11. Titular vacío
    {
        "titular": "   ",
        "numero_cuenta": 1011,
        "saldo_inicial": 30000,
        "tipo": "ahorro"
    },

    # 12. Numero de cuenta inválido
    {
        "titular": "felipe ortiz",
        "numero_cuenta": "cuenta123",
        "saldo_inicial": 60000,
        "tipo": "corriente"
    },

    # 13. Válida, sin tasa_interes
    # Se le asignará 0.5 por defecto
    {
        "titular": "valentina diaz",
        "numero_cuenta": 1013,
        "saldo_inicial": 45000,
        "tipo": "ahorro"
    },

    # 14. Tasa de interés negativa
    # Se le asignará 0.5 por defecto
    {
        "titular": "andres vera",
        "numero_cuenta": 1014,
        "saldo_inicial": 80000,
        "tipo": "ahorro",
        "tasa_interes": -2
    },

    # 15. Tasa de interés inválida
    # Se le asignará 0.5 por defecto
    {
        "titular": "paula navarro",
        "numero_cuenta": 1015,
        "saldo_inicial": 70000,
        "tipo": "ahorro",
        "tasa_interes": "abc"
    },

    # 16. Corriente sin limite_giro
    # Se le asignará 100000 por defecto
    {
        "titular": "roberto mendoza",
        "numero_cuenta": 1016,
        "saldo_inicial": 100000,
        "tipo": "corriente"
    },

    # 17. Limite de giro negativo
    # Se le asignará 100000 por defecto
    {
        "titular": "laura fuentes",
        "numero_cuenta": 1017,
        "saldo_inicial": 55000,
        "tipo": "corriente",
        "limite_giro": -50000
    },

    # 18. Limite de giro inválido
    # Se le asignará 100000 por defecto
    {
        "titular": "martin espinoza",
        "numero_cuenta": 1018,
        "saldo_inicial": 65000,
        "tipo": "corriente",
        "limite_giro": "abc"
    },

    # 19. Válida con espacios y mayúsculas
    {
        "titular": "   ISABEL MARTINEZ   ",
        "numero_cuenta": "1019",
        "saldo_inicial": "90000",
        "tipo": " AHORRO ",
        "tasa_interes": "1.2"
    },

    # 20. Tipo vacío
    {
        "titular": "gabriel reyes",
        "numero_cuenta": 1020,
        "saldo_inicial": 50000,
        "tipo": ""
    },

    # 21. Saldo negativo
    {
        "titular": "nicolas perez",
        "numero_cuenta": 1021,
        "saldo_inicial": -10000,
        "tipo": "corriente"
    },

    # 22. Válida
    {
        "titular": "daniela fuentes",
        "numero_cuenta": 1022,
        "saldo_inicial": 120000,
        "tipo": "corriente",
        "limite_giro": 200000
    }
]


# Ejecucion de la Funcion
cuentas_limpias = preprocesar_cuentas(cuentas_prueba)


#Muestra por pantalla las cuentas validas 
print("Cuenta validas")
print("-" * 50)

for cuenta in cuentas_limpias:
    print(cuenta)