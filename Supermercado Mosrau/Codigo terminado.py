#Librerías
import json #Para usar archivos .json 
from datetime import datetime #Para hacer uso de fechas

#Variables "Globales"
intentos = 5 #Para que no pueda intentar mas de 5 veces hacer algo.
impuestos = [] #Arreglo o lista para gestionar impuestos.
usuarios = {} #Diccionario para los usuarios
stock = {}  #Diccionario para el stock
registros = {} #Registra los productos eliminados
ventas = {} #Es para guardar las ventas.
volver = False  #Para volver atrás en un bucle
rol = "" #Busca el rol actual del usuario, se usara principalmente para evitar errores de login y gestionar roles.
ganancias = {} #Se usara para saber las ganancias por producto.
alerta = "1" #Alerta de forma predeterminada tiene el valor True

#Cargar Datos - Guardar datos
#Usuarios
def cargar_usuarios(): #Carga el archivo anterior con los usuarios existentes. 
    global usuarios
    try:
        with open("usuarios.json", "r") as archivo:
            usuarios.update(json.load(archivo)) #Actualiza el diccionario usuarios con los valores de usuario.json, para eso sirve el .update y load
    except:
        print("Archivo no encontrado, se creara con un usuario admin.")
        usuarios["admin"] = {"contrasena": "12345", "rol": "admin"} #Creara el usuario "admin" con el rol admin y la contraseña 12345.
        guardar_usuarios()


def guardar_usuarios(): #Guarda los nuevos registros de usuarios. 
    try: #Primero intenta escribir sobre el json de usuarios.
        with open("usuarios.json", "w") as archivo:
            json.dump(usuarios, archivo) #Dump sirve para "tirar" o guardar los datos en el archivo ya leído "usuarios.json"
    except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
        print("Archivo no encontrado, se creara uno nuevo para los usuarios.")


#Stock

def guardar_stock(): #Guarda el stock.
    try: #Primero intenta escribir sobre el json de stock.
        with open("stock.json", "w") as archivo:
            json.dump(stock, archivo)
    except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
        print("Archivo no encontrado, se creara uno nuevo para el stock.")


def cargar_stock(): #Carga el archivo anterior con el stock existente
    global stock
    try:
        with open("stock.json", "r") as archivo:
            stock.update(json.load(archivo)) #Actualiza el diccionario stock con los valores de stock.json, para eso sirve el .update y load
    except:
        print("Archivo no encontrado, se creara uno nuevo para el stock.")
        stock["No tocar"] = { "almacen": {"codigo": 1, "cantidad": 9999999, "precio": 0, "vencimiento": "30/12/9999"}}

#Agrega esto al stock para poder decidir un precio extra para cobrar, lo añade al stock y luego si se añade en el carrito puede gestionarse el precio.
def almacen(): 
   while True:
      try:
         precio = float(input("Introduce el precio: $"))
         precio = round(precio)
         stock["No tocar"] = { "almacen": {"codigo": 1, "cantidad": 9999999, "precio": precio, "vencimiento": "30/12/9999"}}
         return precio
      except:
         print("Introduce un precio valido.")

   

#Productos eliminados - Registros de ventas

def cargar_registros(): #Carga el archivo anterior con los registros existente sobre productos eliminados.
    global registros
    try:
        with open("registros.json", "r") as archivo:
            registros.update(json.load(archivo)) #Actualiza el diccionario registros con los valores de registros.json, para eso sirve el .update y load
    except:
        print("Archivo no encontrado, se creara uno nuevo para los registros.")


def guardar_registros(): #Guarda el registro de productos eliminados
    try: #Primero intenta escribir sobre el json de registros.
        with open("registros.json", "w") as archivo:
            json.dump(registros, archivo)
    except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
        print("Archivo no encontrado, se creara uno nuevo para los registros.")        


def guardar_ventas(): #Guarda las ventas
    try: #Primero intenta escribir sobre el json de ventas
        with open("ventas.json", "w") as archivo:
            json.dump(ventas, archivo)
    except FileNotFoundError: #En caso de no encontrar el json, avisa y crea el archivo.
        print("Archivo no encontrado, se creara uno nuevo para las ventas.")


def cargar_ventas(): #Carga el archivo anterior con las ventas anteriores.
    global registrar_venta
    try:
        with open("ventas.json", "r") as archivo:
            ventas.update(json.load(archivo)) #Actualiza el diccionario ventas con los valores de ventas.json, para eso sirve el .update y load
    except:
        print("Archivo no encontrado, se creara para las ventas.")

#Cargas de ganancias e impuestos.

def cargar_ganancias(): 
    global ganancias #Se aclara que se usara el diccionario ganancias global
    try:
        with open("ganancias.json", "r") as archivo:
            ganancias = json.load(archivo)
    except:
        print("Archivo no encontrado, se creara uno nuevo para las ganancias.")
        ganancias = {}
        ganancias["ganancias_productos"] = {} #Aca se almacenara los productos, ganancia de ese producto y demás, con impuestos.


def guardar_ganancias(): 
    global ganancias
    try: 
        with open("ganancias.json", "w") as archivo:
            json.dump(ganancias, archivo)
    except FileNotFoundError: 
        print("Archivo no encontrado, se creara uno nuevo para las ganancias.")    


def cargar_impuestos():
    global impuestos
    try:
        with open("impuestos.json", "r") as archivo:
            impuestos = json.load(archivo)
    except:
        print("Archivo no encontrado, se creara uno nuevo para los impuestos.")
        impuestos = [("IVA", 21.5), ("GANANCIAS", 5)] #Impuestos predeterminados.


def guardar_impuestos(): 
    global impuestos
    try: 
        with open("impuestos.json", "w") as archivo:
            json.dump(impuestos, archivo)
    except FileNotFoundError:
        print("Archivo no encontrado, se creara uno nuevo para los impuestos.")        

#Chequea el stock y busca productos que estén por vencer en menos de 10 días, funciona como una alerta.
def cheq_stock(alerta):  
    if alerta == "1": #Solo se ejecutara si al iniciar sesión se mantiene activada la opción de habilitar alertas.
      global stock #Se deja en claro que se operara con el diccionario global stock y no con la variable local "stock"
      productos_vencimiento = [] #Array para guardar los productos que van a vencer o vencieron.
      fecha_actual = datetime.now() #Se obtiene la fecha actual para operar y saber el vencimiento

      if not stock: #Si el archivo json stock esta vació termina la función para evitar errores.
            return 
      
      for categoria, productos in stock.items(): 
         for producto, detalle in productos.items(): #Detalle es lo que hay dentro de stock/productos funcionando para obtener el valor que se desee.
               vencimiento = datetime.strptime(detalle["vencimiento"], "%d/%m/%Y") #Se obtiene la key "vencimiento" dentro de cada producto.
               dias_restantes = vencimiento - fecha_actual #Se opera para saber los días restantes.
               dias_restantes = dias_restantes.days #Solo se quedara con el .days para no mostrar el resto con el formato de horas.

               if dias_restantes <= 10: #Se guardaran los productos que tengan al menos 10 días restantes para su vencimiento.
                  detalle["dias_restantes"] = dias_restantes
                  if producto == "almacen":
                     continue #Seguirá con el programa y no mostrara el producto "almacén" en la alerta.
                  elif stock[categoria][producto]["cantidad"] == 0:
                     continue #Si no tiene cantidad no lo mostrara en la alerta.
                  else:
                     productos_vencimiento.append((categoria, producto, detalle)) #Añade el producto a esta lista para luego mostrarlo.

      if len(productos_vencimiento) != 0: #Solo mostrara esto si hay productos que vencerán en 10 dias o ya están vencidos, osea que la variable no esta vacía.
         print()
         print("Ten en cuenta que:")
         print()
         try:  #Se intenta mostrar el producto con sus respectivas características, en caso de dar error se ejecuta lo de "except"
            for categoria, producto, detalle in productos_vencimiento: 
               if detalle["dias_restantes"] > 0:
                  print(f"El Producto '{producto}' en la categoria '{categoria}' esta por vencer en {detalle['dias_restantes']} dias, se recomienda colocar el producto en oferta para su venta rápida o perderás un total de ${stock[categoria][producto]['cantidad'] * stock[categoria][producto]['precio']}.")
               else: 
                  print()
                  print(f"El Producto '{producto}' vencio hace {detalle['dias_restantes']} dias, perdiste un total de ${stock[categoria][producto]['cantidad'] * stock[categoria][producto]['precio']}")
                  print("Eliminalo del stock para que deje de mostrarse la alerta.")
         except: 
               return
      
#Funciones - Registro e Inicio de sesión.

def registro_usuario(): #Diccionario para registrar un nuevo Usuario.
    intentos = 5 #El usuario solo tendrá 5 intentos para esta parte del menu.
    while True:
      global usuarios #Se usara la variable global usuarios (que ya fue cargada con los usuarios existentes, roles y contraseñas).
      print()
      while intentos != 0: #Mientras que intentos sea diferente a 0 se ejecutara este bucle.
        nombre = input("ingresa tu nombre: ")
        if not nombre.strip():
          print("Error, introduce un nombre valido.") #El usuario no puede introducir nombres vacíos.
          intentos -= 1 #Resta un intento.
        else:
           break
      if nombre in usuarios and intentos != 0: #Si ingresa un nombre ya existente y puede seguir ingresando, pide ingresar otro.
          print("El nombre ya existe, ingresa otro.")
          print(f"Intentos restantes: {intentos}")
          intentos -= 1
      elif intentos == 0: #Si se queda sin intentos vuelve al menu de iniciar sesión.
         print("Demasiados intentos erróneos, volviendo al menu...")
         return
      else:       
        while True: #Si no presenta ninguno de los errores anteriores, el programa continuara.
          contrasena = input("Ingresa tu contraseña: ")
          if len(contrasena) >=5 and intentos != 0: #La contraseña debe tener mas de 4 caracteres.
            usuarios[nombre] = {"contrasena": contrasena, "rol": "usuario"} #De forma predeterminada cualquier usuario nuevo tendrá el rol "usuario", donde no tiene grandes permisos.
            print("Usuario registrado correctamente, inicia sesión.")
            guardar_usuarios()
            return
          elif intentos == 0:
            print("Demasiados intentos erróneos, volviendo al menu.")
            return
          else:
            print(f"La contraseña debe tener 5 o mas caracteres.") #Da un mensaje de error.
            print(f"Intentos restantes: {intentos}")
            intentos -= 1


def login(): #Inicio de sesión. 
    global volver #Dado a que tenemos un bucle dentro de otro, necesitamos de esta variable para terminar con el programa.
    global usuarios #Se usara para saber los usuarios existentes con sus respectivos roles y contraseñas.
    global rol #Obtiene el rol del usuario.
    global ingresa_usuario #Pedirá su nombre de usuario y también se usa para saber que usuario inicio sesión actualmente.
    global ingresa_contrasena #El usuario tendrá que ingresar su contraseña y si coincide con su nombre ingresara, también se usa para "gestionar cuentas".
    intentos = 5
    while not volver:
      print()
      ingresa_usuario = input("Ingresa tu nombre de usuario: ")
      if intentos != 0:
        if ingresa_usuario in usuarios: #Si el nombre ingresado por el usuario se encuentra en usuarios continuara con el código.
          while True:
            ingresa_contrasena = input("Ingresa tu contraseña: ") 
            if usuarios[ingresa_usuario]["contrasena"] == ingresa_contrasena: #¿La contraseña coincide con el nombre de usuario? si es asi el usuario accede.
                rol = usuarios[ingresa_usuario]["rol"] 
                return rol #Devolvemos el rol para hacer otra verificación en el programa principal, para evitar que si iniciaste y luego cerras sesión otro usuario pueda ingresar como administrador.
            
            elif intentos == 0:
                print("Demasiados intentos fallidos, volverás al menu.")
                print("Si el problema persiste contacta a un operador.")
                volver = True
                break
            else: #La contraseña es invalida.
                print()
                print("Contraseña invalida, vuelve a introducirla.")
                print(f"Intentos restantes: {intentos}")
                intentos -= 1
        else: #Si no se encuentra el usuario pedirá otro.
            print("Usuario no encontrado, introduce uno valido.")
            print(f"Intentos restantes: {intentos}")
            intentos -= 1
      else: #Si intentos vale 0 al entrar ingresar el nombre terminara el bucle.
         print("Demasiados intentos fallidos, volverás al menu.")
         print("Si el problema persiste, intenta registrar nuevamente al usuario o contacta a un operador.")
         volver = True
         break
    volver = False #Volver tendrá de nuevo su valor global para que se vuelva a mostrar el menu "Inicio de Sesión" 

#Menus - Usuario

def menu_usuario():  
  intentos = 5
  while True:
    print() #Solo cuenta con estos permisos
    print("----- Menú Usuario -----") 
    print("1. Stock") 
    print("2. Empezar a Trabajar")  
    print("3. Cerrar sesión")
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
      print()
      menu_stock()
    elif opcion == "2":
      menu_trabajar()
    elif opcion == "3":
      print("Cerrando sesión")
      return
    elif intentos == 0:
      print("Opción incorrecta, por favor vuelve a iniciar sesión.")
      intentos = 5
      return
    else:
      print(f"Opción incorrecta, intentos restantes: {intentos}")
      intentos -= 1


#Menu - Admin
 
def menu_admin(): 
  global alerta
  intentos = 5
  while True:
    cheq_stock(alerta) #Revisara los próximos vencimientos buscando alguno que le queden menos de 10 dias y sugerir.
    print()
    print("----- Menú Administrador -----")
    print("0. Desactivar/Activar alertas.")
    print("1. Stock.") #Dirige al administrador al menu_stock
    print("2. Empezar a trabajar.") #Dirige a menu_trabajar
    print("3. Ganancias.") #Mostrara las ganancias previamente calculadas, si no hay ganancias dará un mensaje de error preparado.
    print("4. Gestionar Cuentas.") #Permite gestionar todas las cuentas que existen en el sistema.
    print("5. Gestionar impuestos") #Puedes borrar, añadir y visualizar los impuestos, obviamente afectaran a las ganancias.
    print("6. Visualizar ventas.") #Visualiza las ventas hechas, incluso al ultimo usuario que la hizo.
    print("7. Volver.")
    opcion = input("Elije una opción: ")
    if opcion == "0":
      if alerta == "1":
         alerta = "0"
         print()
         print("Alertas desactivadas.")
      else:
         alerta = "1"
         print("Alertas Activadas.")

    elif opcion == "1": #Gestionar Stock
      menu_stock()
    elif opcion == "2": #Abrir el menu de trabajo
      menu_trabajar()
    elif opcion == "3": #Visualizar ganancias.
      print()
      ganancias_totales = 0
      try:
         for producto, det in ganancias["ganancias_productos"].items(): #Cada producto tomara el valor de la key "ganancias_productos", mientras que det tomara el detalle que el programador desee.
            gananciaporp = det["ganancia"]
            print(f"Ganancia por el producto '{producto}': ${gananciaporp} Cantidad vendida: {det['cantidad']}")
            ganancias_totales += gananciaporp
         print()
         if ganancias_totales == 0:
            print("No hay ganancias para mirar.") #Si las ganancias son de 0 se mostrara este mensaje.
         else:     
            print(f"Ganancias totales: $",'{:.2f}'.format(ganancias_totales)) #Muestra solo dos dígitos después de la coma.
      except:
         print("No hay ganancias para mirar.") #Si no hay ganancias se mostrara este mensaje.
    elif opcion == "4":
      print()
      int = gestionar_cuentas() #int tomara el valor devuelvo por gestionar cuentas, sirve para decidir si cerrar sesión o no.
      if int == 0: #Si se equivoco todas las veces, cambio el nombre o cambio su propia contraseña necesitara volver a iniciar sesión.
         return
      else:
         print() #Si no se equivoco continua normalmente.
      

    elif opcion == "5": #Gestionar Impuestos.
      while True:
         print()
         print("1. Observar Impuestos.") #Permite saber al usuario que impuestos existen de forma actualizada.
         print("2. Agregar impuesto") #Permite agregar un impuesto nuevo, incluso puede poner uno de 55.9%
         print("3. Eliminar impuesto") #Podrá eliminar cualquier impuesto antes añadido.
         print("4. Volver")
         print()
         elije = input("Coloca tu selección (No introduzca nada para volver al anterior menu): ")
         elije = elije.lower()
         if elije == "1":
            observar_impuestos()
         elif elije == "2":
            agregar_impuesto()
         elif elije == "3":
            eliminar_impuesto()
         elif elije == "4":
            print("Volviendo...")
            break
         else: #Si no elije ninguno mostrara este mensaje.
            print("Selección incorrecta.")

    elif opcion == "6": #Puedes visualizar las ventas hechas.
       registrar_ventas() 
    elif opcion == "7": 
      print("Volviendo al menu anterior...")
      return
    elif intentos == 0:
      print("Muchas selecciones incorrectas, por favor vuelve a iniciar sesión.")
      intentos = 5
      return
    else:
      print(f"Opción incorrecta, intentos restantes: {intentos}")
      intentos -= 1


# (1) Menu stock 

def menu_stock(): 
   global stock
   global intentos
   intentos = 5
   while True:   
    print()
    print("---- Menu del stock ----")
    print("1. Agregar producto al stock.") #Con precio, nombre y código
    print("2. Buscar productos.") #Puede elegir buscar por nombre o código.
    print("3. Eliminar producto de stock.") #Desea eliminar algún producto ya añadido.
    print("4. Modificar producto") #Puede modificar el producto que desee.
    print("5. Mirar stock completo.") #Visualizara el stock.
    print("6. Revisar vencimientos próximos.") #Mostrara los vencimientos próximos, también los que ya vencieron.
    print("7. Registros de productos eliminados del stock.") 
    print("8. Volver.")
    opcion = input("Por favor, selecciona una opcion: ") #Permite que el usuario elija que quiere hacer.
    
    if opcion == "1":
       agregar_producto() 
       intentos = 5
    elif opcion == "2":
       buscar_producto()  
    elif opcion == "3":
       eliminar_producto()  
    elif opcion == "4":
       modificar_producto() 
       intentos = 5 
    elif opcion == "5":
       print()
       mostrar_productos()
       intentos = 5
    elif opcion == "6":
       print() 
       vencimientos_proximos() 
    elif opcion == "7":
       print() 
       registros_todos()
       intentos = 5
    elif opcion == "8":
       print("Volviendo al menu anterior.")
       intentos = 5
       return
    elif intentos == 0:
      print("Muchas selecciones incorrectas, volviendo al menu anterior.")
      intentos = 5
      return
    else:
       print(f"Opcion incorrecta, intentos restantes: {intentos}")
       intentos -= 1               


#Utilidades del menu stock
# (1) Agregar productos
def agregar_producto(): 
  print()
  global stock
  global intentos 
  
  categorias = stock.keys() #Dado a como esta planteado el archivo json, donde las keys serán las categorías de los productos, la variable categorías tomara el valor de esas keys para luego mostrarlas.

  if len(categorias) != 0:
    print("---- Categorías existentes ----") 
    for categoria in categorias: #Bucle, categoria tomara cada key para poder imprimirlas y mostrar una a una.
      if categoria == "No tocar": #No va a mostrar la categoria "No tocar" donde se guarda "almacén" para establecer un precio determinado.
         continue
      else:
         print(f"• {categoria}")
  else:
     print("No hay categorías existentes.") 

  while True:
    categoria = input("Ingresa la categoría del producto a agregar ('salir' para cancelar en cualquier momento): ")
    categoria = categoria.lower() #Transforma los caracteres a minúscula.

    if not categoria.strip(): #Se comprueba cuantos caracteres tiene categoria después de que el usuario lo ingrese.
       print("No puedes introducir categorías vacías, vuelve a intentarlo.")

    elif categoria == "salir":
      print("Saliendo...")
      return #Termina esta función y vuelve al anterior menu.
    
    else: #Si no tiene ninguno de los dos anteriores errores continua.

      break

  while True:
    producto = input("Ingresa el nombre del producto a agregar: ")
    producto = producto.lower() #Convierte el string a minúscula.
    if not producto.strip(): #Comprueba que no introduzca datos vacíos.
      print("Error, introduce un producto valido.")
      print(f"Intentos restantes: {intentos}")
      intentos -= 1
    
    for cat, proda in stock.items(): #Esta parte del código sirve para verificar si ya existe algún producto con el nombre que quiere añadir el usuario.
        for produc, detalle in proda.items():
           if produc == producto: #Si el producto que quiere agregar ya existe tira error.
                print("Ya existe un producto con ese nombre, intenta modificarlo.") 
                return
           else:
                continue #Continua con el bucle.
        
        

    if producto == "salir":
      print("Saliendo...")
      return #Termina esta función y vuelve al anterior menu.
    
    elif not stock: #Si el archivo json esta vació se termina el bucle y almacena lo nuevo ingresado, de lo contrario daría error.
       break 
     
    if intentos == 0: #Si se queda sin intentos vuelve al anterior menu.
       print("Demasiados intentos, prueba nuevamente.")
       return
    
    if len(producto) != 0: #Se necesita volver a hacer la comprobación por los ifs.
       break
    

  while True: 
    cantidad = input("Ingresa la cantidad correspondiente del producto: ") #Pide la cantidad
    cantidad = cantidad.lower() #Convierte el string a minúscula.
    if cantidad == "salir":
       print("Saliendo...")
       return #Termina esta función y vuelve al anterior menu.

    try: #El try se usa porque si ocurre un error inesperado, como en este caso convertir cantidad con un string (en caso de tener palabras y no un numero) a un float daría un error que terminaría con la ejecución del programa.
      cantidad = float(cantidad) #Lo transforma a números y si es un string da error y emite lo de "except"
      intentos = 5

      if cantidad <= 0: #No puede haber una cantidad de 0 o negativa.
       print("La cantidad no puede ser menor o igual a 0.")
       intentos -= 1
      else: #Si la cantidad es mayor a 0 continua.
        break
    except: #El usuario introduce caracteres.
      print("Cantidad errónea, vuelve a introducir una.")
      print(f"Intentos restantes: {intentos}")
      intentos -= 1

    if intentos == 0:
       print("Demasiados intentos, volviendo al menu anterior.")
       return


  while True:
    codigo = input("Ingresa el código correspondiente al producto: #")
    codigo = codigo.lower()
    
    if codigo == "salir":
        print("Saliendo...")
        return
    
    if codigo.strip(): #Si no es un input vació se inicia,  crea la variable codigo_existe false para luego usarla.
        codigo_existe = False

        for cat, productos in stock.items(): #cat toma la primer key y productos toma la que esta dentro de categoria, si estuviera solo productos tomaría el valor de categoria.
            for prod, detalle in productos.items():
                if detalle["codigo"] == codigo:
                    codigo_existe = True #Si ese codigo ya esta registrado devuelve codigo_existe como true
                    break

        if codigo_existe: #Si codigo_existe es true va a mostrar este mensaje y pedir otro.
            print("El código ya existe, ingresa otro.")
        else:
            print("Código único registrado.")
            break
    else: #Si no introduce almenos un caracter da error.
        print("Por favor, ingresa un código válido.")

  while True:
     precio = input("Introduce el precio: $")
     precio = precio.lower() #Convierte precio a minúscula para saber si ingreso salir
     if precio == "salir":
        print("Saliendo...")
        return
     
     try:
        precio = float(precio) #Se asegura que no sea un string
        if precio > 0: #Si es un precio positivo continua el programa.
           break
        else: #Si el precio es 0 o menor no continua el programa.
           print("El precio debe ser mayor a 0.")
           intentos -= 1
     except: #Se intento ingresar un string como precio, da este error.
        print("Precio erróneo, vuelve a intentarlo.")
        intentos -= 1

     if intentos == 0:
        print("Demasiados intentos, volviendo al menu anterior.")
        return

  while True:
     print()
     print("La fecha de vencimiento debe cumplir con el formato Dia/Mes/Año.") #Se aclara la condición.
     vencimiento = input("Ingresa la fecha de vencimiento aproximada de los productos: ")
     vencimiento = vencimiento.lower()
     if vencimiento == "salir":
        print("Saliendo...")
        return
     
     try:    
        vencimiento = datetime.strptime(vencimiento, "%d/%m/%Y") # Intenta convertir la entrada del usuario a un objeto datetime con el formato especificado para comprobar que ingrese fecha validas
        vencimiento = vencimiento.strftime( "%d/%m/%Y") #Lo pasa nuevamente a una fecha texto para guardarla correctamente en un json y que no de error.
        break 
     except ValueError:
            print("Fecha inválida. Por favor, ingresa la fecha en el formato correcto Dia/Mes/Año.")
       
  if categoria in stock: #Si ya existe la categoria que ingreso el usuario guardara el producto y los datos en la misma.
      stock[categoria][producto] = {  "codigo": codigo, "cantidad": cantidad, "precio": precio, "vencimiento": vencimiento}
      print("Producto guardado correctamente, en su respectiva categoria.")
      guardar_stock()

  else: #Si no existe esa categoria en el json, creara la categoria y guardara el producto en este con los respectivos datos. 
     stock[categoria] = {
            producto: {"codigo": codigo, "cantidad": cantidad, "precio": precio, "vencimiento": vencimiento}}
     print("Producto añadido correctamente, creando su correspondiente categoria.")
     guardar_stock()


# (2) Buscar producto

def buscar_producto():
    print()
    global stock
    
    if not stock: #Si el archivo json stock esta vació da mensaje de error y termina esta función.
        print("El stock está vacío. No hay productos para buscar.")
        return

    while True: 
        print("1. Nombre")
        print("2. Código")
        print()
        buscar = input("¿Deseas buscar por nombre o código? ('salir' para cancelar): ")
        buscar = buscar.lower()
        
        if buscar == "salir":
            print("Saliendo...")
            return
        
        elif buscar == "nombre" or buscar == "1": #Introduce 1 o "nombre" para buscar de esa manera.
            nombre = input("Introduce el nombre del producto a buscar: ")
            nombre = nombre.lower()
            for categoria, productos in stock.items(): 
               for producto, detalle in productos.items():
                if nombre == "almacen" and producto == nombre: #Si el nombre ingresado es "almacen" se llamara a esa función que permite gestionar el precio.
                   precio = almacen() #Llama la función almacen
                   cantidad = stock[categoria][producto]["cantidad"] #Mostrara la cantidad disponible.
                   return categoria, producto, precio, cantidad #Devuelve estos valores cuando se usa.

                elif producto == nombre: #Si el producto en ese momento del for coincide con el que busca el usuario obtiene sus valores.
                   vencimiento = datetime.strptime(stock[categoria][producto]["vencimiento"], "%d/%m/%Y") #Obtiene la fecha de vencimiento actual 
                   
                   fecha_actual = datetime.now()
                   vencimiento = vencimiento - fecha_actual
                   vencimiento = vencimiento.days

                   print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y')}") #Se muestra la fecha actual
                   print("Producto encontrado:")
                   print(f"Categoría: {categoria}")
                   print(f"Nombre: {producto}")
                   print("Su codigo es: #"+ stock[categoria][producto]["codigo"]) #Obtiene y muestra el codigo.
                   cantidad = stock[categoria][producto]["cantidad"]
                   cantidad = round(cantidad) #Redondea la cantidad para mostrarla sin el .0, se obtiene de esta manera porque luego necesita devolverse esa cantidad.
                   print(f"Cantidad: {cantidad}")
                   precio = stock[categoria][producto]["precio"] #Se obtiene de esta manera para devolverla en el return si es necesario.
                   print(f"Precio: ${precio}")
                   print("Su fecha de vencimiento es:", stock[categoria][producto]["vencimiento"])
                   if vencimiento < 0: #Si la fecha obtenida es negativa muestra que venció
                      print(f"El producto venció hace {vencimiento} días.")
                   else: #Si la fecha es positiva o igual a 0 todavía falta un poco para el vencimiento.
                      print(f"Quedan {vencimiento} días para el vencimiento.")
                   return categoria, producto, precio, cantidad #Se devuelven estos valores si son necesarios.
            
            print()
            print(f"No se encontró ningún producto con el nombre: {nombre}, vuelve a intentarlo.") #Si no se encuentra vuelve a elegir como quieres buscarlo.

        elif buscar == "codigo" or buscar == "código" or buscar == "2": #Introduce 2 o codigo para buscar de esa forma.
           codigo = input("Introduce el codigo del producto a buscar: ")
           codigo = codigo.lower()
           for categoria, productos in stock.items():
               for producto, detalle in productos.items(): #El .items es para obtener el par key y el valor de cada uno, por lo tanto "producto" guardara la key y "detalle" guardara el valor.
                if detalle["codigo"] == codigo:
                   vencimiento = datetime.strptime(stock[categoria][producto]["vencimiento"], "%d/%m/%Y") 
                   fecha_actual = datetime.now()
                   vencimiento = vencimiento - fecha_actual #Calcula cuanto tiempo le queda al producto para vencer.
                   vencimiento = vencimiento.days #Obtiene solo la parte de "days" sin el resto porque si no se ve raro.
              
                   print(f"Fecha actual: {fecha_actual.strftime('%d/%m/%Y')}")
                   print("Producto encontrado:")
                   print(f"Categoría: {categoria}")
                   print(f"Nombre: {producto}")
                   cantidad = stock[categoria][producto]["cantidad"]
                   cantidad = round(cantidad)
                   print(f"Cantidad: {cantidad}")
                   precio = stock[categoria][producto]["precio"]
                   print(f"Precio: ${precio}")
                   print("Su fecha de vencimiento es:", stock[categoria][producto]["vencimiento"])
                   if vencimiento < 0:
                      print(f"El producto venció hace {vencimiento} días.")
                   else: 
                      print(f"Quedan {vencimiento} días para el vencimiento.")
                   return categoria, producto, precio, cantidad
                
           print(f"No se encontró ningún producto con el codigo: {codigo}, vuelve e intentarlo.") 
        else:
           print("Selección invalida.") #Pedirá al usuario que ingrese algo valido.  
           print() 
        


# (3) Eliminar productos

def eliminar_producto(): 
    global stock
    global intentos
    global registros
    fecha = datetime.now()
    fecha = fecha.strftime( "%d/%m/%Y" ) #Lo cambia a este formato Dia/Mes/Año
    while True:
      print()
      print("¿Deseas eliminar una categoría o un producto?") 
      print("1. Categoría")
      print("2. Producto")
      opcion = input("Introduce tu seleccion: ")
      opcion = opcion.lower()  #Convierte todo a minúscula para guardarlo asi y que no ocurra un error a la hora de buscarlo.
      
      if opcion == "1" or opcion == "categoría" or opcion == "categoria": 
         print()
         for categorias in stock.keys():
            if categorias == "No tocar": #No va a mostrar la categoria de almacén.
                continue
            else:
                print(f"Categoría: {categorias}")
         print()
         eliminar = input("Introduce la categoria que deseas eliminar ('salir' para cancelar): ")
         for categoria in stock.keys():
            if eliminar == categoria: #Si la categoria a eliminar coincide con el for se eliminara.
               
               del(stock[categoria]) #Elimina esa categoria
               print("Categoría eliminada.")
               guardar_stock() #Guarda los cambios hechos.
               return
            elif eliminar == "salir":
               print("Saliendo...")
               return
         print("Categoría no encontrada") #Si ninguna coincidió dará este mensaje.
         return

      
      elif opcion == "2" or opcion == "producto":
         print()
         for categoria, productos in stock.items():
            for producto, cantidad in productos.items():
                if producto == "almacen": #No mostrara el producto "almacen"
                    continue
                else:
                    print(f"Producto: {producto}") #Mostrara todos los productos para que el usuario decida que eliminar sin necesidad de buscar antes.
         print()

         eliminar = input("Introduce el producto que deseas eliminar ('salir' para cancelar): ") 
         eliminar = eliminar.lower()
         for categoria, productos in stock.items():
            for producto, cantidad in productos.items():
                  producto = producto.lower()
                  if producto == eliminar: #Si coincide el producto con lo que el usuario desea eliminar primero obtiene los datos para tener un registro y luego lo elimina.
                     codigo = stock[categoria][producto]["codigo"] #Obtiene el codigo del producto seleccionado.
                     precio = stock[categoria][producto]["precio"] #Obtiene el precio del producto seleccionado.
                     vencimiento = stock[categoria][producto]["vencimiento"] #Obtiene el vencimiento
                     cantidad2 = stock[categoria][producto]["cantidad"] #Obtiene la cantidad del producto, se llama cantidad2 para no pisarse con "cantidad" del for.

                     stock[categoria].pop(producto) #Sirve para borrar el producto que desea el usuario.
                     print(f"El producto {eliminar} fue eliminado.")
                     guardar_stock()

                     registros[producto] = {"categoria": categoria, "producto": producto,  "codigo": codigo, "cantidad": cantidad2, "precio": precio, "vencimiento": vencimiento, "fecha": fecha}
                     
                     guardar_registros()
                     
                     return  #Return para salir de la función después de eliminar un producto
                  elif eliminar == "salir":
                     print("Saliendo...")
                     return
         print("El producto no fue encontrado en el stock.") #Si termina el bucle y ningún producto coincide lanza este mensaje y termina esta función.
         return
      elif opcion == "salir":
         print("Saliendo...")
         break
    
      else:
         print("Selección incorrecta, vuelve a intentarlo.")


# (4) Modificar Productos

def modificar_producto(): 
   global stock
   global volver

   print("---- Modificar Producto -----") 
   print("Primero debes buscar el producto que deseas modificar.")
   try: #Intenta obtener estos valores, en caso de que el usuario al buscar el produzco intente salir daría error si no estuviera el try.
      categoria, producto, precio, cantidad = buscar_producto() 
   except: #Si dio el error termina.
      return
   print("Producto encontrado.")

   print() #Si siguió el bucle, continua.
   print("¿Deseas cambiarle el precio a tu producto?")
   print("1. Si")
   print("2. No")
   while not volver: #El bucle continua mientras que volver tenga el valor False.
      opcion = input("Introduce tu elección: ")
      opcion = opcion.lower()
      if opcion == "1" or opcion == "si":
         while True:
            try:
               precio = input("Introduce el nuevo precio: $")
               precio = float(precio)
               volver = True #Funciono perfecto, termina de pedir el precio y continua el codigo.
               break
            except:
               print("Precio incorrecto.") #En caso de se intente introducir caracteres como precio da error.

      elif opcion == "2" or opcion =="no": #Si no desea cambiar el precio se obtendrá el que ya estaba.
         precio = stock[categoria][producto]["precio"] #Obtiene el precio ya registrado cuando se añadió el producto.
         print("No se modifica el precio.")
         volver = True 
      else: 
         print("Selección incorrecta.")

   volver = False
   print()
   print("¿Deseas cambiarle el codigo a tu producto?")
   print("1. Si")
   print("2. No")
   while not volver:
      opcion = input("Introduce tu elección: ") 
      opcion = opcion.lower() 
      if opcion == "1" or opcion == "si":
         while True:
            codigo = input("Introduce el nuevo codigo: #")
            codigo = codigo.lower() #Siempre se busca convertir lo ingresado por el usuario a minúscula para evitar errores de escritura.
            
            if codigo == "salir":
               print("Saliendo...")
               return
            
            if codigo.strip(): #Si no es un input vació se inicia, luego crea la variable codigo_existe false para que si el codigo es igual a alguno que ya esta en el
               codigo_existe = False

               for cat, productos in stock.items(): #cat toma la primer key y productos toma la que esta dentro de categoria, si estuviera solo productos tomaría el valor de categoria.
                     for prod, detalle in productos.items():
                        if detalle["codigo"] == codigo:
                           codigo_existe = True #Si se encuentra con que el codigo almacenado en algún producto del stock coincide con el nuevo codigo ingresado lo convierte a True.
                           break

               if codigo_existe: 
                     print("El código ya existe o es el mismo, ingresa otro.")
               else:
                     print("Código único registrado.")
                     volver = True #Termina el bucle y continua.
                     break
            else:
               print("Por favor, ingresa un código válido.")

      elif opcion == "2" or opcion =="no":
         codigo = stock[categoria][producto]["codigo"] #Obtiene el codigo ya registrado cuando se añadió el producto.
         print("No se modifica el codigo.")
         volver = True

      else:
         print("Selección incorrecta, vuelve a intentarlo.")

   volver = False
   print()
   print("¿Deseas cambiarle la cantidad a tu producto?")
   print("1. Si")
   print("2. No")
   while not volver:
      opcion = input("Introduce tu elección: ")
      opcion = opcion.lower()
      if opcion == "1" or opcion == "si": #Si desea cambiarle la cantidad.
         while True:
            try:
               cantidad = input("Introduce la nueva cantidad: ")
               cantidad = float(cantidad)
               cantidad = round(cantidad) #Redondea la cantidad, seria absurdo que se almacene 3.5 de cantidad para la venta.
               volver = True
               break
            except:
               print("cantidad incorrecta.") #En caso de introducir un string.
      elif opcion == "2" or opcion =="no":
         cantidad = stock[categoria][producto]["cantidad"] #Obtiene la cantidad ya registrada cuando se añadió el producto.
         print("No se modifica la cantidad.")
         volver = True
      else:
         print("Selección incorrecta, vuelve a intentarlo.")

   vencimiento = stock[categoria][producto]["vencimiento"] #Obtiene el vencimiento ya registrado cuando se añadió el producto.
         

   volver = False
   stock[categoria][producto] = {  "codigo": codigo, "cantidad": cantidad, "precio": precio, "vencimiento": vencimiento} #Guarda los cambios para dicho producto.
   guardar_stock()

   print()
   print("Modificación guardada correctamente.")
   

# (5) Mostrar productos

def mostrar_productos(): 
   global stock
   print("----Mostrar productos---")
   if len(stock) == 1: #Si el diccionario stock esta vació, porque solo contiene el elemento predeterminado, tira este mensaje de error.
      print("No hay productos registrados.")
      return
   
   for categorias, productos in stock.items(): 
      for prod, detalle in productos.items():
         if prod == "almacen": #Si el producto a mostrar es "almacen" no lo mostrara y continuara con el bucle.
            continue
         else: #Mostrara los demas productos. 
            print()
            print(f"Categoría: {categorias}")
            print(f"Nombre: {prod}")
            print(f"Su codigo es: #{detalle['codigo']}")
            print(f"Cantidad: {round(detalle['cantidad'])}") 
            print(f"Precio: ${round(detalle['precio'])}")
            print(f"Su fecha de vencimiento es: {detalle['vencimiento']}")


# (6) Vencimientos Próximos

def vencimientos_proximos(): 
    global stock #Se deja en claro que se operara con el diccionario global stock y no con la variable local "stock"
    print("---- Vencimientos Próximos ----")
    productos_proximos_vencimiento = [] #Array para guardar los productos que van a vencer.
    vencidos = [] #Array para guardar los productos vencidos.
    fecha_actual = datetime.now() #Se obtiene la fecha actual para luego operar con ella.

    if len(stock) == 1: #Si el archivo json stock solo tiene el valor predeterminado "almacen" muestra el mensaje y vuelve al anterior menu.
       print("No hay productos registrados.")
       return
    
    for categoria, productos in stock.items(): #Se obtendrá los valores "Categoría y productos" de el diccionario stock, categoria el valor de la key y productos el valor dentro de categorias. 
        for producto, detalle in productos.items(): #Detalle es lo que hay dentro de stock/productos funcionando para obtener el valor que se desee.
            vencimiento = datetime.strptime(detalle["vencimiento"], "%d/%m/%Y") #Se obtiene la key "vencimiento" dentro de cada producto.
            dias_restantes = vencimiento - fecha_actual #Se opera para saber los días restantes.
            dias_restantes = dias_restantes.days #Solo se quedara con el .days para no mostrar el resto con el formato de horas.

            if dias_restantes >= 0: #Si queda por lo menos unas horas restantes, el producto se guardara.
                detalle["dias_restantes"] = dias_restantes
                if producto == "almacen":
                   continue #Seguirá con el programa y no mostrara el producto "almacen" en los vencimientos próximos para que no se vea feo.
                else:
                  productos_proximos_vencimiento.append((categoria, producto, detalle))
            else: #Si el producto ya venció se guardara.
               detalle["vencido"] = dias_restantes
               vencidos.append((categoria, producto, detalle))

    try:  #Se intenta mostrar el producto con sus respectivas características, en caso de dar error se ejecuta lo de "except"
      for categoria, producto, detalle in productos_proximos_vencimiento: 
         print(f"Categoría: {categoria}, Producto: {producto}, Vencimiento: {detalle['vencimiento']}, Días restantes: {detalle['dias_restantes']}")
    except: 
       print("No hay mas productos proximos a vencer.")

    
    try: #Se mostraran los productos vencidos.
      for categoria, producto, detalle in vencidos:
         print()
         print(f"Categoría: {categoria}, Producto: {producto}, Vencimiento: {detalle['vencimiento']}, Vencido hace: {detalle['vencido']} dias")
    except:
      print("No hay mas productos vencidos.")
       
    return


# (7) Registro de productos eliminados

def registros_todos():
   print("---- Productos Eliminados ----")
   if not registros: #Si no hay por lo menos un elemento en registros dará error.
      print("No se encuentran productos eliminados registrados.")
      return

   try:
        for productos in registros.keys(): #Productos toma el valor de cada key de registros, luego se la usa para imprimir el detalle de cada uno.
            print()
            print(f"Fecha de eliminación: {registros[productos]['fecha']}")
            print(f"Categoría: {registros[productos]['categoria']}")
            print(f"Producto: {registros[productos]['producto'] }")
            print(f"Cantidad: {round(registros[productos]['cantidad'])}")
            print(f"Precio: ${round(registros[productos]['precio'])}")
            print(f"Código: #{registros[productos]['codigo']}")
            print(f"Vencimiento: {registros[productos]['vencimiento']}")

   except: #En caso de que no se pueda imprimir algún producto tirara este error, no debería pasar.
      print("Ocurrió un error inesperado.")

   return


#Menu Admin
# (2) Menu trabajar

def menu_trabajar(): 
   cargados = 1 #Se usa para enumerar los productos que están en el carrito.
   caja = 1 #Numero de caja operante.
   carrito = {} #Diccionario para guardar los productos que van a ser vendidos.
   total = 0 #Variable para hacer las cuentas.
   oferta = "2" #Oferta de forma predeterminada estará como que no esta el producto en oferta.

   while True:
      print()
      print("---- Trabajando ----")
      print()
      print("1. Mirar carrito")
      print("2. Agregar producto al carrito.")
      print("3. Devolver producto.")
      print("4. Imprimir ticket.")
      print("5. Salir.")
      print(f"Caja numero: {caja}")
      print()
      opcion = input("Coloca tu selección ('salir' para cancelar en cualquier momento): ")
      opcion = opcion.lower()

      if opcion == "1": #Opción "1" Visualizar carrito.
          print()
          while True: #El bucle esta para poder salir de las opciones y volver al menu.
            if not carrito: #Si el carrito esta vació tirara este mensaje.
               print("No hay productos para mirar.")
               break

            print("Productos en el carrito:")

            for producto, det in carrito.items():
               print(f"Numero de Producto {det['producto']}: {producto} ${det['precio']} * {det['cantidad']}")
            
            print(f"Total a pagar: ${total}") #Mostrara el total a pagar.
            break

      elif opcion == "2": #Opción "2" Añadir producto.
         try: 
            categoria, producto, precio, cantidad  = buscar_producto() #Busca el producto a agregar.     
            fecha = datetime.now()
            hora = fecha.strftime("%H:%M:%S")
            fecha = fecha.strftime("%d/%m/%Y") #Acomoda al formato a Dia/Mes/Año    
      
            while True:
               print()
               llevar = input("¿Cuantas unidades llevara?: ")
               try:
                  llevar = int(llevar)
                  if llevar > cantidad: #Si la cantidad a llevar no coincide con la cantidad almacenada en el stock, mostrara este mensaje.
                     print("Estas intentando vender mas productos de los que hay en stock, inténtalo de nuevo.")
                  else:
                     break
               except:
                  print("Introduce una cantidad correcta.") #El usuario introdujo un string.
            if llevar >= 2:
               print()
               print("¿El producto esta en oferta 2x1?:")
               print("1. Si") 
               print("2. No")
               oferta = input("Introduce tu seleccion: ")
               oferta = oferta.lower()
            while True:
               if producto not in carrito: #Si el producto no se encuentra en el carrito, lo añadirá.
                  print()
                  print(f"Cantidad a llevar: {llevar}")
                  if oferta == "1" or oferta == "si" and llevar > 1: #Verifica la opcion del usuario y verifica que lleve mas de una cantidad.
                        oferta = "si"
                        prep = precio* (llevar-1) #Resta un producto del que lleva para hacer el calculo.
                        print(f"Total de precio por cantidad: ${prep}")
                        print()
                  else: #Si no ingresa su opcion se tomara como que no tiene oferta.
                     oferta = "no"
                     prep = precio*llevar #Calcula el precio del producto junto a la cantidad.
                     print(f"Total de precio por cantidad: ${prep}")
                     print()

                  carrito[producto] = {"producto": cargados, "precio": precio, "cantidad": llevar, "fecha": fecha, "oferta": oferta, "hora": hora} #Se añadirá esto al carrito.
                  total = total + prep #Calcula y suma entre todos los productos.
                  print("Productos en el inventario:")

                  for producto, det in carrito.items(): #Muestra la lista actualizada de los productos que se encuentran en el carrito.
                     oferta = det["oferta"] 

                     print(f"Numero de Producto {det['producto']}: {producto} ${det['precio']} * {det['cantidad']}   Oferta2x1: {oferta}")

                  print(f"Total: ${total}") #Muestra el total.
                  cargados = cargados + 1
                  oferta = "2" #Devuelve el valor original a oferta.
                  break
               else:
                  print("El producto ya se encuentra en el carrito, eliminalo, cuenta todos y añádelos por única vez.") #Da este mensaje de error.
                  break 
         except:
            print("Error, vuelve a intentarlo.")

      elif opcion == "3":  #Opcion "3" Devolver Producto.

         while True:
            if not carrito: #Si no hay productos en el carrito, dará este mensaje de error.
               print("No hay productos en el carrito.")
               break   
            else: 
               print() 
               producto = input("Ingrese el producto a devolver: ") #Pide el producto a devolver
               producto = producto.lower()
               for prod, detall in carrito.items():
                  if prod == producto: #Si prod es igual al producto que va a devolver el usuario, entra.
                     llevar = carrito[producto]["cantidad"] #Se obtiene la cantidad que se lleva para que no se pueda devolver mas de lo que llevas.
                     precio = carrito[producto]["precio"]
                     while True:
                        try:
                           devolver = input("¿Cuantos productos vas a devolver?: ") #Pide la cantidad a devolver.
                           devolver = int(devolver) #Comprueba que es un entero.
                           print(f"Vas a devolver {devolver} de {producto}") 
                           if devolver <= llevar: #Lo que devuelve tiene que ser igual o menor a lo que lleva.
                              print()
                              oferta = carrito[producto]["oferta"]
                              aux = llevar - devolver
                              aux2 = False

                              if oferta == "si": #Si el producto tiene oferta pasara por aca.
                                 if llevar > 2:
                                    total = total - (precio*devolver)  #Al total a pagar se le resta lo que se devolvió.
                                    if aux == 1: #Si la cantidad que quedara al finalizar la operación es 1 se tomara esto.
                                       total += precio

                                       print(f"Producto devuelto, total: ${total}, se restaron ${(precio*devolver)} pero se sumaron ${precio} dado a que queda un producto. ")
                                       aux2 = True

                                    if total < 0: #En un caso muy raro donde el total sea negativo se restablecerá a 0.
                                       total = 0
                                       print(f"Producto devuelto, total: ${total}, se restaron ${(precio*devolver)}")
                                       
                                    elif total > 0 and aux2 == False: #Si se pone con ese se mostrara si previamente se agrego el valor al precio.
                                       print(f"Producto devuelto, total: ${total}, se restaron ${(precio*devolver)}")


                                 elif llevar > 1:
                                    total = total - (precio*(devolver-1)) #Al total a pagar se le resta lo que se devolvió.
                                    print(f"Producto devuelto, total: ${total}. No se resto nada dado a que era una promoción.") 


                                 else:
                                    total = total - (precio*(devolver-1)) #Al total a pagar se le resta lo que se devolvió.
                                    print(f"Producto devuelto, total: ${total}, se restaron ${(precio*devolver)}") 

                              else:
                                 total = total - (precio*devolver) 
                                 print(f"Producto devuelto, total: ${total}, se restaron ${precio*devolver}")


                              llevar = llevar - devolver #Se restara los productos devueltos de los que lleva el cliente.

                              if oferta == "si":
                                 if llevar > 1:
                                    oferta = "si"
                                 else:
                                    oferta = "no"

                              carrito[producto] = {"producto": cargados, "precio": precio, "cantidad": llevar, "fecha": fecha, "oferta": oferta, "hora": hora }

                              print(f"Quedan {llevar} de {producto}")
                              break

                           else:
                              print("La cantidad que vas a devolver no coincide con la cantidad que llevas.") #En caso de que no se coincida.
                        except:
                           print("Cantidad incorrecta.") #En caso de ser un string.
                  
               if llevar == 0: #Borra si en el carrito no hay mas productos o hay cantidad 0
                  del carrito[producto]
               break

      elif opcion == "4":  #Opción "4" imprimir ticket.
         while True:
            if not carrito: #Comprueba que el carrito no este vació.
               print("No hay productos como para imprimir un ticket.")
               break
            
            else: 
               print("---Método de pago---")
               print("1. Efectivo")
               print("2. Tarjeta")
               print("3. Otro")
               print()
               pago = input("¿Cual es el método de pago?: ")
               monto = input("¿Con cuanto dinero se pago?: $")
            
               try: 
                  monto = float(monto) #Convierte el monto en un float para asegurarse que no sea un string.
               
                  if monto >= total: #El pago debe ser mayor al total a pagar, de lo contrario no se imprime el ticket.
                     try:
                        calcular_ganancias(carrito) #Se le da el carrito a calcular ganancias.
                        ticket(total, carrito, monto, pago) #Se le dan estos valores a la función ticket
                     except:
                        print("Error al añadir los productos a las ganancias")
                     carrito = {} #Al imprimir el ticket se toma como que la compra se realizo, por lo tanto se reinicia el carrito.
                     break
                  else:
                     print("Error, el pago no puede ser menor al total a pagar cuando se imprime el ticket.") #da mensaje de error.
                     print()
               except:
                  print("Monto incorrecto. ")

      elif opcion == "5" or opcion == "salir": #Si selecciona 5 o introduce salir.
         print("Volviendo al anterior menu...") #Vuelve al menu.
         return
      
      else:
         print("Opción incorrecta, inténtalo de nuevo.")


# (4) Menu trabajar - Imprimir ticket

def ticket(total, carrito, monto, pago): #Obtiene los valores anteriormente dados.
   fecha = datetime.now()
   fecha = fecha.strftime("%d/%m/%Y") #Se obtiene la fecha actual y se la ordena con el formato Dia/Mes/Año

   print()
   print("SUPERMERCADO MOSRAU") #Este es un ejemplo del nombre del supermercado, no existe y deberá reemplazarse por el deseado, al igual que los datos.
   print("C. U.I .T. Nro: 20-9527238282-88")
   print("Domicilio: CALLE 12 6975- C.P 1757")
   print(f"Dia de la compra: {fecha}") 
   print()
   print("===Productos===")
   print()


   for producto, det in carrito.items():
      llevar = det["cantidad"] 
      precio = det["precio"]
      precio = round(precio)
      oferta = det["oferta"]
      
      if oferta == "si":
         print(f"Numero de Producto {det['producto']}: {producto}    ${precio} * {llevar} = {precio*llevar}     Oferta 2x1: {oferta}")
         print(f"Descuento 2x1: ${precio}")
         print()
      else:
         print(f"Numero de Producto {det['producto']}: {producto}    ${precio} * {llevar} = {precio*llevar}     Oferta 2x1: {oferta}")
         print()
            
   print("========================")
   print(f"Total a pagar: ${total}")
   print("========================")
   print(f"Pago: ${monto}")
   vuelto = monto - total
   vuelto = round(vuelto)
   print(f"Su vuelto: ${vuelto}")
   if pago == "efectivo" or pago == "1":
      print("Se pago en efectivo.")
   elif pago == "tarjeta" or pago == "2":
      print("Se pago con tarjeta.")
   else:
      print("Otro método de pago")

   print()
   print("        Orientación al consumidor        ")
   print("PROVINCIA DE BUENOS AIRES TEL 0800-222-9042")
   print("REGISTRO: EPEPAAA00000028487")



   acomodar_productos(llevar, carrito) #Acomodara la cantidad de productos vendidos con los que quedaran en el stock.
   return


#En base a la lógica del programa, si se imprime el ticket se tomara que se vendió el producto y se descontara del stock, registrando la ganancia.

def acomodar_productos(llevar, carrito): 
   global stock
   global ingresa_usuario #Se necesita el ingresa_usuario para saber que usuario realizo la venta.

   print()
   total = 0 #Se usara para obtener la cantidad que en verdad quedara en el stock.

   for carro, det in carrito.items():
         for categoria, productos in stock.items():
            for producto, detalle in productos.items():
               if carro == producto: #Si el producto del carrito coincide con el producto del stock continua.
                  cant_lleva = det["cantidad"] #Obtiene la cantidad que lleva el cliente de tal producto.
                  cantidad = detalle["cantidad"] #Obtiene la cantidad que hay en el stock.
                  total = cantidad - cant_lleva  #Calcula la cantidad que quedaría.
                  total = round(total)
                  precio = detalle["precio"] #También obtiene el precio del producto que se vendió para guardarlo nuevamente.
                  vencimiento = detalle["vencimiento"] #Obtiene el vencimiento.
                  codigo = detalle["codigo"] #El codigo.
                  stock[categoria][producto] = {  "codigo": codigo, "cantidad": total, "precio": precio, "vencimiento": vencimiento} #Guarda de nuevo el producto en el stock actualizado con la cantidad correspondiente.


   for carro, det in carrito.items(): #Este for esta para registrar las ventas hechas.
      if carro in ventas: #Si el producto del carro esta ya registrado en alguna venta anterior, se tomaran los valores de esa venta y se realizaran los cálculos correspondientes.
         obtenido = ventas[carro]["cantidad"] #Se obtiene la cantidad que se había llevado anteriormente para luego sumarla.
         vieja = ventas[carro]["ganancia"] #Se obtiene la ganancia obtenida anteriormente por el producto para luego sumarla. 
         fecha = det["fecha"] #Se obtiene la fecha de la ultima venta.
         hora = det["hora"]
         cant_lleva = det["cantidad"] #Obtiene la cantidad nueva
         precio = det["precio"]
         ganancia = cant_lleva*precio #Se calcula la ganancia
         obtenido += cant_lleva #Se suma la cantidad obtenida con la cantidad que se lleva actualmente.
         ganancia += vieja  #Se suma la ganancia vieja con la actual.
         ventas[carro] = {"producto": carro, "cantidades": obtenido, "cantidad": cant_lleva, "precio": precio, "ganancia": ganancia, "fecha": fecha, "usuario": ingresa_usuario, "hora": hora} #En esta parte se registra la venta

      else:
         fecha = det["fecha"] #Obtiene la fecha en la que se vendió el producto.
         hora = det["hora"]
         cant_lleva = det["cantidad"] #Se carga la cantidad que es vendida.
         precio = det["precio"] #Se carga el precio actual del producto a ser vendido.
         ganancia = cant_lleva*precio #Calcula la ganancia sin impuestos.
         ventas[carro] = {"producto": carro, "cantidades": cant_lleva, "cantidad": cant_lleva, "precio": precio, "ganancia": ganancia, "fecha": fecha, "usuario": ingresa_usuario, "hora": hora}
   guardar_ventas() #Llama esta función que sirve para guardar las ventas.

   guardar_stock()           
   print("Cargado al sistema.")




#Se registraran las ventas hechas para que el administrador pueda observar las ganancias y tener un control sobre sus empleados.

def registrar_ventas(): #Sirve para mirar las ventas.
   print()
   print("---- Productos Vendidos ----")
   if not ventas: #Si no hay ventas que mirar, mostrara el siguiente mensaje.
      print("No se encuentran productos vendidos registrados.")
      return

   
   for productos in ventas.keys(): #Productos tomara el valor de cada key de ventas.
      print()
      if productos == "almacen": #Si la venta es "Almacen" se trata de forma diferente.
         print(f"Usuario que realizo la ultima venta: {ventas[productos]['usuario']}")
         print(f"Fecha de venta: {ventas[productos]['fecha']} Hora: {ventas[productos]['hora']}")
         print(f"Producto: {ventas[productos]['producto'] }")
         print(f"Cantidad: {round(ventas[productos]['cantidad'])}")
         print(f"Cantidad total: {round(ventas[productos]['cantidades'])}")
         print(f"Precio: ${round(ventas[productos]['precio'])}") #No se mostrara las ganancia sin impuestos en "almacen" dado a que el precio varia según lo que elija el empleado.
      else: #Mostrara todos los datos.
         print(f"Usuario que realizo la ultima venta: {ventas[productos]['usuario']}")
         print(f"Fecha de venta: {ventas[productos]['fecha']}  Hora: {ventas[productos]['hora']}")
         print(f"Producto: {ventas[productos]['producto'] }")
         print(f"Cantidad: {round(ventas[productos]['cantidad'])}")
         print(f"Cantidad total: {round(ventas[productos]['cantidades'])}")
         print(f"Precio: ${round(ventas[productos]['precio'])}")
   return


# (3) Ganancias - Aca se hacen los cálculos y esta implementado en el menu de admin el mostrar las ganancias.

def calcular_ganancias(carrito): #Esta función esta encargada de hacer los cálculos para saber cuanto gana el dueño realmente.
   global impuestos #Se necesita operar con la variable global impuestos para mantener los impuestos actualizados en todo momento
   global ganancias #Se usa la variable global ganancias para que se actualice en tiempo real.
   total_impuestos = 0

   for nombre, porcentaje in impuestos: #calcula los impuestos que deberá aplicar al producto.
         total_impuestos += porcentaje #Por cada vuelta de el bucle for se tomara el porcentaje del impuesto y se lo sumara a total_impuestos.
   total_impuestos = total_impuestos / 100 #Lo divide en 3 para hacer la regla de tres simple.

   for carro, det in carrito.items(): 
         gananciap = 0 #Ganancia por producto.
         llevar = det["cantidad"] #Se obtiene la cantidad que se vendió
         can = det["cantidad"]
         precio = det["precio"] #Se obtiene el precio al que se vendió el producto. 
         oferta = det["oferta"]
         if oferta == "1" or oferta == "si":
            llevar -= 1
         else:
            print()

         if carro in ganancias["ganancias_productos"]: #Si el carro ya se tomo como una ganancia operara de la siguiente forma:

            viejo = ganancias["ganancias_productos"][carro]["ganancia"] #Obtiene las ganancias anteriores
            gananciap = (precio*llevar) - ((precio *llevar) * total_impuestos) + viejo #Se calcula la ganancia por producto obteniendo la ganancia sin impuestos, luego se obtiene nuevamente y a eso se lo multiplica por los impuestos, obteniendo la ganancia real.
            obtenido = ganancias["ganancias_productos"][carro]["cantidad"] #Obtiene la cantidad antes vendida
            can += obtenido #Suma la cantidad antes vendida con la que se lleva para actualizarla cuando se muestren las ganancias.

            ganancias["ganancias_productos"][carro] = {"ganancia": gananciap, "cantidad": can} #Dentro de el archivo ganancias, en la parte de "ganancias_productos" se guardara el producto con sus respectivas características de ganancias.
            
         else:
            gananciap = (precio*llevar) - ((precio * llevar) * total_impuestos) #Calcula la ganancia por producto, primero obteniendo la ganancia sin impuestos y luego restando por la ganancia aplicada con impuestos.
            ganancias["ganancias_productos"][carro] = {"ganancia": gananciap, "cantidad": can} 

   guardar_ganancias() #Se guarda todo.
   

# (4) Gestionar cuentas

def gestionar_cuentas(): 
   global ingresa_usuario #Obtengo el usuario que esta ahora mismo
   global ingresa_contrasena #Obtengo la contraseña actual sin necesidad de pedirlo del diccionario, ademas de poder verificar credenciales.
   global rol #¿Que rol tiene el usuario actual?
   global volver #Se lo usara para el mismo fin que bandera.
   bandera = False #Se usara para salir de un bucle dentro de otro bucle.
   intentos = 3 #En este caso solo tendrá 3 intentos.

   while True:
      contrasena = input("Por favor, ingresa tu contraseña antes de hacer algún cambio ('salir' para cancelar): ") #Se solicita la contraseña al entrar a este menu dado a que puede contener información sensible.
      if intentos == 0: 
         print("Demasiados intentos, vuelve a iniciar sesión.")
         return intentos #Devuelve intentos para que termine todo el programa y vuelva a iniciar sesión.
      
      if contrasena != ingresa_contrasena:
         print(f"Contraseña incorrecta, tienes {intentos} intentos.")
         intentos -= 1
      else: #Si la contraseña es correcta, continua el programa.
         break

      contrasena = contrasena.lower() #Convierte la contrasena a minúscula para saber si ingreso salir
      if contrasena == "salir":
         print("saliendo...")
         return
   
   while True:
      
      print("1. Visualizar Cuentas Existentes.") 
      print("2. Gestionar Esta Cuenta.") 
      print("3. Gestionar Otra Cuenta.")
      print("4. Volver.")
      print()
      eleccion = input("Ingresa tu selección ('salir' para cancelar): ")
      eleccion = eleccion.lower()
      if eleccion == "salir" or eleccion == "4": #Si el usuario ingresa 4 o "salir" termina el bucle.
         print("Saliendo...")
         return
      elif eleccion == "1": 
         for usuario in usuarios:  #Este for muestra todos los usuarios y sus roles.
            print(f"Usuario: {usuario}") # "Usuario" tomara el valor de cada key de usuarios.
            print(f"Rol: {usuarios[usuario]['rol']} ") #Mostrara el rol correspondiente al usuario obtenido del for.
            print()
         

      elif eleccion == "2": 
         print()
         while not volver: #Bucle donde se incluye toda la opcion 2.
               print("¿Deseas cambiarle el nombre a esta cuenta?: ")
               print("1. Si.")
               print("2. No.")
               while True:
                  print()
                  eleccion = input("Ingresa tu eleccion: ")
                  if eleccion == "1": #Si elige cambiarle el nombre.
                     nombre = input("Ingresa tu nuevo nombre de usuario: ") 
                     if nombre in usuarios: #Si ese nombre ya esta registrado a alguna cuenta muestra el print()
                        print("Este nombre de usuario ya existe o es igual al actual, introduce otro.")
                     else: #Si el nombre de usuario no esta registrado en ninguna cuenta permitirá hacer el cambio.
                        del usuarios[ingresa_usuario] #Elimina el usuario actual para evitar problemas.
                        print("Nombre de usuario cambiado.") # Vas a tener que iniciar sesión con tu nuevo usuario
                        break
                     
                  elif eleccion == "2": #Si no se cambia el nombre de usuario se mantiene.
                     print("No se cambio el nombre de usuario.")
                     nombre = ingresa_usuario #Se cambia para que luego sea mas fácil guardarlo por su eleccion.
                     break

               print()
               print("¿Deseas cambiarle la contraseña?")
               print("1. Si")
               print("2. No.")
               while not bandera: #Bucle donde el usuario introducirá su eleccion.
                  eleccion = input("Ingresa tu eleccion: ")
                  if eleccion == "1":
                     print()
                     while True:
                        ingresa_contrasena = input("Ingresa la nueva contraseña: ")
                        if len(ingresa_contrasena) >= 5: #Si la contraseña tiene por lo menos 5 caracteres la permitirá.
                           print("Contraseña cambiada.")
                           bandera = True #Cambia a True para que se termine el bucle y siga con el codigo.
                           break #Detiene el bucle True
                        else:
                           print("introduce una contraseña valida, debe tener mas de 4 caracteres.")
                           print()
                  elif eleccion == "2":
                     print("Contraseña no cambiada.")
                     bandera = True
                     
                  else:
                     print("Selección incorrecta, vuelve a intentarlo.") 
               volver = True #Termine el bucle de la opcion 2.
               
         volver = False #Devuelve su valor para que cuando inicie sesión no lo saque.
         print("Datos actualizados correctamente, vuelve a iniciar sesión.")
         usuarios[nombre] = {"contrasena": ingresa_contrasena, "rol": rol} #Actualiza los datos.
         guardar_usuarios() #Guarda los usuarios en un json.
         intentos = 0 
         return intentos #Vuelve al anterior menu con el valor de intentos = 0 para que se vuelva a iniciar sesión.
      
      elif eleccion == "3": 
         print()
         while not volver: 
            nombre = input("Ingresa el nombre de usuario de la cuenta a gestionar: ")
            if nombre == ingresa_usuario: #Si el nombre de usuario de la cuenta a gestionar coincide con la sesión actual tira este mensaje.
               print()
               print("¿Intentas cambiarle el nombre a tu cuenta? hazlo desde el menu correspondiente.")
               return
            
            if nombre in usuarios: #Si el nombre ya esta registrado en el diccionario usuarios, continuara el programa.
               con = usuarios[nombre]["contrasena"] #Toma la contraseña del usuario al que se le cambio el nombre.
               roll = usuarios[nombre]["rol"] #toma el rol del usuario ingresado
               
               print("¿Deseas cambiarle el nombre a esta cuenta?: ")
               print("1. Si.")
               print("2. No.")
               while True:
                  print()
                  eleccion = input("Ingresa tu eleccion: ")
                  if eleccion == "1":
                     nuevo = input(f"Ingresa el nuevo nombre de la cuenta {nombre}: ")
                     if nuevo in usuarios: #Si el nuevo nombre de la cuenta ya esta registrado, pedirá otro.
                        print("Ese nombre de usuario ya existe, ingresa otro.")
                     else: #Si ese nombre es "nuevo" se lo tomara como valido.
                        del usuarios[nombre]
                        print(f"El nombre de la cuenta {nombre} fue cambiado a {nuevo}")
                        break
                  elif eleccion == "2": #En caso de elegir no, se guardara el nombre anterior.
                     nuevo = nombre
                     print("Nombre no cambiado.")
                     break
                  else:
                     print("Selección incorrecta. Vuelve a intentarlo.")

               print()
               print("¿Deseas cambiarle el rol?")
               print("1. Cambiar rol.")
               print("2. No.")
               while True:
                  print()
                  eleccion = input("Coloca tu eleccion: ")
                  if eleccion == "1": #Si elige cambiarle el rol va a tener que seleccionar por cual de los dos roles posibles.
                     print("1. Admin")
                     print("2. Usuario")
                     rolnuevo = input("Ingresa el nuevo rol que tendrá el usuario: ")
                     if rolnuevo == "1":
                        roll = "admin"
                        print(f"El nuevo rol para {nuevo} es: '{roll}'")
                        break
                     else:
                        roll = "usuario" #Se forma predeterminada si no se elije el rol se le asignara "usuario".
                        print(f"El nuevo rol para {nuevo} es: '{roll}'")
                        break
                  elif eleccion == "2":
                     print(f"El rol para el usuario {nuevo} sigue siendo {roll}") #Si elije que no se mantiene el rol.
                     break
                  else:
                     print("Selección incorrecta, vuelve a intentarlo.")
                     
               print()
               print("¿Deseas cambiarle la contraseña?")
               print("1. Si")
               print("2. No.")
               while not bandera:
                  eleccion = input("Ingresa tu eleccion: ")
                  if eleccion == "1":
                     print()
                     while True:
                        con = input("Ingresa la nueva contraseña: ")
                        if len(con) >= 5:
                           print("Contraseña cambiada.")
                           bandera = True
                           break
                        else:
                           print("introduce una contraseña valida, debe tener mas de 4 caracteres.")
                           print()
                  elif eleccion == "2":
                     print("Contraseña no cambiada.")
                     bandera = True
                     
                  else:
                     print("Selección incorrecta, vuelve a intentarlo.")
               volver = True
            else:
               print("Usuario no encontrado, vuelve a intentarlo.")
               
         volver = False #Se le devuelve su valor para evitar errores.
         usuarios[nuevo] = {"contrasena": con, "rol": roll} #Guardara el usuario.
         guardar_usuarios()
         return

      else:
         print("Selecciona algo valido.")
      

#Gestionar impuestos

# (1) Observar impuestos
def observar_impuestos():
   global impuestos
   print()
   print("Observa estos impuestos:")
   for i in range (len(impuestos)):

      nombre = impuestos[i][0]
      porcentaje = impuestos[i][1]
            
      
      print(f" {i+1}. {nombre} tiene {porcentaje}% de impuesto.")  
      i += 1
   return i #Devuelve i para conocer cuantos elementos tiene la lista.


# (2) Agregar impuesto

def agregar_impuesto(): 
    global impuestos
    while True:
        nombre = input("Ingrese el nombre del impuesto ('salir' para terminar): ")
        nombre = nombre.lower()
        if nombre == "salir":
            print("Saliendo...")
            break
        if not nombre.strip():
            print("Introduce un impuesto valido.") #El nombre del impuesto no puede estar vació
        else:
            try:
                  porcentaje = float(input(f"Ingrese el porcentaje del impuesto '{nombre}': ")) #Pide el porcentaje que usara ese impuesto.
                  impuestos.append((nombre, porcentaje)) #Se lo añade a la lista.
                  observar_impuestos()
                  break
            except:
                  print("Error: Por favor, ingrese un porcentaje válido.")
    guardar_impuestos()
    return


# (3) Borrar impuestos

def eliminar_impuesto(): 
   global impuestos

   i = observar_impuestos() #En base a los elementos que tiene la lista serán los que podrá seleccionar el usuario.

   while True:
      try:
         print()
         seleccion = input("¿Que impuesto deseas eliminar? ('salir' para terminar): ")
         if seleccion == "salir":
            return
         seleccion = int(seleccion)
         if seleccion > i or seleccion <= 0:
            print("Error, vuelve a seleccionar el impuesto a eliminar")
         else:
            seleccion -= 1 #Se resta uno para que la posición del elemento elegido por el usuario coincida, es una forma de engaño visual.
            impuestos.pop(seleccion)
            print(f"Impuesto eliminado correctamente.")
            guardar_impuestos()
            break
      except:
         print("Intenta seleccionar correctamente el impuesto a eliminar.")


#Obtiene los archivos necesarios para que el programa funcione correctamente.

cargar_usuarios()
cargar_stock()
cargar_registros()
cargar_ventas()
cargar_impuestos()
cargar_ganancias()


#Programa/Bucle principal.

while not volver:

  print()
  print("---- Inicio de sesión ---")
  print("1. Iniciar sesión")
  print("2. Registrar usuario")
  print("3. Salir")
  opcion = input("Seleccione una opcion: ")

  if opcion == "1":
      login()
      if rol == "admin" and ingresa_usuario in usuarios and usuarios[ingresa_usuario]["contrasena"] == ingresa_contrasena:
        print("Bienvenido Admin:", ingresa_usuario)
        menu_admin()
      elif rol == "usuario":
         print("Bienvenido Usuario:", ingresa_usuario)
         menu_usuario()
      else:
         print("¡Ha ocurrido un error inesperado! el rol asignado es erróneo.")
  
  elif opcion == "2":
    registro_usuario()

  elif opcion == "3":
     print("Cerrando el programa...")
     break
  
  elif intentos == 0:
     print("Demasiados intentos erróneos.")
     break
  else:
     print("Opción incorrecta, por favor selecciona una valida.")
     print(f"Intentos restantes: {intentos}")
     intentos -= 1


#Guarda todos los cambios hechos por el usuario que usa el programa.

guardar_usuarios()
guardar_stock()
guardar_registros()
guardar_ventas()
guardar_impuestos()
guardar_ganancias()