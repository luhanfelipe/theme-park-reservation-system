import customtkinter as ctk

class TelaAtracao(ctk.CTkFrame):
    def __init__(self, master, servico):
        super().__init__(master)
        self.servico = servico

        # --- TÍTULO ---
        self.lbl_titulo = ctk.CTkLabel(self, text="Cadastro de Atrações", font=("Arial", 20, "bold"))
        self.lbl_titulo.pack(pady=10)

        # --- FORMULÁRIO (CREATE) ---
        self.frame_form = ctk.CTkFrame(self)
        self.frame_form.pack(pady=10, padx=20, fill="x")

        self.entry_nome = ctk.CTkEntry(self.frame_form, placeholder_text="Nome da Atração", width=200)
        self.entry_nome.grid(row=0, column=0, padx=10, pady=10)

        self.entry_capacidade = ctk.CTkEntry(self.frame_form, placeholder_text="Capacidade (ex: 20)", width=200)
        self.entry_capacidade.grid(row=0, column=1, padx=10, pady=10)

        self.entry_idade = ctk.CTkEntry(self.frame_form, placeholder_text="Idade Mínima", width=200)
        self.entry_idade.grid(row=1, column=0, padx=10, pady=10)

        self.entry_horario = ctk.CTkEntry(self.frame_form, placeholder_text="Horário (ex: 10h-18h)", width=200)
        self.entry_horario.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_prioridade = ctk.CTkLabel(self.frame_form, text="Aceita Passe VIP?")
        self.lbl_prioridade.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.combo_prioridade = ctk.CTkComboBox(self.frame_form, values=["Sim", "Não"], width=100)
        self.combo_prioridade.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        self.combo_prioridade.set("Sim")

        self.btn_salvar = ctk.CTkButton(self.frame_form, text="Salvar Atração", command=self.salvar_atracao)
        self.btn_salvar.grid(row=3, column=0, columnspan=2, pady=15)

        self.lbl_mensagem = ctk.CTkLabel(self.frame_form, text="", text_color="green")
        self.lbl_mensagem.grid(row=4, column=0, columnspan=2)

        # --- VISUALIZAÇÃO (READ) ---
        self.lbl_lista = ctk.CTkLabel(self, text="Atrações Cadastradas:", font=("Arial", 16, "bold"))
        self.lbl_lista.pack(pady=(20, 0))

        self.caixa_texto_lista = ctk.CTkTextbox(self, height=200)
        self.caixa_texto_lista.pack(pady=10, padx=20, fill="both", expand=True)
        self.caixa_texto_lista.configure(state="disabled")

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
        self.caixa_texto_lista.configure(state="normal")
        self.caixa_texto_lista.delete("1.0", "end")

        atracoes = self.servico.listar_atracoes()
        
        if not atracoes:
            self.caixa_texto_lista.insert("end", "Nenhuma atração cadastrada ainda.\n")
        else:
            for a in atracoes:
                priori_txt = "Sim" if a.aceita_prioridade else "Não"
                linha = f"{a.nome} | Capacidade: {a.capacidade} | Idade Mínima: {a.idade_minima} | Horário: {a.horario} | Aceita VIP: {priori_txt}\n"
                self.caixa_texto_lista.insert("end", linha)
        
        self.caixa_texto_lista.configure(state="disabled")