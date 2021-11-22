from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import re
import connection
import sqlite3
import tkinter as tk
import os
from datetime import date,datetime



## FUNCIONES DE VALIDACIÓN DE DATOS

def vacios(dato):
    for letra in dato:
        if(letra==""):
            return False
    return True

def validarSoloLetras(dato):
    for letra in dato:
        if(ord(letra)!=32):
            if(letra.isalpha()==False):
                return True
    return False

def validarLetrasyNumeros(dato):
    for letra in dato:
        if(ord(letra)!=32 and ord(letra)!=46):
            if(letra.isalnum()==False):
                return True
    return False

def validarSoloNum(dato):
    for letra in dato:
        if(ord(letra)!=46):
            if(letra.isdigit()==False):
                return True
    return False

def validarMayusxPalabra(dato):
    for letra in dato:
        if(ord(letra)!=32):
            if(letra.istitle()==True):
                return False
    return True

def validarLongCuitPr(num):
    num=len(str(entryCuitPr.get()))
    if num!=11:
        return True
    else:
        return False

def validarLongCuitCl(num):
    num=len(str(entryCuitCl.get()))
    if num!=11:
        return True
    else:
        return False

def validarLongTelefonoPr(num):
    for dato in num:
        dato=len(str(entryTelefonoPr.get()))
        if dato>=7 and dato<=10:
            return False
        else:
            return True

def validarLongTelefonoCl(num):
    for dato in num:
        dato=len(str(entryTelefonoCl.get()))
        if dato>=7 and dato<=10:
            return False
        else:
            return True



def App1():
    
    ventana1=tk.Tk()
    ventana1.title("Ingreso")
    ancho=ventana1.winfo_screenwidth()
    largo=ventana1.winfo_screenheight()
    x=(ancho//2)-(300//2)
    y=(largo//2)-(150//2)
    ventana1.geometry(f"{300}x{150}+{x}+{y}")
    ventana1.iconbitmap("imagenes/chip.ico")
    ventana1.resizable(0,0)
    ventana1.config(bg='#2F2783')

    fecha = date.today()
    hora = datetime.now()
    fechaActual = fecha.strftime("%d-%m-%Y")

    try:
        if(os.path.isfile("bbdd/base_datos.db"))==True:
            pass
        else:
            raise NameError
    except NameError:
        messagebox.showwarning('Sistema','Base de datos no localizada.\n Comunicarse con administrador.')

    
    usuario=Label(ventana1,text="Usuario: ",bg='#2F2783',fg='white')
    usuario.pack()

    user=StringVar()
    ingresoUsuario=Entry(ventana1, width=20,textvariable=user)
    ingresoUsuario.pack()

    contraseña=Label(ventana1,text="Contraseña: ",bg='#2F2783',fg='white')
    contraseña.pack()

    password=StringVar()
    ingresoContraseña=Entry(ventana1, width=20, show="*",textvariable=password)
    ingresoContraseña.pack()

    def abrirGestion():
        gestionar.pack_forget()
        ventana1.destroy()
        App2()

    def animacionBienvenido(ventana1):

        def ingresar():
            connection.conectar()
            ventana1.destroy()
            App3()

        frameAnimacion=Frame(ventana1,bg='orange')
        labelAnimacion=Label(frameAnimacion,text='Bievenido '+sesion,font=('Calibri',30),bg='orange',fg='black')
        labelAnimacion.pack(pady=30)
        botonIngresar=Button(frameAnimacion, text="INGRESAR",bg='#2F2783',fg='white',command=ingresar)
        botonIngresar.pack()

        def animacion(ancho,largo):
            frameAnimacion.place(x=0,y=0,width=ancho,height=largo)
            ancho +=10
            if (ancho<=300):
                frameAnimacion.after(10,lambda:animacion(ancho,largo))
        frameAnimacion.after(500,lambda:animacion(0,600))



    def verificar(evento):
        try:
            if(os.path.isfile("bbdd/base_datos.db"))==True:
                datos=(ingresoUsuario.get(),ingresoContraseña.get(),)
                global sesion
                sesion=datos[0]
                if (vacios(datos)):
                    connection.Database()
                    sql="SELECT * FROM usuarios WHERE nombreUsuario=? AND claveUsuario=?"
                    connection.cursor.execute(sql,datos)
                    busquedaUsuario=connection.cursor.fetchall()
                    if (len(busquedaUsuario)>0):
                        connection.cursor.close()
                        ingresoUsuario.delete(0,END)
                        ingresoContraseña.delete(0,END)
                        gestionar.pack_forget()
                        animacionBienvenido(ventana1)
                    else:
                        messagebox.showinfo("Ingreso", 'Usuario Incorrecto')
                else:
                    messagebox.showerror("Ingreso", "Complete todos los datos")
            else:
                raise sqlite3.OperationalError
        except sqlite3.OperationalError:
            messagebox.showwarning('Sistema','Base de datos no localizada.\n Comunicarse con administrador.')
    

    #verificar=Button(ventana1, text="VERIFICAR",bg='#2F2783',fg='white',command=verificar)
    #verificar.pack()

    gestionar=Button(ventana1, text="GESTION DE USUARIOS",bg='#2F2783',fg='white',command=abrirGestion)
    gestionar.pack()

    ingresoContraseña.bind('<Return>',verificar)

    ventana1.mainloop()







def App2():

    ventana2=tk.Tk()
    ventana2.title("Gestion de Usuarios")
    ancho=ventana2.winfo_screenwidth()
    largo=ventana2.winfo_screenheight()
    x=(ancho//2)-(300//2)
    y=(largo//2)-(150//2)
    tamaño=f"{440}x{180}+{x}+{y}"
    ventana2.geometry(tamaño)
    ventana2.iconbitmap("imagenes/chip.ico")
    ventana2.resizable(0,0)
    ventana2.config(bg='#2F2783')


    # FRAMES 
    frameVerificarPass=Frame(ventana2)
    frameVerificarPass.pack()

    frameIngreso=Frame(ventana2, bg='#2F2783')

    frBns=Frame(ventana2)


    # PARA VERIFICAR PASS
    labelVerificarPass=Label(frameVerificarPass,text="Ingresar password de administrador y presionar 'Enter'",bg='#2F2783',fg='white')
    labelVerificarPass.pack()

    passw=StringVar(frameVerificarPass)
    entryVerificarPass=Entry(frameVerificarPass, width=20, show="*",textvariable=passw)
    entryVerificarPass.pack()

    def verificarContraseña(evento):
        dato=(entryVerificarPass.get(),)
        if (vacios(dato)):
            connection.Database()
            sql="SELECT claveUsuario FROM usuarios WHERE claveUsuario=?"
            connection.cursor.execute(sql,dato)
            busquedaUsuario=connection.cursor.fetchall()
            if (len(busquedaUsuario)>0):
                mensaje=f'Bievenido {dato[0]}'
                global sesion
                sesion=dato[0]
                messagebox.showinfo("Ingreso", mensaje)
                connection.cursor.close()
                entryVerificarPass.delete(0,END)
                frameVerificarPass.pack_forget()
                frameIngreso.pack(fill=X)
                frBns.pack(fill=X,side=BOTTOM)
            else:
                messagebox.showinfo("Ingreso", 'Contraseña Incorrecta')
        else:
            messagebox.showerror("Ingreso", "Ingrese una contraseña")

    entryVerificarPass.bind("<Return>",verificarContraseña)

    # FUNCIONES CRUD

    def showPass():
        ingresoContraseña.config(frameIngreso, width=20,textvariable=password)
    def hidePass():
        ingresoContraseña.config(show="*")

    def vaciarEntryU():
        ingresoUsuario.delete(0,END)
        ingresoContraseña.delete(0,END)
        tipoUsuario.delete(0,END)

    def brUser(evento):
        busUser=[ingresoUsuario.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM usuarios WHERE nombreUsuario=?",busUser)
        connection.conn.commit()
        datoU=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryU()
        if(len(datoU)>0):
            for dato in datoU:
                    ingresoUsuario.delete(0,END)
                    ingresoUsuario.insert(END,dato["nombreUsuario"])
                    ingresoContraseña.delete(0,END)
                    ingresoContraseña.insert(END,dato["claveUsuario"])
                    tipoUsuario.delete(0,END)
                    tipoUsuario.insert(END,dato["tipoUsuario"])
                    messagebox.showinfo("Resultado de la busqueda","Encontrado")
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado ")

    def grUser():
        dato=(ingresoUsuario.get(),ingresoContraseña.get(),tipoUsuario.get(),)

        if validarSoloLetras(dato[2]):
            messagebox.showwarning("Guardar datos","Tipo Usuario debe ser sólo letras")
        
        else:
            try:
                connection.Database()
                sql="INSERT INTO usuarios(nombreUsuario,claveUsuario,tipoUsuario)VALUES(?,?,?)"
                connection.cursor.execute(sql,dato)
                connection.conn.commit()
                connection.cursor.close()
                connection.conn.close()
                messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
                vaciarEntryU()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Error en BD","Usuario existente")
            

    def mfrUser():
        dato=(ingresoUsuario.get(),ingresoContraseña.get(),tipoUsuario.get(),ingresoUsuario.get())
        if vacios(dato)==False:
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloLetras(dato[2]):
            messagebox.showwarning("Guardar datos","Tipo de Usuario debe ser sólo letras")
        else:
            connection.Database()
            connection.cursor.execute("UPDATE usuarios SET nombreUsuario=?, claveUsuario=?, tipoUsuario=? WHERE nombreUsuario=?",dato)
            connection.conn.commit()
            datosU=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryU()
            if(len(datosU)>0):
                for dato in datosU:
                    id.delete(0,END)
                    id.insert(END,dato[1])
                    nombreUsuario.delete(0,END)
                    nombreUsuario.insert(END,dato[1])
                    ingresoContraseña.delete(0,END)
                    ingresoContraseña.insert(END,dato[2])
                    tipoUsuario.delete(0,END)
                    tipoUsuario.insert(END,dato[3])
                    messagebox.showerror("Error al modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")

    def emrUser():
        datos=(ingresoUsuario.get(),ingresoContraseña.get(),tipoUsuario.get())
        if vacios(datos[0])==False:
            messagebox.showerror("Error al Eliminar","Debes colocar un usuario")
        else:
            elrUser=[ingresoUsuario.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM usuarios WHERE nombreUsuario=?",elrUser)
            connection.conn.commit()
            datosUser = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryU()
            if(len(datosUser)>0):
                for dato in datosUser:
                    id.delete(0,END)
                    id.insert(END,dato[1])
                    nombreUsuario.delete(0,END) 
                    nombreUsuario.insert(END,dato[1])
                    ingresoContraseña.delete(0,END)
                    ingresoContraseña.insert(END,dato[2])
                    tipoUsuario.delete(0,END)
                    tipoUsuario.insert(END,dato[3])
                    messagebox.showerror("Error al eliminar","Seleccionar usuario correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")


    # PARA GESTIONAR USUARIOS

    usuario=Label(frameIngreso,text="Usuario: ",bg='#2F2783',fg='white')
    usuario.grid(row=0,column=0,pady=10,padx=80)

    user=StringVar(frameIngreso)
    ingresoUsuario=Entry(frameIngreso, width=20,textvariable=user)
    ingresoUsuario.grid(row=0,column=1)

    ingresoUsuario.bind('<Return>',brUser)

    contraseña=Label(frameIngreso,text="Contraseña: ",bg='#2F2783',fg='white')
    contraseña.grid(row=1,column=0,pady=10,padx=80)

    password=StringVar(frameIngreso)
    ingresoContraseña=Entry(frameIngreso, width=20, show="*",textvariable=password)
    ingresoContraseña.grid(row=1,column=1)

    ingresoContraseña.bind("<Enter>",showPass)
    ingresoContraseña.bind("<Leave>",hidePass)

    tipoUsuario=Label(frameIngreso,text="Tipo Usuario: ",bg='#2F2783',fg='white')
    tipoUsuario.grid(row=2,column=0,pady=10,padx=80)

    comboUser = ttk.Combobox (frameIngreso,width=18)
    opcion=[]
    comboUser.grid(row=2,column=1)
    opcion.append("admin")
    opcion.append("comun")
    comboUser["values"]=opcion

    # BOTONES CRUD

    chkPass= Checkbutton(frameIngreso,variable=ingresoContraseña,onvalue=True,offvalue=False)
    chkPass.grid(row=1,column=3)

    bnCreate=Button(frBns,width=20,text='Crear',bg='#2F2783',fg='white',command=grUser)
    bnCreate.pack(side=LEFT)

    bnUpdate=Button(frBns,width=20,text='Modificar',bg='#2F2783',fg='white',command=mfrUser)
    bnUpdate.pack(side=LEFT)

    bnDelete=Button(frBns,width=20,text='Eliminar',bg='#2F2783',fg='white',command=emrUser)
    bnDelete.pack(side=LEFT)

    ventana2.mainloop()






def App3():

    ventana3=tk.Tk()
    ventana3.title("Fullgeek")
    ventana3.state("zoomed")
    ventana3.iconbitmap("imagenes/chip.ico")
    

    ###################################################################################
    #################################################################### FRAMES #######
    
    ubFrameBotones={'x':'170','y':'0','width':'1196','height':'705'}
    FrameInfoMod={'x':'170','y':'80','width':'1196','height':'545'}
    colorFrameBot={'bg':'#2C3234'}
    colorFrameMod={'bg':'#344c51'}
    fecha=date.today()
    hora=datetime.now()
    fechaActual=fecha.strftime("%d-%m-%Y")
    horaActual=hora.strftime("%H-%M-%S")
    listadoCompras=[]
    listadoVentas=[]
    

    frameBotonesAbajoP = Frame(ventana3)
    frameBotonesAbajoP.place(**ubFrameBotones)
    frameBotonesAbajoP.config(**colorFrameBot)

    frameBotonesAbajoCl = Frame(ventana3)
    frameBotonesAbajoCl.place(**ubFrameBotones)
    frameBotonesAbajoCl.config(**colorFrameBot)

    frameBotonesAbajoA = Frame(ventana3)
    frameBotonesAbajoA.place(**ubFrameBotones)
    frameBotonesAbajoA.config(**colorFrameBot)

    frameBotonesAbajoCo = Frame(ventana3)
    frameBotonesAbajoCo.place(**ubFrameBotones)
    frameBotonesAbajoCo.config(**colorFrameBot)

    frameBotonesAbajoVe = Frame(ventana3)
    frameBotonesAbajoVe.place(**ubFrameBotones)
    frameBotonesAbajoVe.config(**colorFrameBot)

    frameModificarInfoPr=Frame(ventana3)
    frameModificarInfoPr.place(**FrameInfoMod)
    frameModificarInfoPr.config(**colorFrameMod)

    frameModificarInfoCl= Frame(ventana3)
    frameModificarInfoCl.place(**FrameInfoMod)
    frameModificarInfoCl.config(**colorFrameMod)

    frameModificarInfoA= Frame(ventana3)
    frameModificarInfoA.place(**FrameInfoMod)
    frameModificarInfoA.config(**colorFrameMod)

    frameModificarInfoCo=Frame(ventana3)
    frameModificarInfoCo.place(**FrameInfoMod)
    frameModificarInfoCo.config(**colorFrameMod)

    frameModificarInfoVe=Frame(ventana3)
    frameModificarInfoVe.place(**FrameInfoMod)
    frameModificarInfoVe.config(**colorFrameMod)

    frameInfo=Frame(ventana3)
    frameInfo.place(**FrameInfoMod)

    frameInfoCl= Frame(ventana3)
    frameInfoCl.place(**FrameInfoMod)

    frameInfoA= Frame(ventana3)
    frameInfoA.place(**FrameInfoMod)

    frameInfoCo= Frame(ventana3)
    frameInfoCo.place(**FrameInfoMod)

    frameInfoVe= Frame(ventana3)
    frameInfoVe.place(**FrameInfoMod)
    
    frameImagenInfo= Frame(ventana3)
    frameImagenInfo.place(**FrameInfoMod)
    fondoPrincipal=PhotoImage(file="imagenes/imagenInfo.png")
    imagenPrincipal= Label(frameImagenInfo,image=fondoPrincipal,bd=0)
    imagenPrincipal.place(x=0,y=0)
    
    frameBotonesDerecha = Frame(ventana3)
    frameBotonesDerecha.place(x=0,y=0,width=170,height=705)
    fondoBotonesDerecha=PhotoImage(file="imagenes/imagenBD.png")
    imagenBotonesDerecha= Label(frameBotonesDerecha,image=fondoBotonesDerecha,bd=0)
    imagenBotonesDerecha.place(x=0,y=0)
    

    # funcion para cerrar frames
    def cerrarFrames():
        frameModificarInfoPr.place_forget()
        frameModificarInfoCl.place_forget()
        frameModificarInfoA.place_forget()
        frameModificarInfoCo.place_forget()
        frameModificarInfoVe.place_forget()
        frameInfo.place_forget()
        frameInfoVe.place_forget()
        frameInfoCo.place_forget()
        frameInfoA.place_forget()
        frameInfoCl.place_forget()
        frameBotonesAbajoP.place_forget()
        frameBotonesAbajoCl.place_forget()
        frameBotonesAbajoCo.place_forget()
        frameBotonesAbajoVe.place_forget()
        frameBotonesAbajoA.place_forget()
        frameImagenInfo.place_forget()



    ###################################################################################
    ########################################################## LABELS & ENTRYS ########
    
    vistaLabel={'width':'16','font':("calibri",18),'bg':'#1e1c1d','fg':'white'}
    vistaEntry={'width':'19','font':("calibri",25)}
    vistaEntryBuscar={'width':'40','font':("calibri",25)}
    vistaEntryCombobox={'width':'19','font':("calibri", 24)}

    labelCodigo=Label(frameModificarInfoPr,text="CÓDIGO",**vistaLabel)

    # COMBOBOX PARA BUSCAR DATOS REPETIDOS #

    labelComboPr=Label(frameModificarInfoPr,text="OPCIONES",**vistaLabel)
    labelComboCl=Label(frameModificarInfoCl,text="OPCIONES",**vistaLabel)

    comboBuscarP=ttk.Combobox(frameModificarInfoPr,**vistaEntryCombobox)
    comboBuscarCl=ttk.Combobox(frameModificarInfoCl,**vistaEntryCombobox)


    # PROVEEDORES

    labelRazonSocialPr=Label(frameModificarInfoPr,text="RAZÓN SOCIAL",**vistaLabel)
    labelRazonSocialPr.place(x=50,y=50)
    
    entryRazonSocialPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryRazonSocialPr.place(x=250,y=50)

    labelCuitPr=Label(frameModificarInfoPr,text="CUIT",**vistaLabel)
    labelCuitPr.place(x=50,y=140)
    
    entryCuitPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryCuitPr.place(x=250,y=140)

    labelDireccionPr=Label(frameModificarInfoPr,text="DIRECCIÓN",**vistaLabel)
    labelDireccionPr.place(x=50,y=230)
    
    entryDireccionPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryDireccionPr.place(x=250,y=230)
                                
    labelTelefonoPr=Label(frameModificarInfoPr,text="TELÉFONO",**vistaLabel)
    labelTelefonoPr.place(x=50,y=320)
    
    entryTelefonoPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryTelefonoPr.place(x=250,y=320)


    labelIvaPr=Label(frameModificarInfoPr,text="IVA",**vistaLabel)
    labelIvaPr.place(x=650,y=50)
    
    comboPr = ttk.Combobox (frameModificarInfoPr,width=19,font=("calibri", 24))
    opcion=[]
    comboPr.place(x=850, y=50)
    opcion.append("Monotributista")
    opcion.append("Responsable Inscripto")
    comboPr["values"]=opcion

    labelLocalidadPr=Label(frameModificarInfoPr,text="LOCALIDAD",**vistaLabel)
    labelLocalidadPr.place(x=650,y=140)
    
    entryLocalidadPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryLocalidadPr.place(x=850,y=140)

    labelProvinciaPr=Label(frameModificarInfoPr,text="PROVINCIA",**vistaLabel)
    labelProvinciaPr.place(x=650,y=230)

    comboPr1 = ttk.Combobox (frameModificarInfoPr,width=19,font=("calibri", 24))
    opcion=[]
    comboPr1.place(x=850, y=230)
    opcion.append("MENDOZA")
    opcion.append("BUENOS AIRES")
    opcion.append("CATAMARCA")
    opcion.append("MISIONES")
    opcion.append("TUCUMAN")
    opcion.append("SALTA")
    opcion.append("FORMOSA")
    opcion.append("CÓRDOBA")
    opcion.append("CHUBUT")
    opcion.append("SANTA CRUZ")
    opcion.append("LA PAMPA")
    opcion.append("CHACO")
    opcion.append("ENTRE RÍOS")
    opcion.append("TIERRA DEL FUEGO")
    opcion.append("SANTA FE")
    opcion.append("JUJUY")
    opcion.append("NEUQUÉN")
    opcion.append("SANTIAGO DEL ESTEREO")
    opcion.append("SAN LUIS")
    opcion.append("SAN JUAN")
    opcion.append("LA RIOJA")
    opcion.append("RÍO NEGRO")
    opcion.append("CORRIENTES")
    comboPr1["values"]=opcion

    labelCpPr=Label(frameModificarInfoPr,text="CP",**vistaLabel)
    labelCpPr.place(x=650,y=320)
    
    entryCpPr=Entry(frameModificarInfoPr,**vistaEntry)
    entryCpPr.place(x=850,y=320)


    #  CLIENTES

    labelRazonSocialCl=Label(frameModificarInfoCl,text="RAZÓN SOCIAL",**vistaLabel)
    labelRazonSocialCl.place(x=50,y=50)
    
    entryRazonSocialCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryRazonSocialCl.place(x=250,y=50)

    labelCuitCl=Label(frameModificarInfoCl,text="CUIT",**vistaLabel)
    labelCuitCl.place(x=50,y=140)
    
    entryCuitCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryCuitCl.place(x=250,y=140)

    labelDireccionCl=Label(frameModificarInfoCl,text="DIRECCIÓN",**vistaLabel)
    labelDireccionCl.place(x=50,y=230)
    
    entryDireccionCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryDireccionCl.place(x=250,y=230)
                                
    labelTelefonoCl=Label(frameModificarInfoCl,text="TELÉFONO",**vistaLabel)
    labelTelefonoCl.place(x=50,y=320)
    
    entryTelefonoCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryTelefonoCl.place(x=250,y=320)

    labelIvaCl=Label(frameModificarInfoCl,text="IVA",**vistaLabel)
    labelIvaCl.place(x=650,y=50)

    comboCl = ttk.Combobox (frameModificarInfoCl,width=19,font=("calibri", 24))
    opcion=[]
    comboCl.place(x=850, y=50)
    opcion.append("Monotributista")
    opcion.append("Responsable Inscripto")
    comboCl["values"]=opcion

    labelLocalidadCl=Label(frameModificarInfoCl,text="LOCALIDAD",**vistaLabel)
    labelLocalidadCl.place(x=650,y=140)
    
    entryLocalidadCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryLocalidadCl.place(x=850,y=140)

    labelProvinciaCl=Label(frameModificarInfoCl,text="PROVINCIA",**vistaLabel)
    labelProvinciaCl.place(x=650,y=230)

    comboCl1 = ttk.Combobox (frameModificarInfoCl,width=19,font=("calibri", 24))
    opcion=[]
    comboCl1.place(x=850, y=230)
    opcion.append("MENDOZA")
    opcion.append("BUENOS AIRES")
    opcion.append("CATAMARCA")
    opcion.append("MISIONES")
    opcion.append("TUCUMAN")
    opcion.append("SALTA")
    opcion.append("FORMOSA")
    opcion.append("CÓRDOBA")
    opcion.append("CHUBUT")
    opcion.append("SANTA CRUZ")
    opcion.append("LA PAMPA")
    opcion.append("CHACO")
    opcion.append("ENTRE RÍOS")
    opcion.append("TIERRA DEL FUEGO")
    opcion.append("SANTA FE")
    opcion.append("JUJUY")
    opcion.append("NEUQUÉN")
    opcion.append("SANTIAGO DEL ESTEREO")
    opcion.append("SAN LUIS")
    opcion.append("SAN JUAN")
    opcion.append("LA RIOJA")
    opcion.append("RÍO NEGRO")
    opcion.append("CORRIENTES")
    comboCl1["values"]=opcion

    labelCpCl=Label(frameModificarInfoCl,text="CP",**vistaLabel)
    labelCpCl.place(x=650,y=320)
    
    entryCpCl=Entry(frameModificarInfoCl,**vistaEntry)
    entryCpCl.place(x=850,y=320)


    #   COMPRA

    labelCodigoCompra=Label(frameModificarInfoCo,text="Código",**vistaLabel)
    labelCodigoCompra.place(x=50,y=50)

    entryCodigoCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryCodigoCompra.place(x=250,y=50)


    labelMarcaCompra=Label(frameModificarInfoCo,text="Marca",**vistaLabel)
    labelMarcaCompra.place(x=50,y=140)

    entryMarcaCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryMarcaCompra.place(x=250,y=140)


    labelModeloCompra=Label(frameModificarInfoCo,text="Modelo",**vistaLabel)
    labelModeloCompra.place(x=50,y=230)

    entryModeloCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryModeloCompra.place(x=250,y=230)


    labelPrecioCompra=Label(frameModificarInfoCo,text="SUBTOTAL",**vistaLabel)
    labelPrecioCompra.place(x=650,y=50)

    entryPrecioCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryPrecioCompra.place(x=850,y=50)

    labelCantidadCompra=Label(frameModificarInfoCo,text="CANTIDAD",**vistaLabel)
    labelCantidadCompra.place(x=650,y=140)

    entryCantidadCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryCantidadCompra.place(x=850,y=140)

    labelIvaCompra=Label(frameModificarInfoCo,text="TOTAL+IVA",**vistaLabel)
    labelIvaCompra.place(x=650,y=230)

    entryIvaCompra=Entry(frameModificarInfoCo,**vistaEntry)
    entryIvaCompra.place(x=850,y=230)


    #  VENTA

    labelCodigoVenta=Label(frameModificarInfoVe,text="Código",**vistaLabel)
    labelCodigoVenta.place(x=50,y=50)

    entryCodigoVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryCodigoVenta.place(x=250,y=50)



    labelMarcaVenta=Label(frameModificarInfoVe,text="Marca",**vistaLabel)
    labelMarcaVenta.place(x=50,y=140)

    entryMarcaVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryMarcaVenta.place(x=250,y=140)



    labelModeloVenta=Label(frameModificarInfoVe,text="Modelo",**vistaLabel)
    labelModeloVenta.place(x=50,y=230)

    entryModeloVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryModeloVenta.place(x=250,y=230)


    labelPrecioVenta=Label(frameModificarInfoVe,text="Subtotal",**vistaLabel)
    labelPrecioVenta.place(x=650,y=50)

    entryPrecioVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryPrecioVenta.place(x=850,y=50)


    labelCantidadVenta=Label(frameModificarInfoVe,text="Cantidad",**vistaLabel)
    labelCantidadVenta.place(x=650,y=140)

    entryCantidadVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryCantidadVenta.place(x=850,y=140)


    labelTotalVenta=Label(frameModificarInfoVe,text="Total",**vistaLabel)
    labelTotalVenta.place(x=650,y=230)

    entryTotalVenta=Entry(frameModificarInfoVe,**vistaEntry)
    entryTotalVenta.place(x=850,y=230)



    #  ARTÍCULOS

    labelMarcaA=Label(frameModificarInfoA,text="MARCA",**vistaLabel)
    labelMarcaA.place(x=400,y=50)

    comboA = ttk.Combobox (frameModificarInfoA,width=19,font=("calibri", 24))
    opcion=[]
    comboA.place(x=600, y=50)
    opcion.append("INTEL")
    opcion.append("AMD")
    opcion.append("NVIDIA")
    opcion.append("WINDOWS")
    opcion.append("SAMSUNG")
    opcion.append("KINGSTON")
    opcion.append("DELL")
    opcion.append("ASUS")
    opcion.append("MSI")
    opcion.append("LG")
    opcion.append("NOGA")
    opcion.append("WESTERN")
    comboA["values"]=opcion

    labelModeloA=Label(frameModificarInfoA,text="MODELO",**vistaLabel)
    labelModeloA.place(x=400,y=140)

    entryModeloA=Entry(frameModificarInfoA,**vistaEntry)
    entryModeloA.place(x=600,y=140)

    labelStockA=Label(frameModificarInfoA,text="STOCK",**vistaLabel)
    labelStockA.place(x=400,y=230)

    entryStockA=Entry(frameModificarInfoA,**vistaEntry)
    entryStockA.place(x=600,y=230)

    labelPrecioCostoA=Label(frameModificarInfoA,text="PRECIO COSTO",**vistaLabel)
    labelPrecioCostoA.place(x=400,y=320)

    entryPrecioCostoA=Entry(frameModificarInfoA,**vistaEntry)
    entryPrecioCostoA.place(x=600,y=320)


    entryBuscar_Ve=Entry(frameBotonesAbajoVe,**vistaEntryBuscar)

    entryBuscar_Co=Entry(frameBotonesAbajoCo,**vistaEntryBuscar)

    entryBuscar_a=Entry(frameBotonesAbajoA,**vistaEntryBuscar)

    entryBuscar_Cl=Entry(frameBotonesAbajoCl,**vistaEntryBuscar)

    entryBuscar_p=Entry(frameBotonesAbajoP,**vistaEntryBuscar)
    
    entryCodigo=Entry(frameModificarInfoPr,**vistaEntryBuscar)
    #entryCodigo.place(x=250,y=25)


    ################################################################### COMANDOS #######


    ## FUNCIONES DE VALIDACIÓN DE DATOS

    def vacios(dato):
        for letra in dato:
            if(letra==""):
                return True
        return False

    def validarSoloLetras(dato):
        for letra in dato:
            if(ord(letra)!=32):
                if(letra.isalpha()==False):
                    return True
        return False

    def validarLetrasyNumeros(dato):
        for letra in dato:
            if(ord(letra)!=32 and ord(letra)!=46):
                if(letra.isalnum()==False):
                    return True
        return False

    def validarSoloNum(dato):
        for letra in dato:
            if(ord(letra)!=46):
                if(letra.isdigit()==False):
                    return True
        return False

    def validarMayusxPalabra(dato):
        for letra in dato:
            if(ord(letra)!=32):
                if(letra.istitle()==True):
                    return False
        return True

    def validarLongCuitPr(num):
        num=len(str(entryCuitPr.get()))
        if num!=11:
            return True
        else:
            return False

    def validarLongCuitCl(num):
        num=len(str(entryCuitCl.get()))
        if num!=11:
            return True
        else:
            return False

    def validarLongTelefonoPr(num):
        for dato in num:
            dato=len(str(entryTelefonoPr.get()))
            if dato>=7 and dato<=10:
                return False
            else:
                return True

    def validarLongTelefonoCl(num):
        for dato in num:
            dato=len(str(entryTelefonoCl.get()))
            if dato>=7 and dato<=10:
                return False
            else:
                return True

    def validarFecha(dato):
        patron='^2[0-9]{3}/(0\d|1[0-2])/(0\d|1[0-9]|2[0-9]|3[0-1])$'
        if (bool(re.search(patron, dato)))==False:
            return True
        else:
            return False

    ### VACÍAR ENTRYS #

    def vaciarEntryP():
        entryCodigo.delete(0,END)
        entryRazonSocialPr.delete(0,END)
        entryCuitPr.delete(0,END)
        entryDireccionPr.delete(0,END)
        comboPr.delete(0,END)
        entryTelefonoPr.delete(0,END)
        entryLocalidadPr.delete(0,END)
        comboPr1.delete(0,END)
        entryCpPr.delete(0,END)
        entryBuscar_p.delete(0,END)
        comboBuscarP.delete(0,END)

    def vaciarEntryCl():
        entryCodigo.delete(0,END)
        entryRazonSocialCl.delete(0,END)
        entryCuitCl.delete(0,END)
        entryDireccionCl.delete(0,END)
        comboCl.delete(0,END)
        entryTelefonoCl.delete(0,END)
        entryLocalidadCl.delete(0,END)
        comboCl1.delete(0,END)
        entryCpCl.delete(0,END)
        entryBuscar_Cl.delete(0,END)
        comboBuscarCl.delete(0,END)

    def vaciarEntryCo():
        entryCodigoCompra.delete(0,END)
        entryMarcaCompra.delete(0,END)
        entryModeloCompra.delete(0,END)
        entryPrecioCompra.delete(0,END)
        entryCantidadCompra.delete(0,END)
        entryIvaCompra.delete(0,END)

    def vaciarEntryVe():
        entryCodigoVenta.delete(0,END)
        entryCodigoVenta.delete(0,END)
        entryMarcaVenta.delete(0,END)
        entryModeloVenta.delete(0,END)
        entryPrecioVenta.delete(0,END)
        entryCantidadVenta.delete(0,END)
        entryTotalVenta.delete(0,END)

    ################################################################# PROVEEDORES ######
    def buscar_p():
        buscar_id_p=[entryBuscar_p.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM proveedores WHERE nombre=?",buscar_id_p)
        connection.conn.commit()
        datos_p=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryP()

        if(len(datos_p)>0):
            if (len(datos_p)>1):
                frameModificarInfoPr.place(**FrameInfoMod)
                frameImagenInfo.place_forget()
                frameInfo.place_forget()
                messagebox.showinfo("Resultado de la busqueda","Se encontraron varios resultados")
                comboBuscarP.place(x=850,y=410)
                labelComboPr.place(x=650,y=410)
                listadoCuit=[]

                for dato in datos_p:
                    listadoCuit.append(dato["cuit"])
                comboBuscarP["values"] = listadoCuit

                def mostrarEnEntry(evento):
                    cuit=comboBuscarP.get()
                    for dato in datos_p:
                        if (dato["cuit"] == int(cuit)):
                            vaciarEntryP()
                            entryCodigo.insert(END,dato["id"])
                            entryRazonSocialPr.insert(END,dato["nombre"])
                            entryCuitPr.insert(END,dato["cuit"])
                            entryDireccionPr.insert(END,dato["direccion"])
                            entryTelefonoPr.insert(END,dato["telefono"])
                            comboPr.insert(END,dato["iva"])
                            entryLocalidadPr.insert(END,dato["localidad"])
                            comboPr1.insert(END,dato["provincia"])
                            entryCpPr.insert(END,dato["cp"])
                comboBuscarP.bind("<<ComboboxSelected>>",mostrarEnEntry)
            else:
                vaciarEntryP()
                for dato in datos_p:
                    entryCodigo.delete(0,END)
                    entryCodigo.insert(END,dato["id"])
                    entryRazonSocialPr.delete(0,END)
                    entryRazonSocialPr.insert(END,dato["nombre"])
                    entryCuitPr.delete(0,END)
                    entryCuitPr.insert(END,dato["cuit"])
                    entryDireccionPr.delete(0,END)
                    entryDireccionPr.insert(END,dato["direccion"])
                    entryTelefonoPr.delete(0,END)
                    entryTelefonoPr.insert(END,dato["telefono"])
                    comboPr.delete(0,END)
                    comboPr.insert(END,dato["iva"])
                    entryLocalidadPr.delete(0,END)
                    entryLocalidadPr.insert(END,dato["localidad"])
                    comboPr1.delete(0,END)
                    comboPr1.insert(END,dato["provincia"])
                    entryCpPr.delete(0,END)
                    entryCpPr.insert(END,dato["cp"])
                    frameModificarInfoPr.place(**FrameInfoMod)
                    messagebox.showinfo("Resultado de la busqueda","Encontrado")
                    frameImagenInfo.place_forget()
                    frameInfo.place_forget()
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado ")

    def guardarP():
        dato=(entryRazonSocialPr.get(),entryCuitPr.get(),entryDireccionPr.get(),entryTelefonoPr.get(),comboPr.get(),entryLocalidadPr.get(),comboPr1.get(),entryCpPr.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarMayusxPalabra(dato[0]) or validarMayusxPalabra(dato[5]) or validarMayusxPalabra(dato[6]):
            messagebox.showwarning("Guardar datos","Deben tener mayúsculas ciertos datos")
        elif validarLongTelefonoPr(dato[3]):
            messagebox.showwarning("Guardar datos","Teléfono incorrecto")
        elif validarLongCuitPr(dato[1]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL incorrecto")
        elif validarSoloNum(dato[1]) or validarSoloNum(dato[3]) or validarSoloNum(dato[7]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL, teléfono o CP sólo números")
        elif validarSoloLetras(dato[0]) or validarSoloLetras(dato[5]) or validarSoloLetras(dato[6]):
            messagebox.showwarning("Guardar datos","Razon Social, localidad o provincia sólo letras")
        
        else:
            try:
                connection.Database()
                sql="INSERT INTO proveedores(nombre,cuit,direccion,telefono,iva,localidad,provincia,cp)VALUES(?,?,?,?,?,?,?,?)"
                connection.cursor.execute(sql,dato)
                connection.conn.commit()
                connection.cursor.close()
                connection.conn.close()
                messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
                vaciarEntryP()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Error en BD","Ya existe un cliente con ese CUIT")
            

    def modificarP():
        dato=(entryRazonSocialPr.get(),entryCuitPr.get(),entryDireccionPr.get(),entryTelefonoPr.get(),comboPr.get(),entryLocalidadPr.get(),comboPr1.get(),entryCpPr.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarMayusxPalabra(dato[0]) or validarMayusxPalabra(dato[5]) or validarMayusxPalabra(dato[6]):
            messagebox.showwarning("Guardar datos","Deben tener mayúsculas ciertos datos")
        elif validarLongTelefonoPr(dato[3]):
            messagebox.showwarning("Guardar datos","Teléfono incorrecto")
        elif validarLongCuitPr(dato[1]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL incorrecto")
        elif validarSoloNum(dato[1]) or validarSoloNum(dato[3]) or validarSoloNum(dato[7]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL, teléfono o CP sólo números")
        elif validarSoloLetras(dato[0]) or validarSoloLetras(dato[5]) or validarSoloLetras(dato[6]):
            messagebox.showwarning("Guardar datos","Razon Social, localidad o provincia sólo letras")
        else:
            datosPr=[entryRazonSocialPr.get(),entryCuitPr.get(),entryDireccionPr.get(),entryTelefonoPr.get(),comboPr.get(),entryLocalidadPr.get(),comboPr1.get(),entryCpPr.get(),entryCodigo.get()]
            connection.Database()
            connection.cursor.execute("UPDATE proveedores SET nombre=?,cuit=?,direccion=?,telefono=?,iva=?,localidad=?,provincia=?,cp=? WHERE id=?",datosPr)
            connection.conn.commit()
            datosPr=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryP()
            if(len(datosPr)>0):
                for dato in datosPr:
                    id.delete(0,END)
                    id.insert(END,dato[1])
                    nombre.delete(0,END)
                    nombre.insert(END,dato[1])
                    cuit.delete(0,END)
                    cuit.insert(END,dato[2])
                    direccion.delete(0,END)
                    direccion.insert(END,dato[3])
                    telefono.delete(0,END)
                    telefono.insert(END,dato[4])
                    iva.delete(0,END)
                    iva.insert(END,dato[5])
                    localidad.delete(0,END)
                    localidad.insert(END,dato[6])
                    provincia.delete(0,END)
                    provincia.insert(END,dato[7])
                    cp.delete(0,END)
                    cp.insert(END,dato[8])
                    messagebox.showerror("Error al modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")

    def eliminarP():
        if (entryBuscar_p.get()==""):
            messagebox.showerror("Error al Eliminar","Debes colocar un número de ID")
        elif (entryBuscar_p.get()=="000"):
            messagebox.showerror("Error al Eliminar","Debes colocar un número diferente a cero")
        else:
            eliminaridP=[entryBuscar_p.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM proveedores WHERE id=?",eliminaridP)
            connection.conn.commit()
            datosPre = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryP
            if(len(datosPre)>0):
                for dato in datosPre:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    nombre.delete(0,END)
                    nombre.insert(END,dato[1])
                    cuit.delete(0,END)
                    cuit.insert(END,dato[2])
                    direccion.delete(0,END)
                    direccion.insert(END,dato[3])
                    telefono.delete(0,END)
                    telefono.insert(END,dato[4])
                    iva.delete(0,END)
                    iva.insert(END,dato[5])
                    localidad.delete(0,END)
                    localidad.insert(END,dato[6])
                    provincia.delete(0,END)
                    provincia.insert(END,dato[7])
                    cp.delete(0,END)
                    cp.insert(END,dato[8])
                    messagebox.showerror("Error al eliminar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")






    ####################################################################################            
    ################################################################### CLIENTES ##########

    def buscar_Cl():
        buscar_id_Cl=[entryBuscar_Cl.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM clientes WHERE nombre=?",buscar_id_Cl)
        connection.conn.commit()
        datos_Cl=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryCl()
        if(len(datos_Cl)>0):
            if (len(datos_Cl)>1):
                frameModificarInfoCl.place(**FrameInfoMod)
                frameImagenInfo.place_forget()
                frameInfoCl.place_forget()
                messagebox.showinfo("Resultado de la busqueda","Se encontraron varios resultados")
                comboBuscarCl.place(x=850,y=410)
                labelComboCl.place(x=650,y=410)
                listadoCuit=[]

                for dato in datos_Cl:
                    listadoCuit.append(dato["cuit"])
                comboBuscarCl["values"] = listadoCuit

                def mostrarEnEntry(evento):
                    cuit=comboBuscarCl.get()
                    for dato in datos_Cl:
                        if (dato["cuit"] == int(cuit)):
                            vaciarEntryCl()
                            entryCodigo.insert(END,dato["id"])
                            entryRazonSocialCl.insert(END,dato["nombre"])
                            entryCuitCl.insert(END,dato["cuit"])
                            entryDireccionCl.insert(END,dato["direccion"])
                            entryTelefonoCl.insert(END,dato["telefono"])
                            comboCl.insert(END,dato["iva"])
                            entryLocalidadCl.insert(END,dato["localidad"])
                            comboCl1.insert(END,dato["provincia"])
                            entryCpCl.insert(END,dato["cp"])
                comboBuscarCl.bind("<<ComboboxSelected>>",mostrarEnEntry)
            else:
                vaciarEntryCl()
                for dato in datos_Cl:
                    entryCodigo.delete(0,END)
                    entryCodigo.insert(END,dato[0])
                    entryRazonSocialCl.delete(0,END)
                    entryRazonSocialCl.insert(END,dato[1])
                    entryCuitCl.delete(0,END)
                    entryCuitCl.insert(END,dato[2])
                    entryDireccionCl.delete(0,END)
                    entryDireccionCl.insert(END,dato[3])
                    entryTelefonoCl.delete(0,END)
                    entryTelefonoCl.insert(END,dato[4])
                    comboCl.delete(0,END)
                    comboCl.insert(END,dato[5])
                    entryLocalidadCl.delete(0,END)
                    entryLocalidadCl.insert(END,dato[6])
                    comboCl1.delete(0,END)
                    comboCl1.insert(END,dato[7])
                    entryCpCl.delete(0,END)
                    entryCpCl.insert(END,dato[8])
                    frameModificarInfoCl.place(**FrameInfoMod)
                    messagebox.showinfo("Resultado de la busqueda","Encontrado")
                    frameImagenInfo.place_forget()
                    frameInfoCl.place_forget()
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado ")

    def guardarCl():
        dato=(entryRazonSocialCl.get(),entryCuitCl.get(),entryDireccionCl.get(),entryTelefonoCl.get(),comboCl.get(),entryLocalidadCl.get(),comboCl1.get(),entryCpCl.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarMayusxPalabra(dato[0]) or validarMayusxPalabra(dato[5]) or validarMayusxPalabra(dato[6]):
            messagebox.showwarning("Guardar datos","Deben tener mayúsculas ciertos datos")
        elif validarLongTelefonoCl(dato[3]):
            messagebox.showwarning("Guardar datos","Teléfono incorrecto")
        elif validarLongCuitCl(dato[1]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL incorrecto")
        elif validarSoloNum(dato[1]) or validarSoloNum(dato[3]) or validarSoloNum(dato[7]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL, teléfono o CP sólo números")
        elif validarSoloLetras(dato[0]) or validarSoloLetras(dato[5]) or validarSoloLetras(dato[6]):
            messagebox.showwarning("Guardar datos","Razon Social, localidad o provincia sólo letras")
        else:
            try:
                connection.Database()
                sql="INSERT INTO clientes(nombre,cuit,direccion,telefono,iva,localidad,provincia,cp)VALUES(?,?,?,?,?,?,?,?)"
                connection.cursor.execute(sql,dato)
                connection.conn.commit()
                connection.cursor.close()
                connection.conn.close()
                messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
                vaciarEntryCl()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Error en BD","Ya existe un cliente con ese CUIT")

    def modificarCl():
        dato=(entryRazonSocialCl.get(),entryCuitCl.get(),entryDireccionCl.get(),entryTelefonoCl.get(),comboCl.get(),entryLocalidadCl.get(),comboCl1.get(),entryCpCl.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarMayusxPalabra(dato[0]) or validarMayusxPalabra(dato[5]) or validarMayusxPalabra(dato[6]):
            messagebox.showwarning("Guardar datos","Deben tener mayúsculas ciertos datos")
        elif validarLongTelefonoCl(dato[3]):
            messagebox.showwarning("Guardar datos","Teléfono incorrecto")
        elif validarLongCuitCl(dato[1]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL incorrecto")
        elif validarSoloNum(dato[1]) or validarSoloNum(dato[3]) or validarSoloNum(dato[7]):
            messagebox.showwarning("Guardar datos","CUIT/CUIL, teléfono o CP sólo números")
        elif validarSoloLetras(dato[0]) or validarSoloLetras(dato[5]) or validarSoloLetras(dato[6]):
            messagebox.showwarning("Guardar datos","Razon Social, localidad o provincia sólo letras")
        else:
            datosCl=[entryRazonSocialCl.get(),entryCuitCl.get(),entryDireccionCl.get(),entryTelefonoCl.get(),comboCl.get(),entryLocalidadCl.get(),comboCl1.get(),entryCpCl.get(),entryCodigo.get()]
            connection.Database()
            connection.cursor.execute("UPDATE clientes SET nombre=?,cuit=?,direccion=?,telefono=?,iva=?,localidad=?,provincia=?,cp=? WHERE id=?",datosCl)
            connection.conn.commit()
            datosCl=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryCl()
            if(len(datosCl)>0):
                for dato in datosCl:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    nombre.delete(0,END)
                    nombre.insert(END,dato[1])
                    cuit.delete(0,END)
                    cuit.insert(END,dato[2])
                    direccion.delete(0,END)
                    direccion.insert(END,dato[3])
                    telefono.delete(0,END)
                    telefono.insert(END,dato[4])
                    iva.delete(0,END)
                    iva.insert(END,dato[5])
                    localidad.delete(0,END)
                    localidad.insert(END,dato[6])
                    provincia.delete(0,END)
                    provincia.insert(END,dato[7])
                    cp.delete(0,END)
                    cp.insert(END,dato[8])
                    messagebox.showinfo("Error al Modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")

    def eliminarCl():
        if (entryCodigo.get()==""):
            messagebox.showerror("Error al Eliminar","Debes colocar un número de ID")
        elif (entryCodigo.get()=="0"):
            messagebox.showerror("Error al Eliminar","Debes colocar un número diferente a cero")
        else:
            eliminaridCl=[entryBuscar_Cl.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM clientes WHERE id=?",eliminaridCl)
            connection.conn.commit()
            datosCl = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryCl()
            if(len(datosCl)>0):
                for dato in datosCl:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    nombre.delete(0,END)
                    nombre.insert(END,dato[1])
                    cuit.delete(0,END)
                    cuit.insert(END,dato[2])
                    direccion.delete(0,END)
                    direccion.insert(END,dato[3])
                    telefono.delete(0,END)
                    telefono.insert(END,dato[4])
                    iva.delete(0,END)
                    iva.insert(END,dato[5])
                    localidad.delete(0,END)
                    localidad.insert(END,dato[6])
                    provincia.delete(0,END)
                    provincia.insert(END,dato[7])
                    cp.delete(0,END)
                    cp.insert(END,dato[8])
                    messagebox.showinfo("Error al eliminar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")






    ####################################################################################
    ################################################################## ARTÍCULOS #######

    def vaciarEntryA():
        comboA.delete(0,END)
        entryModeloA.delete(0,END)
        entryStockA.delete(0,END)
        entryPrecioCostoA.delete(0,END)
        entryBuscar_a.delete(0,END)

    def buscar_a():
        buscar_id_a=[entryBuscar_a.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM articulos WHERE id=?",buscar_id_a)
        connection.conn.commit()
        datos_a=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryA()
        if(len(datos_a)>0):
            for dato in datos_a:
                entryCodigo.delete(0,END)
                entryCodigo.insert(END,dato[0])
                comboA.delete(0,END)
                comboA.insert(END,dato[1])
                entryModeloA.delete(0,END)
                entryModeloA.insert(END,dato[2])
                entryStockA.delete(0,END)
                entryStockA.insert(END,dato[3])
                entryPrecioCostoA.delete(0,END)
                entryPrecioCostoA.insert(END,dato[4])
                frameModificarInfoA.place(**FrameInfoMod)
                messagebox.showinfo("Resultado de la busqueda","Encontrado")
                frameImagenInfo.place_forget()
                frameInfoA.place_forget()
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado ")

    def guardar_a():
        dato=(comboA.get(),entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloNum(dato[2]) or validarSoloNum(dato[3]):
            messagebox.showwarning("Guardar datos","Stock precio costo/venta sólo números")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","Marca sólo letras")
        else:
            connection.Database()
            sql="INSERT INTO articulos(marca,modelo,stock,precio_costo)VALUES(?,?,?,?)"
            connection.cursor.execute(sql,dato)
            connection.conn.commit()
            connection.cursor.close()
            connection.conn.close()
            messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
            vaciarEntryA()

    def modificar_a():
        #datos=(comboA.get(),entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get())
        dato=(comboA.get(),entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloNum(dato[2]) or validarSoloNum(dato[3]):
            messagebox.showwarning("Guardar datos","Stock precio costo sólo números")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","Marca sólo letras")
        else:
            datos_a=[comboA.get(),entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get(),entryCodigo.get(),]
            connection.Database()
            connection.cursor.execute("UPDATE articulos SET marca=?,modelo=?,stock=?,precio_costo=? WHERE id=?",datos_a)
            connection.conn.commit()
            datos_a=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryA()
            if(len(datos_a)>0):
                for dato in datos_a:
                    entryCodigo.delete(0,END)
                    entryCodigo.insert(END,dato["id"])
                    comboA.delete(0,END)
                    comboA.insert(END,dato["marca"])
                    entryModeloA.delete(0,END)
                    entryModeloA.insert(END,dato["modelo"])
                    entryStockA.delete(0,END)
                    entryStockA.insert(END,dato["stock"])
                    entryPrecioCostoA.delete(0,END)
                    entryPrecioCostoA.insert(END,dato["precio_costo"])
                    messagebox.showinfo("Error al modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")

    def eliminar_a():
        if (entryBuscar_a.get()==""):
            messagebox.showerror("Error al Eliminar","Debes colocar un número de ID")
        elif (entryBuscar_a.get()=="0"):
            messagebox.showerror("Error al Eliminar","Debes colocar un número diferente a cero")
        else:
            eliminarid_a=[entryBuscar_a.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM articulos WHERE id=?",eliminarid_a)
            connection.conn.commit()
            datos_a = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryA()
            if(len(datos_a)>0):
                for dato in datos_a:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    nombre.delete(0,END)
                    nombre.insert(END,dato[1])
                    modelo.delete(0,END)
                    modelo.insert(END,dato[2])
                    stock.delete(0,END)
                    stock.insert(END,dato[3])
                    precio_costo.delete(0,END)
                    precio_costo.insert(END,dato[4])
                    messagebox.showerror("Error al eliminar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")



    ###################################################################################
    ################################################################## COMPRA #########

    # AL GUARDAR CADA COMPRA

    def compraArticulo():

        # Calcular total
        total=0
        for articulo in listadoCompras:
            total = total + float(articulo[5])

        # Guardar la compra
        datosCompra=(fechaActual,total)
        connection.Database()
        tabla = connection.cursor.fetchall()
        sqlGuardar = "INSERT INTO compra(fecha,total) VALUES (?,?)"
        connection.cursor.execute(sqlGuardar,datosCompra)
        connection.conn.commit()

        # Para buscar la última compra, esto lo hacemos para guardarla en articuloCompras
        sqlMax= 'SELECT MAX(id) FROM compra'
        connection.cursor.execute(sqlMax)
        datosBuscados = connection.cursor.fetchall()
        ultimaCompra = datosBuscados[0][0]

        for articulo in listadoCompras:
            # Se ubica la cantidad y el id de c/articulo y se suma el stock.
            cantidadNueva = int(articulo[4])
            idArt = []
            idArt=articulo[0]
            connection.cursor.execute("SELECT stock FROM articulos WHERE id=?",idArt)
            stockArticulo=connection.cursor.fetchall()
            nuevoStock = stockArticulo[0][0] + cantidadNueva

            # Se actualiza en la BD la cantidad del stock de c/articulo
            actualizarStock=(nuevoStock,idArt)
            sql="UPDATE articulos SET stock=? WHERE id=?"
            connection.cursor.execute(sql,actualizarStock)
            connection.conn.commit()

            # Guardar cada articulo en articuloCompras
            datosArticulos=(ultimaCompra,articulo[0],articulo[5])
            connection.cursor.execute("INSERT INTO articuloCompras(numeroCompra,idArticulo,total) VALUES (?,?,?)",datosArticulos)
            connection.conn.commit()

        # Por ultimo se cierra la conexión y se muestra el cartel
        connection.cursor.close()
        connection.conn.close()
        messagebox.showinfo("Compra","Compra realizada")

        # Hacer el ticket
        nombreArchivo = f"ticketsCompras//Ticket {fechaActual} {horaActual}.txt"
        escribir = open(nombreArchivo,"w")
        escribir.write("                                                   Compra\n")
        escribir.write("Fecha: "+fechaActual)
        escribir.write("\n")
        escribir.write("Hora: "+horaActual)
        escribir.write("\n")
        escribir.write("\n\n")
        escribir.write("-----------------------------------------------------------------------------------\n")
        for articulo in listadoCompras:
            escribir.write(f"{articulo[0]} - {articulo[1]} - {articulo[2]} - {articulo[4]} - {articulo[5]} \n")
        escribir.write("\n\n")
        escribir.write("Total: $"+str(total))
        escribir.close()
        # Se realiza lo siguiente para poder darle una ruta a los tickes, y para ello se utiliza la barra \. NO LA  /.
        archivoImprimir = nombreArchivo.replace("/","\\")
        # Esto lo manda a imprimir a la impresora PREDETERMINADA
        os.startfile(archivoImprimir,"print")



        """
        connection.Database()
        datos=(comboA.get(),entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get(),)
        elif validarSoloNum(datos[2])==False or validarSoloNum(datos[3])==False:
            messagebox.showwarning("Guardar datos","Stock precio costo sólo números")
        elif validarSoloLetras(datos[0])==False:
            messagebox.showwarning("Guardar datos","Marca sólo letras")"""
        #else:
        # guardar articulos
        #sql="INSERT INTO articulos(marca,modelo,stock,precio_costo)VALUES(?,?,?,?)"
        #connection.cursor.execute(sql,datos)
        #connection.conn.commit()
        #messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
        # guardar compra
        """datosCompra=(fechaActual,entryIvaCompra.get(),)
        sql2="INSERT INTO compra(fecha,total)VALUES(?,?)"
        connection.cursor.execute(sql2,datosCompra)
        connection.conn.commit()
        # guardar articulos comprados
        buscarNCompra='SELECT MAX(id) FROM compra'
        connection.cursor.execute(buscarNCompra)
        maxNCompra=connection.cursor.fetchall()
        buscarIdArticulo='SELECT MAX (id) FROM articulos'
        connection.cursor.execute(buscarIdArticulo)
        maxIdArticulo=connection.cursor.fetchall()
        #se le coloca [0][0] por que se forma una lista dentro de otra lista
        datosArticulos=(maxNCompra[0][0],maxIdArticulo[0][0],entryIvaCompra.get())
        sql3='INSERT INTO articuloCompras(numeroCompra,idArticulo,total) VALUES(?,?,?)'
        connection.cursor.execute(sql3,datosArticulos)
        connection.conn.commit()
        connection.cursor.close()
        connection.conn.close()
        
        """

    def buscar_Co():
        buscar_id_Co=[entryBuscar_Co.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM compra WHERE id=?",buscar_id_Co)
        connection.conn.commit()
        datos_Co=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryCo()

        if(len(datos_Co)>0):
            for dato in datos_Co:
                entryCodigoCompra.delete(0,END)
                entryCodigoCompra.insert(END,dato[0])
                entryIvaCompra.delete(0,END)
                entryIvaCompra.insert(END,dato[1])
                fechaActual.insert(END,dato[2])
                frameModificarInfoCo.place(**FrameInfoMod)
                messagebox.showinfo("Resultado de la busqueda","Encontrado")
                frameImagenInfo.place_forget()
                frameInfoCo.place_forget()
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado")

    def guardar_Co():
        dato=(entryMarcaCompra.get(),
                entryModeloCompra.get(),
                entryPrecioCompra.get(),
                entryCantidadCompra.get(),
                entryIvaCompra.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloNum(dato[2]) or validarSoloNum(dato[3]) or validarSoloNum(dato[4]):
            messagebox.showwarning("Guardar datos","Precio,Cantidad o Total solo números deben ser.")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","La marca debe ser solo letras")
        else:
            connection.Database()
            sql="INSERT INTO compra(fecha,total)VALUES(?,?)"
            connection.cursor.execute(sql,dato)
            connection.conn.commit()
            connection.cursor.close()
            connection.conn.close()
            messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
            vaciarEntryCo()


    # Treeview donde se muestra los articulos que se van a COMPRAR #

    scrollbaryArt = Scrollbar(frameModificarInfoCo, orient=VERTICAL)

    treeArt = ttk.Treeview(frameModificarInfoCo, columns=("ID","Marca","Modelo","Subtotal","Cantidad","Total mas IVA"), selectmode="extended", height=300, yscrollcommand=scrollbaryArt.set)
    scrollbaryArt.config(command=treeArt.yview)
    scrollbaryArt.pack(side=RIGHT, fill=Y)

    treeArt.column('ID', stretch=NO, minwidth=0, width=54)
    treeArt.column('Marca', stretch=NO, minwidth=0, width=222)
    treeArt.column('Modelo', stretch=NO, minwidth=0, width=222)
    treeArt.column('Subtotal', stretch=NO, minwidth=0, width=222)
    treeArt.column('Cantidad', stretch=NO, minwidth=0, width=222)
    treeArt.column('Total mas IVA', stretch=NO, minwidth=0, width=222)

    treeArt['show'] = 'headings'
    treeArt.heading('ID', text="ID", anchor=CENTER)
    treeArt.heading('Marca', text="Marca", anchor=CENTER)
    treeArt.heading('Modelo', text="Modelo", anchor=CENTER)
    treeArt.heading('Subtotal', text="Subtotal", anchor=CENTER)
    treeArt.heading('Cantidad', text="Cantidad", anchor=CENTER)
    treeArt.heading('Total mas IVA', text="Total mas IVA", anchor=CENTER)
    
    treeArt.place(x=0,y=290,width=1200,height=300)
    treeArt.delete(*treeArt.get_children())
    
    def agregarArticuloCompra():
        datos=[entryCodigoCompra.get(),entryMarcaCompra.get(),entryModeloCompra.get(),entryPrecioCompra.get(),
        entryCantidadCompra.get(),entryIvaCompra.get()]
        if vacios(datos)==True:
            evento_Ac()
        else:
            for data in datos:
                treeArt.insert('', END,values=(entryCodigoCompra.get(),entryMarcaCompra.get(),
                    entryModeloCompra.get(),entryPrecioCompra.get(),entryCantidadCompra.get(),
                    entryIvaCompra.get()))
                #se le agrega los diversos articulos y cantidades a la lista listadoCompras
                listadoCompras.append(datos,)
                entryCodigoCompra.delete(0,END)
                entryMarcaCompra.delete(0,END)
                entryModeloCompra.delete(0,END)
                entryPrecioCompra.delete(0,END)
                entryIvaCompra.delete(0,END)
                entryCantidadCompra.delete(0,END)
                break

    def modificar_Co():
        dato=(entryMarcaCompra.get(),
                entryModeloCompra.get(),
                entryPrecioCompra.get(),
                entryCantidadCompra.get(),
                entryIvaCompra.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloNum(dato[2]) or validarSoloNum(dato[3]) or validarSoloNum(dato[4]):
            messagebox.showwarning("Guardar datos","Subtotal, cantidad o Total deben ser números")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","Verificar que sean solo letra la marca, forma pago y tipo factura.")

        else:
            datos_Co=(fechaActual,entryIvaCompra.get(),)
            connection.Database()
            sql="UPDATE compra SET fecha=?,total=? WHERE id=?"
            connection.cursor.execute(sql,datos_Co)
            connection.conn.commit()
            datosCo=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryCo()
            if(len(datos_Co)>0):
                for dato in datos_Co:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    fecha.delete(0,END)
                    fecha.insert(END,dato[1])
                    total.delete(0,END)
                    total.insert(END,dato[2])
                    messagebox.showinfo("Error al modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")



    def eliminar_Co():
        if (entryBuscar_Co.get()==""):
            messagebox.showerror("Error al Eliminar","Debes colocar un número de ID")
        elif (entryBuscar_Co.get()=="0"):
            messagebox.showerror("Error al Eliminar","Debes colocar un número diferente a cero")
        else:
            eliminarid_Co=[entryBuscar_Co.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM compra WHERE id=?",eliminarid_Co)
            connection.conn.commit()
            datos_Co = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryCo()
            if(len(datos_Co)>0):
                for dato in datos_Co:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    fecha.insert(END,dato[1])
                    total.delete(0,END)
                    total.insert(END,dato[2])
                    messagebox.showerror("Error al eliminar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")




    
    ######################################################################################
    ################################################################## VENTA #############


    # AL VENDER CADA COMPRA

    def ventaArticulo():

        # Calcular total
        total=0
        for articulo in listadoVentas:
            total = total + float(articulo[5])

        # Guardar la venta
        datosVenta=(fechaActual,total)
        connection.Database()
        tabla = connection.cursor.fetchall()
        sqlGuardar = "INSERT INTO venta(fecha,total) VALUES (?,?)"
        connection.cursor.execute(sqlGuardar,datosVenta)
        connection.conn.commit()

        # Para buscar la última venta, esto lo hacemos para guardarla en articuloVentas
        sqlMax= 'SELECT MAX(id) FROM venta'
        connection.cursor.execute(sqlMax)
        datosBuscados = connection.cursor.fetchall()
        ultimaVenta = datosBuscados[0][0]

        for articulo in listadoVentas:
            # Se ubica la cantidad y el id de c/articulo y se resta el stock.
            cantidadNueva = int(articulo[4])
            idArt = []
            idArt=articulo[0]
            connection.cursor.execute("SELECT stock FROM articulos WHERE id=?",idArt)
            stockArticulo=connection.cursor.fetchall()
            nuevoStock = stockArticulo[0][0] - cantidadNueva

            # Se actualiza en la BD la cantidad del stock de c/articulo
            actualizarStock=(nuevoStock,idArt)
            sql="UPDATE articulos SET stock=? WHERE id=?"
            connection.cursor.execute(sql,actualizarStock)
            connection.conn.commit()

            # Guardar cada articulo en articuloVentas
            datosArticulos=(ultimaVenta,articulo[0],articulo[5])
            connection.cursor.execute("INSERT INTO articuloVentas(numeroVenta,idArticulo,total) VALUES (?,?,?)",datosArticulos)
            connection.conn.commit()

        # Por ultimo se cierra la conexión y se muestra el cartel
        connection.cursor.close()
        connection.conn.close()
        messagebox.showinfo("Venta","Venta realizada")

        # Hacer el ticket
        nombreArchivo = f"ticketsVentas//Ticket {fechaActual} {horaActual}.txt"
        escribir = open(nombreArchivo,"w")
        escribir.write("                                                   Venta\n")
        escribir.write("Fecha: "+fechaActual)
        escribir.write("\n")
        escribir.write("Hora: "+horaActual)
        escribir.write("\n")
        escribir.write("\n\n")
        escribir.write("-----------------------------------------------------------------------------------\n")
        for articulo in listadoVentas:
            escribir.write(f"{articulo[0]} - {articulo[1]} - {articulo[2]} - {articulo[4]} - {articulo[5]} \n")
        escribir.write("\n\n")
        escribir.write("Total: $"+str(total))
        escribir.close()
        # Se realiza lo siguiente para poder darle una ruta a los tickes, y para ello se utiliza la barra \. NO LA  /.
        archivoImprimir = nombreArchivo.replace("/","\\")
        # Esto lo manda a imprimir a la impresora PREDETERMINADA
        os.startfile(archivoImprimir,"print")
    
    def buscar_Ve():
        buscar_id_Ve=[entryBuscar_Ve.get()]
        connection.Database()
        connection.cursor.execute("SELECT * FROM venta WHERE id=?",buscar_id_Ve)
        connection.conn.commit()
        datos_Ve=connection.cursor.fetchall()
        connection.cursor.close()
        connection.conn.close()
        vaciarEntryVe()
        if(len(datos_Ve)>0):
            for dato in datos_Ve:
                entryCodigoVenta.delete(0,END)
                entryCodigoVenta.insert(END,dato[0])
                entryMarcaVenta.delete(0,END)
                entryMarcaVenta.insert(END,dato[1])
                entryModeloVenta.delete(0,END)
                entryModeloVenta.insert(END,dato[2])
                entryPrecioVenta.delete(0,END)
                entryPrecioVenta.insert(END,dato[3])
                entryCantidadVenta.delete(0,END)
                entryCantidadVenta.insert(END,dato[4])
                entryTotalVenta.delete(0,END)
                entryTotalVenta.insert(END,dato[5])
                frameModificarInfoVe.place(**FrameInfoMod)
                messagebox.showinfo("Resultado de la busqueda","Encontrado")
                frameImagenInfo.place_forget()
                frameInfoVe.place_forget()
        else:
            messagebox.showerror("Resultado de busqueda", "No localizado")

    def guardar_Ve():
        dato=(entryMarcaVenta.get(),
            entryModeloVenta.get(),
            entryPrecioVenta.get(),
            entryCantidadVenta.get(),
            entryTotalVenta.get(),)
        if validarSoloNum(dato[2]) or validarSoloNum(dato[3]) or validarSoloNum(dato[4]):
            messagebox.showwarning("Guardar datos","Subtotal, cantidad y/o total deben ser sólo números")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","Verificar que sean solo letra la marca.")
        else:
            connection.Database()
            sql="INSERT INTO venta(marca,modelo,subtotal,cantidad,total)VALUES(?,?,?,?,?)"
            connection.cursor.execute(sql,dato)
            connection.conn.commit()
            connection.cursor.close()
            connection.conn.close()
            messagebox.showinfo("Guardar datos","Datos guardados exitosamente")
            vaciarEntryVe()



    # Treeview donde se muestra los articulos que se van a VENDER #

    scrollbaryVen = Scrollbar(frameModificarInfoVe, orient=VERTICAL)

    treeVen = ttk.Treeview(frameModificarInfoVe, columns=("ID","Marca","Modelo","Subtotal","Cantidad","Total"), selectmode="extended", height=300, yscrollcommand=scrollbaryVen.set)
    scrollbaryVen.config(command=treeVen.yview)
    scrollbaryVen.pack(side=RIGHT, fill=Y)

    treeVen.column('ID', stretch=NO, minwidth=0, width=54)
    treeVen.column('Marca', stretch=NO, minwidth=0, width=222)
    treeVen.column('Modelo', stretch=NO, minwidth=0, width=222)
    treeVen.column('Subtotal', stretch=NO, minwidth=0, width=222)
    treeVen.column('Cantidad', stretch=NO, minwidth=0, width=222)
    treeVen.column('Total', stretch=NO, minwidth=0, width=222)

    treeVen['show'] = 'headings'
    treeVen.heading('ID', text="ID", anchor=CENTER)
    treeVen.heading('Marca', text="Marca", anchor=CENTER)
    treeVen.heading('Modelo', text="Modelo", anchor=CENTER)
    treeVen.heading('Subtotal', text="Subtotal", anchor=CENTER)
    treeVen.heading('Cantidad', text="Cantidad", anchor=CENTER)
    treeVen.heading('Total', text="Total", anchor=CENTER)
    
    treeVen.place(x=0,y=290,width=1200,height=300)
    treeVen.delete(*treeVen.get_children())
    
    def agregarArticuloVenta():
        datos=[entryCodigoVenta.get(),
        entryMarcaVenta.get(),
        entryModeloVenta.get(),
        entryPrecioVenta.get(),
        entryCantidadVenta.get(),
        entryTotalVenta.get(),]
        if vacios(datos)==True:
            evento_Av()
        else:
            for data in datos:
                treeVen.insert('', END,values=(entryCodigoVenta.get(),entryMarcaVenta.get(),entryModeloVenta.get(),
                    entryPrecioVenta.get(),entryCantidadVenta.get(),entryTotalVenta.get()))
                #se le agrega los diversos articulos y cantidades a la lista listadoVentas
                listadoVentas.append(datos,)
                entryCodigoVenta.delete(0,END)
                entryMarcaVenta.delete(0,END)
                entryModeloVenta.delete(0,END)
                entryCantidadVenta.delete(0,END)
                entryPrecioVenta.delete(0,END)
                entryTotalVenta.delete(0,END)
                break


    def modificar_Ve():
        dato=(entryMarcaVenta.get(),
            entryModeloVenta.get(),
            entryPrecioVenta.get(),
            entryCantidadVenta.get(),
            entryTotalVenta.get(),)
        if vacios(dato):
            messagebox.showwarning("Guardar datos","Te faltan completar datos")
        elif validarSoloNum(dato[2]) or validarSoloNum(dato[3]) or validarSoloNum(dato[4]):
            messagebox.showwarning("Guardar datos","Subtotal, cantidad y/o total deben ser sólo números")
        elif validarSoloLetras(dato[0]):
            messagebox.showwarning("Guardar datos","Verificar que sea solo letra la marca.")

        else:
            datos_Ve=(entryMarcaVenta.get(),
            entryModeloVenta.get(),
            entryPrecioVenta.get(),
            entryCantidadVenta.get(),
            entryTotalVenta.get(),)

            connection.Database()
            sql="UPDATE venta SET marca=?,modelo=?,subtotal=?,cantidad=?,total=? WHERE id=?"
            connection.cursor.execute(sql,datos_Ve)
            connection.conn.commit()
            datosVe=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryVe()

            if(len(datos_Ve)>0):
                for dato in datos_Ve:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    marca.delete(0,END)
                    marca.insert(END,dato[1])
                    modelo.delete(0,END)
                    modelo.insert(END,dato[2])
                    subtotal.delete(0,END)
                    subtotal.insert(END,dato[3])
                    cantidad.delete(0,END)
                    cantidad.insert(END,dato[4])
                    total.delete(0,END)
                    total.insert(END,dato[5])
                    messagebox.showinfo("Error al Modificar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Modificar datos","Datos modificados")

    def eliminar_Ve():
        if (entryBuscar_Ve.get()==""):
            messagebox.showerror("Error al Eliminar","Debes colocar un número de ID")
        elif (entryBuscar_Ve.get()=="0"):
            messagebox.showerror("Error al Eliminar","Debes colocar un número diferente a cero")
        else:
            eliminarid_Ve=[entryBuscar_Ve.get()]
            connection.Database()
            connection.cursor.execute("DELETE FROM venta WHERE id=?",eliminarid_Ve)
            connection.conn.commit()
            datos_Ve = connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            vaciarEntryVe()
            if(len(datos_Ve)>0):
                for dato in datos_Ve:
                    id.delete(0,END)
                    id.insert(END,dato[0])
                    marca.delete(0,END)
                    marca.insert(END,dato[1])
                    modelo.delete(0,END)
                    modelo.insert(END,dato[2])
                    subtotal.delete(0,END)
                    subtotal.insert(END,dato[3])
                    cantidad.delete(0,END)
                    cantidad.insert(END,dato[4])
                    total.delete(0,END)
                    total.insert(END,dato[5])
                    messagebox.showerror("Error al eliminar","Tenes que seleccionar uno correcto")
            else:
                messagebox.showinfo("Eliminación de objetos","Se elimino correctamente")
    
    
    
    
    def volver():
        frameImagenInfo.place(**FrameInfoMod)
        botonBuscarP.place_forget()
        botonCrearP.place_forget()
        botonEliminarP.place_forget()
        botonModificarP.place_forget()
        botonNuevoP.place_forget()
        entryBuscar_p.place_forget()
        botonBuscarCl.place_forget()
        botonCrearCl.place_forget()
        botonEliminarCl.place_forget()
        botonModificarCl.place_forget()
        botonNuevoCl.place_forget()
        entryBuscar_Cl.place_forget()
        botonBuscar_a.place_forget()
        botonCrear_a.place_forget()
        botonEliminar_a.place_forget()
        botonModificar_a.place_forget()
        botonNuevo_a.place_forget()
        entryBuscar_a.place_forget()
        botonBuscarCo.place_forget()
        botonCrearCo.place_forget()
        botonAgregarCo.place_forget()
        botonEliminarCo.place_forget()
        botonModificarCo.place_forget()
        botonNuevoCo.place_forget()
        entryBuscar_Co.place_forget()
        botonBuscarVe.place_forget()
        botonCrearVe.place_forget()
        botonAgregarVe.place_forget()
        botonEliminarVe.place_forget()
        botonModificarVe.place_forget()
        botonNuevoVe.place_forget()
        entryBuscar_Ve.place_forget()
        
        
                        
    def limpiar():

        limpiarEntrada=[comboCl1.get(),comboPr1.get(),comboPr.get(),comboCl.get(),comboA.get(),
        entryBuscar_p.get(),entryBuscar_a.get(),entryBuscar_Ve.get(),entryBuscar_Co.get(),
        entryBuscar_Cl.get(),entryRazonSocialPr.get(),entryCuitPr.get(),entryDireccionPr.get(),
        entryTelefonoPr.get(),entryLocalidadPr.get(),entryCpPr.get(),entryRazonSocialCl.get(),entryCuitCl.get(),
        entryDireccionCl.get(),entryTelefonoCl.get(),entryCodigo.get(),entryLocalidadCl.get(),entryCpCl.get(),
        entryModeloA.get(),entryStockA.get(),entryPrecioCostoA.get(),entryCodigoCompra.get(),
        entryMarcaCompra.get(),entryModeloCompra.get(),entryPrecioCompra.get(),entryCantidadCompra.get(),
        entryIvaCompra.get(),entryCodigoVenta.get(),entryMarcaVenta.get(),entryModeloVenta.get(),
        entryPrecioVenta.get(),entryCantidadVenta.get(),entryTotalVenta.get()]

        comboPr.delete(0,END)
        comboCl.delete(0,END)
        comboA.delete(0,END)
        comboPr1.delete(0,END)
        comboCl1.delete(0,END)
        entryBuscar_p.delete(0,END)
        entryBuscar_a.delete(0,END)
        entryBuscar_Ve.delete(0,END)
        entryBuscar_Co.delete(0,END)
        entryBuscar_Cl.delete(0,END)
        entryRazonSocialPr.delete(0,END)
        entryCuitPr.delete(0,END)
        entryDireccionPr.delete(0,END)
        entryTelefonoPr.delete(0,END)
        entryLocalidadPr.delete(0,END)
        entryCpPr.delete(0,END)
        entryRazonSocialCl.delete(0,END)
        entryCuitCl.delete(0,END)
        entryDireccionCl.delete(0,END)
        entryTelefonoCl.delete(0,END)
        entryLocalidadCl.delete(0,END)
        entryCpCl.delete(0,END)
        entryModeloA.delete(0,END)
        entryStockA.delete(0,END)
        entryPrecioCostoA.delete(0,END)
        entryCodigoCompra.delete(0,END)
        entryMarcaCompra.delete(0,END)
        entryModeloCompra.delete(0,END)
        entryPrecioCompra.delete(0,END)
        entryCantidadCompra.delete(0,END)
        entryIvaCompra.delete(0,END)
        entryCodigoVenta.delete(0,END)
        entryMarcaVenta.delete(0,END)
        entryModeloVenta.delete(0,END)
        entryPrecioVenta.delete(0,END)
        entryCantidadVenta.delete(0,END)
        entryTotalVenta.delete(0,END)

    def messageAbout():
        messagebox.showinfo("Acerca de...","Producto hecho por Axel Araya, cursante de segundo año de la carrera de desarrollo de software.")

    def messageHelp():
        messagebox.showinfo("Ayuda", "Para solicitar ayuda contactar al correo: arayavalencia96@gmail.com")

    def cerrarSesion():
        msgbox=messagebox.askquestion("Exit","Seguro que quieres cerrar sesion?")
        if msgbox == 'yes':
            ventana3.destroy()
            App1()




     
    ###################################################################################
    ############################################################## BOTONES ############
    
    # vista de los botones
    vistaBotones={'width':'12','font':("calibri",16),'bg':'#9FB6D9'}


    botonLimpiar=Button(frameBotonesDerecha,text="LIMPIAR",**vistaBotones,command=limpiar)
    botonLimpiar.place(x=13,y=511)
    
    botonAtras=Button(frameBotonesDerecha,text="VOLVER",**vistaBotones,command=volver)
    botonAtras.place(x=13,y=571)

    botonCerrarSesion=Button(frameBotonesDerecha,text="cerrar sesion, "+sesion,width=19,font=('calibri',12),bg='#9FB6D9',command=cerrarSesion)
    botonCerrarSesion.place(x=8,y=631)
    
                                         ################## PROVEEDORES ###############

    def eventoP(evento):
        cerrarFrames()
        frameModificarInfoPr.place(**FrameInfoMod)
        frameBotonesAbajoP.place(**ubFrameBotones)
        
    
    botonNuevoP=Button(frameBotonesAbajoP,text="NUEVO",**vistaBotones)
    botonNuevoP.bind("<Button-1>",eventoP)

    botonCrearP=Button(frameBotonesAbajoP,text="CREAR",**vistaBotones,command=guardarP)

    botonModificarP=Button(frameBotonesAbajoP,text="MODIFICAR",**vistaBotones,command=modificarP)

    botonEliminarP=Button(frameBotonesAbajoP,text="ELIMINAR",**vistaBotones,command=eliminarP)

    botonBuscarP=Button(frameBotonesAbajoP,text="BUSCAR",**vistaBotones,command=buscar_p)

    
                                         ################### CLIENTES #################

    def eventoCl(evento):
        cerrarFrames()
        frameModificarInfoCl.place(**FrameInfoMod)
        frameBotonesAbajoCl.place(**ubFrameBotones)
    
    botonNuevoCl=Button(frameBotonesAbajoCl,text="NUEVO",**vistaBotones)
    botonNuevoCl.bind("<Button-1>",eventoCl)

    botonCrearCl=Button(frameBotonesAbajoCl,text="CREAR",**vistaBotones,command=guardarCl)

    botonModificarCl=Button(frameBotonesAbajoCl,text="MODIFICAR",**vistaBotones,command=modificarCl)

    botonEliminarCl=Button(frameBotonesAbajoCl,text="ELIMINAR",**vistaBotones,command=eliminarCl)
    
    botonBuscarCl=Button(frameBotonesAbajoCl,text="BUSCAR",**vistaBotones,command=buscar_Cl)

                                            ################### ARTICULOS #############

    def eventoA(evento):
        cerrarFrames()
        frameModificarInfoA.place(**FrameInfoMod)
        frameBotonesAbajoA.place(**ubFrameBotones)
    
    botonNuevo_a=Button(frameBotonesAbajoA,text="NUEVO",**vistaBotones)
    botonNuevo_a.bind("<Button-1>",eventoA)

    botonCrear_a=Button(frameBotonesAbajoA,text="CREAR",**vistaBotones,command=guardar_a)

    botonModificar_a=Button(frameBotonesAbajoA,text="MODIFICAR",**vistaBotones,command=modificar_a)

    botonEliminar_a=Button(frameBotonesAbajoA,text="ELIMINAR",**vistaBotones,command=eliminar_a)

    botonBuscar_a=Button(frameBotonesAbajoA,text="BUSCAR",**vistaBotones,command=buscar_a)
    
                                            ################### COMPRA ################

    def eventoCo(evento):
        cerrarFrames()
        frameModificarInfoCo.place(**FrameInfoMod)
        frameBotonesAbajoCo.place(**ubFrameBotones)

    def calcularTotalMasIvaCompra(evento):
        total=(float(entryPrecioCompra.get())*float(entryCantidadCompra.get()))
        ivaDelTotal=(total*0.2)
        totalMasIva=(total+ivaDelTotal)
        entryIvaCompra.insert(END,str(totalMasIva))
    entryCantidadCompra.bind("<Return>",calcularTotalMasIvaCompra)
    
    botonNuevoCo=Button(frameBotonesAbajoCo,text="NUEVO",**vistaBotones)
    botonNuevoCo.bind("<Button-1>",eventoCo)

    botonCrearCo=Button(frameBotonesAbajoCo,text="COMPRAR",**vistaBotones,command=compraArticulo)

    botonAgregarCo=Button(frameBotonesAbajoCo,text="AGREG/SELEC",**vistaBotones,command=agregarArticuloCompra)

    botonModificarCo=Button(frameBotonesAbajoCo,text="MODIFICAR",**vistaBotones,command=modificar_Co)

    botonEliminarCo=Button(frameBotonesAbajoCo,text="ELIMINAR",**vistaBotones,command=eliminar_Co)

    botonBuscarCo=Button(frameBotonesAbajoCo,text="BUSCAR",**vistaBotones,command=buscar_Co)

                                            ################### VENTA #################
    
    def eventoVe(evento):
        cerrarFrames()
        frameModificarInfoVe.place(**FrameInfoMod)
        frameBotonesAbajoVe.place(**ubFrameBotones)

    def calcularTotalMasIvaVenta(evento):
        total=(float(entryPrecioVenta.get())*float(entryCantidadVenta.get()))
        ivaDelTotal=(total*0.2)
        totalMasIva=(total+ivaDelTotal)
        entryTotalVenta.insert(END,str(totalMasIva))
    entryCantidadVenta.bind("<Return>",calcularTotalMasIvaVenta)
    
    botonNuevoVe=Button(frameBotonesAbajoVe,text="NUEVO",**vistaBotones)
    botonNuevoVe.bind("<Button-1>",eventoVe)

    botonCrearVe=Button(frameBotonesAbajoVe,text="VENDER",**vistaBotones,command=ventaArticulo)

    botonAgregarVe=Button(frameBotonesAbajoVe,text="AGREG/SELEC",**vistaBotones,command=agregarArticuloVenta)

    botonModificarVe=Button(frameBotonesAbajoVe,text="MODIFICAR",**vistaBotones,command=modificar_Ve)

    botonEliminarVe=Button(frameBotonesAbajoVe,text="ELIMINAR",**vistaBotones,command=eliminar_Ve)

    botonBuscarVe=Button(frameBotonesAbajoVe,text="BUSCAR",**vistaBotones,command=buscar_Ve)



    ###################################################################################
    ############################################################## TABLAS #############

    ############################################################## PROVEEDORES ########


    # Se abre el frame donde muestra la tabla con la información
    
    def evento_p():

        # CREAMOS EL TREEVIEW

        scrollbaryp = Scrollbar(frameInfo, orient=VERTICAL)
        scrollbarxp = Scrollbar(frameInfo, orient=HORIZONTAL)

        treep = ttk.Treeview(frameInfo, columns=("ID", "Nombre","CUIT","Direccion","Telefono","IVA","Localidad","Provincia","C.P."),
            selectmode="extended", height=300, yscrollcommand=scrollbaryp.set, xscrollcommand=scrollbarxp.set)

        scrollbaryp.config(command=treep.yview)
        scrollbaryp.pack(side=RIGHT, fill=Y)
        scrollbarxp.config(command=treep.xview)
        scrollbarxp.pack(side=BOTTOM, fill=X)

        treep['show'] = 'headings'
        treep.heading('ID', text="ID", anchor=CENTER)
        treep.heading('Nombre', text="Nombre", anchor=CENTER)
        treep.heading('CUIT', text="CUIT", anchor=CENTER)
        treep.heading('Direccion', text="Dirección", anchor=CENTER)
        treep.heading('Telefono', text="Teléfono", anchor=CENTER)
        treep.heading('IVA', text="IVA", anchor=CENTER)
        treep.heading('Localidad', text="Localidad", anchor=CENTER)
        treep.heading('Provincia', text="Provincia", anchor=CENTER)
        treep.heading('C.P.', text="C.P.", anchor=CENTER)

        treep.column('#1', stretch=NO, minwidth=0, width=50)
        treep.column('#2', stretch=NO, minwidth=0, width=196)
        treep.column('#3', stretch=NO, minwidth=0, width=196)
        treep.column('#4', stretch=NO, minwidth=0, width=196)
        treep.column('#5', stretch=NO, minwidth=0, width=196)
        treep.column('#6', stretch=NO, minwidth=0, width=196)
        treep.column('#7', stretch=NO, minwidth=0, width=196)
        treep.column('#8', stretch=NO, minwidth=0, width=196)
        treep.column('#9', stretch=NO, minwidth=0, width=196)
        treep.pack()

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaP(evento):
            mostrar=0
            ids=treep.item(treep.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'proveedores'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_p=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            frameModificarInfoPr.place(x=170,y=80,width=1196,height=545)
            frameImagenInfo.place_forget()
            frameInfo.place_forget()
            for dato in datos_p:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT * FROM proveedores WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_p=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_p:
                        entryCodigo.delete(0,END)
                        entryCodigo.insert(END,dato["id"])
                        entryRazonSocialPr.delete(0,END)
                        entryRazonSocialPr.insert(END,dato["nombre"])
                        entryCuitPr.delete(0,END)
                        entryCuitPr.insert(END,dato["cuit"])
                        entryDireccionPr.delete(0,END)
                        entryDireccionPr.insert(END,dato["direccion"])
                        entryTelefonoPr.delete(0,END)
                        entryTelefonoPr.insert(END,dato["telefono"])
                        comboPr.delete(0,END)
                        comboPr.insert(END,dato["iva"])
                        entryLocalidadPr.delete(0,END)
                        entryLocalidadPr.insert(END,dato["localidad"])
                        comboPr1.delete(0,END)
                        comboPr1.insert(END,dato["provincia"])
                        entryCpPr.delete(0,END)
                        entryCpPr.insert(END,dato["cp"])
                        break

        treep.bind("<<TreeviewSelect>>",mostrarDatoListaP)


        # Se puede buscar por nombre, por CUIT o por direccion

        def buscarPorNombreP(evento):
            buscar=("%"+entryBuscar_p.get()+"%","%"+entryBuscar_p.get()+"%","%"+entryBuscar_p.get()+"%")
            connection.Database()
            connection.cursor.execute("SELECT * FROM proveedores WHERE nombre LIKE ? OR cuit LIKE ? OR direccion LIKE ?",buscar)
            connection.conn.commit()
            datosBuscados= connection.cursor.fetchall()
            for filas in treep.get_children():
                treep.delete(filas)
            for data in datosBuscados:
                treep.insert('', 'end', values=[data[0],data[1], data[2], data[3], data[4], data[5],data[6],data[7],data[8]])

        entryBuscar_p.bind("<Key>",buscarPorNombreP)


        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfo.place(**FrameInfoMod)
        frameBotonesAbajoP.place(**ubFrameBotones)
        botonBuscarP.place(x=850,y=19)
        botonCrearP.place(x=200,y=631)
        botonEliminarP.place(x=850,y=631)
        botonModificarP.place(x=545,y=631)
        botonNuevoP.place(x=10,y=631)
        entryBuscar_p.place(x=150,y=19)
        treep.delete(*treep.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `proveedores` ORDER BY `id` ASC")
        fetch = connection.cursor.fetchall()
        for data in fetch:
            treep.insert('', 'end', values=[data[0],data[1], data[2], data[3], data[4], data[5],data[6],data[7],data[8]])
        connection.cursor.close()
        connection.conn.close()


    # se crea el botón el cual genera varios evento, entre los cuales busqueda,mostrar Treeview y seleccionar items

    botonProveedores=Button(frameBotonesDerecha,text="PROVEEDORES",**vistaBotones,command=evento_p)
    botonProveedores.place(x=13,y=20)

       

    ###################################################################################
    ############################################################## CLIENTES ###########
    
    # Se abre el frame donde muestra la tabla con la información

    def evento_Cli():

        # CREAMOS EL TREEVIEW

        scrollbaryCl = Scrollbar(frameInfoCl, orient=VERTICAL)
        scrollbarxCl = Scrollbar(frameInfoCl, orient=HORIZONTAL)

        treeCl = ttk.Treeview(frameInfoCl, columns=("ID", "Nombre","CUIT","Direccion","Telefono","IVA","Localidad","Provincia","C.P."), selectmode="extended", height=300, yscrollcommand=scrollbaryCl.set, xscrollcommand=scrollbarxCl.set)
        scrollbaryCl.config(command=treeCl.yview)
        scrollbaryCl.pack(side=RIGHT, fill=Y)
        scrollbarxCl.config(command=treeCl.xview)
        scrollbarxCl.pack(side=BOTTOM, fill=X)

        treeCl['show'] = 'headings'
        treeCl.heading('ID', text="ID", anchor=CENTER)
        treeCl.heading('Nombre', text="Nombre", anchor=CENTER)
        treeCl.heading('CUIT', text="CUIT", anchor=CENTER)
        treeCl.heading('Direccion', text="Dirección", anchor=CENTER)
        treeCl.heading('Telefono', text="Teléfono", anchor=CENTER)
        treeCl.heading('IVA', text="IVA", anchor=CENTER)
        treeCl.heading('Localidad', text="Localidad", anchor=CENTER)
        treeCl.heading('Provincia', text="Provincia", anchor=CENTER)
        treeCl.heading('C.P.', text="C.P.", anchor=CENTER)
        
        treeCl.column('#1', stretch=NO, minwidth=0, width=50)
        treeCl.column('#2', stretch=NO, minwidth=0, width=196)
        treeCl.column('#3', stretch=NO, minwidth=0, width=196)
        treeCl.column('#4', stretch=NO, minwidth=0, width=196)
        treeCl.column('#5', stretch=NO, minwidth=0, width=196)
        treeCl.column('#6', stretch=NO, minwidth=0, width=196)
        treeCl.column('#7', stretch=NO, minwidth=0, width=196)
        treeCl.column('#8', stretch=NO, minwidth=0, width=196)
        treeCl.column('#9', stretch=NO, minwidth=0, width=196)
        treeCl.pack()

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaCl(evento):
            mostrar=0
            ids=treeCl.item(treeCl.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'clientes'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_Cl=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            frameModificarInfoCl.place(x=170,y=80,width=1196,height=545)
            frameImagenInfo.place_forget()
            frameInfoCl.place_forget()
            for dato in datos_Cl:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT * FROM clientes WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_Cl=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_Cl:
                        entryCodigo.delete(0,END)
                        entryCodigo.insert(END,dato["id"])
                        entryRazonSocialCl.delete(0,END)
                        entryRazonSocialCl.insert(END,dato["nombre"])
                        entryCuitCl.delete(0,END)
                        entryCuitCl.insert(END,dato["cuit"])
                        entryDireccionCl.delete(0,END)
                        entryDireccionCl.insert(END,dato["direccion"])
                        entryTelefonoCl.delete(0,END)
                        entryTelefonoCl.insert(END,dato["telefono"])
                        comboCl.delete(0,END)
                        comboCl.insert(END,dato["iva"])
                        entryLocalidadCl.delete(0,END)
                        entryLocalidadCl.insert(END,dato["localidad"])
                        comboCl1.delete(0,END)
                        comboCl1.insert(END,dato["provincia"])
                        entryCpCl.delete(0,END)
                        entryCpCl.insert(END,dato["cp"])
                        break

        treeCl.bind("<<TreeviewSelect>>",mostrarDatoListaCl)

        
        # Se puede buscar por nombre, por CUIT o por direccion

        def buscarPorNombreCl(evento):
            buscar=("%"+entryBuscar_Cl.get()+"%","%"+entryBuscar_Cl.get()+"%","%"+entryBuscar_Cl.get()+"%")
            connection.Database()
            connection.cursor.execute("SELECT * FROM clientes WHERE nombre LIKE ? OR cuit LIKE ? OR direccion LIKE ?",buscar)
            connection.conn.commit()
            datosBuscados= connection.cursor.fetchall()
            for filas in treeCl.get_children():
                treeCl.delete(filas)
            for data in datosBuscados:
                treeCl.insert('', 'end', values=[data[0],data[1], data[2], data[3], data[4], data[5],data[6],data[7],data[8]])

        entryBuscar_Cl.bind("<Key>",buscarPorNombreCl)


        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfoCl.place(**FrameInfoMod)
        frameBotonesAbajoCl.place(**ubFrameBotones)
        entryBuscar_Cl.place(x=150,y=19)
        botonNuevoCl.place(x=10,y=631)
        botonCrearCl.place(x=200,y=631)
        botonModificarCl.place(x=545,y=631)
        botonEliminarCl.place(x=850,y=631)
        botonBuscarCl.place(x=850,y=19)
        treeCl.delete(*treeCl.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `clientes` ORDER BY `id` ASC")
        fetchCl = connection.cursor.fetchall()
        for data in fetchCl:
            treeCl.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4], data[5],data[6],data[7],data[8]])
        connection.cursor.close()
        connection.conn.close()


    # se crea el botón el cual genera varios evento, entre los cuales busqueda,mostrar Treeview y seleccionar items

    botonClientes=Button(frameBotonesDerecha,text="CLIENTES",**vistaBotones,command=evento_Cli)
    botonClientes.place(x=13,y=90)



    ###################################################################################
    ############################################################## ARTICULOS ##########

    
    # COMPRA
    def evento_Ac():

        scrollbaryAc = Scrollbar(frameInfoA, orient=VERTICAL)
        scrollbarxAc = Scrollbar(frameInfoA, orient=HORIZONTAL)

        treeAc = ttk.Treeview(frameInfoA, columns=("ID", "Marca","Modelo","Stock","Precio Costo"), selectmode="extended", height=300, yscrollcommand=scrollbaryAc.set, xscrollcommand=scrollbarxAc.set)
        scrollbaryAc.config(command=treeAc.yview)
        scrollbaryAc.pack(side=RIGHT, fill=Y)
        scrollbarxAc.config(command=treeAc.xview)
        scrollbarxAc.pack(side=BOTTOM, fill=X)

        treeAc['show'] = 'headings'
        treeAc.heading('ID', text="ID", anchor=CENTER)
        treeAc.heading('Marca', text="Marca", anchor=CENTER)
        treeAc.heading('Modelo', text="Modelo", anchor=CENTER)
        treeAc.heading('Stock', text="Stock", anchor=CENTER)
        treeAc.heading('Precio Costo', text="Precio Costo", anchor=CENTER)
        
        treeAc.column('#1', stretch=NO, minwidth=0, width=54)
        treeAc.column('#2', stretch=NO, minwidth=0, width=222)
        treeAc.column('#3', stretch=NO, minwidth=0, width=222)
        treeAc.column('#4', stretch=NO, minwidth=0, width=222)
        treeAc.column('#5', stretch=NO, minwidth=0, width=222)
        treeAc.pack()

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaAc(evento):
            mostrar=0
            ids=treeAc.item(treeAc.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'articulos'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_Ac=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            cerrarFrames()
            frameModificarInfoCo.place(**FrameInfoMod)
            frameBotonesAbajoCo.place(**ubFrameBotones)
            for dato in datos_Ac:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT id,marca,modelo,precio_costo FROM articulos WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_Ac=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_Ac:
                        entryCodigoCompra.delete(0,END)
                        entryCodigoCompra.insert(END,dato['id'])
                        entryMarcaCompra.delete(0,END)
                        entryMarcaCompra.insert(END,dato['marca'])
                        entryModeloCompra.delete(0,END)
                        entryModeloCompra.insert(END,dato['modelo'])
                        entryPrecioCompra.delete(0,END)
                        entryPrecioCompra.insert(END,dato['precio_costo'])
                        treeAc.pack_forget()
                        break

        treeAc.bind("<<TreeviewSelect>>",mostrarDatoListaAc)

        cerrarFrames()
        frameInfoA.place(**FrameInfoMod)
        frameBotonesAbajoA.place(**ubFrameBotones)
        entryBuscar_a.place(x=150,y=19)
        treeAc.delete(*treeAc.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `articulos` ORDER BY `id` ASC")
        fetchAc = connection.cursor.fetchall()
        for data in fetchAc:
            treeAc.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4]])
        connection.cursor.close()
        connection.conn.close()


    # VENTA
    def evento_Av():
        
        scrollbaryAv = Scrollbar(frameInfoA, orient=VERTICAL)
        scrollbarxAv = Scrollbar(frameInfoA, orient=HORIZONTAL)

        treeAv = ttk.Treeview(frameInfoA, columns=("ID", "Marca","Modelo","Stock","Precio Costo"), selectmode="extended", height=300, yscrollcommand=scrollbaryAv.set, xscrollcommand=scrollbarxAv.set)
        scrollbaryAv.config(command=treeAv.yview)
        scrollbaryAv.pack(side=RIGHT, fill=Y)
        scrollbarxAv.config(command=treeAv.xview)
        scrollbarxAv.pack(side=BOTTOM, fill=X)

        treeAv['show'] = 'headings'
        treeAv.heading('ID', text="ID", anchor=CENTER)
        treeAv.heading('Marca', text="Marca", anchor=CENTER)
        treeAv.heading('Modelo', text="Modelo", anchor=CENTER)
        treeAv.heading('Stock', text="Stock", anchor=CENTER)
        treeAv.heading('Precio Costo', text="Precio Costo", anchor=CENTER)
        
        treeAv.column('#1', stretch=NO, minwidth=0, width=54)
        treeAv.column('#2', stretch=NO, minwidth=0, width=222)
        treeAv.column('#3', stretch=NO, minwidth=0, width=222)
        treeAv.column('#4', stretch=NO, minwidth=0, width=222)
        treeAv.column('#5', stretch=NO, minwidth=0, width=222)
        treeAv.pack()

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaAv(evento):
            mostrar=0
            ids=treeAv.item(treeAv.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'articulos'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_Av=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            cerrarFrames()
            frameModificarInfoVe.place(**FrameInfoMod)
            frameBotonesAbajoVe.place(**ubFrameBotones)
            for dato in datos_Av:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT id,marca,modelo,precio_costo FROM articulos WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_Av=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_Av:
                        entryCodigoVenta.delete(0,END)
                        entryCodigoVenta.insert(END,dato['id'])
                        entryMarcaVenta.delete(0,END)
                        entryMarcaVenta.insert(END,dato['marca'])
                        entryModeloVenta.delete(0,END)
                        entryModeloVenta.insert(END,dato['modelo'])
                        entryPrecioVenta.delete(0,END)
                        entryPrecioVenta.insert(END,dato['precio_costo'])
                        treeAv.pack_forget()
                        break

        treeAv.bind("<<TreeviewSelect>>",mostrarDatoListaAv)

        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfoA.place(**FrameInfoMod)
        frameBotonesAbajoA.place(**ubFrameBotones)
        botonBuscar_a.place(x=850,y=19)
        entryBuscar_a.place(x=150,y=19)
        treeAv.delete(*treeAv.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `articulos` ORDER BY `id` ASC")
        fetchAv = connection.cursor.fetchall()
        for data in fetchAv:
            treeAv.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4]])
        connection.cursor.close()
        connection.conn.close()





    def evento_A():

        scrollbaryA = Scrollbar(frameInfoA, orient=VERTICAL)
        scrollbarxA = Scrollbar(frameInfoA, orient=HORIZONTAL)

        treeA = ttk.Treeview(frameInfoA, columns=("ID", "Marca","Modelo","Stock","Precio Costo"), selectmode="extended", height=300, yscrollcommand=scrollbaryA.set, xscrollcommand=scrollbarxA.set)
        scrollbaryA.config(command=treeA.yview)
        scrollbaryA.pack(side=RIGHT, fill=Y)
        scrollbarxA.config(command=treeA.xview)
        scrollbarxA.pack(side=BOTTOM, fill=X)

        treeA['show'] = 'headings'
        treeA.heading('ID', text="ID", anchor=CENTER)
        treeA.heading('Marca', text="Marca", anchor=CENTER)
        treeA.heading('Modelo', text="Modelo", anchor=CENTER)
        treeA.heading('Stock', text="Stock", anchor=CENTER)
        treeA.heading('Precio Costo', text="Precio Costo", anchor=CENTER)
        
        treeA.column('#1', stretch=NO, minwidth=0, width=54)
        treeA.column('#2', stretch=NO, minwidth=0, width=222)
        treeA.column('#3', stretch=NO, minwidth=0, width=222)
        treeA.column('#4', stretch=NO, minwidth=0, width=222)
        treeA.column('#5', stretch=NO, minwidth=0, width=222)
        treeA.pack()

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaA(evento):
            mostrar=0
            ids=treeA.item(treeA.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'articulos'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_A=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            cerrarFrames()
            frameModificarInfoA.place(**FrameInfoMod)
            frameBotonesAbajoA.place(**ubFrameBotones)
            for dato in datos_A:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT * FROM articulos WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_A=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_A:
                        entryCodigoCompra.delete(0,END)
                        entryCodigoCompra.insert(END,dato['id'])
                        comboA.delete(0,END)
                        comboA.insert(END,dato['marca'])
                        entryModeloA.delete(0,END)
                        entryModeloA.insert(END,dato['modelo'])
                        entryStockA.delete(0,END)
                        entryStockA.insert(END,dato['stock'])
                        entryPrecioCostoA.delete(0,END)
                        entryPrecioCostoA.insert(END,dato['precio_costo'])
                        break

        treeA.bind("<<TreeviewSelect>>",mostrarDatoListaA)
    
        # Se puede buscar por nombre, por CUIT o por direccion

        def buscarPorNombreA(evento):
            buscar=("%"+entryBuscar_a.get()+"%","%"+entryBuscar_a.get()+"%","%"+entryBuscar_a.get()+"%")
            connection.Database()
            connection.cursor.execute("SELECT * FROM articulos WHERE id LIKE ? OR marca LIKE ? OR modelo LIKE ?",buscar)
            connection.conn.commit()
            datosBuscados= connection.cursor.fetchall()
            for filas in treeA.get_children():
                treeA.delete(filas)
            for data in datosBuscados:
                treeA.insert('', 'end', values=[data[0],data[1], data[2], data[3], data[4]])

        entryBuscar_a.bind("<Key>",buscarPorNombreA)

        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfoA.place(**FrameInfoMod)
        frameBotonesAbajoA.place(**ubFrameBotones)
        botonNuevo_a.place(x=10,y=631)
        botonCrear_a.place(x=200,y=631)
        botonModificar_a.place(x=545,y=631)
        botonEliminar_a.place(x=850,y=631)
        botonBuscar_a.place(x=850,y=19)
        entryBuscar_a.place(x=150,y=19)
        treeA.delete(*treeA.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `articulos` ORDER BY `id` ASC")
        fetchA = connection.cursor.fetchall()
        for data in fetchA:
            treeA.insert('', 'end', values=[data[0], data[1], data[2], data[3], data[4]])
        connection.cursor.close()
        connection.conn.close()

    # se crea el botón el cual genera varios evento, entre los cuales busqueda,mostrar Treeview y seleccionar items

    botonArticulos=Button(frameBotonesDerecha,text="ARTICULOS",**vistaBotones,command=evento_A)
    botonArticulos.place(x=13,y=160)



    ###################################################################################
    ############################################################## COMPRA #############

    def evento_Co():

        # CREAMOS EL TREEVIEW

        scrollbaryCo = Scrollbar(frameInfoCo, orient=VERTICAL)
        scrollbarxCo = Scrollbar(frameInfoCo, orient=HORIZONTAL)

        treeCo = ttk.Treeview(frameInfoCo, columns=("ID","Fecha","Total"), selectmode="extended", height=300, yscrollcommand=scrollbaryCo.set, xscrollcommand=scrollbarxCo.set)
        scrollbaryCo.config(command=treeCo.yview)
        scrollbaryCo.pack(side=RIGHT, fill=Y)
        scrollbarxCo.config(command=treeCo.xview)
        scrollbarxCo.pack(side=BOTTOM, fill=X)

        treeCo['show'] = 'headings'
        treeCo.heading('ID', text="ID", anchor=CENTER)
        treeCo.heading('Fecha', text="Fecha", anchor=CENTER)
        treeCo.heading('Total', text="Total", anchor=CENTER)
        
        treeCo.column('#1', stretch=NO, minwidth=0, width=100)
        treeCo.column('#2', stretch=NO, minwidth=0, width=215)
        treeCo.column('#3', stretch=NO, minwidth=0, width=215)
        treeCo.pack()

        # Se puede buscar por nombre, por CUIT o por direccion

        def buscarPorNombreCo(evento):
            buscar=("%"+entryBuscar_Co.get()+"%","%"+entryBuscar_Co.get()+"%","%"+entryBuscar_Co.get()+"%")
            connection.Database()
            connection.cursor.execute("SELECT * FROM compra WHERE id LIKE ? OR total LIKE ? OR fecha LIKE ?",buscar)
            connection.conn.commit()
            datosBuscados= connection.cursor.fetchall()
            for filas in treeCo.get_children():
                treeCo.delete(filas)
            for data in datosBuscados:
                treeCo.insert('', 'end', values=[data[0],data[1], data[2]])

        entryBuscar_Co.bind("<Key>",buscarPorNombreCo)

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaCo(evento):
            mostrar=0
            ids=treeCo.item(treeCo.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'compra'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_Co=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            frameModificarInfoCo.place(x=170,y=80,width=1196,height=545)
            frameImagenInfo.place_forget()
            frameInfoCo.place_forget()
            for dato in datos_Co:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT * FROM compra WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_Co=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_Co:
                        entryCodigoCompra.delete(0,END)
                        entryCodigoCompra.insert(END,dato['id'])
                        entryIvaCompra.delete(0,END)
                        entryIvaCompra.insert(END,dato['total'])
                        break

        treeCo.bind("<<TreeviewSelect>>",mostrarDatoListaCo)

        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfoCo.place(**FrameInfoMod)
        frameBotonesAbajoCo.place(**ubFrameBotones)
        botonNuevoCo.place(x=10,y=631)
        botonCrearCo.place(x=200,y=631)
        botonAgregarCo.place(x=370,y=631)
        botonModificarCo.place(x=670,y=631)
        botonEliminarCo.place(x=970,y=631)
        botonBuscarCo.place(x=850,y=19)
        entryBuscar_Co.place(x=150,y=19)
        treeCo.delete(*treeCo.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `compra` ORDER BY `id` ASC")
        fetchCo = connection.cursor.fetchall()
        for data in fetchCo:
            treeCo.insert('', 'end', values=[data[0], data[1], data[2]])
        connection.cursor.close()
        connection.conn.close()

    # se crea el botón el cual genera varios evento, entre los cuales busqueda,mostrar Treeview y seleccionar items

    botonCompra=Button(frameBotonesDerecha,text="COMPRA",**vistaBotones,command=evento_Co)
    botonCompra.place(x=13,y=230)



    ###################################################################################
    ############################################################## VENTA ##############

    def evento_Ve():

        # CREAMOS EL TREEVIEW

        scrollbaryVe = Scrollbar(frameInfoVe, orient=VERTICAL)
        scrollbarxVe = Scrollbar(frameInfoVe, orient=HORIZONTAL)

        treeVe = ttk.Treeview(frameInfoVe, columns=("ID","Fecha","Total"), selectmode="extended", height=300, yscrollcommand=scrollbaryVe.set, xscrollcommand=scrollbarxVe.set)
        scrollbaryVe.config(command=treeVe.yview)
        scrollbaryVe.pack(side=RIGHT, fill=Y)
        scrollbarxVe.config(command=treeVe.xview)
        scrollbarxVe.pack(side=BOTTOM, fill=X)

        treeVe['show'] = 'headings'
        treeVe.heading('ID', text="ID", anchor=CENTER)
        treeVe.heading('Fecha', text="Fecha", anchor=CENTER)
        treeVe.heading('Total', text="Total", anchor=CENTER)
        
        treeVe.column('#1', stretch=NO, minwidth=0, width=100)
        treeVe.column('#2', stretch=NO, minwidth=0, width=215)
        treeVe.column('#3', stretch=NO, minwidth=0, width=215)
        treeVe.pack()

        # Se puede buscar por nombre, por CUIT o por direccion

        def buscarPorNombreVe(evento):
            buscar=("%"+entryBuscar_Ve.get()+"%","%"+entryBuscar_Ve.get()+"%","%"+entryBuscar_Ve.get()+"%")
            connection.Database()
            connection.cursor.execute("SELECT * FROM venta WHERE id LIKE ? OR total LIKE ? OR fecha LIKE ?",buscar)
            connection.conn.commit()
            datosBuscados= connection.cursor.fetchall()
            for filas in treeVe.get_children():
                treeVe.delete(filas)
            for data in datosBuscados:
                treeVe.insert('', 'end', values=[data[0],data[1], data[2]])

        entryBuscar_Ve.bind("<Key>",buscarPorNombreVe)

        # al seleccionar un item del Treeview te manda al frame para poder modificarlo

        def mostrarDatoListaVe(evento):
            mostrar=0
            ids=treeVe.item(treeVe.selection())["values"]
            mostrar=f"{ids[0]}"
            connection.Database()
            sql="SELECT id FROM 'venta'"
            connection.cursor.execute(sql)
            connection.conn.commit()
            datos_Ve=connection.cursor.fetchall()
            connection.cursor.close()
            connection.conn.close()
            frameModificarInfoVe.place(x=170,y=80,width=1196,height=545)
            frameImagenInfo.place_forget()
            frameInfoVe.place_forget()
            for dato in datos_Ve:
                if int(dato[0])==int(mostrar):
                    connection.Database()
                    connection.cursor.execute("SELECT * FROM venta WHERE id=?",(mostrar,))
                    connection.conn.commit()
                    datos_Ve=connection.cursor.fetchall()
                    connection.cursor.close()
                    connection.conn.close()
                    for dato in datos_Ve:
                        entryCodigoVenta.delete(0,END)
                        entryCodigoVenta.insert(END,dato['id'])
                        entryTotalVenta.delete(0,END)
                        entryTotalVenta.insert(END,dato['total'])
                        break

        treeVe.bind("<<TreeviewSelect>>",mostrarDatoListaVe)

        # Finalmente cierra ciertos frames, muestra otro, y nos devuelve el Treeview con los datos cargados

        cerrarFrames()
        frameInfoVe.place(**FrameInfoMod)
        frameBotonesAbajoVe.place(**ubFrameBotones)
        botonNuevoVe.place(x=10,y=631)
        botonCrearVe.place(x=200,y=631)
        botonAgregarVe.place(x=370,y=631)
        botonModificarVe.place(x=670,y=631)
        botonEliminarVe.place(x=970,y=631)
        botonBuscarVe.place(x=850,y=19)
        entryBuscar_Ve.place(x=150,y=19)
        treeVe.delete(*treeVe.get_children())
        connection.Database()
        connection.cursor.execute("SELECT * FROM `venta` ORDER BY `id` ASC")
        fetchVe = connection.cursor.fetchall()
        for data in fetchVe:
            treeVe.insert('', 'end', values=[data[0], data[1], data[2]])
        connection.cursor.close()
        connection.conn.close()

    # se crea el botón el cual genera varios evento, entre los cuales busqueda,mostrar Treeview y seleccionar items

    botonVenta=Button(frameBotonesDerecha,text="VENTA",**vistaBotones,command=evento_Ve)
    botonVenta.place(x=13,y=300)


    ## ACLARECER LOS BOTONES AL PASAR EL MOUSE POR ENCIMA DE LOS MISMOS

    def hoverOn(boton):
        boton.config(bg='#476DA6')
    def hoverOff(boton):
        boton.config(bg='#9FB6D9')

    botonProveedores.bind('<Enter>',lambda x:hoverOn(botonProveedores))
    botonProveedores.bind('<Leave>',lambda x:hoverOff(botonProveedores))
    botonClientes.bind('<Enter>',lambda x:hoverOn(botonClientes))
    botonClientes.bind('<Leave>',lambda x:hoverOff(botonClientes))
    botonArticulos.bind('<Enter>',lambda x:hoverOn(botonArticulos))
    botonArticulos.bind('<Leave>',lambda x:hoverOff(botonArticulos))
    botonCompra.bind('<Enter>',lambda x:hoverOn(botonCompra))
    botonCompra.bind('<Leave>',lambda x:hoverOff(botonCompra))
    botonVenta.bind('<Enter>',lambda x:hoverOn(botonVenta))
    botonVenta.bind('<Leave>',lambda x:hoverOff(botonVenta))
    botonNuevoP.bind('<Enter>',lambda x:hoverOn(botonNuevoP))
    botonNuevoP.bind('<Leave>',lambda x:hoverOff(botonNuevoP))
    botonLimpiar.bind('<Enter>',lambda x:hoverOn(botonLimpiar))
    botonLimpiar.bind('<Leave>',lambda x:hoverOff(botonLimpiar))
    botonAtras.bind('<Enter>',lambda x:hoverOn(botonAtras))
    botonAtras.bind('<Leave>',lambda x:hoverOff(botonAtras))
    botonCerrarSesion.bind('<Enter>',lambda x:hoverOn(botonCerrarSesion))
    botonCerrarSesion.bind('<Leave>',lambda x:hoverOff(botonCerrarSesion))
    botonNuevoCl.bind('<Enter>',lambda x:hoverOn(botonNuevoCl))
    botonNuevoCl.bind('<Leave>',lambda x:hoverOff(botonNuevoCl))
    botonNuevoCo.bind('<Enter>',lambda x:hoverOn(botonNuevoCo))
    botonNuevoCo.bind('<Leave>',lambda x:hoverOff(botonNuevoCo))
    botonNuevoVe.bind('<Enter>',lambda x:hoverOn(botonNuevoVe))
    botonNuevoVe.bind('<Leave>',lambda x:hoverOff(botonNuevoVe))
    botonNuevo_a.bind('<Enter>',lambda x:hoverOn(botonNuevo_a))
    botonNuevo_a.bind('<Leave>',lambda x:hoverOff(botonNuevo_a))
    botonModificarP.bind('<Enter>',lambda x:hoverOn(botonModificarP))
    botonModificarP.bind('<Leave>',lambda x:hoverOff(botonModificarP))
    botonModificarCl.bind('<Enter>',lambda x:hoverOn(botonModificarCl))
    botonModificarCl.bind('<Leave>',lambda x:hoverOff(botonModificarCl))
    botonModificarCo.bind('<Enter>',lambda x:hoverOn(botonModificarCo))
    botonModificarCo.bind('<Leave>',lambda x:hoverOff(botonModificarCo))
    botonModificarVe.bind('<Enter>',lambda x:hoverOn(botonModificarVe))
    botonModificarVe.bind('<Leave>',lambda x:hoverOff(botonModificarVe))
    botonModificar_a.bind('<Enter>',lambda x:hoverOn(botonModificar_a))
    botonModificar_a.bind('<Leave>',lambda x:hoverOff(botonModificar_a))
    botonBuscarCo.bind('<Enter>',lambda x:hoverOn(botonBuscarCo))
    botonBuscarCo.bind('<Leave>',lambda x:hoverOff(botonBuscarCo))
    botonBuscarP.bind('<Enter>',lambda x:hoverOn(botonBuscarP))
    botonBuscarP.bind('<Leave>',lambda x:hoverOff(botonBuscarP))
    botonBuscarCl.bind('<Enter>',lambda x:hoverOn(botonBuscarCl))
    botonBuscarCl.bind('<Leave>',lambda x:hoverOff(botonBuscarCl))
    botonBuscarVe.bind('<Enter>',lambda x:hoverOn(botonBuscarVe))
    botonBuscarVe.bind('<Leave>',lambda x:hoverOff(botonBuscarVe))
    botonBuscar_a.bind('<Enter>',lambda x:hoverOn(botonBuscar_a))
    botonBuscar_a.bind('<Leave>',lambda x:hoverOff(botonBuscar_a))
    botonEliminarP.bind('<Enter>',lambda x:hoverOn(botonEliminarP))
    botonEliminarP.bind('<Leave>',lambda x:hoverOff(botonEliminarP))
    botonEliminarCl.bind('<Enter>',lambda x:hoverOn(botonEliminarCl))
    botonEliminarCl.bind('<Leave>',lambda x:hoverOff(botonEliminarCl))
    botonEliminarCo.bind('<Enter>',lambda x:hoverOn(botonEliminarCo))
    botonEliminarCo.bind('<Leave>',lambda x:hoverOff(botonEliminarCo))
    botonEliminarVe.bind('<Enter>',lambda x:hoverOn(botonEliminarVe))
    botonEliminarVe.bind('<Leave>',lambda x:hoverOff(botonEliminarVe))
    botonEliminar_a.bind('<Enter>',lambda x:hoverOn(botonEliminar_a))
    botonEliminar_a.bind('<Leave>',lambda x:hoverOff(botonEliminar_a))
    botonCrearP.bind('<Enter>',lambda x:hoverOn(botonCrearP))
    botonCrearP.bind('<Leave>',lambda x:hoverOff(botonCrearP))
    botonCrearCl.bind('<Enter>',lambda x:hoverOn(botonCrearCl))
    botonCrearCl.bind('<Leave>',lambda x:hoverOff(botonCrearCl))
    botonCrearCo.bind('<Enter>',lambda x:hoverOn(botonCrearCo))
    botonCrearCo.bind('<Leave>',lambda x:hoverOff(botonCrearCo))
    botonCrearVe.bind('<Enter>',lambda x:hoverOn(botonCrearVe))
    botonCrearVe.bind('<Leave>',lambda x:hoverOff(botonCrearVe))
    botonCrear_a.bind('<Enter>',lambda x:hoverOn(botonCrear_a))
    botonCrear_a.bind('<Leave>',lambda x:hoverOff(botonCrear_a))

    ###################################################################################
    ############################################################## MENU ###############

    menubar = Menu(ventana3)
    ventana3.config(menu=menubar)

    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Salir", command=ventana3.destroy)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="Ayuda",command=messageHelp)
    helpmenu.add_separator()
    helpmenu.add_command(label="Acerca de...",command=messageAbout)

    menubar.add_cascade(label="Archivo", menu=filemenu)
    menubar.add_cascade(label="Ayuda", menu=helpmenu)
    
    mainloop()


if __name__ == '__main__':
    app1 = App1()