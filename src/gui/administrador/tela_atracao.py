import customtkinter as ctk
from src.gui.componentes.tema import (
    COR_FUNDO_APP, COR_CARD, COR_INPUT, COR_TEXTO, COR_TEXTO_SEC,
    COR_BOTAO, COR_BOTAO_HOVER, COR_BORDA_NEON,
    COR_SUCESSO, COR_ERRO, COR_VIP, carregar_fundo,
)


class TelaAtracao(ctk.CTkScrollableFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master, fg_color=COR_FUNDO_APP)

        self._scrollbar.grid_forget()
        self.servico = servico

        # --- Imagem de fundo ---
        self._fundo_img = carregar_fundo((1100, 650))
        if self._fundo_img is not None:
            self._label_fundo = ctk.CTkLabel(self, image=self._fundo_img, text="")
            self._label_fundo.place(x=0, y=0, relwidth=1, relheight=1)

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, text="⬅ Voltar", width=80, height=32,
            fg_color="transparent", border_width=1,
            border_color=COR_BORDA_NEON, hover_color=COR_CARD,
            text_color=COR_TEXTO, command=comando_voltar
        )
        self.btn_voltar.pack(anchor="nw", padx=20, pady=(20, 0))

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Cadastro de Atrações",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=COR_TEXTO
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # --- FORMULÁRIO ---
        self.frame_form = ctk.CTkFrame(
            self, corner_radius=15, fg_color=COR_CARD,
            border_width=1, border_color=COR_BORDA_NEON
        )
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # --- LINHA 0/1: Nome e Capacidade ---
        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome da Atração:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: Vendaval Eterno", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 10))

        self.lbl_capacidade = ctk.CTkLabel(self.frame_form, text="Capacidade Max.:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_capacidade.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.entry_capacidade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 20", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_capacidade.grid(row=1, column=1, padx=15, pady=(0, 10))

        # --- LINHA 2/3: Tipo e Idade ---
        self.lbl_tipo = ctk.CTkLabel(self.frame_form, text="Tipo de Atração:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_tipo.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))
        self.combo_tipo = ctk.CTkComboBox(
            self.frame_form,
            values=["Montanha-Russa", "Simulador", "Teatro", "Brinquedo Infantil", "Carrossel", "Roda-Gigante", "Show"],
            width=220, fg_color=COR_INPUT, border_color="#374151",
            button_color=COR_BOTAO, button_hover_color=COR_BOTAO_HOVER
        )
        self.combo_tipo.grid(row=3, column=0, padx=15, pady=(0, 10))
        self.combo_tipo.set("Montanha-Russa")

        self.lbl_idade = ctk.CTkLabel(self.frame_form, text="Idade Mínima (anos):", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_idade.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 2))
        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 12", width=220, fg_color=COR_INPUT, border_color="#374151")
        self.entry_idade.grid(row=3, column=1, padx=15, pady=(0, 10))

        # --- LINHA 4/5: Horário ---
        self.lbl_horario = ctk.CTkLabel(self.frame_form, text="Horário de Funcionamento:", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_horario.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 2))
        self.entry_horario = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 10h-18h", width=470, fg_color=COR_INPUT, border_color="#374151")
        self.entry_horario.grid(row=5, column=0, columnspan=2, padx=15, pady=(0, 10))

        # --- LINHA 6/7: Aceita Passe ---
        self.lbl_prioridade = ctk.CTkLabel(self.frame_form, text="Aceita Passe VIP / Anual?", font=ctk.CTkFont(size=12, weight="bold"), text_color=COR_TEXTO_SEC)
        self.lbl_prioridade.grid(row=6, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 2))

        self.combo_prioridade = ctk.CTkComboBox(
            self.frame_form, values=["Sim", "Não"], width=470,
            fg_color=COR_INPUT, border_color="#374151",
            button_color=COR_BOTAO, button_hover_color=COR_BOTAO_HOVER
        )
        self.combo_prioridade.grid(row=7, column=0, columnspan=2, padx=15, pady=(0, 10))
        self.combo_prioridade.set("Sim")

        # --- BOTÃO SALVAR ---
        self.btn_salvar = ctk.CTkButton(
            self.frame_form, text=" ✓ Salvar Atração",
            fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER,
            font=ctk.CTkFont(size=14, weight="bold"), height=38, width=200,
            command=self.salvar_atracao
        )
        self.btn_salvar.grid(row=8, column=0, columnspan=2, pady=(15, 10))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=9, column=0, columnspan=2, pady=(0, 10))

        # --- LISTAGEM ---
        self.lbl_lista = ctk.CTkLabel(self, text="🎢 Atrações Cadastradas", font=ctk.CTkFont(size=16, weight="bold"), text_color=COR_TEXTO)
        self.lbl_lista.pack(pady=(15, 5))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=220, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    def salvar_atracao(self):
        nome = self.entry_nome.get()
        tipo = self.combo_tipo.get()
        capacidade = self.entry_capacidade.get()
        idade = self.entry_idade.get()
        horario = self.entry_horario.get()
        prioridade_str = self.combo_prioridade.get()

        if not nome or not capacidade or not idade:
            self.lbl_mensagem.configure(text="⚠ Preencha Nome, Capacidade e Idade Mínima!", text_color=COR_ERRO)
            return

        try:
            capacidade_int = int(capacidade)
            idade_int = int(idade)
        except ValueError:
            self.lbl_mensagem.configure(text="⚠ Capacidade e Idade devem ser apenas números!", text_color=COR_ERRO)
            return

        aceita_prioridade = True if prioridade_str == "Sim" else False

        msg = self.servico.cadastrar_atracao(nome, tipo, capacidade_int, idade_int, horario, aceita_prioridade)
        self.lbl_mensagem.configure(text=f"✓ {msg}", text_color=COR_SUCESSO)

        self.entry_nome.delete(0, 'end')
        self.entry_capacidade.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_horario.delete(0, 'end')
        self.combo_tipo.set("Montanha-Russa")
        self.combo_prioridade.set("Sim")

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        atracoes = self.servico.listar_atracoes()

        if not atracoes:
            lbl_vazio = ctk.CTkLabel(
                self.frame_lista, text="Nenhuma atração cadastrada ainda.",
                font=ctk.CTkFont(size=14, slant="italic"), text_color=COR_TEXTO_SEC
            )
            lbl_vazio.pack(pady=30)
            return

        for a in atracoes:
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, fg_color=COR_CARD, border_width=1, border_color="#374151")
            card.pack(pady=4, padx=5, fill="x")

            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(8, 2))

            lbl_nome = ctk.CTkLabel(frame_topo, text=a.nome, font=ctk.CTkFont(size=15, weight="bold"), text_color=COR_TEXTO)
            lbl_nome.pack(side="left")

            if hasattr(a, 'aceita_prioridade') and a.aceita_prioridade:
                lbl_prio = ctk.CTkLabel(
                    frame_topo, text=" ⚡ ACEITA VIP / ANUAL ",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    text_color=COR_VIP, fg_color="#4B4000", corner_radius=6
                )
            else:
                lbl_prio = ctk.CTkLabel(
                    frame_topo, text=" FILA COMUM ",
                    font=ctk.CTkFont(size=12),
                    text_color=COR_TEXTO_SEC, fg_color=COR_INPUT, corner_radius=6
                )
            lbl_prio.pack(side="right")

            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(2, 8))

            info_texto = f"Tipo: {a.tipo}  •  Capacidade: {a.capacidade} pessoas  •  Idade Mínima: {a.idade_minima} anos  •  Horário: {a.horario}"
            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=ctk.CTkFont(size=12), text_color=COR_TEXTO_SEC)
            lbl_info.pack(side="left")
