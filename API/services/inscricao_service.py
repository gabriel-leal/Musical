from fastapi import HTTPException
from core.connectmySQL import create_connect, execute_query, execute_insert
import datetime
from core.geraqrcode import criaqrcode
from core.logs import registrar_log

def inscricao(inscricao, banco, request):
    try:
        conn = create_connect(banco)
        select_query = f"""
            select i.id, i.nome
            from inscricao i
            where (i.telefone = "{inscricao.telefone}" or i.email = "{inscricao.email}")
            and i.ativo = 1
        """
        retorno = execute_query(conn, select_query)
        if len(retorno) == 0:
            select_query = f"""
            select d.id, d.nome
            from dependentes d
            where d.telefone = "{inscricao.telefone}"
            """
            retorno = execute_query(conn, select_query)
            if len(retorno) == 0:
                data_atual = datetime.datetime.now()
                nome = inscricao.nome
                nome_formatado = nome.title()
                insert_query = f"""
                    insert into inscricao (nome, datanas, telefone, email, membro, presenca, dataCadastro, dataAlteracao, ativo)
                    VALUES("{nome_formatado}", "{inscricao.datanas}", "{inscricao.telefone}", "{inscricao.email}", "{inscricao.membro}", 0, "{data_atual}", "{data_atual}", 1)
                """
                execute_insert(conn, insert_query) 
                select_query = f"""
                    select i.id, i.nome
                    from inscricao i
                    where i.telefone = "{inscricao.telefone}" and i.email = "{inscricao.email}"
                    and i.ativo = 1
                """
                retorno = execute_query(conn, select_query)
                criaqrcode(retorno[0][0], retorno[0][1])
                #envia_email("gabrielealmenezes@gmail.com", inscricao.nome, retorno[0][0])
                registrar_log(conn, retorno[0][0], 'Criar', 'Inscrição', insert_query, request.client.host, request.headers.get("user-agent"))
                return {"detail": "registration created", "id": retorno[0][0]} 
            else:
                raise HTTPException(status_code=409, detail="registration already exists in dependents")
        else:
            select_query = f"""
                select i.id, i.nome
                from inscricao i
                where i.telefone = "{inscricao.telefone}" and i.email = "{inscricao.email}"
                and i.ativo = 1
            """
            retorno = execute_query(conn, select_query)
            if len(retorno) > 0:
                raise HTTPException(status_code=409, detail={"message": "login in registration","value": retorno[0][0]})
            else:
                raise HTTPException(status_code=409, detail="registration already exists")
    except HTTPException:
        raise
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        
def deletapessoa(id, banco, user_ip, user_agent):
    try:
        conn = create_connect(banco)
        select_query = f"""
            SELECT i.id, i.nome
            FROM inscricao i
            WHERE i.id = {id}
        """
        retorno = execute_query(conn, select_query)
        if len(retorno) > 0:
            data_atual = datetime.datetime.now()
            update_query = f"""
                UPDATE inscricao i
                SET i.ativo = 0, i.dataAlteracao = '{data_atual}'
                WHERE i.id = {id}
            """
            execute_query(conn, update_query)
            execute_query(conn, 'commit')
            # registra log
            registrar_log(conn, retorno[0][0], 'Desativar', 'Inscricao', update_query, user_ip, user_agent)
            return {"detail": "delete Successful"}
        else:
            select_query = f"""
            SELECT d.id, d.nome
            FROM dependentes d
            WHERE d.id = {id}
            """
            retorno = execute_query(conn, select_query)
            if len(retorno) > 0:
                data_atual = datetime.datetime.now()
                update_query = f"""
                    UPDATE dependentes d
                    SET d.ativo = 0, d.dataAlteracao = '{data_atual}'
                    WHERE d.id = {id}
                """
                execute_query(conn, update_query)
                execute_query(conn, 'commit')
                # registra log
                registrar_log(conn, retorno[0][0], 'Desativar', 'Dependente', update_query, user_ip, user_agent)
                return {"detail": "delete Successful"}
            else:
                raise HTTPException(status_code=409, detail="pessoa not exist")
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        
def listainscricoes(id, banco):
    try:
        conn = create_connect(banco)
        select_query = f"""
        select i.id, i.nome, i.datanas, i.telefone, i.email, i.membro
        from inscricao i 
        where i.id = {id}
        and i.ativo = 1
        """        
        pessoa = execute_query(conn, select_query)
        content = []
        for dado in pessoa:
            content.append({"id": dado[0],"nomecompleto": dado[1], "datanas": dado[2], "telefone": dado[3], "email": dado[4], "membro": dado[5]})
        select_query = f"""
        select d.id, d.nome, d.datanas, d.telefone, d.email, d.membro
        from dependentes d 
        where d.idpai = {id}
        and d.ativo = 1
        """        
        dependentes = execute_query(conn, select_query)
        for dado in dependentes:
            content.append({"id": dado[0],"nomecompleto": dado[1], "datanas": dado[2], "telefone": dado[3], "email": dado[4], "membro": dado[5]})
        res = {"size": len(pessoa+dependentes) ,"content": content}
    except HTTPException:
        raise
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        return res
    
######### ordem por nome crescente    
# def totalinscricoes(banco):
#     try:
#         conn = create_connect(banco)
#         # Buscar inscritos principais
#         select_query = """
#         SELECT i.id, i.nome, i.datanas, i.telefone, i.email, i.membro, i.presenca
#         FROM inscricao i
#         Where i.ativo = 1
#         """
#         pessoas = execute_query(conn, select_query)
#         # Buscar dependentes
#         select_query = """
#         SELECT d.id, d.nome, d.datanas, d.telefone, d.email, d.membro, d.idpai, d.presenca
#         FROM dependentes d
#         where d.ativo = 1
#         """
#         dependentes = execute_query(conn, select_query)
#         # Criar um dicionário para associar dependentes ao seu responsável
#         dependentes_por_pai = {}
#         for d in dependentes:
#             idpai = d[6]  # idpai (chave estrangeira que referencia a inscrição principal)
#             if idpai not in dependentes_por_pai:
#                 dependentes_por_pai[idpai] = []
#             dependentes_por_pai[idpai].append({"id": d[0], "nomecompleto": d[1], "datanas": d[2], "telefone": d[3], "email": d[4], "membro": d[5], "presenca": d[7], "idpai": idpai})
#         # Construir a lista final intercalando pessoa e seus dependentes
#         content = []
#         for p in sorted(pessoas, key=lambda x: x[1]):  # Ordena pessoas pelo nome
#             content.append({"id": p[0], "nomecompleto": p[1], "datanas": p[2], "telefone": p[3], "email": p[4], "membro": p[5], "presenca": p[6]})
#             if p[0] in dependentes_por_pai:
#                 for d in sorted(dependentes_por_pai[p[0]], key=lambda x: x["nomecompleto"]):  # Ordena dependentes pelo nome
#                     content.append(d)
#         res = {"size": len(content), "content": content}
#     except Exception as err:
#         print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")
#     finally:
#         conn.close()
#         return res
######### ordem por id decrescente  
def totalinscricoes(banco):
    try:
        conn = create_connect(banco)
        # Buscar inscritos principais
        select_query = """
        SELECT i.id, i.nome, i.datanas, i.telefone, i.email, i.membro, i.presenca
        FROM inscricao i
        WHERE i.ativo = 1
        """
        pessoas = execute_query(conn, select_query)

        # Buscar dependentes
        select_query = """
        SELECT d.id, d.nome, d.datanas, d.telefone, d.email, d.membro, d.idpai, d.presenca
        FROM dependentes d
        WHERE d.ativo = 1
        """
        dependentes = execute_query(conn, select_query)

        # Criar um dicionário para associar dependentes ao seu responsável
        dependentes_por_pai = {}
        for d in dependentes:
            idpai = d[6]
            if idpai not in dependentes_por_pai:
                dependentes_por_pai[idpai] = []
            dependentes_por_pai[idpai].append({
                "id": d[0],
                "nomecompleto": d[1],
                "datanas": d[2],
                "telefone": d[3],
                "email": d[4],
                "membro": d[5],
                "presenca": d[7],
                "idpai": idpai
            })

        # Construir a lista final intercalando pessoa e seus dependentes
        content = []
        for p in sorted(pessoas, key=lambda x: x[0], reverse=True):  # Ordena pessoas pelo ID decrescente
            content.append({
                "id": p[0],
                "nomecompleto": p[1],
                "datanas": p[2],
                "telefone": p[3],
                "email": p[4],
                "membro": p[5],
                "presenca": p[6]
            })
            if p[0] in dependentes_por_pai:
                for d in sorted(dependentes_por_pai[p[0]], key=lambda x: x["id"], reverse=True):  # Dependentes pelo ID decrescente
                    content.append(d)

        res = {"size": len(content), "content": content}
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        return res
    
    
def totalpresenca(banco):
    try:
        conn = create_connect(banco)

        queryselect = f"""
            select count(*) total 
            from inscricao
            where presenca = 1
            """
            
        totpresenca = 0
        presencas = execute_query(conn, queryselect)
        ret = {}
        if(len(presencas) > 0):
            for presenca in presencas:        
                totpresenca += int(presenca[0])
            
            queryselect = f"""
            select count(*) total 
            from dependentes
            where presenca = 1
            """
            dependentes = execute_query(conn, queryselect)
            if(len(dependentes) > 0):
                for dependente in dependentes:        
                    totpresenca += int(dependente[0])
            ret['totalpresenca'] = totpresenca
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()
        return ret
    
    
def mudapresenca(id, banco):
    try:
        conn = create_connect(banco)

        queryselect = f"""
                select i.id, i.nome, i.presenca 
                from inscricao i
                where i.id = {id} and i.ativo = 1
            """
        inscricao = execute_query(conn, queryselect)
        if len(inscricao) > 0:
            presenca = 0
            if inscricao[0][2] == 0:
                presenca = 1
            queryedit = f"""
                update inscricao
                set presenca = {presenca}
                where id = {id} 
            """
            execute_query(conn, queryedit)
            execute_query(conn, 'commit')
        else :
            queryselect = f"""
                select d.id, d.nome, d.presenca 
                from dependentes d
                where d.id = {id} and d.ativo = 1
            """
            dependentes = execute_query(conn, queryselect)
            if len(dependentes) > 0:
                presenca = 0
                if dependentes[0][2] == 0:
                    presenca = 1
                queryedit = f"""
                    update dependentes
                    set presenca = {presenca}
                    where id = {id}
                """
                execute_query(conn, queryedit)
                execute_query(conn, 'commit')
    except Exception as err:
        print(f"Ocorreu um erro do tipo {type(err).__name__}: {err}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        conn.close()