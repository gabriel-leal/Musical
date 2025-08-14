from fastapi import HTTPException
from connectmySQL import create_connect, execute_query
import requests

banco = {'host': 'localhost', 'port': 3306, 'user': 'root', 'password': '12345', 'database': 'musical'}
#banco = {'host': '172.17.0.2', 'port': 3306, 'user': 'root', 'password': '123', 'database': 'musical'}

def envia_mensagem(id: int, telefone: str):
    nome = pega_nome(id)
    msg = f"""Olá {nome}! 🎶 Que alegria ter você com a gente! Sua inscrição no musical deste ano foi confirmada com sucesso.

Logo abaixo está o QR Code da sua inscrição e dos seus dependentes (se houver). Ele deverá ser apresentado na recepção no dia do evento para validar sua presença.

Fique atento(a) às próximas mensagens. Que Deus te abençoe nessa jornada conosco! 🙌"""
    header = {
        "authorization": "chave-evolution"
    }
    body = {
        "fone": f'55{telefone}',
        "message": msg,
    }
    print(header)
    print(body)
    #requests.post('https://whatsapp.dominio.com.br/message', json=body, headers=header)

def pega_nome(id: int):
    try:
        conn = create_connect(banco)
        if id > 500:
            select_query = f"SELECT Nome FROM dependentes WHERE id = {id}"
        else:
            select_query = f"SELECT Nome FROM inscricao WHERE id = {id}"
        retorno = execute_query(conn, select_query)
        return retorno[0][0]
    except Exception as error:
        print(error)

def update_qrenviado(id):
    try:
        conn = create_connect(banco)
        if id > 500:
            update_query = f"UPDATE dependentes SET qrenviado = 1 WHERE id = {id}"
        else:
            update_query = f"UPDATE inscricao SET qrenviado = 1 WHERE id = {id}"
        execute_query(conn, update_query)
        execute_query(conn, 'commit')
    except Exception as error:
        print(error)

def envia_qrcode(enviar):
    if len(enviar) > 1:
        telefone = enviar[0]
        for envia in enviar[1:]:
            img = f'http://000.000.000.0/qrcodes/{envia}.png'
            try:
                body = {
                    "fone": f'55{telefone}',
                    "image": img,
                    "caption": pega_nome(envia)
                }
                header = {
                    "authorization": "chave evolution"
                }
                print(header)
                print(body)
                #requests.post('https://whatsapp.dominio.com.br/image', json=body, headers=header)
                update_qrenviado(envia)
            except Exception as error:
                print(error)

def envia_whatsapp():
    try:
        conn = create_connect(banco)
        select_query = """
            SELECT ins.id, ins.nome, ins.qrenviado, dep.id, dep.nome, dep.qrenviado, ins.telefone, dep.telefone
            FROM inscricao ins
            LEFT JOIN dependentes dep ON dep.idpai = ins.id
            WHERE IFNULL(dep.ativo, 1) = 1
            AND ins.ativo = 1
            ORDER BY ins.telefone
        """
        pessoas = execute_query(conn, select_query)
        if not pessoas:
            print('não há pessoas para enviar')
            return 'não há pessoas para enviar'

        idpaiMem = ''
        enviar = []

        for pessoa in pessoas:
            idpaiLido, _, qrenviadoins, iddepLido, _, qrenviadodep, insfone, _ = pessoa

            if idpaiMem == '':
                idpaiMem = insfone

            if idpaiMem != insfone:
                processar_envio(enviar)
                idpaiMem = insfone
                enviar = []

            if qrenviadoins == 0:
                if insfone not in enviar:
                    enviar.append(insfone)
                    enviar.append(idpaiLido)  # ID do titular
            else:
                if insfone not in enviar:
                    enviar.append(insfone)

            if iddepLido and qrenviadodep == 0:
                enviar.append(iddepLido)

        # Último grupo
        if len(enviar) > 0:
            processar_envio(enviar)

    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        return 'QR Enviado!'

def processar_envio(enviar):
    telefone_inscrito = enviar[0]
    id_inscrito = None

    # Encontrar o ID do titular (inscricao)
    for item in enviar[1:]:
        if item <= 500:
            id_inscrito = item
            break

    # Verifica se nenhum QR Code já foi enviado
    nenhum_enviado = True
    for i in range(1, len(enviar)):
        tipo = "inscricao" if enviar[i] <= 500 else "dependentes"
        select = f"SELECT qrenviado FROM {tipo} WHERE id = {enviar[i]}"
        try:
            conn_check = create_connect(banco)
            status = execute_query(conn_check, select)
            if status and status[0][0] == 1:
                nenhum_enviado = False
                break
        except Exception as e:
            print(f"Erro verificando qrenviado: {e}")

    # Envia mensagem só uma vez para o titular
    if nenhum_enviado and id_inscrito and telefone_inscrito:
        envia_mensagem(id_inscrito, telefone_inscrito)

    # Sempre envia os QR Codes pendentes
    envia_qrcode(enviar)

envia_whatsapp()
