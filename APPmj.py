# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 01:00:54 2019

@author: JEFF (Union)
"""
#--------------------------------------------------------LIBRARIES 
import os
from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from tkinter.messagebox import showerror, showinfo
from tkinter.scrolledtext import ScrolledText
import pymysql
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import time
from PIL import ImageTk, Image

import tkinter as tk
from pandas import DataFrame
import matplotlib.pyplot as plt

from datetime import datetime
from tkintertable import TableCanvas, TableModel

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import  threading
from time import sleep
import random 


#--------------------------------------------------GLOBAL VARIABLES 
copia = []
principal_data= dict()
data_list=[] # lista para bajr de BD y mostrar en interface 
lista_principal = []  #lista para guardar e introducir en BD
lista_company_data = [] #lista para guardar e introducir en BD
lista_puntos = []
lista_comentarios = []
empresa_obtenida =''
N_puntuadores = 0

PUNTO_A = 0
PUNTO_P  = 0
PUNTO_G = 0
PUNTO_S = 0
PUNTO_R = 0
PUNTO_Sup = 0 
PUNTO_C = 0
PUNTO_J  = 0
PUNTO_Pr = 0 
PUNTO_E2 = 0
PUNTO_D = 0
PUNTO_TOTAL = 0

#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CONEXION CON CLOVER CLOUD >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
BD_control = 1 # para hacer Break al threading


connection = pymysql.connect(
                host = 'bzg8txsasm4yllthbsic-mysql.services.clever-cloud.com', #ip si es remoto
                user = 'ur7rdgpabg2zcsau',
                password = 'Qpm83aqUEDEqF0nJXZYb',
                db = 'bzg8txsasm4yllthbsic'
            )
      
cursor = connection.cursor()
print('conexion estabablecidad exitosamente!')


def conexion_a_BD(t):
    while True:   
        
        connection = pymysql.connect(
                        host = 'bzg8txsasm4yllthbsic-mysql.services.clever-cloud.com', #ip si es remoto
                        user = 'ur7rdgpabg2zcsau',
                        password = 'Qpm83aqUEDEqF0nJXZYb',
                        db = 'bzg8txsasm4yllthbsic'
                    )
        
        cursor = connection.cursor()
        print('conexion estabablecidad exitosamente!')
        sleep(t)
        connection.close()
        print("Conexion cerrada")
        
        if BD_control ==0:
            break 
        
    
def Enviar_codigo_validacion():
        
        global COD_VALIDATION
        COD_VALIDATION = random.randint(1000,9999)
        
        msg = MIMEMultipart() 
        message = f"Este es su código de validación: {COD_VALIDATION} \n Será valido durante los próximos 10 minutos"
        # setup the parameters of the message
        password = "BasedeDatospro."
        msg['From'] = "basededatosmj@gmail.com"
        msg['To'] = entMail.get()
        msg['Subject'] = "CÓDIGO DE VALIDACIÓN"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        Comunica_con_variable('Se envió el código a su correo electrónico')
        
        
def Validar_codigo():
    
    if str(COD_VALIDATION) == entCod_validation.get():
        entCod_validation.delete(0,END)
        entCod_validation.insert(0,"Validación excitosa")
        global Bandera_codigo
        Bandera_codigo = 'True'
        print(Bandera_codigo)
        
    else:
        Comunica_con_variable('El código no es correcto, revise que sea el correcto o generelo nuevamente')
    
    

def insert_global_user():
    print(Bandera_codigo)
    if Bandera_codigo == 'True':
        try:
            sql = """INSERT INTO usuarios(tipo, nombre, ruc, e_mail, celular, pasword, verificado)VALUES('%s','%s','%s','%s','%s','%s','%s')"""\
                            %tuple([cboType.get(), entNombre.get(), entRuc.get(), entMail.get(), entContac.get(), entContra.get(),'NO VERIFICADO']);
                            
            cursor.execute(sql)
            connection.commit()  
            
            msg = MIMEMultipart() 
            message = f"El nuevo usuario se a registrado con el e-mail: {entMail.get()}"
            # setup the parameters of the message
            password = "BasedeDatospro."
            msg['From'] = "basededatosmj@gmail.com"
            msg['To'] = "basededatosmj@gmail.com"
            msg['Subject'] = "NUEVO REGISTRO"
            # add in the message body
            msg.attach(MIMEText(message, 'plain'))
            #create server
            server = smtplib.SMTP('smtp.gmail.com: 587')
            server.starttls()
            # Login Credentials for sending the mail
            server.login(msg['From'], password)
            # send the message via the server.
            server.sendmail(msg['From'], msg['To'], msg.as_string())
            server.quit()
            
            entNombre.delete(0,END)
            entRuc.delete(0,END)
            entMail.delete(0,END)
            entContac.delete(0,END)
            entContra.delete(0,END)
            
            Comunica_con_variable('Nuevo usuario creado con exito \n\n Su inicio de sesión será como invitado hasta que el administrador verifique sus datos.')
        except:
            
            Comunica_con_variable('Oh oh... Ocurrio algún error, verifique que sus datos sean correctos')
    else:
        Comunica_con_variable('No ha validado su correo electrónico')
            

def login_global_user():
    
    try:
        sql = "SELECT tipo, nombre, pasword, verificado FROM usuarios WHERE e_mail = '%s'"%entCorreo.get()
        cursor.execute(sql) 
        data_usuario = cursor.fetchall()[0]
       
        if data_usuario[2] == entPassword.get():
            global TYPE
            TYPE = data_usuario[0]
            global NAME
            NAME = data_usuario[1]
            global VERIFICADO
            VERIFICADO = data_usuario[3]
            global CORREO 
            CORREO = entCorreo.get()
            
            MAIN()
        else:
            Comunica_con_variable('El usuario o la contraseña no es correcto')
    except:        
        Comunica_con_variable('El usuario o la contraseña no es correcto')
            
    entCorreo.delete(0,END) 
    entPassword.delete(0,END)
    

def Solicita_premium():
    
    try:
        msg = MIMEMultipart() 
        message = f"El usuario {CORREO} solicita un cambio a PREMIUM"
        # setup the parameters of the message
        password = "BasedeDatospro."
        msg['From'] = "basededatosmj@gmail.com"
        msg['To'] = "basededatosmj@gmail.com"
        msg['Subject'] = "SOLICITUD DE CAMBIO A PREMIUM"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        Comunica_con_variable('Gracias por confiar en nosotros\n En breve el administrador se pondrá en contacto vía e-mail')
    except:
        Comunica_con_variable('Ocurrió algún error, se recomienda que vuelva a iniciar sesión')
        
    
        
def select_user():
    
        data_list.clear()
        sql = 'SELECT partida, empresa, puntuacion,number_puntuadores FROM principal ORDER BY puntuacion' # EN ESTA LINEA SE ESCRIBE EL CODIGO EN SQL
        
        cursor.execute(sql) # ESTA LINEA EJECUTA EL CODIGO EN SQL
        empresas = cursor.fetchall()
        empresas = list(empresas)
        descrip = ["PARTIDA","EMPRESA", "PUNTUACION","NUMERO_PUNTUADORES", "ESTADO"]
          
            
        for user in empresas:
                user = list(user)
                user.append("")
                principal_data= dict(zip(descrip, user))
                data_list.append(principal_data)
                

def  select_unic_user():
    
    global user_F
    user_F = []
    
    cursor.execute("SELECT * FROM principal WHERE empresa = '%s'"%empresa_obtenida)
    user = list(cursor.fetchall())
    user_F = list(user[0])
    

    
def insert_user():
        
        de_principal = """INSERT INTO principal(partida, empresa, puntuacion,number_puntuadores)VALUES('%s','%s','%s','%s')"""\
                        %tuple(lista_principal);
        
        de_company_data = """INSERT INTO company_data(razon_social, ruc, direccion,telefono, email, modalidad_contrato, gerente,\
                        carta_fianza,especializacion, number_of_personal, E1, E2, E3, E4, E5, servicio_1, servicio_2, servicio_3, servicio_4)\
                        VALUES('%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s','%s', '%s','%s','%s','%s','%s','%s','%s')"""\
                        %tuple(lista_company_data);
                                         
        de_puntos = """INSERT INTO puntos(razon_social, atencion, precios,garantias, seguridad, responsabilidad, supervision,\
                          cumplimiento, job_equipo, procedimiento, eficaz, documentacion)VALUES('%s','%s', '%s','%s','%s','%s',\
                          '%s','%s','%s','%s', '%s','%s')"""\
                          %tuple(lista_puntos);
                          
        #de_comentarios = """INSERT INTO usuarios(tipo, nombre, ruc, e_mail, celular, pasword)VALUES('ADMI','José','456','u201520244@upc.edu.pe','984794967','POWERadmin')"""

        cursor.execute(de_principal) 
        cursor.execute(de_company_data)
        cursor.execute(de_puntos)
        connection.commit()   
        
        
def  select_partidas():
    
    global Partidas
    Partidas = []
    
    sql = 'SELECT partida FROM partidas ORDER BY partida' 
        
    cursor.execute(sql) 
    Part = cursor.fetchall()
    
    for a in Part:
    
        Partidas = Partidas + list(a) 
        
def  select_comentarios():
    
    global coments_F
    global empresa_proyecto_F
    coments_F = []
    empresa_proyecto_F = []
    
    cursor.execute("SELECT * FROM comentarios WHERE empresa = '%s'"%empresa_obtenida)
    user = list(cursor.fetchall())
    coments_F = user
    
    for i in coments_F:
        temporal= list(i)
        empresa_proyecto_F.append(i[3])
        
        
       
def insert_partida():
    
    prev = []
    par = Partida_G.get()
    par = par.upper()
    prev = prev + [par]

    
    de_partida = """INSERT INTO partidas(partida)VALUES('%s')"""\
                        %tuple(prev);
                        
    cursor.execute(de_partida)
    connection.commit()  
    select_partidas()
    comboPartidas.config(values=Partidas)
    Guardado_con_exito()
    
    
def delete_partida():
    
    cursor.execute("""DELETE FROM partidas WHERE partida = '%s'"""%EntPartida_2.get())
    connection.commit()
    select_partidas()
    comboPartidas.config(values=Partidas)
    Guardado_con_exito()
    
    
    
    

# Hacemos la primera a select para capturar todos los usuarios desde la BD
select_user()
select_partidas()
select_comentarios()




def  select_puntos():
    
    global Puntitos_F
    Puntitos_F = []
    
    cursor.execute("SELECT * FROM puntos WHERE razon_social = '%s'"%empresa_obtenida)
    Puntitos = list(cursor.fetchall())
    Puntitos = list(Puntitos[0])
    
    for i in range(1,12):
        Puntitos_F.append(Puntitos[i])
        

def Select_Divine_Puntos():

    global OF_F
    global ST_F
    global PRO_F
    global CA_F
    global AD_F
    Divine_P_F = []
    OF_F = []
    ST_F = []
    PRO_F = []
    CA_F = []
    AD_F = []
        
    cursor.execute("SELECT * FROM Divine_puntos WHERE empresa_puntuada = '%s'"%empresa_obtenida)
    Divine_P_F = list(cursor.fetchall())
    tamm = len(Divine_P_F)
    
    for i in Divine_P_F:
        per = list(i)
        
        OF_F.append(per[3])
        ST_F.append(per[4])
        PRO_F.append(per[5])
        CA_F.append(per[6])
        AD_F.append(per[7])
        
    
    

def Guardado_con_exito():
    
    wixu = tkinter.Toplevel()
    wixu.geometry('300x100+100+100')
    wixu.configure(bg='white')
    
    
    #-------- widgets ----------------------------------------------------------------------
    lblTit_G = Label(wixu, text="GUARDADO EXITOSO...", font= "Helvetica 10 bold", fg='black', bg='white')
    #---------grid--------------------------------------------------------------------------
    lblTit_G.grid(row=1, column=1, padx=50, pady= 30)
    
    
def Comunica_con_variable(var):
    
    weon = tkinter.Toplevel()
    weon.iconbitmap(r'db.ico')
    weon.configure(bg='white')
    
    
    #-------- widgets ----------------------------------------------------------------------
    lblhj_G = Label(weon, text=var, font= "Helvetica 14 bold", fg='black', bg='white')
    #---------grid--------------------------------------------------------------------------
    lblhj_G.grid(row=1, column=1, padx=50, pady= 30)
    
    
        






#:::::::::::::::::::::::::::::::::::::: Funciones ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: 
  
    
def salir():
    yes = tkinter.messagebox.askyesno("Salir", "Desea salir?")
    if yes:
        root.destroy()
        
        
    
        
def Agregar_Empresa():
    
    win=tkinter.Toplevel()
    win.geometry('750x580+100+100')
    #win.configure(background='white')
    
    #-------- widgets ----------------------------------------------------------------------
    
    lblLaBusqueda = ttk.Label(win, text="Busca una empresa existente:", font= "12")
    global EntLoBuscado
    EntLoBuscado = ttk.Entry(win, width=95, textvariable=Empresa_existente)
    btnSerch = Button(win, text='Buscar', fg='white', bg='darkblue',width=10,command=Busca_empresa)
    lblGuiones = ttk.Label(win, text="--------------------------------------------------------------------------------------------------------------------------------------")
    EntLoBuscado.delete(0,END)
    EntLoBuscado.insert(0,empresa_obtenida)
    
    lblContacto = ttk.Label(win, text="Datos de contacto", font= "Helvetica 12 bold italic")
    lbldat11 = ttk.Label(win, text="                                    Razon Social:")
    lbldat12 = ttk.Label(win, text="                                            N° RUC:")
    lbldat13 = ttk.Label(win, text="                                        Direccion:")
    lbldat14 = ttk.Label(win, text="                                         Celular:")
    lbldat15 = ttk.Label(win, text="                                            E-mail:")
    lbldat16 = ttk.Label(win, text="               Modalidad de contrato:")
    lbldat17 = ttk.Label(win, text="               Gerente de la empresa:")
    global lbldat18c 
    lbldat18c = ttk.Entry(win, width=40, textvariable=Razon_S)
    global lbldat19c
    lbldat19c = ttk.Entry(win, width=15, textvariable=N_RUC)
    global lbldat110c 
    lbldat110c = ttk.Entry(win, width=40, textvariable=Direccion)
    global lbldat111c 
    lbldat111c = ttk.Entry(win, width=15, textvariable=Telefono)
    global lbldat112c 
    lbldat112c = ttk.Entry(win, width=40, textvariable=E_mail)
    global comboContrato 
    comboContrato = ttk.Combobox(win, width=30 ,values=['Preguntar'], textvariable=Mod_contrato)
    global lbldat114c 
    lbldat114c = ttk.Entry(win, width=30, textvariable=Gerente)
    
    lblnada = ttk.Label(win, text="")
    
    lblDatos = ttk.Label(win, text="Trabajos realizados", font= "Helvetica 12 bold italic")
    lbldat21 = ttk.Label(win, text="                     Tipo de carta fianza:")
    lbldat23 = ttk.Label(win, text="                                     Partida:")
    lbldat24 = ttk.Label(win, text="                     Servicios que brinda:")
    lbldat25 = ttk.Label(win, text=" Fecha de inicio de actividades:")
    lbldat26 = ttk.Label(win, text="                     Empresa/Proyecto:")
    global comboC_Fianza 
    comboC_Fianza = ttk.Combobox(win, width=30 ,values=['Si','No'], textvariable=Carta_fianza)
    comboPartidas = ttk.Combobox(win, width=60 ,values=Partidas, textvariable=destino_combo)
    global comboPartidas_2
    global comboPartidas_3
    global comboPartidas_4
    global comboPartidas_5
    destino_combo_2 = StringVar()
    destino_combo_3 = StringVar()
    destino_combo_4 = StringVar()
    destino_combo_5 = StringVar()
    comboPartidas_2 = Entry(win, width=60 , textvariable=destino_combo_2)
    comboPartidas_3 = Entry(win, width=60 , textvariable=destino_combo_3)
    comboPartidas_4 = Entry(win, width=60 , textvariable=destino_combo_4)
    comboPartidas_5 = Entry(win, width=60 , textvariable=destino_combo_5)
    btnAgregar_partida = Button(win, text="+", fg='white', bg='darkblue',width=5, command= Agregar_Partida)
    btnEliminar_partida = Button(win, text="X", fg='white', bg='red',width=5, command= Eliminar_Partida)
    #lbldat29 = ttk.Entry(win, width=30, textvariable=Especializacion) # se cambio por comboBOX
    global lbldat211c
    lbldat211c = ttk.Entry(win, width=25, textvariable=Personal)  
    global lbldat212c
    lbldat212c = ttk.Entry(win, width=30, textvariable=E1)
    global lbldat213c
    lbldat213c = ttk.Entry(win, width=30, textvariable=E2)
    global lbldat214c 
    lbldat214c = ttk.Entry(win, width=30, textvariable=E3)
    global lbldat215c 
    lbldat215c = ttk.Entry(win, width=30, textvariable=E4)
    global lbldat216c 
    lbldat216c = ttk.Entry(win, width=30, textvariable=E5)
    
    lblGuiones_2 = ttk.Label(win, text="--------------------------------------------------------------------------------------------------------------------------------------")
    
    btnGrabar = Button(win, text='GRABAR NUEVA EMPRESA', fg='white', bg='darkblue',command=Grabar_Empresa)
    btnRechange = Button(win, text='CAMBIAR DATOS', fg='white', bg='darkblue', command=Modificar_datos_company)
    
    
    #------- grid and pack ------------------------------------------------------------------
    lblLaBusqueda.grid(row=1, column=0, pady=5)
    EntLoBuscado.grid(row=2, column=0,columnspan=2, sticky = 'W' )
    btnSerch.grid(row=2, column=2, padx=1, sticky = 'W')
    lblGuiones.grid(row=3, column=0,columnspan=3 , padx=11, pady=10)
    
    lblContacto.grid(row=4, column=0, padx=10)

    lbldat11.grid(row=5, column=0, padx=1)
    lbldat12.grid(row=6, column=0, padx=1)
    lbldat13.grid(row=7, column=0, padx=1)
    lbldat14.grid(row=8, column=0, padx=1)
    lbldat15.grid(row=9, column=0, padx=1)
    
    lbldat17.grid(row=10, column=0, padx=1)
    lbldat18c.grid(row=5, column=1, sticky = W, padx=1, pady=5)
    lbldat19c.grid(row=6, column=1,  sticky = W, padx=1, pady=5)
    lbldat110c.grid(row=7, column=1,   sticky = W, padx=1, pady=5)
    lbldat111c.grid(row=8, column=1,   sticky = W, padx=1, pady=5)
    lbldat112c.grid(row=9, column=1,   sticky= W, padx=1, pady=5)
    lbldat114c.grid(row=10, column=1,   sticky= W, padx=1, pady=5)
    
    #lbldat16.grid(row=13, column=0, padx=1)
    #lbldat21.grid(row=14, column=0, padx=1)
    lbldat23.grid(row=15, column=0, padx=1)
    lbldat24.grid(row=16, column=0, padx=1)
    lbldat25.grid(row=20, column=0, padx=1)
    #lbldat26.grid(row=23, column=0, padx=1)
    #comboContrato.grid(row=13, column=1,   sticky= W, padx=1, pady=5)
    #comboC_Fianza.grid(row=14, sticky= W,column=1, padx=1, pady=5)
    comboPartidas.grid(row=15, sticky= W,column=1, padx=1, pady=5)
    comboPartidas_2.grid(row=16, sticky= W,column=1, padx=1, pady=5)
    comboPartidas_3.grid(row=17, sticky= W,column=1, padx=1, pady=5)
    comboPartidas_4.grid(row=18, sticky= W,column=1, padx=1, pady=5)
    comboPartidas_5.grid(row=19, sticky= W,column=1, padx=1, pady=5)
    btnAgregar_partida.grid(row=15, column=2, padx =2, pady=5, sticky = 'W') 
    btnEliminar_partida.grid(row=15, column=3, padx =2, pady=5, sticky = 'W') 
    #lbldat29.grid(row=12, sticky= W,column=1, padx=1, pady=5) # se cambio por comboBOX
    lbldat211c.grid(row=20, sticky= W,column=1, padx=1, pady=5)
    
    
    
    #lblDatos.grid(row=22, column=0, padx=10, pady=15)
    #lbldat212c.grid(row=23, sticky= W,column=1, padx=1, pady=2)
    #lbldat213c.grid(row=24, sticky= W,column=1, padx=1, pady=2)
    #lbldat214c.grid(row=25, sticky= W,column=1, padx=1, pady=2)
    #lbldat215c.grid(row=26, sticky= W,column=1, padx=1, pady=2)
    #lbldat216c.grid(row=27, sticky= W,column=1, padx=1, pady=2)
    
    lblGuiones_2.grid(row=28, columnspan=3, pady=5, padx=1)
    
    btnGrabar.grid(row=29, column=0, pady=15, padx=1)
    btnRechange.grid(row=29, column=1, pady=15, padx=1, sticky=E)
    
    #-------------------
    lbldat18c.delete(0, END)
    lbldat19c.delete(0, END)
    lbldat110c.delete(0, END)
    lbldat111c.delete(0, END)
    lbldat112c.delete(0, END)
    lbldat114c.delete(0, END)
    
    lbldat211c.delete(0, END)
    lbldat212c.delete(0, END)
    lbldat213c.delete(0, END)
    lbldat214c.delete(0, END)
    lbldat215c.delete(0, END)
    lbldat216c.delete(0, END)
    
    comboPartidas_2.delete(0, END)
    comboPartidas_3.delete(0, END)
    comboPartidas_4.delete(0, END)
    comboPartidas_5.delete(0, END)
    
    lbldat111c.delete(0,END)
    lbldat112c.delete(0,END)
    lbldat211c.delete(0,END)
    lbldat111c.insert(0, 'cel1/cel2')
    lbldat112c.insert(0, 'mail1/mail2')
    lbldat211c.insert(0, 'dd/mm/aaaa')
        
    
def Busca_empresa():
    
    
    cursor.execute("SELECT * FROM company_data WHERE razon_social = '%s'"%EntLoBuscado.get())
    data = list(cursor.fetchall())
    data = list(data[0])
    
    lbldat18c.delete(0, END)
    lbldat19c.delete(0, END)
    lbldat110c.delete(0, END)
    lbldat111c.delete(0, END)
    lbldat112c.delete(0, END)
    lbldat114c.delete(0, END)
    
    lbldat211c.delete(0, END)
    lbldat212c.delete(0, END)
    lbldat213c.delete(0, END)
    lbldat214c.delete(0, END)
    lbldat215c.delete(0, END)
    lbldat216c.delete(0, END)
    
    comboPartidas_2.delete(0, END)
    comboPartidas_3.delete(0, END)
    comboPartidas_4.delete(0, END)
    comboPartidas_5.delete(0, END)
    
    lbldat18c.insert(0,data[0])
    lbldat19c.insert(0,data[1])
    lbldat110c.insert(0,data[2])
    lbldat111c.insert(0,data[3])
    lbldat112c.insert(0,data[4])
    comboContrato.set(data[5])
    lbldat114c.insert(0,data[6])
    
    comboC_Fianza.set(data[7])
    comboPartidas.set(data[8])
    lbldat211c.insert(0,data[9])     
    lbldat212c.insert(0,data[10])
    lbldat213c.insert(0,data[11])
    lbldat214c.insert(0,data[12])
    lbldat215c.insert(0,data[13])
    lbldat216c.insert(0,data[14])
    comboPartidas_2.insert(0,data[15])
    comboPartidas_3.insert(0,data[16])
    comboPartidas_4.insert(0,data[17])
    comboPartidas_5.insert(0,data[18])

    
    
    
    data = []
    
    
def Grabar_Empresa():
    
    global lista_principal
    global lista_company_data
    global lista_puntos
    global lista_comentarios
    
    lista_company_data.clear()
    lista_principal.clear()
    lista_puntos.clear()
    lista_comentarios.clear()
    
    
    
    #simepre que no se encuentre una empresa con el mismo nombre usss sera 0    


        #lista principal
    lista_principal = lista_principal + [comboPartidas.get(), Razon_S.get(), 0, 0]
        
        # lista company_data
        
    lista_company_data = lista_company_data + [Razon_S.get(), N_RUC.get(), Direccion.get(), Telefono.get(), E_mail.get(),\
                             comboContrato.get(), Gerente.get(),comboC_Fianza.get(),\
                             comboPartidas.get(), Personal.get(), E1.get(),E2.get(),E3.get(),E4.get(), E5.get(),comboPartidas_2.get()\
                             ,comboPartidas_3.get(), comboPartidas_4.get(), comboPartidas_5.get()]
        
        #lista puntos                  
    lista_puntos = lista_puntos + [Razon_S.get(),float(PUNTO_A), float(PUNTO_P), float(PUNTO_G), float(PUNTO_S), float(PUNTO_R),\
                                    float(PUNTO_Sup), float(PUNTO_C), float(PUNTO_J), float(PUNTO_Pr), float(PUNTO_E2), float(PUNTO_D)]
        
    lista_comentarios = lista_comentarios + [Razon_S.get(), '']
        
        
    insert_user()
    select_user()
    Guardado_con_exito()
        
    #-----------------------------------reseteando Entrys
    lbldat18c.delete(first=0,last=END)
    lbldat19c.delete(first=0,last=END)
    lbldat110c.delete(first=0,last=END)
    lbldat111c.delete(first=0,last=END)
    lbldat112c.delete(first=0,last=END)
    #comboContrato.delete(first=0,last=END)
    lbldat114c.delete(first=0,last=END)
    comboPartidas_2.delete(first=0,last=END)
    comboPartidas_3.delete(first=0,last=END)
    comboPartidas_4.delete(first=0,last=END)
    comboPartidas_5.delete(first=0,last=END)        
    #comboC_Fianza.delete(first=0,last=END)
    comboPartidas.delete(first=0,last=END)
    lbldat211c.delete(first=0,last=END) 
    lbldat212c.delete(first=0,last=END)
    lbldat213c.delete(first=0,last=END)
    lbldat214c.delete(first=0,last=END)
    lbldat215c.delete(first=0,last=END)
    lbldat216c.delete(first=0,last=END)
        

    #servicio_5

def Cambiando_Datos():
    
    
        cursor.execute("""SELECT * FROM company_data WHERE Razon_social = '%s'"""\
                       %Razon_S.get())
        data = list(cursor.fetchall())
        
        #---------para probar que la empresa exista --------------
        if len(data)==0:
            data = data +[0,0]
            
        else:    
            data = list(data[0])
        #---------------------------------------------------------
                
        if data[0] == Razon_S.get():
            
            
            cursor.execute("UPDATE company_data SET  ruc= %s WHERE  razon_social= %s", (N_RUC.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  direccion= %s WHERE  razon_social= %s", (Direccion.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  telefono= %s WHERE  razon_social= %s", (Telefono.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  email= %s WHERE  razon_social= %s", (E_mail.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  modalidad_contrato= %s WHERE  razon_social= %s", (comboContrato.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  gerente= %s WHERE  razon_social= %s", (Gerente.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  carta_fianza= %s WHERE  razon_social= %s", (comboC_Fianza.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  especializacion= %s WHERE  razon_social= %s", (comboPartidas.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  number_of_personal= %s WHERE  razon_social= %s", (Personal.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  E1= %s WHERE  razon_social= %s", (E1.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  E2= %s WHERE  razon_social= %s", (E2.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  E3= %s WHERE  razon_social= %s", (E3.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  E4= %s WHERE  razon_social= %s", (E4.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  E5= %s WHERE  razon_social= %s", (E5.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  servicio_1= %s WHERE  razon_social= %s", (comboPartidas_2.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  servicio_2= %s WHERE  razon_social= %s", (comboPartidas_3.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  servicio_3= %s WHERE  razon_social= %s", (comboPartidas_4.get(), EntLoBuscado.get()))
            cursor.execute("UPDATE company_data SET  servicio_4= %s WHERE  razon_social= %s", (comboPartidas_5.get(), EntLoBuscado.get()))
            
            cursor.execute("UPDATE principal SET  partida= %s WHERE  empresa= %s", (comboPartidas.get(), EntLoBuscado.get()))
            
            connection.commit() 
            Guardado_con_exito()
            #-----------------------------------reseteando Entrys
            lbldat18c.delete(first=0,last=END)
            lbldat19c.delete(first=0,last=END)
            lbldat110c.delete(first=0,last=END)
            lbldat111c.delete(first=0,last=END)
            lbldat112c.delete(first=0,last=END)
            comboContrato.delete(first=0,last=END)
            lbldat114c.delete(first=0,last=END)
            
            comboC_Fianza.delete(first=0,last=END)
            comboPartidas.delete(first=0,last=END)
            lbldat211c.delete(first=0,last=END) 
            lbldat212c.delete(first=0,last=END)
            lbldat213c.delete(first=0,last=END)
            lbldat214c.delete(first=0,last=END)
            lbldat215c.delete(first=0,last=END)
            lbldat216c.delete(first=0,last=END)
            comboPartidas_2.delete(first=0,last=END)
            comboPartidas_3.delete(first=0,last=END)
            comboPartidas_4.delete(first=0,last=END)
            comboPartidas_5.delete(first=0,last=END)
            
            
        else:
            
            Comunica_con_variable('LA EMPRESA NO EXISTE')

        
        #cursor.execute("UPDATE tabla SET peso = ? WHERE id = ?", (0, 1))
        #connection.commit() 
        data =[]

        

def evaluar_estado():
    cont=0
    copia.reverse()
    
    for i in copia: # Bueno de 4<puntuacion, Medio 4=<puntuacion<=2.5, Malo puntuacion>2.5   
           
        if copia[cont]["PUNTUACION"]>4:
           copia[cont]["ESTADO"]="MUY BUENO"
           
        elif copia[cont]["PUNTUACION"]<=4 and copia[cont]["PUNTUACION"]>3:
           copia[cont]["ESTADO"]="BUENO"
           
        elif copia[cont]["PUNTUACION"]<=3 and copia[cont]["PUNTUACION"]>2:
           copia[cont]["ESTADO"]="REGULAR"
            
        elif copia[cont]["PUNTUACION"]<=2 and copia[cont]["PUNTUACION"]>0:
           copia[cont]["ESTADO"]="MALO"
           
        elif copia[cont]["PUNTUACION"] == 0:
           copia[cont]["ESTADO"]=""
        
        cont+=1

def evaluar_partida(event):
    
    select_user()
    cont=0
    
    for j in data_list:
        
        if data_list[cont]["PARTIDA"] == comboPartidas.get():
            
            copia.append(j)
            
        cont+=1
        
    tabla.delete(*tabla.get_children())
   
    evaluar_estado()
    
    for reg in copia:
        
         tabla.insert('', 'end', text=reg['EMPRESA'],
                         values= [reg['ESTADO'],reg['NUMERO_PUNTUADORES'] ,'%.2f'%reg['PUNTUACION'] ])
         
    copia.clear()
       
    
def insertar(event):
    
    global N_puntuadores 
    #tabla.delete(*tabla.get_children())
    evaluar_estado()
    for reg in data_list: #inserta datos a tabla

        tabla.insert('', 'end', text=reg['EMPRESA'],
                         values= [reg['ESTADO'],reg['NUMERO_PUNTUADORES'] ,reg['PUNTUACION'] ])
         
def cambiar_datos(event):
    
    text_area_descrip.delete(1.0,END)
    empresa_proyecto.set('Seleccionar Proyecto')
    
    row = tabla.focus()
    a = tabla.item(row)
    
    global empresa_obtenida 
    empresa_obtenida = a['text']
    
    cursor.execute("""SELECT * FROM company_data WHERE Razon_social = '%s'"""\
                   %empresa_obtenida)
    data = list(cursor.fetchall())
    data = list(data[0])
    
    
    lbldat18.config(text=data[0])
    lbldat19.config(text=data[1])
    lbldat110.config(text=data[2])
    lbldat111.config(text=data[3])
    lbldat112.config(text=data[4])
    lbldat113.config(text=data[5])
    lbldat114.config(text=data[6])
    lbldat27.config(text=data[7])
    lbldat29.config(text=data[8])

    if data[9]==0:
        lbldat211.config(text='')
    else:
        lbldat211.config(text=data[9])
    
    
    lblService_1.config(text=data[15])
    lblService_2.config(text=data[16])
    lblService_3.config(text=data[17])
    lblService_4.config(text=data[18])
    
    select_comentarios()
    comboProyecto_Servicio.config(values = empresa_proyecto_F)
    
    
def write_description(event):
    
    cursor.execute("SELECT * FROM comentarios WHERE empresa_proyecto = '%s'"%empresa_proyecto.get())
    user = list(cursor.fetchall())
    user = list(user[0])
    user = user[2]
    text_area_descrip.delete(1.0,END)
    text_area_descrip.insert(1.0, user)
    
    
    

def PUNTUAR():
    
    wiu = tkinter.Toplevel()
    wiu.geometry('1300x700+100+100')
    wiu.resizable(1,1)
    wiu.config(bg='white')
    
    frm_wiu_L = Frame(wiu, bg='white')
    frm_wiu_R2 = Frame(wiu, bg='white')
    frm_wiu_R = Frame(wiu, bg='white')
    
    frm_wiu_L.pack(side=LEFT)
    frm_wiu_R2.pack(side=LEFT)
    frm_wiu_R.pack(side=LEFT)

    #my_por2 = ImageTk.PhotoImage(Image.open("por6.png"))
    #my_p2 = Label(frm_wiu_R2,image=my_por2)
    #my_p2.grid(row=1,column=1)
    
    #------------------------ leyenda ---------------------------------------------
    
    leyenda_1 = Label(frm_wiu_L, font= 'Arial 10 bold',text='OFICINA TÉCNICA', fg='white', bg= '#2F88DB', width=15)
    leyenda_2 = Label(frm_wiu_L, font= 'Arial 10 bold',text='SSOMA', fg='white', bg= '#F2D200', width=15)
    leyenda_3 = Label(frm_wiu_L, font= 'Arial 10 bold',text='PRODUCCIÓN', fg='white', bg= '#30D9A6', width=15)
    leyenda_4 = Label(frm_wiu_L, font= 'Arial 10 bold',text='CALIDAD', fg='white', bg= '#EB4841', width=15)
    leyenda_5 = Label(frm_wiu_L, font= 'Arial 10 bold',text='ADMINISTRACIÓN', fg='white', bg= '#913AC7', width=15)
    
    leyenda_1.grid(row= 3, column= 7, padx=5)
    leyenda_2.grid(row= 6, column= 7, padx=5)
    leyenda_3.grid(row= 8, column= 7, padx=5)
    leyenda_4.grid(row= 11, column= 7, padx=5)
    leyenda_5.grid(row= 14, column= 7, padx=5)
    
    
    #-------- widgets ----------------------------------------------------------------------
    lblTit = Label(frm_wiu_L, text="CALIFICAR EMPRESA", font= "Arial 14 bold", fg='white', bg='darkgrey', width=35)
    
    lblEmpty = Label(frm_wiu_L, text='  ', fg='white', bg='white')
    
    lblAtencion = Label(frm_wiu_L, text='1.NIVEL DE ATENCIÓN: ', bg='white')
    lblPrecios = Label(frm_wiu_L, text='2.PRECIOS EN EL MERCADO: ', bg='white')
    lblGarantias = Label(frm_wiu_L, text='3.ENTREGA DE VALORIZACIONES Y GARANTÍAS: ', bg='white')
    lblSeguridad = Label(frm_wiu_L, text='4.CUMPLIMIENTO DE SEGURIDAD: ', bg='white')
    lblResponsabilidad = Label(frm_wiu_L, text='5.RESPONSABILIDAD AMBIENTAL Y CONDUCTA: ', bg='white')
    lblSupervision = Label(frm_wiu_L, text='6.SUPERVISIÓN EN OBRA: ', bg='white')
    lblCumplimiento = Label(frm_wiu_L, text='7.CUMPLIMIENTO DE LA PROGRAMACIÓN : ', bg='white')
    lblJob_equipo = Label(frm_wiu_L, text='8.TRABAJO EN EQUIPO: ', bg='white')
    lblProcedimiento = Label(frm_wiu_L, text='9.GESTIÓN DE CALIDAD: ', bg='white')
    lblEficaz_1 = Label(frm_wiu_L, text='10.ES EFICAZ EN SUS PROCEDIMIENTOS Y BRINDA', bg='white')
    lblEficaz_2 = Label(frm_wiu_L, text='SOLUCIONES EFECTIVAS A SUS OBSERVACIONES: ', bg='white')
    lblDocumentacion = Label(frm_wiu_L, text='10.ENTREGA DE DOCUMENTACIÓN: ', bg='white')
    
    var1 = IntVar()
    var2 = IntVar()
    var3 = IntVar()
    var4 = IntVar()
    var5 = IntVar()
    var6 = IntVar()
    var7 = IntVar()
    var8 = IntVar()
    var9 = IntVar()
    var10 = IntVar()
    var11 = IntVar()
    cont_pun_combo = StringVar()
    cont_pun_combo.set('Seleccione modalidad de contrato')
    fia_pun_combo = StringVar()
    fia_pun_combo.set('Cuenta con Carta Fianza?')
    pago_pun_combo = StringVar()
    pago_pun_combo.set("Selecione forma de pago")

    #botones
    btnA_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var1, command= PP_A_1) 
    btnA_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var1, command= PP_A_2)
    btnA_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var1, command= PP_A_3)
    btnA_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var1, command= PP_A_4)
    btnA_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var1, command= PP_A_5)
    
    btnP_1 = Radiobutton(frm_wiu_L, text='1',width=5,value=1, variable=var2, command= PP_P_1)
    btnP_2 = Radiobutton(frm_wiu_L, text='2',width=5,value=2, variable=var2, command= PP_P_2)
    btnP_3 = Radiobutton(frm_wiu_L, text='3',width=5,value=3, variable=var2, command= PP_P_3)
    btnP_4 = Radiobutton(frm_wiu_L, text='4',width=5,value=4, variable=var2, command= PP_P_4)
    btnP_5 = Radiobutton(frm_wiu_L, text='5',width=5,value=5, variable=var2, command= PP_P_5)
    
    btnG_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var3, command= PP_G_1)
    btnG_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var3, command= PP_G_2)
    btnG_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var3, command= PP_G_3)
    btnG_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var3, command= PP_G_4)
    btnG_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var3, command= PP_G_5)
    
    btnS_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var4, command= PP_S_1)
    btnS_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var4, command= PP_S_2)
    btnS_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var4, command= PP_S_3)
    btnS_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var4, command= PP_S_4)
    btnS_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var4, command= PP_S_5)
    
    btnR_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var5, command= PP_R_1)
    btnR_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var5, command= PP_R_2)
    btnR_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var5, command= PP_R_3)
    btnR_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var5, command= PP_R_4)
    btnR_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var5, command= PP_R_5)
    
    btnSup_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var6, command= PP_Sup_1)
    btnSup_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var6, command= PP_Sup_2)
    btnSup_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var6, command= PP_Sup_3)
    btnSup_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var6, command= PP_Sup_4)
    btnSup_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var6, command= PP_Sup_5)
    
    btnC_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var7, command= PP_C_1)
    btnC_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var7, command= PP_C_2)
    btnC_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var7, command= PP_C_3)
    btnC_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var7, command= PP_C_4)
    btnC_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var7, command= PP_C_5)
    
    btnJ_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var8, command= PP_J_1)
    btnJ_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var8, command= PP_J_2)
    btnJ_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var8, command= PP_J_3)
    btnJ_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var8, command= PP_J_4)
    btnJ_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var8, command= PP_J_5)
    
    btnPr_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var9, command= PP_Pr_1)
    btnPr_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var9, command= PP_Pr_2)
    btnPr_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var9, command= PP_Pr_3)
    btnPr_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var9, command= PP_Pr_4)
    btnPr_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var9, command= PP_Pr_5)    
    
    btnE2_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var10, command= PP_E2_1)
    btnE2_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var10, command= PP_E2_2)
    btnE2_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var10, command= PP_E2_3)
    btnE2_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var10, command= PP_E2_4)
    btnE2_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var10, command= PP_E2_5)
    
    btnD_1 = Radiobutton(frm_wiu_L, text='1',width=5, value=1,variable=var11, command= PP_D_1)
    btnD_2 = Radiobutton(frm_wiu_L, text='2',width=5, value=2,variable=var11, command= PP_D_2)
    btnD_3 = Radiobutton(frm_wiu_L, text='3',width=5, value=3,variable=var11, command= PP_D_3)
    btnD_4 = Radiobutton(frm_wiu_L, text='4',width=5, value=4,variable=var11, command= PP_D_4)
    btnD_5 = Radiobutton(frm_wiu_L, text='5',width=5, value=5,variable=var11, command= PP_D_5)
    
    btn_GUARDAR = Button(frm_wiu_R, text='GUARDAR', font='Arial 12 bold', fg='darkblue', bg='white', width=20, command=Guardar_punto)    
    
    
    #------- grid and pack ------------------------------------------------------------------
    lblTit.grid(row=1, columnspan=6, padx=1, sticky=E)
    lblEmpty.grid(row=2, column=0, padx=1, pady=3)
    
    lblAtencion.grid(row=3, column=0, padx=1, pady=8, sticky = E)
    lblPrecios.grid(row=4, column=0, padx=1, pady=8, sticky = E)
    lblGarantias.grid(row=5, column=0, padx=1, pady=8, sticky = E)
    lblSeguridad.grid(row=6, column=0, padx=1, pady=8, sticky = E)
    lblResponsabilidad.grid(row=7, column=0, padx=1, pady=8, sticky = E)
    lblSupervision.grid(row=8, column=0, padx=1, pady=8, sticky = E)
    lblCumplimiento.grid(row=9, column=0, padx=1, pady=8, sticky = E)
    lblJob_equipo.grid(row=10, column=0, padx=1, pady=8, sticky = E)
    lblProcedimiento.grid(row=11, column=0, padx=1, pady=20, sticky = E)
    #lblEficaz_1.grid(row=12, column=0, padx=1, pady=0, sticky = E)
    #lblEficaz_2.grid(row=13, column=0, padx=1, pady=0, sticky = E)
    lblDocumentacion.grid(row=14, column=0, padx=1, pady=12, sticky = E)
    
    #botones
    btnA_1.grid(row=3, column=1, padx=1, pady=12, sticky = E)
    btnA_2.grid(row=3, column=2, padx=1, pady=12, sticky = E)
    btnA_3.grid(row=3, column=3, padx=1, pady=12, sticky = E)
    btnA_4.grid(row=3, column=4, padx=1, pady=12, sticky = E)
    btnA_5.grid(row=3, column=5, padx=1, pady=12, sticky = E)
    
    btnP_1.grid(row=4, column=1, padx=1, pady=12, sticky = E)
    btnP_2.grid(row=4, column=2, padx=1, pady=12, sticky = E)
    btnP_3.grid(row=4, column=3, padx=1, pady=12, sticky = E)
    btnP_4.grid(row=4, column=4, padx=1, pady=12, sticky = E)
    btnP_5.grid(row=4, column=5, padx=1, pady=12, sticky = E)
    
    btnG_1.grid(row=5, column=1, padx=1, pady=12, sticky = E)
    btnG_2.grid(row=5, column=2, padx=1, pady=12, sticky = E)
    btnG_3.grid(row=5, column=3, padx=1, pady=12, sticky = E)
    btnG_4.grid(row=5, column=4, padx=1, pady=12, sticky = E)
    btnG_5.grid(row=5, column=5, padx=1, pady=12, sticky = E)
    
    btnS_1.grid(row=6, column=1, padx=1, pady=12, sticky = E)
    btnS_2.grid(row=6, column=2, padx=1, pady=12, sticky = E)
    btnS_3.grid(row=6, column=3, padx=1, pady=12, sticky = E)
    btnS_4.grid(row=6, column=4, padx=1, pady=12, sticky = E)
    btnS_5.grid(row=6, column=5, padx=1, pady=12, sticky = E)
    
    btnR_1.grid(row=7, column=1, padx=1, pady=12, sticky = E)
    btnR_2.grid(row=7, column=2, padx=1, pady=12, sticky = E)
    btnR_3.grid(row=7, column=3, padx=1, pady=12, sticky = E)
    btnR_4.grid(row=7, column=4, padx=1, pady=12, sticky = E)
    btnR_5.grid(row=7, column=5, padx=1, pady=12, sticky = E)
    
    btnSup_1.grid(row=8, column=1, padx=1, pady=12, sticky = E)
    btnSup_2.grid(row=8, column=2, padx=1, pady=12, sticky = E)
    btnSup_3.grid(row=8, column=3, padx=1, pady=12, sticky = E)
    btnSup_4.grid(row=8, column=4, padx=1, pady=12, sticky = E)
    btnSup_5.grid(row=8, column=5, padx=1, pady=12, sticky = E)
    
    btnC_1.grid(row=9, column=1, padx=1, pady=12, sticky = E)
    btnC_2.grid(row=9, column=2, padx=1, pady=12, sticky = E)
    btnC_3.grid(row=9, column=3, padx=1, pady=12, sticky = E)
    btnC_4.grid(row=9, column=4, padx=1, pady=12, sticky = E)
    btnC_5.grid(row=9, column=5, padx=1, pady=12, sticky = E)
    
    btnJ_1.grid(row=10, column=1, padx=1, pady=12, sticky = E)
    btnJ_2.grid(row=10, column=2, padx=1, pady=12, sticky = E)
    btnJ_3.grid(row=10, column=3, padx=1, pady=12, sticky = E)
    btnJ_4.grid(row=10, column=4, padx=1, pady=12, sticky = E)
    btnJ_5.grid(row=10, column=5, padx=1, pady=12, sticky = E)
    
    btnPr_1.grid(row=11, column=1, padx=1, pady=12, sticky = E)
    btnPr_2.grid(row=11, column=2, padx=1, pady=12, sticky = E)
    btnPr_3.grid(row=11, column=3, padx=1, pady=12, sticky = E)
    btnPr_4.grid(row=11, column=4, padx=1, pady=12, sticky = E)
    btnPr_5.grid(row=11, column=5, padx=1, pady=12, sticky = E)
    
    #btnE2_1.grid(row=13, column=1, padx=1, pady=12, sticky = E)
    #btnE2_2.grid(row=13, column=2, padx=1, pady=12, sticky = E)
    #btnE2_3.grid(row=13, column=3, padx=1, pady=12, sticky = E)
    #btnE2_4.grid(row=13, column=4, padx=1, pady=12, sticky = E)
    #btnE2_5.grid(row=13, column=5, padx=1, pady=12, sticky = E)
    
    btnD_1.grid(row=14, column=1, padx=1, pady=12, sticky = E)
    btnD_2.grid(row=14, column=2, padx=1, pady=12, sticky = E)
    btnD_3.grid(row=14, column=3, padx=1, pady=12, sticky = E)
    btnD_4.grid(row=14, column=4, padx=1, pady=12, sticky = E)
    btnD_5.grid(row=14, column=5, padx=1, pady=12, sticky = E)
    
    btn_GUARDAR.grid(row=18,column=7,columnspan=6, padx=1, pady=10)
    
    
    #----------------- FRAME DERECHO 
    
    # Nombre de proyecto 
    global Ent_Company
    Ent_Company = Entry(frm_wiu_R, width=70, textvariable=La_Company_comenta)
    Ent_Company.grid(row=1, column=7, padx=5, pady=10)
    Ent_Company.delete(0, END)
    Ent_Company.insert(0, "Escriba aquí el nombre del proyecto...")
    
    # Descripcion de proyecto 
    global text_area3
    text_area3 = ScrolledText(frm_wiu_R, width=45, height=7)
    text_area3.grid(row=2, column=7, padx=60)
    
    text_area3.insert(1.0, 'Área construida:\n')
    text_area3.insert(1.0, 'Área del terreno:\n')
    text_area3.insert(1.0, 'N° de sótanos:\n')
    text_area3.insert(1.0, 'N° de pisos:\n')
    text_area3.insert(1.0, 'Ubicación:\n')
    text_area3.insert(1.0, '       .................................\n')
    text_area3.insert(1.0, '           Descripción del proyecto\n')
    
    
    # Combos: Tipo de pago, Tipo contarto, Tipo carta fianza 
    global Ent_Pago
    Ent_Pago = ttk.Combobox(frm_wiu_R, width=40 ,values=['Semanal','Quincenal','Mensual'], textvariable=pago_pun_combo)
    Ent_Pago.grid(row=4, column=7, padx=5, pady=10)
    global combo_conTr
    combo_conTr = ttk.Combobox(frm_wiu_R, width=40 ,values=['Suma alzada', 'Precio unitario'], textvariable=cont_pun_combo)
    combo_conTr.grid(row=5, column=7, padx=5, pady=10)
    global combo_Fianza
    combo_Fianza = ttk.Combobox(frm_wiu_R, width=40 ,values=['Si','No'], textvariable=fia_pun_combo)
    combo_Fianza.grid(row=6, column=7, padx=5, pady=10)
    
    cont_pun_combo.set('Seleccione modalidad de contrato')
    fia_pun_combo.set('Cuenta con Carta Fianza?')
    pago_pun_combo.set("Selecione forma de pago")
    
    
    # comentarios 
    lblcCOMENTA = Label(frm_wiu_R, text='AGREGUE UN COMENTARIO')
    lblcCOMENTA.grid(row=7, column=7, padx=5)
    
    global text_area
    text_area = ScrolledText(frm_wiu_R, width=45, height=8)
    text_area.grid(row=8, column=7, padx=60)
    
    
    # cuadro prrecios unitarios 
    btnUnitarios = Button(frm_wiu_R, fg='white',bg='darkgrey' ,text= 'INGRESAR PRECIOS UNITARIOS', command=cuadro)
    btnUnitarios.grid(row=9, column=7, padx=60, pady= 20)
    
    # Iniciando variables 
    PUNTO_A = 0
    PUNTO_P  = 0
    PUNTO_G = 0
    PUNTO_S = 0
    PUNTO_R = 0
    PUNTO_Sup = 0 
    PUNTO_C = 0
    PUNTO_J  = 0
    PUNTO_Pr = 0 
    PUNTO_E2 = 0
    PUNTO_D = 0
    PUNTO_TOTAL = 0
    PUNTO_TOTAL_prev = 0
    
    #---------------------------------------------------------------------------
    
    select_unic_user()
    select_puntos()
    
    
def cuadro():
    
    global cua 
    cua = tkinter.Toplevel()
    cua.resizable(1,1)
    cua.config(bg='white')
    
    global model 
    global tablo
     
    
    tframe = Frame(cua)
    tframe.grid(row=9, column=7, padx=5, pady= 10)
   
    data = {0:{'DESCRIPCIÓN': '', 'UNIDAD': '', 'PRECIO[S/.]': ''}}
    model  =  TableModel ()
    tablo = TableCanvas(tframe,  model = model, cellwidth=200, data= data)
    tablo.show()

    #-------------------------- Bind ---------------------------------
    cua.protocol("WM_DELETE_WINDOW", save_price_values)
    cua.bind('<Return>', pre_send)
    global t_row
    t_row = 0
        

    
    
def pre_send( handle):
    
    global t_row
    t_row += 1
    tablo.addRow(t_row)
    
def save_price_values():
    global datat 
    datat = tablo.model.getAllCells()
    cua.destroy()
    
  
     

#-----------------  DEFINICON DE PUNTOS --------------------------------------
def PP_A_1():
    global PUNTO_A 
    PUNTO_A = (1+(Puntitos_F[0]*user_F[3]))/(user_F[3]+1)
def PP_A_2():
    global PUNTO_A 
    PUNTO_A = (2+(Puntitos_F[0]*user_F[3]))/(user_F[3]+1)
def PP_A_3():
    global PUNTO_A 
    PUNTO_A = (3+(Puntitos_F[0]*user_F[3]))/(user_F[3]+1)
def PP_A_4():
    global PUNTO_A 
    PUNTO_A = (4+(Puntitos_F[0]*user_F[3]))/(user_F[3]+1)
def PP_A_5():
    global PUNTO_A 
    PUNTO_A = (5+(Puntitos_F[0]*user_F[3]))/(user_F[3]+1)
    
    
def PP_P_1():
    global PUNTO_P
    PUNTO_P = (1+(Puntitos_F[1]*user_F[3]))/(user_F[3]+1)
def PP_P_2():
    global PUNTO_P
    PUNTO_P = (2+(Puntitos_F[1]*user_F[3]))/(user_F[3]+1)
def PP_P_3():
    global PUNTO_P
    PUNTO_P = (3+(Puntitos_F[1]*user_F[3]))/(user_F[3]+1)
def PP_P_4():
    global PUNTO_P
    PUNTO_P = (4+(Puntitos_F[1]*user_F[3]))/(user_F[3]+1)
def PP_P_5():
    global PUNTO_P
    PUNTO_P = (5+(Puntitos_F[1]*user_F[3]))/(user_F[3]+1)

def PP_G_1():
    global PUNTO_G
    PUNTO_G = (1+(Puntitos_F[2]*user_F[3]))/(user_F[3]+1)
def PP_G_2():
    global PUNTO_G
    PUNTO_G = (2+(Puntitos_F[2]*user_F[3]))/(user_F[3]+1)
def PP_G_3():
    global PUNTO_G
    PUNTO_G = (3+(Puntitos_F[2]*user_F[3]))/(user_F[3]+1)
def PP_G_4():
    global PUNTO_G
    PUNTO_G = (4+(Puntitos_F[2]*user_F[3]))/(user_F[3]+1)
def PP_G_5():
    global PUNTO_G
    PUNTO_G = (5+(Puntitos_F[2]*user_F[3]))/(user_F[3]+1)
    
def PP_S_1():
    global PUNTO_S
    PUNTO_S = (1+(Puntitos_F[3]*user_F[3]))/(user_F[3]+1)
def PP_S_2():
    global PUNTO_S
    PUNTO_S = (2+(Puntitos_F[3]*user_F[3]))/(user_F[3]+1)
def PP_S_3():
    global PUNTO_S
    PUNTO_S = (3+(Puntitos_F[3]*user_F[3]))/(user_F[3]+1)
def PP_S_4():
    global PUNTO_S
    PUNTO_S = (4+(Puntitos_F[3]*user_F[3]))/(user_F[3]+1)
def PP_S_5():
    global PUNTO_S
    PUNTO_S = (5+(Puntitos_F[3]*user_F[3]))/(user_F[3]+1)
    
def PP_R_1():
    global PUNTO_R
    PUNTO_R = (1+(Puntitos_F[4]*user_F[3]))/(user_F[3]+1)
def PP_R_2():
    global PUNTO_R
    PUNTO_R = (2+(Puntitos_F[4]*user_F[3]))/(user_F[3]+1)
def PP_R_3():
    global PUNTO_R
    PUNTO_R = (3+(Puntitos_F[4]*user_F[3]))/(user_F[3]+1)
def PP_R_4():
    global PUNTO_R
    PUNTO_R = (4+(Puntitos_F[4]*user_F[3]))/(user_F[3]+1)
def PP_R_5():
    global PUNTO_R
    PUNTO_R = (5+(Puntitos_F[4]*user_F[3]))/(user_F[3]+1)
    
def PP_Sup_1():
    global PUNTO_Sup
    PUNTO_Sup = (1+(Puntitos_F[5]*user_F[3]))/(user_F[3]+1)
def PP_Sup_2():
    global PUNTO_Sup
    PUNTO_Sup = (2+(Puntitos_F[5]*user_F[3]))/(user_F[3]+1)
def PP_Sup_3():
    global PUNTO_Sup
    PUNTO_Sup = (3+(Puntitos_F[5]*user_F[3]))/(user_F[3]+1)
def PP_Sup_4():
    global PUNTO_Sup
    PUNTO_Sup = (4+(Puntitos_F[5]*user_F[3]))/(user_F[3]+1)
def PP_Sup_5():
    global PUNTO_Sup
    PUNTO_Sup = (5+(Puntitos_F[5]*user_F[3]))/(user_F[3]+1)
    
def PP_C_1():
    global PUNTO_C
    PUNTO_C = (1+(Puntitos_F[6]*user_F[3]))/(user_F[3]+1)
def PP_C_2():
    global PUNTO_C
    PUNTO_C = (2+(Puntitos_F[6]*user_F[3]))/(user_F[3]+1)
def PP_C_3():
    global PUNTO_C
    PUNTO_C = (3+(Puntitos_F[6]*user_F[3]))/(user_F[3]+1)
def PP_C_4():
    global PUNTO_C
    PUNTO_C = (4+(Puntitos_F[6]*user_F[3]))/(user_F[3]+1)
def PP_C_5():
    global PUNTO_C
    PUNTO_C = (5+(Puntitos_F[6]*user_F[3]))/(user_F[3]+1)
    
def PP_J_1():
    global PUNTO_J
    PUNTO_J = (1+(Puntitos_F[7]*user_F[3]))/(user_F[3]+1)
def PP_J_2():
    global PUNTO_J
    PUNTO_J = (2+(Puntitos_F[7]*user_F[3]))/(user_F[3]+1)
def PP_J_3():
    global PUNTO_J
    PUNTO_J = (3+(Puntitos_F[7]*user_F[3]))/(user_F[3]+1)
def PP_J_4():
    global PUNTO_J
    PUNTO_J = (4+(Puntitos_F[7]*user_F[3]))/(user_F[3]+1)
def PP_J_5():
    global PUNTO_J
    PUNTO_J = (5+(Puntitos_F[7]*user_F[3]))/(user_F[3]+1)
    
def PP_Pr_1():
    global PUNTO_Pr
    PUNTO_Pr = (1+(Puntitos_F[8]*user_F[3]))/(user_F[3]+1)
def PP_Pr_2():
    global PUNTO_Pr
    PUNTO_Pr = (2+(Puntitos_F[8]*user_F[3]))/(user_F[3]+1)
def PP_Pr_3():
    global PUNTO_Pr
    PUNTO_Pr = (3+(Puntitos_F[8]*user_F[3]))/(user_F[3]+1)
def PP_Pr_4():
    global PUNTO_Pr
    PUNTO_Pr = (4+(Puntitos_F[8]*user_F[3]))/(user_F[3]+1)
def PP_Pr_5():
    global PUNTO_Pr
    PUNTO_Pr = (5+(Puntitos_F[8]*user_F[3]))/(user_F[3]+1)
    
def PP_E2_1():
    global PUNTO_E2
    PUNTO_E2 = (1+(Puntitos_F[9]*user_F[3]))/(user_F[3]+1)
def PP_E2_2():
    global PUNTO_E2
    PUNTO_E2 = (2+(Puntitos_F[9]*user_F[3]))/(user_F[3]+1)
def PP_E2_3():
    global PUNTO_E2
    PUNTO_E2 = (3+(Puntitos_F[9]*user_F[3]))/(user_F[3]+1)
def PP_E2_4():
    global PUNTO_E2
    PUNTO_E2 = (4+(Puntitos_F[9]*user_F[3]))/(user_F[3]+1)
def PP_E2_5():
    global PUNTO_E2
    PUNTO_E2 = (5+(Puntitos_F[9]*user_F[3]))/(user_F[3]+1)
    
def PP_D_1():
    global PUNTO_D
    PUNTO_D = (1+(Puntitos_F[10]*user_F[3]))/(user_F[3]+1)
def PP_D_2():
    global PUNTO_D
    PUNTO_D = (2+(Puntitos_F[10]*user_F[3]))/(user_F[3]+1)
def PP_D_3():
    global PUNTO_D
    PUNTO_D = (3+(Puntitos_F[10]*user_F[3]))/(user_F[3]+1)
def PP_D_4():
    global PUNTO_D
    PUNTO_D = (4+(Puntitos_F[10]*user_F[3]))/(user_F[3]+1)
def PP_D_5():
    global PUNTO_D
    PUNTO_D = (5+(Puntitos_F[10]*user_F[3]))/(user_F[3]+1)
    

#------------------------------------------------------------------------------
           
    
def Guardar_punto():

    global PUNTO_TOTAL
    global N_puntuadores
    
    global PUNTO_A
    global PUNTO_P  
    global PUNTO_G
    global PUNTO_S
    global PUNTO_R 
    global PUNTO_Sup  
    global PUNTO_C 
    global PUNTO_J  
    global PUNTO_Pr 
    global PUNTO_E2 
    global PUNTO_D 
    
    # cuenta para mostrar mensaje dependiendo de lo que falte rellenar
    cuenta=0
    
    select_unic_user()
    PUNTO_E2 = PUNTO_Pr
    PUNTO_TOTAL_prev =(PUNTO_A + PUNTO_P + PUNTO_G + PUNTO_S + PUNTO_R + PUNTO_Sup + PUNTO_C + PUNTO_J + PUNTO_Pr + PUNTO_E2 + PUNTO_D)/11
    PUNTO_OF = (PUNTO_A + PUNTO_P + PUNTO_G )/3
    PUNTO_STMA = ( PUNTO_S + PUNTO_R)/2
    PUNTO_PRODUC = ( PUNTO_Sup + PUNTO_C + PUNTO_J )/3
    PUNTO_CALI = ( PUNTO_Pr + PUNTO_E2 )/2
    PUNTO_ADMI =  PUNTO_D
    PUNTO_TOTAL = (PUNTO_TOTAL_prev+(user_F[2]*user_F[3]))/(user_F[3]+1)
    
    # descargando datos de empresa
    cursor.execute("SELECT * FROM company_data WHERE razon_social = '%s'"%empresa_obtenida)
    data = list(cursor.fetchall())
    data = list(data[0])
    
    
    
    #Guardando los puntos
    
    if len(Ent_Company.get()) !=0 and  Ent_Company.get() !='Escriba aquí el nombre del proyecto...'\
       and Ent_Pago.get()!='Seleccione la forma de pago...'\
       and len(Ent_Pago.get())!=0 and combo_conTr.get()!='Modalidad de contrato' and combo_Fianza.get()!='Carta Fianza':
        
        cuenta = cuenta+1
        
        if PUNTO_A != 0 and PUNTO_P!= 0 and PUNTO_G!= 0 and PUNTO_S!= 0 and PUNTO_R!= 0 and PUNTO_Sup!= 0 and PUNTO_C!= 0 and PUNTO_J!= 0\
        and PUNTO_Pr!= 0 and PUNTO_E2!= 0 and PUNTO_D!= 0:
            
            cuenta = cuenta+1
            
            # Carga de puntos 
            N_puntuadores = user_F[3] + 1
            cursor.execute("UPDATE puntos SET  atencion= %s  WHERE  razon_social= %s", (PUNTO_A,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  precios = %s  WHERE  razon_social= %s", (PUNTO_P,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  garantias = %s  WHERE  razon_social= %s", (PUNTO_G,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  seguridad = %s  WHERE  razon_social= %s", (PUNTO_S,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  responsabilidad = %s  WHERE  razon_social= %s", (PUNTO_R,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  supervision = %s  WHERE  razon_social= %s", (PUNTO_Sup,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  cumplimiento = %s  WHERE  razon_social= %s", (PUNTO_C,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  job_equipo = %s  WHERE  razon_social= %s", (PUNTO_J,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  procedimiento =%s  WHERE  razon_social= %s", (PUNTO_Pr,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  eficaz =%s  WHERE  razon_social= %s", (PUNTO_E2,empresa_obtenida))
            cursor.execute("UPDATE puntos SET  documentacion =%s  WHERE  razon_social= %s", (PUNTO_D,empresa_obtenida))
            
            
            cursor.execute("UPDATE principal SET   number_puntuadores =%s  WHERE  empresa= %s", (N_puntuadores,empresa_obtenida))
            cursor.execute("UPDATE principal SET   puntuacion =%s  WHERE  empresa= %s", (PUNTO_TOTAL,empresa_obtenida))
            
            cursor.execute("""INSERT INTO Divine_puntos(empresa_puntuada, empresa_puntuadora, oficina, stma, produccion, calidad, administracion)\
                           VALUES('%s','%s','%s','%s','%s','%s','%s')"""%(empresa_obtenida, Ent_Company.get(), PUNTO_OF, PUNTO_STMA, PUNTO_PRODUC, PUNTO_CALI, PUNTO_ADMI))
            
            # Reset variables de puntuacion
            PUNTO_A = 0
            PUNTO_P  = 0
            PUNTO_G = 0
            PUNTO_S = 0
            PUNTO_R = 0
            PUNTO_Sup = 0 
            PUNTO_C = 0
            PUNTO_J  = 0
            PUNTO_Pr = 0 
            PUNTO_E2 = 0
            PUNTO_D = 0
            PUNTO_TOTAL = 0
            PUNTO_TOTAL_prev = 0
            
                  
            Guarda_Proyecto_Servicio = Ent_Company.get()
            
            # Insertar precios unitarios 
            all_data = []
            for i in datat:
                pre = datat[i]
                pre.append(Guarda_Proyecto_Servicio)
                pre = tuple(pre)
            
                cursor.execute("""INSERT INTO precios_unitarios(descripcion, unidad, precios, nombre_proyecto)VALUES('%s','%s','%s','%s')"""%pre)
                
            
            # Insertar comentarios   
            cursor.execute("""INSERT INTO comentarios(empresa, comentario, project_description, empresa_proyecto)VALUES('%s','%s','%s','%s')"""\
                              %(empresa_obtenida, 'Empresa/Proyecto: '+Ent_Company.get()+'\n'\
                                +'Forma de pago: '+Ent_Pago.get()+'\n'+'Modalidad de contrato: '+combo_conTr.get()\
                                +'\n'+'Cuenta con Carta Fianza: '+combo_Fianza.get()+'\n'\
                                +'Comentario: \n'+ text_area.get(1.0, END)+'\n'+str(datetime.now()), text_area3.get(1.0, END), Guarda_Proyecto_Servicio))
             
            
            cuenta_coment = 1
            Ent_Company.delete(0,END)
            text_area.delete(1.0, END)
            text_area3.delete(1.0, END)
            
    # Validacion de llenano de datos         
    else:
        Comunica_con_variable('NO COMPLETÓ LOS DATOS')

    connection.commit() 
    
    if cuenta ==1:
        Comunica_con_variable('NO SE GUARDARON LOS DATOS, REVISE QUE TODOS CRITERIOS ESTEN CALIFICADOS')
        
    elif cuenta ==2:
        Comunica_con_variable('GUARDADO EXITOSO')
  
    cuenta=0
    cuenta_coment=0
    


def animate():
    Ver_Puntuacion()

def Ver_Puntuacion():
    
        global d
        global won
        global tlt
        
        won=tkinter.Toplevel()
        won.geometry('1150x730+50+50')
        won.configure(background='white')
        
        #para tener los valores de los puntos y mostrarlos     
        select_puntos()
        Select_Divine_Puntos()
        
        lab = Label(won, text='PUNTUACIÓN DETALLADA Y COMENTARIOS', bg='black', fg='white')   #, bg='black', fg='white'
        lab.pack(side ='top', fill=X)
        
        # Frames 
        L_frame = Frame(won,width=1000,height=800, background='white')
        R_frame = Frame(won,width=1000,height=800, background='white')
        
        L_frame.pack(padx=5,pady=5, side = LEFT)
        R_frame.pack(pady=5, side = LEFT)
        
        la_enty00 = Label(L_frame, text='',bg='white')
        la_enty01 = Label(L_frame, text='',bg='white')
        la_enty02 = Label(L_frame, text='',bg='white')
        la_enty03 = Label(L_frame, text='',bg='white')
        
        #la_enty00.pack(side='top')
        #la_enty01.pack(side='top')
        #la_enty02.pack(side='top')
        #la_enty03.pack(side='top')
        
        #------------------------------------PIE--------------------------------------
        fig = Figure(figsize= (3,3))      #facecolor='black'
        ax = fig.add_subplot(111)    # facecolor='black'
        
        graphh = FigureCanvasTkAgg(fig, master=L_frame)
        graphh.get_tk_widget().pack(side='top', fill='both', anchor=N)
        
        GPP=[]
        GPP.append((Puntitos_F[0]+Puntitos_F[1]+Puntitos_F[2])/3)
        GPP.append((Puntitos_F[3]+Puntitos_F[4])/2)
        GPP.append((Puntitos_F[5]+Puntitos_F[6]+Puntitos_F[7])/3)
        GPP.append((Puntitos_F[8]+Puntitos_F[9])/2)
        GPP.append(Puntitos_F[10])
        
        
        recipe = ["OFICINA TÉCNICA: "+str('%.2f'%GPP[0]),
                  "SSOMA: "+str('%.2f'%GPP[1]),
                  "PRODUCCIÓN: "+str('%.2f'%GPP[2]),
                  "CALIDAD: "+str('%.2f'%GPP[3]),
                  "ADMINISTRACIÓN: "+str('%.2f'%GPP[4])]
        
    
        explode = (0.1, 0.1, 0.1, 0.1,0.1) 
        
        wedges, texts = ax.pie(GPP,  explode=explode ,wedgeprops=dict(width=0.3), startangle=0, radius=0.8)
        
        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.4)
        kw = dict(arrowprops=dict(arrowstyle="-"),
                  bbox=bbox_props, zorder=0, va="center")
        
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            ax.annotate(recipe[i], xy=(x, y), xytext=(1*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, **kw)
            
        #-------------------------------LABEL VACIO----------------------------------------------
        la_enty1 = Label(L_frame, text='',bg='white')
        la_enty2 = Label(L_frame, text='',bg='white')
        la_enty3 = Label(L_frame, text='',bg='white')
        la_enty4 = Label(L_frame, text='',bg='white')
        la_enty5 = Label(L_frame, text='',bg='white')
        
        #la_enty1.pack(side='top')
        #la_enty2.pack(side='top')
        #la_enty3.pack(side='top')
        #la_enty4.pack(side='top')
        #la_enty5.pack(side='top')
        
        
        #---------------------------------GRAFICO in time--------------------------------------
        global ax1
        global graph 
        
        fig1 = Figure(facecolor='white',figsize=(8, 6)) # color frame de graficas
            
        ax1 = fig1.add_subplot(111, facecolor='white') # color de fondo de la grafica 
            
        graph = FigureCanvasTkAgg(fig1, master=L_frame)   # figura, frame
        graph.get_tk_widget().pack(side=BOTTOM)
        
        # BARRA DE HERRAMIENTAS
        toolbar = NavigationToolbar2Tk(graph, L_frame)# barra de iconos
        toolbar.update()
        graph.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        
        global col
        global d 
        global tlt
        col = 'blue'
        d = []
        tlt = 'SELECCIONE UN ÁREA DE EVALUACIÓN PARA VER LOS DATOS'
        
        ax1.cla() #borra el axes 
        ax1.plot(['P'+str(a+1) for a in range(len(d))],d,'-o' ,color=col,linewidth=2)
        ax1.set_title(tlt)
        ax1.set_xlabel("Proyectos evaluados", color='blue')
        ax1.set_ylabel("Calificación", color='blue')
        ax1.set_ylim(0, 5.5)
        #ax1.set_xlim(0, 9)
        ax1.set_yticklabels([0, 1, 2, 3, 4, 5, 5.5], color='black')
        ax1.set_xticklabels(['P'+str(a+1) for a in range(len(d))], color='black')
        ax1.grid(color='grey')
        graph.draw()
        
        
        #-------------------------------- widgets RIGHT --------------------------------------------
        
        lbl_tlt_AREAS = Label(R_frame, text='ÁREAS DE EVALUACIÓN', fg='black', bg='white', font='Arial 12 bold')
        
        btn_OFICINA = Button(R_frame, text="OFICINA TÉCNICA  (13%)", bg='darkblue', fg = 'white', relief='flat',width=35, command=OFICINA)
        lbl_Nivel_A = Label(R_frame, text='Nivel de atención al cliente: '+str('%.2f'%Puntitos_F[0]))
        lbl_Precios = Label(R_frame, text='Precios en el mercado: '+str('%.2f'%Puntitos_F[1]))
        lbl_Valorizaciones = Label(R_frame, text='Entrega de valorizaciones y garantías: ' +str('%.2f'%Puntitos_F[2]))
        
        btn_STMA = Button(R_frame, text="SSOMA  (20%)", bg='orange', fg = 'grey', relief='flat',width=35, command=STMA)
        lbl_Seguridad = Label(R_frame, text='Cumplimiento de seguridad: '+str('%.2f'%Puntitos_F[3]))
        lbl_Responsabilidad = Label(R_frame, text='Responsabiliadad Ambiental y conducta: ' +str('%.2f'%Puntitos_F[4]))
        
        btn_PRODUCCION = Button(R_frame, text="PRODUCCIÓN (30%)", bg='lightgreen', fg = 'grey', relief='flat',width=35, command=PRODUCCION)
        lbl_Supervision = Label(R_frame, text='Supervición en obra: '+str('%.2f'%Puntitos_F[5]))
        lbl_Prigramacion = Label(R_frame, text='Cumple con la programción: '+str('%.2f'%Puntitos_F[6]))
        lbl_Trabajo = Label(R_frame, text='Trabajo en equipo:' +str('%.2f'%Puntitos_F[7]))
        
        btn_CALIDAD = Button(R_frame, text="CALIDAD  (30%)", bg='red', fg = 'lightgrey', relief='flat',width=35, command=CALIDAD)
        lbl_Procedimiento = Label(R_frame, text='Gestión de calidad: '+str('%.2f'%Puntitos_F[8]))
        lbl_Eficaz = Label(R_frame, text='Es eficaz en sus procedimientos: ' +str('%.2f'%Puntitos_F[9]))
        
        btn_ADMINISTRACION = Button(R_frame, text="ADMINISTRACIÓN  (7%)", bg='purple', fg = 'lightgrey', relief='flat',width=35, command=ADMIN)
        lbl_Doc = Label(R_frame, text='Entrega de documentación: '+str('%.2f'%Puntitos_F[10]))
        
        # grid
        lbl_tlt_AREAS.grid(row=0, column=0, pady=5)
        
        btn_OFICINA.grid(row=1, column=0, pady=5)
        lbl_Nivel_A.grid(row=2, column=0)
        lbl_Precios.grid(row=3, column=0)
        lbl_Valorizaciones.grid(row=4, column=0)
        
        btn_STMA.grid(row=5, column=0, pady=5)
        lbl_Seguridad.grid(row=6, column=0)
        lbl_Responsabilidad.grid(row=7, column=0)
        
        btn_PRODUCCION.grid(row=8, column=0, pady=5)
        lbl_Supervision.grid(row=9, column=0)
        lbl_Prigramacion.grid(row=10, column=0)
        lbl_Trabajo.grid(row=11, column=0) 
        
        btn_CALIDAD.grid(row=12, column=0, pady=5)
        lbl_Procedimiento.grid(row=13, column=0) 
        #lbl_Eficaz.grid(row=14, column=0) 
        
        btn_ADMINISTRACION.grid(row=15, column=0, pady=5)
        lbl_Doc.grid(row=16, column=0) 
        
    
        # COMENTARIOS 
        lab = Label(R_frame, text='TRABAJOS Y COMENTARIOS', font='Arial 12 bold', width=40)   #, bg='black', fg='white'
        lab.grid(row=18, column=0, pady=5)
    
        text_area = ScrolledText(R_frame, width=60, height=13, bg='darkgrey', fg='white', font='12bold')
        text_area.grid(row=19, column=0)
        
        select_comentarios()
        text_area.delete(1.0, END)
        
        for i in range(len(coments_F)):
            
            a = list(coments_F[i])
            b = a[1]
            text_area.insert(1.0, b)
            text_area.insert(1.0, '\n\n')
            text_area.insert(1.0, f'-----------------------------------------------Proyecto({i+1})---------------------------------------')
            text_area.insert(1.0, '\n\n')
        
    

# PARA GRAFICAR 
def draw_graph():
    
        ax1.cla() #borra el axes 
        ax1.plot(['P'+str(a+1) for a in range(len(d))],d,'-o' ,color=col,linewidth=2)
        ax1.set_title(tlt)
        ax1.set_xlabel("Proyectos evaluados", color='blue')
        ax1.set_ylabel("Calificación", color='blue')
        ax1.set_ylim(0, 5.5)
        #ax1.set_xlim(0, 9)
        ax1.set_yticklabels([0, 1, 2, 3, 4, 5, 5.5], color='black')
        ax1.set_xticklabels(['P'+str(a+1) for a in range(len(d))], color='black')
        ax1.grid(color='grey')
        graph.draw()
                


def OFICINA():
    
    global data_cpu
    global d
    global tlt
    global dx
    global col 
    tlt='OFICINA TECNICA'
    col='darkblue'
    data_cpu = ['A. al cliente', 'Precios' ,'Valorizaciones']
    d = OF_F 
    draw_graph()
    

def STMA():
    global col
    global data_cpu
    global d
    global tlt
    tlt='SSOMA'
    data_cpu = ['Seguridad', 'Ambiental']
    d = ST_F
    col='orange'
    draw_graph()
    
    

def PRODUCCION():
    global col
    global data_cpu
    global d
    global tlt
    tlt='PRODUCCION'
    col='darkgreen'
    data_cpu = ['Supervisión', 'Programación' ,'T. en equipo']
    d = PRO_F
    draw_graph()

def CALIDAD():
    global col
    global data_cpu
    global d
    global tlt
    tlt='CALIDAD'
    col='red'
    data_cpu = ['Procedimiento', 'Eficacia']
    d = CA_F 
    draw_graph()

def ADMIN():
    global col
    global data_cpu
    global d
    global tlt
    tlt='ADMINISTRACION'
    col='violet'
    data_cpu = ['Documentacón']
    d = AD_F
    draw_graph()
    
#------------------------------------------------------


def Modificar():
    
    wuu = tkinter.Toplevel()
    
    #-------- widgets 
    
    
    lblTi = ttk.Label(wuu, text="Está seguro de eliminar esta empresa y toda su información de manera permanenete? ", font= "Helvetica 11 bold")
    lblrow2 = ttk.Label(wuu, text="<<Si la respuesta es sí, entonces, click en CONFIRMAR>> ", font= "Helvetica 9")
    btnConfirm = Button(wuu, text='CONFIRMAR', fg='white', bg='red', command= Eliminando_company)
    
    #------- grid and pack 
    lblTi.grid(row=1, column=0, padx=90, pady=10)
    lblrow2.grid(row=2, column=0, padx=10)
    btnConfirm.grid(row=4, column=0, padx=10, pady=15) 
    
    
def Modificar_datos_company():
    
    wuu = tkinter.Toplevel()
    
    #-------- widgets 
    lblTi = ttk.Label(wuu, text="Está seguro de cammbiar los datos de la empresa? ", font= "Helvetica 12 bold")
    lblrow2 = ttk.Label(wuu, text="<<Si la respuesta es sí, entonces, click en CONFIRMAR>> ", font= "Helvetica 9")
    btnConfirm = Button(wuu, text='CONFIRMAR', fg='white', bg='darkblue', command=Cambiando_Datos)
    
    #------- grid and pack 
    lblTi.grid(row=1, column=0, padx=90, pady=10)
    lblrow2.grid(row=2, column=0, padx=10)
    btnConfirm.grid(row=4, column=0, padx=10, pady=15) 
    
    
# Eliminaremos la empresa    
def Eliminando_company():
       
        cursor.execute("""DELETE FROM principal WHERE empresa = '%s'"""%empresa_obtenida)
        cursor.execute("""DELETE FROM company_data WHERE razon_social = '%s'"""%empresa_obtenida)
        cursor.execute("""DELETE FROM puntos WHERE razon_social = '%s'"""%empresa_obtenida)
        cursor.execute("""DELETE FROM comentarios WHERE empresa = '%s'"""%empresa_obtenida)
        cursor.execute("""DELETE FROM Divine_puntos WHERE empresa_puntuada = '%s'"""%empresa_obtenida)
        connection.commit()
        Guardado_con_exito()


def Agregar_Partida():
    
    wee = tkinter.Toplevel()
    wee.geometry('500x180+100+100')
    
    #-------- widgets 
    lblTi = ttk.Label(wee, text="       AGREGA UNA PARTIDA NUEVA", font= "Helvetica 10 bold italic")
    lblAdvert_1 = ttk.Label(wee, text='"Si hiciste la busqueda y no encoontraste lo que buscabas,')
    lblAdvert_2 = ttk.Label(wee, text='         aquí puedes agregar una nueva partida"')
    global EntPartida
    EntPartida = ttk.Entry(wee, width=80, textvariable=Partida_G)
    btnGrabaP = Button(wee, text='GRABAR',width=10, fg='white', bg='darkblue', command=insert_partida)
    
    #------- grid and pack
    lblTi.grid(row=1, column=0, padx=1, pady=10) 
    lblAdvert_1.grid(row=2, column=0, padx=1, pady=3) 
    lblAdvert_2.grid(row=3, column=0, padx=1, pady=3) 
    EntPartida.grid(row=4, column=0, padx=1, pady=5) 
    btnGrabaP.grid(row=5, column=0, padx=1, pady=5) 
    
    EntPartida.delete(0, END)
    
    
def Eliminar_Partida():
    
    were = tkinter.Toplevel()
    were.geometry('505x180+100+100')
    
    global EntPartida_2
    
    #-------- widgets
    lblTi = ttk.Label(were, text="       ELIMINA UNA PARTIDA ", font= "Helvetica 10 bold italic")
    lblAdvert_1 = ttk.Label(were, text='"Si hiciste la busqueda y hay algun error en el nombre de la partida,')
    lblAdvert_2 = ttk.Label(were, text='         aquí puedes eliminar la partida"')
    EntPartida_2 = ttk.Entry(were, width=80, textvariable=Partida_G)
    btnGrabaP = Button(were, text='ELIMINAR',width=10, fg='white', bg='red', command=delete_partida)
    
    #------- grid and pack 
    lblTi.grid(row=1, column=0, padx=1, pady=10) 
    lblAdvert_1.grid(row=2, column=0, padx=1, pady=3) 
    lblAdvert_2.grid(row=3, column=0, padx=1, pady=3) 
    EntPartida_2.grid(row=4, column=0, padx=1, pady=5) 
    btnGrabaP.grid(row=5, column=0, padx=1, pady=5) 
    
    EntPartida_2.delete(0, END)
    EntPartida_2.insert(0, comboPartidas.get())
    
    
def show_price():
    
    cuo = tkinter.Toplevel()
    cuo.resizable(1,1)
    cuo.config(bg='white')
    
    global modell 
    global table 
    
    tframe = Frame(cuo)
    tframe.grid(row=0, column=0, padx=5, pady= 10)
        
    
    cursor.execute("SELECT descripcion, unidad, precios FROM precios_unitarios WHERE nombre_proyecto = '%s'"%empresa_proyecto.get())
    use = list(cursor.fetchall())
    use_dic = []
    
    for u in use:
        dic = dict(zip(['DESCRIPCIÓN','UNIDAD','PRECIO[S/.]'],u))
        use_dic.append(dic)
        
    indices = [i for i in range(len(use_dic))] 
    dataa = dict(zip(indices,use_dic)) 
    
    modell  =  TableModel ()
    tabli = TableCanvas(tframe,  model = modell, cellwidth=200, data= dataa)
    tabli.show()
        
    # Bind 
    cuo.bind('<Return>', pre_send)
    global t_row
    t_row = 0
    
def Change_tipo_usuario():
    
    cred = tkinter.Toplevel()
    cred.config(bg='white')
    
    frm1 = Frame(cred, bg='white')
    frm2 = Frame(cred, bg='white')
    frm1.pack()
    frm2.pack()
    
    # TABLA
    global tabloid
    tabloid = ttk.Treeview(frm1, columns=["TIPO","VERIFICADO"])
    tabloid.pack()
    # Se definen los encabezados de las columnas
    tabloid.heading("#0", text="e-mail")
    tabloid.heading("#1", text="TIPO") 
    tabloid.heading("#2", text="VERIFICADO")    
    # Se definen las propiedades de las columns
    tabloid.column("#0", stretch=False, minwidth=300, width=370) # width cambia el tamano de la pestanaw
    tabloid.column("#1", stretch=False, minwidth=100, width=130, anchor='e') #anchor='e' no deja cambiar tamano de pestana
    tabloid.column("#2", stretch=False, minwidth=100, width=130, anchor='e') #anchor='e' no deja cambiar tamano de pestana
    # Insertando usuarios 
    
    cursor.execute("SELECT e_mail, tipo, verificado FROM usuarios")
    users = list(cursor.fetchall())
    
    for use in users:
        tabloid.insert('', 'end', text=use[0], values= [use[1],use[2]])
    
    # MANDO
    global cboOptions
    cboOptions = ttk.Combobox(frm2, width=20 ,values=['VERIFICADO', 'NO VERIFICADO', 'PREMIUM'])
    cboOptions.grid(row=0, column=0, pady= 20, padx= 10)
    cboOptions.set('Choose')
    btnCambio = Button(frm2, text='GUARDAR CAMBIO', bg='white', command= change_state_user)
    btnCambio.grid(row=0, column=1, pady= 20)
    
def change_state_user():
    
    # Changing STATE of user
    row = tabloid.focus()
    a = tabloid.item(row)
    mail = a['text']
    cursor.execute("UPDATE usuarios SET  verificado= %s WHERE  e_mail= %s", (cboOptions.get(), mail))
    connection.commit() 
    
    # Re-Inserting data in tabloid 
    tabloid.delete(*tabloid.get_children())
    cursor.execute("SELECT e_mail, tipo, verificado FROM usuarios")
    users = list(cursor.fetchall())
    
    for use in users:
        tabloid.insert('', 'end', text=use[0], values= [use[1],use[2]])
   
    # Aviso de cambio de tipo de usuario via e-mail    
    try:
        msg = MIMEMultipart() 
        message = f"Su usuario {mail} se cambio a tipo {cboOptions.get()}"
        # setup the parameters of the message
        password = "BasedeDatospro."
        msg['From'] = "basededatosmj@gmail.com"
        msg['To'] = mail
        msg['Subject'] = "CAMBIO DE TIPO DE USUARIO"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
    except:
        Comunica_con_variable('Ocurrió algún error, se recomienda que vuelva a iniciar sesión')
        
        
def Olvide_mi_contrasena():
    
    olv = tkinter.Toplevel()
    olv.iconbitmap(r'db.ico')
    olv.title("Restablecimiento de contraseña")
    
    lblAviso = Label(olv, text='Escribe tú correo electrónico para enviarte tú contraseña')
    lblAviso.grid(row=0,column=0, pady=5)
    global entMail_con
    entMail_con = Entry(olv, width=55)    
    entMail_con.grid(row=1,column=0, pady=10, padx=10)
    btnEnviar_olvido = Button(olv, text= 'Enviar', command= Envia_la_contrasena_ya)
    btnEnviar_olvido.grid(row=2,column=0, pady=0)
    
def Envia_la_contrasena_ya():
     
    cursor.execute("SELECT pasword FROM usuarios WHERE e_mail = '%s'"%entMail_con.get())
    user = list(cursor.fetchall())[0]
    
    
    # Aviso de cambio de tipo de usuario via e-mail    
    try:
        msg = MIMEMultipart() 
        message = f"Su contraseña es: {user[0]}"
        # setup the parameters of the message
        password = "BasedeDatospro."
        msg['From'] = "basededatosmj@gmail.com"
        msg['To'] = entMail_con.get()
        msg['Subject'] = "RESTABLECIMIENTO DE CONTRASEÑA"
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
        #create server
        server = smtplib.SMTP('smtp.gmail.com: 587')
        server.starttls()
        # Login Credentials for sending the mail
        server.login(msg['From'], password)
        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string())
        server.quit()
        
        Comunica_con_variable('Su contraseña ha sido enviada')
        
    except:
        Comunica_con_variable('Ocurrió algún error, revise que su correo sea el correcto')
        
def Cambiar_contrasena():
    
    cab = tkinter.Toplevel()
    cab.iconbitmap(r'db.ico')
    cab.title("Cambio de password")
    
    lblAviso = Label(cab, text='Escribe tú contraseña actual')
    lblAviso.grid(row=0,column=0, pady=5)
    global entpass_actual
    entpass_actual = Entry(cab, show='*')    
    entpass_actual.grid(row=1,column=0, pady=5, padx=10)
    
    lblAviso2 = Label(cab, text='Escribe tú nueva contraseña: [números, letras y símbolos]')
    lblAviso2.grid(row=2,column=0, pady=5)
    global entpass_nueva
    entpass_nueva = Entry(cab, show='*')    
    entpass_nueva.grid(row=3,column=0, pady=5, padx=10)
    
    
    btnEnviar_olvido = Button(cab, text= 'GUARDAR CAMBIO', command= Hacer_cambio_contrasena_ya)
    btnEnviar_olvido.grid(row=4,column=0, pady=5)
    

def Hacer_cambio_contrasena_ya():
    
    
    cursor.execute("SELECT pasword FROM usuarios WHERE e_mail = '%s'"%CORREO)
    user = list(cursor.fetchall())[0]
    print(user[0])
    
    if entpass_actual.get() == user[0]:
            
        cursor.execute("UPDATE usuarios SET  pasword= %s WHERE  e_mail= %s", (entpass_nueva.get(), CORREO))
        connection.commit() 
        Comunica_con_variable('Cambio exitoso!')
    else:
        Comunica_con_variable('La contraseña actual no coincide con la que se tiene en registro')
        
    
    
def Manual_usuario():
    
    import webbrowser
    webbrowser.open("https://1drv.ms/u/s!Av75RrM1LwTqvFEJQB6ski_yEs_Z?e=wjPoYd")
    
    
    



#::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::        
#<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< MAIN PROGRAM >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def MAIN():
    
    # COFIGURACION GENERAL VENTANA PRINCIPAL
    global root 
    root = tkinter.Toplevel()
    
    # Configuracion de la ventana
    root.iconbitmap(r'db.ico')
    root.title("BASE DE DATOS MJ")
    root.geometry("1300x650+100+100")
    root.resizable(1, 1)
    root.config()
    
    # Frames 
    frm = Frame(root)
    frm1 = Frame(root)
    
    
    # Obj-Var 
    global destino_combo 
    destino_combo = StringVar()
    global Razon_S 
    Razon_S = StringVar()
    global N_RUC
    N_RUC = StringVar()
    global Direccion 
    Direccion = StringVar()
    global Telefono
    Telefono = StringVar()
    global E_mail 
    E_mail = StringVar()
    global Mod_contrato 
    Mod_contrato = StringVar()
    global Gerente 
    Gerente = StringVar()
    global Carta_fianza 
    Carta_fianza = StringVar()
    global Especializacion 
    Especializacion = StringVar()
    global Certificado
    Certificado = StringVar()
    global Personal 
    Personal = StringVar()
    global empresa_proyecto 
    empresa_proyecto = StringVar() 
    global E1
    E1 = StringVar()
    global E2
    E2 = StringVar()
    global E3
    E3 = StringVar()
    global E4
    E4 = StringVar()
    global E5
    E5 = StringVar()
    global Partida_G 
    Partida_G = StringVar()
    global Empresa_existente 
    Empresa_existente = StringVar()
    global La_Contra_E
    La_Contra_E = StringVar()
    
    global La_Company_comenta
    La_Company_comenta = StringVar()
    La_Proyecto_comenta = StringVar()
    La_Pago_comenta = StringVar()
    La_Precio_unitario = StringVar()
    
    
    destino_combo.set("Seleccione PARTIDA...")
    empresa_proyecto.set('Seleccionar proyecto')
    
    frm.pack(padx=5, pady=10, side = LEFT)
    frm1.pack(pady=10, padx=30, side = RIGHT)
    
    
    # Menu
    menubar = Menu(root)
    menu_archivo = Menu(menubar, tearoff=False)
    menu_ayuda = Menu(menubar, tearoff=False)
    root.config(menu=menubar)
            
    menubar.add_cascade(label='Archivo', menu=menu_archivo)
    menubar.add_cascade(label='Ayuda', menu=menu_ayuda)
    
            
    menu_archivo.add_command(label='Cambiar contraseña', command=Cambiar_contrasena)
    menu_archivo.add_command(label='Salir', command=salir)
    menu_ayuda.add_command(label='Manual de usuario', command= Manual_usuario)
    menu_ayuda.add_command(label='Acerca de..', command= lambda: showinfo("Acerca de...",
                                                                          "Base de datos subcontratistas\n\
                                                                          Por: Marilyn Cotrina\n\
                                                                                  José Reynaldo\n \n\
                                                                      Sofware: jefferespri@gmail.com"))
    
    
    #------------------------- LEFT 
    Frame_Primium = LabelFrame(frm, relief=FLAT)
    Frame_Primium.grid(row=0, column= 0, sticky= W)
    
    lblWelcom = Label(Frame_Primium, text='', font='Calibri 14 bold')
    lblWelcom.grid(row=0, column=0, sticky= W)
    btnHaste_Premium = Button(Frame_Primium, text='Hazte Premium', font='Calibri 13 bold', bg='#38D682', fg='white', relief=FLAT,command=Solicita_premium)
    btnHaste_Premium.grid(row=0, column=1, padx =10 ,sticky= W)
    
    lblTitleee = Label(frm, text=' EMPRESAS SUBCONTRATISTAS DE ACABADOS', font='Aharoni 14 bold ', fg='darkblue')
    global comboPartidas 
    comboPartidas = ttk.Combobox(frm, width=70 ,values=Partidas, textvariable=destino_combo)
    
    btnAgregar = Button(frm, text="AGREGAR EMPRESA o CAMBIAR DATOS", fg='white', bg='darkblue', command=Agregar_Empresa)
    btnModify = Button(frm, text="ELIMINAR EMPRESA", bg='red', fg = 'white', relief='flat',width=35, command=Modificar)
    btnTypo_usuario = Button(frm, text="USUARIOS", fg='white', bg='darkblue', command=Change_tipo_usuario)
    
    status_bar = Label(root, text="Listo", bd=1, relief=SUNKEN, anchor=W)
    
    #---------------------- RIGHT
    lblFrame1 = LabelFrame(frm1, relief=FLAT)
    lblFrame2 = LabelFrame(frm1, relief=FLAT)
    lblFrame1.grid(row=0)
    lblFrame2.grid(row=3)
    
    lblContacto = Label(lblFrame1, text="Datos de contacto", font= "Helvetica 12 bold italic")
    lbldat11 = Label(lblFrame1, text="Razón Social:")
    lbldat12 = Label(lblFrame1, text="RUC:")
    lbldat13 = Label(lblFrame1, text="Dirección:")
    lbldat14 = Label(lblFrame1, text="Celular:")
    lbldat15 = Label(lblFrame1, text="Correo electrónico:")
    lbldat16 = Label(lblFrame1, text="Modalidad de contrato:")
    lbldat17 = Label(lblFrame1, text="Gerente de empresa:")
    global lbldat18
    lbldat18 = Label(lblFrame1, text="...................",state='normal')
    global lbldat19 
    lbldat19 = Label(lblFrame1, text="...................")
    global lbldat110
    lbldat110 = Label(lblFrame1, text="...................")
    global lbldat111
    lbldat111 = Label(lblFrame1, text="...................")
    global lbldat112
    lbldat112 = Label(lblFrame1, text="...................")
    global lbldat113
    lbldat113 = Label(lblFrame1, text="...................")
    global lbldat114
    lbldat114 = Label(lblFrame1, text="...................")
    
    lbldat21 = Label(lblFrame1, text="Tipo de Carta fianza:")
    lbldat25 = Label(lblFrame1, text="Fecha de inicio de actividades:")
    lbldat26 = Label(lblFrame1, text="Servicios que brinda:")
    global lblService_1
    lblService_1 = Label(lblFrame1, text="...................", state='normal')
    global lblService_2 
    lblService_2 = Label(lblFrame1, text="...................")
    global lblService_3
    lblService_3 = Label(lblFrame1, text="...................")
    global lblService_4 
    lblService_4 = Label(lblFrame1, text="...................")
    
    global lbldat27 
    lbldat27 = Label(lblFrame1, text="...................")
    global lbldat29
    lbldat29 = Label(lblFrame1, text="...................")
    global lbldat211
    lbldat211 = Label(lblFrame1, text="...................")
    
    # Botones
    btnPuntuacion = Button(lblFrame1, text="VER DESEMPEÑO", command=Ver_Puntuacion, bg='darkblue', fg='white')
    btnPuntuar = Button(lblFrame1, text="CALIFICAR y COMENTAR", command=PUNTUAR, bg='darkblue', fg='white')
    
             
    lblnada = Label(frm1, text="-------------------------------------------------------------------------", fg ='darkblue')
    lblnada.grid(row=2)
    
    # Widgets para visualizacion de proyectos
    global comboProyecto_Servicio 
    global text_area_descrip
    comboProyecto_Servicio = ttk.Combobox(lblFrame2, width=50 ,values=empresa_proyecto_F, textvariable=empresa_proyecto)
    text_area_descrip = ScrolledText(lblFrame2, width=45, height=5, font= 'Arial 10')
    text_area_descrip.grid(row=24, column=0, columnspan=2, padx=10, sticky = W)
    

    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::: GRID and PACK :::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    #--------------------------LEFT 
    
    lblTitleee.grid(row=1, column =0 , pady=10)
    comboPartidas.grid(row=2, column=0, pady=10)
    btnAgregar.grid(row=4, column=0, pady=15)
    btnModify.grid(row=5, column=0, pady=5, padx=5)
    btnTypo_usuario.grid(row=6, column=0, pady=5, padx=5)
    
    #-------------------- RIGHT
    lblContacto.grid(row=1, column=0, padx=0)
    
    lbldat11.grid(row=2, column=0, padx=1,sticky=W)
    lbldat12.grid(row=3, column=0, padx=1,sticky=W)
    lbldat13.grid(row=4, column=0, padx=1,sticky=W)
    lbldat14.grid(row=5, column=0, padx=1,sticky=W)
    lbldat15.grid(row=6, column=0, padx=1,sticky=W)
    lbldat17.grid(row=7, column=0, padx=1,sticky=W)
    lbldat18.grid(row=2, column=1, sticky = W, padx=1)
    lbldat19.grid(row=3, column=1, sticky = W, padx=1)
    lbldat110.grid(row=4, column=1, sticky = W, padx=1)
    lbldat111.grid(row=5, column=1, sticky = W, padx=1)
    lbldat112.grid(row=6, column=1, sticky = W, padx=1)
    
    lbldat114.grid(row=7, column=1, sticky = W, padx=1)
    
    lbldat25.grid(row=14, column=0, padx=1,sticky=W)
    lbldat26.grid(row=15, column=0, padx=1,sticky=W)
    lbldat211.grid(row=14, column=1, sticky = W,padx=1)
    lblService_1.grid(row=15, column=1, sticky = W, padx=1)
    lblService_2.grid(row=16, column=1, sticky = W, padx=1)
    lblService_3.grid(row=17, column=1, sticky = W, padx=1)
    lblService_4.grid(row=18, column=1, sticky = W, padx=1)
    
    btnPuntuacion.grid(row=19, column=0, pady=20, padx=1)
    btnPuntuar.grid(row=19, column=1, pady=20, padx=10,sticky = W)
    
    lblDatos = Label(lblFrame2, text="Proyectos en los que participó", font= "Helvetica 12 bold italic")
    lblDatos.grid(row=22, column=0, padx=1)
    
    #-----------------------------------------------------
    comboProyecto_Servicio.grid(row=23, column=0, pady=10 , sticky = E)
    
    #-----------------------------------------------------
    btnUni = Button(lblFrame2, text='PRECIOS', bg='darkblue', fg='white', command=show_price)
    btnUni.grid(row=23, column=1, pady=10, padx=10 ,sticky = W)
    
    #-----------------------------------------------------
    
    
    #----------------------- LABEL TIPO STATUS BAR ------------------------------
    lblWelcom.config(text=f'Hola, {NAME}')
    lbl_Evaluadores = Label(frm, text='*Número de empresas constructoras que han evaluado a los subcontratistas')
    lbl_Evaluadores.grid(row=20, sticky=W)
    
    
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: Tree view ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    global tabla
    tabla = ttk.Treeview(frm, columns=["RANKING","EVALUADORES*","CALIFICACIÓN"])
    tabla.grid(row=3, column=0,columnspan=1, padx=30)
                
    lblvac1 = Label(frm)
    lblvac2 = Label(frm)
    lblvac3 = Label(frm)
    lblvac4 = Label(frm)
    lblvac5 = Label(frm)
    lblvac6 = Label(frm)
    
    lblvac1.grid(row=5, column=0)
    lblvac2.grid(row=6, column=0)
    lblvac3.grid(row=7, column=0)
    lblvac1.grid(row=8, column=0)
    lblvac2.grid(row=9, column=0)
    lblvac3.grid(row=10, column=0)
        
    # Se definen los encabezados de las columnas
    tabla.heading("#0", text="EMPRESAS SUBCONTRATISTAS")
    tabla.heading("#1", text="NIVEL DE DESEMPEÑO")
    tabla.heading("#2", text="EVALUADORES*")
    tabla.heading("#3", text="CALIFICACIÓN")
        
    # Se definen las propiedades de las columns
    tabla.column("#0", stretch=False, minwidth=300, width=370) # width cambia el tamano de la pestanaw
    tabla.column("#1", stretch=False, minwidth=100, width=130, anchor='e') #anchor='e' no deja cambiar tamano de pestana
    tabla.column("#2", stretch=False, minwidth=100, width=100, anchor='e') #anchor='e' no deja cambiar tamano de pestana
    tabla.column("#3", stretch=False, minwidth=100, width=100, anchor='e') #anchor='e' no deja cambiar tamano de pestana
    
    #::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: STATE OF WIDGETS :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    if TYPE == 'ADMI':
        btnHaste_Premium.grid_forget() 
    
    elif TYPE == 'Constructora' and VERIFICADO == 'VERIFICADO':
        btnTypo_usuario.grid_forget()
        
        btnUni.config(state='disabled')
        btnPuntuacion.config(state='disabled')
    
    elif TYPE == 'Constructora' and VERIFICADO == 'NO VERIFICADO':
        btnAgregar.config(state='disabled')
        btnModify.config(state='disabled')
        btnTypo_usuario.grid_forget()
        
        btnUni.config(state='disabled')
        btnPuntuacion.config(state='disabled')
        btnPuntuar.config(state='disabled')
    
    elif TYPE == 'Constructora' and VERIFICADO == 'PREMIUM':
        btnHaste_Premium.grid_forget()
        btnTypo_usuario.grid_forget()
        
    #:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: BINDS ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    
    comboPartidas.bind("<<ComboboxSelected>>", evaluar_partida)
    tabla.bind_all("<<TreeviewSelect>>",cambiar_datos)
    comboProyecto_Servicio.bind("<<ComboboxSelected>>", write_description)
    
    

# INICIO DE SESION 
th2 = threading.Thread(target=conexion_a_BD, args=(60,), daemon=True)
th2.start()

#def Inicio_sesion(t):
reet = Tk()

reet.iconbitmap(r'db.ico')
reet.title("BASE DE DATOS MJ")
#reet.geometry("1270x600+100+100")
#root.configure(background='white')
reet.resizable(0, 0)

Type_usuario = StringVar()
Type_usuario.set("Tipo de usuario")

frm1 = Frame(reet, bg= '#0689F8')
frm2 = Frame(reet)
frm3 = Frame(reet)

frm1.grid(row=0,columnspan= 2)
frm2.grid(row=1,column= 0)
frm3.grid(row=1,column= 1)


# Widgets Frame 1

logo = ImageTk.PhotoImage(Image.open("logi.png"))
my_logo = Label(frm1,image= logo, bg= '#0689F8')
my_logo.grid(rowspan=2 , column=0, padx=10, pady=5)
lblvaci = Label(frm1, bg= '#0689F8')
lblvaci.grid(rowspan=2 , column=1, padx=200)

lblCorreo = Label(frm1, text='Correo electrónico', font='Calibri 12 bold', bg='#0689F8', fg='white')
lblCorreo.grid(row=0 , column=2)
lblPassword = Label(frm1, text='Contraseña', font='Calibri 12 bold', bg='#0689F8', fg='white')
lblPassword.grid(row=0 , column=3)
global entCorreo
entCorreo = Entry(frm1)
entCorreo.grid(row=1 , column=2, padx=5)
global entPassword
entPassword = Entry(frm1, show='*')
entPassword.grid(row=1 , column=3, padx=5)
btnOlvidate_password = Button(frm1, text='Olvidates tú contraseña?', font='Calibri 9 bold', relief=FLAT, bg='#0689F8', fg='darkgrey', command=Olvide_mi_contrasena)
btnOlvidate_password.grid(row=2, column=3, padx=5)

btnInicio = Button(frm1, text= 'Iniciar Sesión', relief='flat', command=login_global_user)
btnInicio.grid(row=1, column=4, padx=5)

# Widgets Frame 2
imagen = ImageTk.PhotoImage(Image.open("constructor.png"))
my_imagen = Label(frm2,image= imagen)
my_imagen.grid(row=0 ,column=0,pady=100 , padx=5)


# Widgets Frame 3

lblCrea = Label(frm3, text='Crea una cuenta', font='Calibri 16 bold')
lblCrea.grid(row=0 , column=0, columnspan=2, sticky=W)
global cboType
cboType = ttk.Combobox(frm3, width=52,values=['Constructora','Sub-contratista'], textvariable=Type_usuario)
cboType.grid(row=1, column=0, columnspan=2, pady=10)

lblNombre = Label(frm3, text='Razón Social')
lblNombre.grid(row=2,column=0, columnspan=2, sticky=W)
global entNombre
entNombre = Entry(frm3, width=55)
entNombre.grid(row=3, column=0, columnspan=2, sticky=E)

lblRuc = Label(frm3, text='RUC')
lblRuc.grid(row=4,column=0, columnspan=2, sticky=W)
global entRuc
entRuc = Entry(frm3, width=55)
entRuc.grid(row=5, column=0, columnspan=2)

lblMail = Label(frm3, text='Correo electrónico')
lblMail.grid(row=6,column=0, sticky=W)
global entMail
entMail = Entry(frm3, width=25)
entMail.grid(row=7, column=0, sticky=W)
btnEnviar_codigo = Button(frm3, text='Enviar código de validación', bg='#0B62B5', fg='white', relief=FLAT, command=Enviar_codigo_validacion)
btnEnviar_codigo.grid(row=7, column=1, sticky=W)

global entCod_validation
entCod_validation = Entry(frm3, width=25)
entCod_validation.grid(row=8,column=0,  sticky=W)
btnValida_mail = Button(frm3, text='Validar', bg='#0B62B5', fg='white', relief=FLAT, command=Validar_codigo)
btnValida_mail.grid(row=8,column=1, sticky=W, pady=5)

lblContac = Label(frm3, text='Fijo o celular')
lblContac.grid(row=9,column=0,columnspan=2, sticky=W)
global entContac
entContac = Entry(frm3, width=55)
entContac.grid(row=10, column=0,columnspan=2)

lblContra = Label(frm3, text='Contraseña nueva: [números, letras y símbolos]')
lblContra.grid(row=11,column=0,columnspan=2, sticky=W)
global entContra
entContra = Entry(frm3, width=55, show='*')
entContra.grid(row=12, column=0,columnspan=2)


btnRegistrar = Button(frm3, text='Registrarte', font='Calibri 13 bold', bg='#38D682', fg='white', command=insert_global_user)
btnRegistrar.grid(row=13, column=0,columnspan=1, pady=15 )

reet.mainloop()


# Threading     
#th1 = threading.Thread(target=Inicio_sesion, args=(60,), daemon=True)
#th2 = threading.Thread(target=conexion_a_BD, args=(60,), daemon=True)

#th1.start()
#th2.start()



#%%
