import os
from PIL import Image
from customtkinter import CTkImage


# --- Cores do sistema (paleta quente combinando com a imagem de fundo) ---
COR_FUNDO_APP = "#1A1410"          # Fundo escuro com toque quente (marrom profundo)
COR_MENU = "#241A14"               # Menu lateral
COR_CARD = "#2A1F18"               # Cards
COR_INPUT = "#1A1410"              # Inputs

# Botões principais (laranja queimado)
COR_BOTAO = "#E8734A"
COR_BOTAO_HOVER = "#C25B3A"
COR_BORDA_NEON = "#C25B3A"

# Botões de perigo (vermelho escuro)
COR_VERMELHO = "#C9302C"
COR_HOVER_VERMELHO = "#AC2925"

# Textos
COR_TEXTO = "#FFFFFF"
COR_TEXTO_SEC = "#C4B5A8"          # Cinza quente

# Semânticas
COR_SUCESSO = "#4ADE80"
COR_ERRO = "#F87171"
COR_VIP = "#FFD700"
COR_ANUAL = "#FBBF24"              # Âmbar (combina com quente)
COR_DOURADO = "#F5A623"            # Laranja dourado


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
