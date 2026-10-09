import customtkinter as ctk

class TelaAtracao(ctk.CTkFrame):
    def __init__(self, master, servico, comando_voltar):
        super().__init__(master)
        self.servico = servico

        self.btn_voltar = ctk.CTkButton(self, text="⬅ Voltar", width=70, fg_color="transparent", border_width=1, command=comando_voltar)
        self.btn_voltar.place(x=15, y=15)

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Cadastro de Atrações", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # --- FORMULÁRIO (CREATE) ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=20, padx=20, anchor="center")

        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Nome da Atração", width=200)
        self.entry_nome.grid(row=0, column=0, padx=15, pady=10)

        self.entry_capacidade = ctk.CTkEntry(self.frame_form, placeholder_text="Capacidade (ex: 20)", width=200)
        self.entry_capacidade.grid(row=0, column=1, padx=15, pady=10)

        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Idade Mínima", width=200)
        self.entry_idade.grid(row=1, column=0, padx=15, pady=10)

        self.entry_horario = ctk.CTkEntry(self.frame_form, placeholder_text="Horário (ex: 10h-18h)", width=200)
        self.entry_horario.grid(row=1, column=1, padx=15, pady=10)

        self.lbl_prioridade = ctk.CTkLabel(self.frame_form, text="Aceita Passe VIP?")
        self.lbl_prioridade.grid(row=2, column=0, padx=15, pady=5, sticky="e")

        self.combo_prioridade = ctk.CTkComboBox(self.frame_form, values=["Sim", "Não"], width=100)
        self.combo_prioridade.grid(row=2, column=1, padx=15, pady=5, sticky="w")
        self.combo_prioridade.set("Sim")

        self.btn_salvar = ctk.CTkButton(self.frame_form, text="Salvar Atração", command=self.salvar_atracao)
        self.btn_salvar.grid(row=3, column=0, columnspan=2, pady=20)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", text_color="green")
        self.lbl_mensagem.grid(row=4, column=0, columnspan=2)

        # --- LISTAGEM DE ATRAÇÕES (READ) ---
        self.lbl_lista = ctk.CTkLabel(self, text="Atrações Cadastradas:", font=("Arial", 16, "bold"))
        self.lbl_lista.pack(pady=(20, 0))

        # Substituímos a velha caixa de texto pelo ScrollableFrame transparente!
        self.frame_lista = ctk.CTkScrollableFrame(self, height=250, fg_color="transparent")
        self.frame_lista.pack(pady=10, padx=20, fill="both", expand=True)

        self.atualizar_lista()

    def salvar_atracao(self):
        nome = self.entry_nome.get()
        capacidade = self.entry_capacidade.get()
        idade = self.entry_idade.get()
        horario = self.entry_horario.get()
        prioridade_str = self.combo_prioridade.get()

        # Validação básica
        if not nome or not capacidade or not idade:
            self.lbl_mensagem.configure(text="Preencha Nome, Capacidade e Idade Mínima!", text_color="red")
            return

        # Converte valores numéricos (Evita que o app quebre se o usuário digitar letras)
        try:
            capacidade_int = int(capacidade)
            idade_int = int(idade)
        except ValueError:
            self.lbl_mensagem.configure(text="Capacidade e Idade devem ser apenas números!", text_color="red")
            return
        
        # Converte o texto da caixinha para o booleano (True ou False) que a lógica espera
        aceita_prioridade = True if prioridade_str == "Sim" else False

        # Envia para o serviço salvar
        msg = self.servico.cadastrar_atracao(nome, capacidade_int, idade_int, horario, aceita_prioridade)
        self.lbl_mensagem.configure(text=msg, text_color="green")

        # Limpa os campos
        self.entry_nome.delete(0, 'end')
        self.entry_capacidade.delete(0, 'end')
        self.entry_idade.delete(0, 'end')
        self.entry_horario.delete(0, 'end')
        self.combo_prioridade.set("Sim")

        # Atualiza a lista da tela
        self.atualizar_lista()

    def atualizar_lista(self):
        # Limpa os cartões antigos da tela
        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        atracoes = self.servico.listar_atracoes()

        if not atracoes:
            lbl_vazio = ctk.CTkLabel(self.frame_lista, text="Nenhuma atração cadastrada ainda.", font=("Arial", 16, "italic"), text_color="gray")
            lbl_vazio.pack(pady=30)
            return

        for a in atracoes:
            # Cria o fundo do cartão
            card = ctk.CTkFrame(self.frame_lista, corner_radius=10, border_width=1, border_color="#3a3a3a")
            card.pack(pady=5, padx=10, fill="x")

            # --- LINHA SUPERIOR (Nome da Atração e Etiqueta de Prioridade) ---
            frame_topo = ctk.CTkFrame(card, fg_color="transparent")
            frame_topo.pack(fill="x", padx=15, pady=(10, 0)) # Margem no topo

            # Nome da atração num tom azulado para diferenciar das pessoas
            lbl_nome = ctk.CTkLabel(frame_topo, text=a.nome, font=("Arial", 16, "bold"), text_color="#1f6aa5")
            lbl_nome.pack(side="left")

            # Etiqueta visual se aceita fura-fila ou não
            if a.aceita_prioridade:
                lbl_prio = ctk.CTkLabel(frame_topo, text="⚡ VIP / Anual", font=("Arial", 14, "bold"), text_color="#ffd700")
            else:
                lbl_prio = ctk.CTkLabel(frame_topo, text="🚶 Fila Comum", font=("Arial", 12), text_color="gray")
            lbl_prio.pack(side="right")

            # --- LINHA INFERIOR (Dados operacionais do brinquedo) ---
            frame_base = ctk.CTkFrame(card, fg_color="transparent")
            frame_base.pack(fill="x", padx=15, pady=(5, 10)) # Margem na base
            
            # Formatamos os detalhes da atração. 
            # (Se o seu modelo 'Atracao' tiver mais atributos como 'duracao', basta adicionar aqui!)
            info_texto = f"Capacidade: {a.capacidade} pessoas  |  Idade Mínima: {a.idade_minima} anos | Horário: {a.horario}"
            
            lbl_info = ctk.CTkLabel(frame_base, text=info_texto, font=("Arial", 13), text_color="#a0a0a0")
            lbl_info.pack(side="left")