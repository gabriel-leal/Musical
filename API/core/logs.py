# log.py
import datetime

def registrar_log(conn, usuario_id, acao, tipo, detalhes, ip=None, navegador=None):
    query = """
        INSERT INTO logs (usuario_id, acao, tipo, detalhes, data_hora, ip, navegador)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        usuario_id,
        acao,
        tipo,
        detalhes,
        datetime.datetime.now(),
        ip,
        navegador
    )
    with conn.cursor() as cursor:
        cursor.execute(query, valores)
        conn.commit()
