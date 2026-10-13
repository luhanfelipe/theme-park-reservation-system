import customtkinter as ctk
from src.gui.componentes.tema import (
    COR_FUNDO_APP, COR_CARD, COR_INPUT, COR_TEXTO, COR_TEXTO_SEC,
    COR_BOTAO, COR_BOTAO_HOVER, COR_BORDA_NEON,
    COR_SUCESSO, COR_ERRO, COR_VIP,
)


class TelaReservas(ctk.CTkFrame):
    def __init__(self, master, servico, cpf_visitante, comando_voltar):
        super().__init__(master, fg_color=COR_FUNDO_APP)

        self.servico = servico
        self.cpf_visitante = cpf_visitante

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, text="⬅ Voltar ao Menu", width=120, height=32,
            fg_color="transparent", border_width=1, border_color=COR_BORDA_NEON,
            hover_color=COR_CARD, text_color=COR_TEXTO, command=comando_voltar
        )
        self.btn_voltar.pack(anchor="nw", padx=20, pady=(20, 0))

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="🎡 Reservar Atração",
            font=ctk.CTkFont(size=24, weight="bold"), text_color=COR_TEXTO
        )
        self.lbl_titulo.pack(pady=(15, 5))

        self.lbl_subtitulo = ctk.CTkLabel(
            self, text="Escolha sua próxima aventura e garanta seu lugar!",
            font=ctk.CTkFont(size=14), text_color=COR_TEXTO_SEC
        )
        self.lbl_subtitulo.pack(pady=(0, 15))

        # --- FORMULÁRIO DE RESERVA ---
        self.frame_form = ctk.CTkFrame(
            self, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BORDA_NEON
        )
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.lbl_atracao = ctk.CTkLabel(self.frame_form, text="Selecione a Atração:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_atracao.grid(row=0, column=0, sticky="w", padx=20, pady=(15, 2))

        self.combo_atracao = ctk.CTkComboBox(
            self.frame_form, values=["Nenhuma atração disponível"], width=250,
            fg_color=COR_INPUT, border_color="#374151",
            button_color=COR_BOTAO, button_hover_color=COR_BOTAO_HOVER
        )
        self.combo_atracao.grid(row=1, column=0, padx=20, pady=(0, 15))

        self.lbl_horario = ctk.CTkLabel(self.frame_form, text="Horário Desejado:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_horario.grid(row=0, column=1, sticky="w", padx=20, pady=(15, 2))

        horarios = ["10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
        self.combo_horario = ctk.CTkComboBox(
            self.frame_form, values=horarios, width=150,
            fg_color=COR_INPUT, border_color="#374151",
            button_color=COR_BOTAO, button_hover_color=COR_BOTAO_HOVER
        )
        self.combo_horario.grid(row=1, column=1, padx=20, pady=(0, 15))

        self.btn_reservar = ctk.CTkButton(
            self.frame_form, text=" ✓ Confirmar Reserva",
            fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"), height=38,
            command=self.efetuar_reserva
        )
        self.btn_reservar.grid(row=1, column=2, padx=20, pady=(0, 15))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=2, column=0, columnspan=3, pady=(0, 10))

        # --- CATÁLOGO ---
        self.lbl_catalogo = ctk.CTkLabel(self, text="🎢 Atrações Disponíveis no Parque", font=ctk.CTkFont(size=18, weight="bold"), text_color=COR_TEXTO)
        self.lbl_catalogo.pack(pady=(25, 10))

        self.frame_lista = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)
        self.frame_lista._scrollbar.grid_forget()

        self.carregar_dados()

    def carregar_dados(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        atracoes = self.servico.listar_atracoes()

        if not atracoes:
            self.combo_atracao.set("Sem atrações")
            lbl_vazio = ctk.CTkLabel(self.frame_lista, text="Nenhuma atração cadastrada pelo administrador no momento.", font=ctk.CTkFont(slant="italic"), text_color=COR_TEXTO_SEC)
            lbl_vazio.pack(pady=20)
            return

        nomes_atracoes = [a.nome for a in atracoes]
        self.combo_atracao.configure(values=nomes_atracoes)
        self.combo_atracao.set(nomes_atracoes[0])

        for a in atracoes:
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, fg_color=COR_CARD, border_width=1, border_color="#374151")
            card.pack(pady=6, fill="x")

            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(10, 2))

            lbl_nome = ctk.CTkLabel(frame_topo, text=a.nome, font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO)
            lbl_nome.pack(side="left")

            aceita_passe = getattr(a, 'aceita_prioridade', True)
            if aceita_passe:
                lbl_badge = ctk.CTkLabel(frame_topo, text=" ✨ VIP / ANUAL ", font=ctk.CTkFont(size=11, weight="bold"), text_color=COR_VIP, fg_color="#4B4000", corner_radius=6)
                lbl_badge.pack(side="right")

            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(2, 10))

            tipo = getattr(a, 'tipo', 'Atração')
            info_texto = f"Tipo: {tipo}  •  Capacidade: {a.capacidade} pessoas  •  Idade Mínima: {a.idade_minima} anos"

            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=ctk.CTkFont(size=12), text_color=COR_TEXTO_SEC)
            lbl_info.pack(side="left")

    def efetuar_reserva(self):
        nome_atracao = self.combo_atracao.get()
        horario = self.combo_horario.get()

        if nome_atracao == "Sem atrações" or nome_atracao == "Nenhuma atração disponível":
            return

        resultado = self.servico.criar_reserva(self.cpf_visitante, nome_atracao, horario)

        if isinstance(resultado, str) and "Erro" in resultado:
            self.lbl_mensagem.configure(text=f"⚠ {resultado}", text_color=COR_ERRO)
        else:
            self.lbl_mensagem.configure(text=f"✓ Reserva confirmada para {horario} com sucesso!", text_color=COR_SUCESSO)
