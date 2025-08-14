from fastapi import HTTPException
from core.connectmySQL import create_connect, execute_query, execute_insert
import datetime
from core.geraqrcode import criaqrcode
from core.logs import registrar_log

def inscricaodep(dep, banco, request):
    try:
        conn = create_connect(banco)
        select_query = f"""
            select d.id, d.idpai, d.nome
            from dependentes d 
            where d.nome = "{dep.nome}" and d.idpai = "{dep.idpai}"
            and d.ativo = 1
        """
        retorno = execute_query(conn, select_query) 
        if len(retorno) == 0:
            select_query = f"""
            select i.id, i.nome
            from inscricao i 
            where i.telefone = "{dep.telefone}"
            """
            retorno = execute_query(conn, select_query)
            if len(retorno) == 0:
                data_atual = datetime.datetime.now()
                nome = dep.nome
                nome_formatado = nome.title()
                insert_query = f"""
                    insert into dependentes (idpai, nome, datanas, telefone, email, membro, presenca, dataCadastro, dataAlteracao, ativo)
                    VALUES({dep.idpai}, "{nome_formatado}", "{dep.datanas}", "{dep.telefone}", "{dep.email}", {dep.membro}, 0, "{data_atual}", "{data_atual}", 1)
                """
                execute_insert(conn, insert_query)
                select_query = f"""
                    select d.id, d.nome
                    from dependentes d
                    where d.nome = "{dep.nome}" and d.idpai = "{dep.idpai}" and d.ativo = 1
                """
                retorno = execute_query(conn, select_query)
                for dependente in retorno:
                    criaqrcode(dependente[0], dependente[1])
                    #envia_email("gabrielealmenezes@gmail.com", dependente[1], dependente[0])
                registrar_log(conn, retorno[0][0], 'Criar', 'Dependente', insert_query, request.client.host, request.headers.get("user-agent"))
                return {"detail": "registration created"} 
            else:
                raise HTTPException(status_code=409, detail="registration already exists in main registration")
        else:
            raise HTTPException(status_code=409, detail="registration already exists")
    except HTTPException:
        raise
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()