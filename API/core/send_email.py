import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from fastapi import HTTPException
from connectmySQL import create_connect, execute_query

banco = {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '123', 'database': 'musical'}

import os

def envia_email(receiver_email: str, nome: str, id: int):

    try:
        conn = create_connect(banco)
       # Buscar inscritos principais
        select_query = """
            select ins.id, ins.nome, ins.qrenviado, dep.id, dep.nome, dep.qrenviado 
              from inscricao ins
              join dependentes dep ON dep.idpai = ins.id
             where 1=1
               and dep.ativo = 1
               and ins.ativo = 1
               and dep.qrenviado = 0
             order by ins.id
        """
        pessoas = execute_query(conn, select_query)
        idpaiMem = 0
        enviar = []
        for pessoa in pessoas:
            idpaiLido = pessoa[0]
            qrenviadoins = pessoa[2]
            qrenviadodep = pessoa[5]
            if idpaiMem == 0:
                idpaiMem = idpaiLido

            # aqui terminou de ler tudo do IDPAI pode enviar
            if idpaiMem != idpaiLido:
                # logica de enviar o que precisa
                idpaiMem = idpaiLido
                enviar = []

            if qrenviadoins == 0:
                if idpaiMem not in enviar:
                    enviar.append(pessoa[0])

            if qrenviadodep == 0:
                enviar.append(pessoa[3])

            print(enviar)

        if idpaiMem > 0:
            # logica de enviar o que precisa
            pass
        
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        
        
def envia_inscricao(nome: str, receiver_email: str):
    email = "emailbot@gmail.com"
    password = "senha"

    data_atual = datetime.datetime.now()
    subject = "Inscrição Realizada"
    message_body = f"Inscrição de {nome} feita com sucesso em: {data_atual}"
    
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(message_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password) 
        server.sendmail(email, receiver_email, message.as_string())
        server.quit()
        print(f"E-mail enviado com sucesso para {receiver_email}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")    
    
    
def envia_erro(erro: str, receiver_email: str):
    email = "emailbot@gmail.com"
    password = "senha"

    subject = "Erro"
    message_body = f"Erro: {erro}"
    
    message = MIMEMultipart()
    message["From"] = email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(message_body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password) 
        server.sendmail(email, receiver_email, message.as_string())
        server.quit()
        print(f"E-mail enviado com sucesso para {receiver_email}")
    except Exception as e:
        print(f"Erro ao enviar o e-mail: {e}")