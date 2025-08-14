import csv, requests

def cria_visitante(body):
    try:
        response = requests.post('http://musical.dominio.com.br/inscricao', json=body)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print(e) 
        

def read_csv_file(file_path):
    """Reads a CSV file and prints its contents row by row."""
    try:
        cabec = True
        with open(file_path, 'r', newline='') as file:
            csv_reader = csv.reader(file, delimiter=',')
            for row in csv_reader:
                if cabec:
                    cabec = False
                    continue

                # Verifica se a linha tem colunas suficientes
                if len(row) < 5:
                    print(f"Linha ignorada (colunas insuficientes): {row}")
                    continue

                try:
                    nomecompleto = row[1].strip()
                    datanascimento = row[2][6:10] + '-' + row[2][3:5] + '-' + row[2][0:2]
                    fone = row[4].strip()
                    email = row[3].strip()
                    membro = 1

                    payload = {
                        'nome': nomecompleto,
                        'datanas': datanascimento,
                        'telefone': fone,
                        'email': email,
                        'membro': membro
                    }

                    print(payload)
                    cria_visitante(payload)

                except Exception as e:
                    print(f"Erro ao processar linha: {row} - {e}")

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
         print(f"An error occurred: {e}")


file_path = 'Formulario.csv'
read_csv_file(file_path)
