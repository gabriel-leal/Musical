import schedule
import time
from send_whatsapp import envia_whatsapp
from send_email import envia_erro
import requests

def lista():
    url = "http://000.000.000.000:8000/instance/connectionState/whatsappapi"
    headers = {"apikey": "chave-evolution"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        state = data.get("instance", {}).get("state")
        print("Estado:", state)
        if state == 'open':
            print('funcionando')
            try:
                envia_whatsapp()
            except Exception as e:
                print(f"Erro ao enviar WhatsApp: {e}")
                return {f"Erro ao enviar WhatsApp: {e}"}
        else:
            print('erro')
            envia_erro(data, 'email@gmail.com')
    else:
        envia_erro("Erro ao acessar a API: " + response.status_code, 'email@gmail.com')
        print("Erro ao acessar a API:", response.status_code)
        return {"Erro ao acessar a API:", response.status_code}
    

    
    
schedule.every(30).minutes.do(lista)

while True:
    schedule.run_pending()
    time.sleep(60)