import customtkinter as ctk

class TelaAtracao(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        self.servico = servico

        # --- BOTÃO VOLTAR ---
        self.btn_voltar = ctk.CTkButton(
            self, 
            text="⬅ Voltar", 
            width=80, 
            height=32,
            fg_color="transparent", 
            border_width=1, 
            border_color="#4b5563",
            hover_color="#374151",
            command=comando_voltar
        )
        self.btn_voltar.place(x=20, y=15)

        # --- TÍTULO DA TELA ---
        self.lbl_titulo = ctk.CTkLabel(
            self, 
            text=" ✦ Cadastro de Atrações", 
            font=ctk.CTkFont(size=22, weight="bold")
        )
        self.lbl_titulo.pack(pady=(15, 10))

        # --- FORMULÁRIO DE CADASTRO ---
        self.frame_form = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#374151")
        self.frame_form.pack(pady=10, padx=20, anchor="center")

        # --- LINHA 0: Nome e Capacidade ---
        # Campo Nome da Atração
        self.lbl_nome = ctk.CTkLabel(self.frame_form, text="Nome da Atração:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_nome.grid(row=0, column=0, sticky="w", padx=15, pady=(12, 2))
        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: Montanha-Russa do Terror", width=220)
        self.entry_nome.grid(row=1, column=0, padx=15, pady=(0, 10))

        # Campo Capacidade
        self.lbl_capacidade = ctk.CTkLabel(self.frame_form, text="Capacidade Max.:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_capacidade.grid(row=0, column=1, sticky="w", padx=15, pady=(12, 2))
        self.entry_capacidade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 20", width=220)
        self.entry_capacidade.grid(row=1, column=1, padx=15, pady=(0, 10))

        # --- LINHA 1: Idade Mínima e Horário ---
        # Campo Idade Mínima
        self.lbl_idade = ctk.CTkLabel(self.frame_form, text="Idade Mínima (anos):", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_idade.grid(row=2, column=0, sticky="w", padx=15, pady=(5, 2))
        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 12", width=220)
        self.entry_idade.grid(row=3, column=0, padx=15, pady=(0, 10))

        # Campo Horário
        self.lbl_horario = ctk.CTkLabel(self.frame_form, text="Horário de Funcionamento:", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_horario.grid(row=2, column=1, sticky="w", padx=15, pady=(5, 2))
        self.entry_horario = ctk.CTkEntry(self.frame_form, placeholder_text="Ex: 10h-18h", width=220)
        self.entry_horario.grid(row=3, column=1, padx=15, pady=(0, 10))

        # --- LINHA 2: Aceita Passe VIP ---
        self.lbl_prioridade = ctk.CTkLabel(self.frame_form, text="Aceita Passe VIP / Anual?", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_prioridade.grid(row=4, column=0, columnspan=2, sticky="w", padx=15, pady=(5, 2))

        self.combo_prioridade = ctk.CTkComboBox(
            self.frame_form, 
            values=["Sim", "Não"], 
            width=470
        )
        self.combo_prioridade.grid(row=5, column=0, columnspan=2, padx=15, pady=(0, 10))
        self.combo_prioridade.set("Sim")

        # --- BOTÃO DE AÇÃO (Verde de Confirmação) ---
        self.btn_salvar = ctk.CTkButton(
            self.frame_form, 
            text=" ✓ Salvar Atração", 
            fg_color="#10b981", 
            hover_color="#059669",
            font=ctk.CTkFont(size=14, weight="bold"),
            height=38,
            width=200,
            command=self.salvar_atracao
        )
        self.btn_salvar.grid(row=6, column=0, columnspan=2, pady=(15, 10))

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", font=ctk.CTkFont(size=12, weight="bold"))
        self.lbl_mensagem.grid(row=7, column=0, columnspan=2, pady=(0, 10))

        # --- LISTAGEM DE ATRAÇÕES ---
        self.lbl_lista = ctk.CTkLabel(self, text="Atrações Cadastradas", font=ctk.CTkFont(size=16, weight="bold"))
        self.lbl_lista.pack(pady=(15, 5))

        self.frame_lista = ctk.CTkScrollableFrame(self, height=220, fg_color="transparent")
        self.frame_lista.pack(pady=5, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    def salvar_atracao(self):
        nome = self.entry_nome.get()
        capacidade = self.entry_capacidade.get()
        idade = self.entry_idade.get()
        horario = self.entry_horario.get()
        prioridade_str = self.combo_prioridade.get()

        if not nome or not capacidade or not idade:
            self.lbl_mensagem.configure(text="⚠ Preencha Nome, Capacidade e Idade Mínima!", text_color="#f87171")
            return

        try:
            capacidade_int = int(capacidade)
            idade_int = int(idade)
        except ValueError:
            self.lbl_mensagem.configure(text="⚠ Capacidade e Idade devem ser apenas números!", text_color="#f87171")
            return
        
        aceita_prioridade = True if prioridade_str == "Sim" else False

        msg = self.servico.cadastrar_atracao(nome, capacidade_int, idade_int, horario, aceita_prioridade)
        self.lbl_mensagem.configure(text=f"✓ {msg}", text_color="#34d399")

        # Limpar os campos
        self.entry_nome.delete(0, 'end')
        self.entry_capacidade.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_horario.delete(0, 'end')
        self.combo_prioridade.set("Sim")

        self.atualizar_lista()

    def atualizar_lista(self):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        atracoes = self.servico.listar_atracoes()

        if not atracoes:
            lbl_vazio = ctk.CTkLabel(
                self.frame_lista, 
                text="Nenhuma atração cadastrada ainda.", 
                font=ctk.CTkFont(size=14, slant="italic"), 
                text_color="#9ca3af"
            )
            lbl_vazio.pack(pady=30)
            return

        for a in atracoes:
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#374151")
            card.pack(pady=4, padx=5, fill="x")

            # Topo do Card
            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(8, 2))

            lbl_nome = ctk.CTkLabel(frame_topo, text=a.nome, font=ctk.CTkFont(size=15, weight="bold"), text_color="#38bdf8")
            lbl_nome.pack(side="left")

            # Etiqueta visual de Aceita Prioridade
            if a.aceita_prioridade:
                lbl_prio = ctk.CTkLabel(
                    frame_topo, 
                    text=" ⚡ ACEITA VIP / ANUAL ", 
                    font=ctk.CTkFont(size=12, weight="bold"), 
                    text_color="#fef08a", 
                    fg_color="#854d0e", 
                    corner_radius=6
                )
            else:
                lbl_prio = ctk.CTkLabel(
                    frame_topo, 
                    text=" FILA COMUM ", 
                    font=ctk.CTkFont(size=12), 
                    text_color="#e5e7eb", 
                    fg_color="#374151", 
                    corner_radius=6
                )
            lbl_prio.pack(side="right")

            # Base do Card
            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(2, 8))
            
            info_texto = f"Capacidade: {a.capacidade} pessoas  •  Idade Mínima: {a.idade_minima} anos  •  Horário: {a.horario}"
            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=ctk.CTkFont(size=12), text_color="#9ca3af")
            lbl_info.pack(side="left")