import customtkinter as ctk
from src.gui.componentes.tema import (
    COR_FUNDO_APP, COR_CARD, COR_TEXTO, COR_TEXTO_SEC,
    COR_BOTAO, COR_BOTAO_HOVER, COR_BORDA_NEON,
    COR_SUCESSO, COR_VIP, COR_ANUAL, carregar_fundo,
)


class TelaHomeVisitante(ctk.CTkFrame):
    def __init__(self, master, servico, cpf_visitante):
        super().__init__(master, fg_color=COR_FUNDO_APP)

        self.servico = servico
        self.cpf_visitante = cpf_visitante

        # --- Imagem de fundo ---
        self._fundo_img = carregar_fundo((1100, 650))
        if self._fundo_img is not None:
            self._label_fundo = ctk.CTkLabel(self, image=self._fundo_img, text="")
            self._label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # Buscar dados do visitante logado
        visitante = self.servico.buscar_visitante_por_cpf(self.cpf_visitante)
        nome = visitante.nome.split()[0] if visitante else "Visitante"
        passe = str(getattr(visitante, 'tipo_passe', 'Normal')).upper()

        # --- TÍTULO E BOAS-VINDAS ---
        self.lbl_boas_vindas = ctk.CTkLabel(
            self, text=f"💀Olá, {nome}!💀",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=COR_TEXTO
        )
        self.lbl_boas_vindas.pack(pady=(30, 5), anchor="w", padx=30)

        self.lbl_sub = ctk.CTkLabel(
            self, text="Bem-vindo ao seu portal. O que vamos fazer hoje?",
            font=ctk.CTkFont(size=16), text_color=COR_TEXTO_SEC
        )
        self.lbl_sub.pack(pady=(0, 30), anchor="w", padx=30)

        # --- CARDS DE RESUMO ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(fill="x", padx=20, pady=10)

        # Card 1: Status do Passe
        self.card_passe = ctk.CTkFrame(
            self.frame_cards, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BORDA_NEON
        )
        self.card_passe.pack(side="left", fill="both", expand=True, padx=10)

        ctk.CTkLabel(
            self.card_passe, text="🎟️ Seu Passe",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COR_TEXTO_SEC
        ).pack(pady=(20, 5))

        cor_passe = COR_VIP if "VIP" in passe else (COR_ANUAL if "ANUAL" in passe else COR_TEXTO)
        ctk.CTkLabel(
            self.card_passe, text=passe,
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=cor_passe
        ).pack(pady=(0, 20))

        # Card 2: Reservas Ativas
        reservas = []
        if hasattr(self.servico, 'listar_reservas_do_visitante'):
            reservas = self.servico.listar_reservas_do_visitante(self.cpf_visitante)
        ativas = [r for r in reservas if getattr(r, 'status', '') == "Ativa"]

        self.card_reservas = ctk.CTkFrame(
            self.frame_cards, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BORDA_NEON
        )
        self.card_reservas.pack(side="left", fill="both", expand=True, padx=10)

        ctk.CTkLabel(
            self.card_reservas, text="🎡 Reservas Ativas",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COR_TEXTO_SEC
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            self.card_reservas, text=str(len(ativas)),
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=COR_SUCESSO
        ).pack(pady=(0, 20))

        # --- BANNER DE DICA ---
        self.banner = ctk.CTkFrame(
            self, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BORDA_NEON
        )
        self.banner.pack(fill="x", padx=30, pady=30)

        ctk.CTkLabel(
            self.banner, text="Dica Magia Premium ✨",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO
        ).pack(pady=(20, 5))
        ctk.CTkLabel(
            self.banner,
            text="Use o menu lateral para agendar suas próximas atrações e evitar filas físicas!\nAcompanhe o status e cancele reservas a qualquer momento em 'Minhas Filas'.",
            font=ctk.CTkFont(size=14), text_color=COR_TEXTO_SEC, justify="center"
        ).pack(pady=(0, 20))
