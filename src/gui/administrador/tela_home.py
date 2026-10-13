import customtkinter as ctk
from src.gui.componentes.tema import (
    COR_FUNDO_APP, COR_CARD, COR_TEXTO, COR_TEXTO_SEC,
    COR_BOTAO, COR_BOTAO_HOVER, COR_DOURADO, COR_VIP,
    COR_SUCESSO, carregar_fundo,
)


class TelaHome(ctk.CTkFrame):
    def __init__(self, master, servico):
        super().__init__(master, fg_color=COR_FUNDO_APP)
        self.servico = servico

        # --- IMAGEM DE FUNDO (cobre a tela toda) ---
        self._fundo_img = carregar_fundo((1100, 650))
        if self._fundo_img is not None:
            self._label_fundo = ctk.CTkLabel(self, image=self._fundo_img, text="")
            self._label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # --- OVERLAY ESCURO (pra dar contraste sem esconder a imagem) ---
        # Usamos um frame com cor escura, mas SEM cobrir 100% — deixamos os
        # cards aparecerem por cima.
        # Nota: CTk não tem opacidade real. O que fazemos é usar cor sólida
        # nos cards e deixar os vãos mostrando a imagem.

        # Título
        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="🎢 Painel do Parque",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=COR_TEXTO,
            fg_color="transparent"
        )
        self.lbl_titulo.pack(pady=(25, 25))

        # --- CARDS DE KPI ---
        self.frame_cards = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_cards.pack(pady=10, padx=30, fill="x")
        self.frame_cards.grid_columnconfigure((0, 1, 2), weight=1)

        card_vis = self._criar_card_kpi("👤 Visitantes", "0", COR_BOTAO)
        card_vis.grid(row=0, column=0, padx=10, sticky="nsew")
        self.lbl_num_visitantes = card_vis._valor_label

        card_atr = self._criar_card_kpi("✨ Atrações", "0", COR_DOURADO)
        card_atr.grid(row=0, column=1, padx=10, sticky="nsew")
        self.lbl_num_atracoes = card_atr._valor_label

        card_st = self._criar_card_kpi("⚙️ Status", "Ativo", COR_SUCESSO, tamanho_valor=32)
        card_st.grid(row=0, column=2, padx=10, sticky="nsew")
        self.lbl_status = card_st._valor_label

        # --- FRAME CENTRAL ---
        self.frame_central = ctk.CTkFrame(
            self, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BOTAO_HOVER
        )
        self.frame_central.pack(pady=(25, 20), padx=30, fill="both", expand=True)

        self.frame_central.grid_columnconfigure(0, weight=1)
        self.frame_central.grid_columnconfigure(1, weight=1)
        self.frame_central.grid_rowconfigure(0, weight=1)

        # LADO ESQUERDO: Capacidade
        frame_esq = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        frame_esq.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            frame_esq, text="📊 Capacidade do Parque",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO
        ).pack(pady=(10, 20))

        self.barra_capacidade = ctk.CTkProgressBar(
            frame_esq, orientation="horizontal", height=18,
            progress_color=COR_BOTAO
        )
        self.barra_capacidade.pack(fill="x", padx=20)
        self.barra_capacidade.set(0.0)

        self.lbl_detalhe_cap = ctk.CTkLabel(
            frame_esq, text="0 / 500 Visitantes Máx.",
            font=ctk.CTkFont(size=13),
            text_color=COR_TEXTO_SEC
        )
        self.lbl_detalhe_cap.pack(pady=10)

        # LADO DIREITO: Filas
        frame_dir = ctk.CTkFrame(self.frame_central, fg_color="transparent")
        frame_dir.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        ctk.CTkLabel(
            frame_dir, text="⏳ Filas Mais Longas",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COR_TEXTO
        ).pack(pady=(10, 15))

        self.frame_mini_filas = ctk.CTkScrollableFrame(
            frame_dir, fg_color="transparent", height=150
        )
        self.frame_mini_filas.pack(fill="both", expand=True)
        self.frame_mini_filas._scrollbar.grid_forget()

        self.atualizar_dashboard()

    def _criar_card_kpi(self, titulo, valor_inicial, cor_valor, tamanho_valor=48):
        """Cria um card de KPI reutilizável."""
        card = ctk.CTkFrame(
            self.frame_cards,
            corner_radius=15,
            fg_color=COR_CARD,       # fundo sólido escuro, esconde a imagem atrás
            border_width=1,
            border_color=COR_BOTAO_HOVER
        )

        ctk.CTkLabel(
            card, text=titulo,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=COR_TEXTO_SEC
        ).pack(pady=(18, 5))

        card._valor_label = ctk.CTkLabel(
            card, text=valor_inicial,
            font=ctk.CTkFont(size=tamanho_valor, weight="bold"),
            text_color=cor_valor
        )
        card._valor_label.pack(pady=(0, 18))

        return card

    def atualizar_dashboard(self):
        try:
            visitantes = self.servico.listar_visitantes()
            total = len(visitantes)
            self.lbl_num_visitantes.configure(text=str(total))
            capacidade_max = 500
            self.barra_capacidade.set(total / capacidade_max)
            self.lbl_detalhe_cap.configure(text=f"{total} / {capacidade_max} Visitantes Máx.")
        except Exception:
            self.lbl_num_visitantes.configure(text="0")
            self.barra_capacidade.set(0)

        try:
            atracoes = self.servico.listar_atracoes()
            self.lbl_num_atracoes.configure(text=str(len(atracoes)))

            for widget in self.frame_mini_filas.winfo_children():
                widget.destroy()

            if not atracoes:
                ctk.CTkLabel(
                    self.frame_mini_filas,
                    text="Nenhuma atração registada.",
                    text_color=COR_TEXTO_SEC
                ).pack(pady=20, anchor="w", padx=10)
                return

            todas_reservas = self.servico.listar_reservas() if hasattr(self.servico, 'listar_reservas') else []
            reservas_ativas = [r for r in todas_reservas if getattr(r, 'status', '') == "Ativa"]

            def tamanho_real_fila(atracao):
                return len([r for r in reservas_ativas if getattr(r, 'nome_atracao', '') == atracao.nome])

            atracoes_ordenadas = sorted(atracoes, key=tamanho_real_fila, reverse=True)

            for a in atracoes_ordenadas:
                tamanho = tamanho_real_fila(a)

                mini_card = ctk.CTkFrame(self.frame_mini_filas, fg_color="transparent")
                mini_card.pack(fill="x", pady=5, anchor="w")

                if hasattr(a, 'aceita_prioridade') and a.aceita_prioridade:
                    texto_tag = "(Prioridade)"
                    cor_tag = COR_VIP
                else:
                    texto_tag = "(Comum)"
                    cor_tag = COR_TEXTO_SEC

                ctk.CTkLabel(
                    mini_card, text=a.nome,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    text_color=COR_TEXTO
                ).pack(side="left", padx=(10, 5))

                ctk.CTkLabel(
                    mini_card, text=texto_tag,
                    font=ctk.CTkFont(size=12),
                    text_color=cor_tag
                ).pack(side="left", padx=(0, 5))

                cor_texto = COR_VIP if tamanho > 0 else COR_TEXTO_SEC
                ctk.CTkLabel(
                    mini_card, text=f"{tamanho} à espera",
                    font=ctk.CTkFont(size=14),
                    text_color=cor_texto
                ).pack(side="right", padx=(5, 10))

        except Exception as e:
            print(f"Erro ao atualizar filas: {e}")
            self.lbl_num_atracoes.configure(text="0")
