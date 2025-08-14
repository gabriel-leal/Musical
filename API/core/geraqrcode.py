from fastapi import HTTPException
import qrcode
from PIL import Image, ImageDraw, ImageOps, ImageEnhance
import unicodedata
import re
import os


# def formatar_nome(nome: str) -> str:
#     nome = unicodedata.normalize('NFKD', nome).encode('ASCII', 'ignore').decode()
#     nome = re.sub(r'\s+', ' ', nome).strip()
#     partes = nome.split(' ')
#     if len(partes) < 2:
#         raise HTTPException(status_code=400, detail="Nome deve conter pelo menos dois nomes.")
#     return f"{partes[0]}_{partes[1]}"


def preparar_logo_fundo_branco_simples(logo: Image.Image, tamanho: int, margem_branca: int) -> Image.Image:
    # Converte para escala de cinza e melhora contraste
    logo = logo.convert("L")
    enhancer = ImageEnhance.Contrast(logo)
    logo = enhancer.enhance(2.0)

    # Inverte se necessário (fundo escuro vira branco)
    logo = ImageOps.invert(logo).convert("RGB")

    # Redimensiona
    logo = logo.resize((tamanho, tamanho), Image.LANCZOS)

    # Cria fundo branco ao redor da logo
    fundo = Image.new("RGB", (tamanho + 2*margem_branca, tamanho + 2*margem_branca), (255, 255, 255))
    fundo.paste(logo, (margem_branca, margem_branca))

    return fundo

def criaqrcode(id: int, nome: str, caminho_logo: str = "./logo.png"):
    try:
        # Criar o QR code
        qr = qrcode.QRCode(
            version=2,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(str(id))
        qr.make(fit=True)

        img_qr = qr.make_image(fill_color="black", back_color="white").convert('RGB')

        # Inserir logo no centro
        if os.path.exists(caminho_logo):
            logo_original = Image.open(caminho_logo)
            qr_width, qr_height = img_qr.size

            proporcao_logo = 0.20
            logo_size = int(qr_width * proporcao_logo)
            margem_branca = int(logo_size * 0.003)

            logo = preparar_logo_fundo_branco_simples(logo_original, logo_size, margem_branca)

            pos = ((qr_width - logo.width) // 2, (qr_height - logo.height) // 2)
            img_qr.paste(logo, pos)

        else:
            print("Logo não encontrada. Continuando sem logo.")

        os.makedirs("./qrcodes", exist_ok=True)
        img_qr.save(f"./qrcodes/{id}.png")
        try:
            img_qr.save(f"../../html/qrcodes/{id}.png")
        except:
            print('não está no servidor')
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar o QR Code com logo")
    
#criaqrcode(5, "teste", "./qrcodes/logo.png")
