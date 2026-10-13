import os
from PIL import Image
from customtkinter import CTkImage


# --- Cores do sistema ---
COR_FUNDO_APP = "#1F1D2B"
COR_MENU = "#252836"
COR_CARD = "#2A2D3E"
COR_INPUT = "#1F1D2B"

COR_BOTAO_ROXO = "#6C63FF"
COR_HOVER_ROXO = "#5A52D5"
COR_BORDA_NEON = "#5A52D5"

COR_VERMELHO = "#C9302C"
COR_HOVER_VERMELHO = "#AC2925"

COR_TEXTO = "#FFFFFF"
COR_TEXTO_SEC = "#A0A0A0"

COR_SUCESSO = "#34d399"
COR_ERRO = "#f87171"
COR_VIP = "#FFD700"
COR_ANUAL = "#38bdf8"


# --- Imagem de fundo ---
_CAMINHO_FUNDO = os.path.join("assets", "fundo.jpg")


def carregar_fundo(tamanho):
    """Carrega a imagem de fundo no tamanho (largura, altura) informado.

    Retorna None se a imagem não existir, para não quebrar a aplicação.
    """
    if not os.path.exists(_CAMINHO_FUNDO):
        return None

    imagem_pil = Image.open(_CAMINHO_FUNDO)
    return CTkImage(light_image=imagem_pil, dark_image=imagem_pil, size=tamanho)
