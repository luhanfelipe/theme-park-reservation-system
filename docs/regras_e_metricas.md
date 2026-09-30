# Regras do Sistema e Métricas do Parque Temático

## 1. Cadastro de Visitantes
* **Informações obrigatórias:** Nome completo, CPF, Data de nascimento, E-mail e Dados do cartão de crédito (se for usado).
* **Tipos de ingressos/passes:**
  * **Normal:** Acesso padrão às atrações e filas virtuais comuns.
  * **VIP / Passe Especial:** Garante prioridade no atendimento e inserção à frente das filas normais.

## 2. Cadastro de Atrações
* **Informações da Atração:** Nome, Tipo (Montanha-russa, simulador, teatro, brinquedo infantil, etc.), Capacidade por horário, Horários disponíveis e Faixa etária / Idade mínima.
* **Controle de prioridade:** Flag indicando se aceita ou não prioridade para determinados passes (VIP / Passe Especial).

## 3. Funcionamento das Filas Virtuais
* **Funcionamento geral:** Quando o visitante solicita entrada em uma atração, ele entra na fila específica daquela atração.
* **Fila Normal:** Funciona no modelo FIFO (Primeiro a Entrar, Primeiro a Sair).
* **Fila com Prioridade:** Visitantes com ingressos VIP ou passes especiais passam na frente de quem possui ingressos normais.
* **Avanço da fila:** A fila avança conforme os visitantes vão entrando na atração.
* **Atração Cheia:** Quando a capacidade máxima de uma sessão é atingida, os próximos visitantes são alocados para o horário seguinte.

## 4. Regras das Reservas
* **Visualizações do visitante:**
  * Atrações em que está aguardando
  * Posição em cada fila
  * Histórico de visitas e reservas realizadas
* **Informações registradas:** Código da reserva, visitante responsável, atração, horário agendado e status (`Ativa`, `Concluída` ou `Cancelada`).
* **Regras de agendamento:** O visitante só pode reservar uma atração por vez no mesmo horário.

## 5. Métricas do Parque (Painel Administrativo)
* Quantidade total de visitantes cadastrados.
* Quantidade total de reservas feitas por dia.
* Atração mais disputada do dia (maior fila/procura).
* Visitante que mais usou o sistema no dia.
* Quantidade/percentual de visitantes utilizando passes de prioridade.