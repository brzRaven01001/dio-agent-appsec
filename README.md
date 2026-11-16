# DIO Agent — Especialização em Cibersegurança & AppSec

> **Repositório Base Original:** [digitalinnovationone/dio-agent](https://github.com/digitalinnovationone/dio-agent)  
> **Desafio de Projeto:** Trilha Santander — Cibersegurança do Zero à Prática ([DIO](https://dio.me))  
> **Mentor de IA Especializado:** Análise de Vulnerabilidades, Auditoria de SQL Injection e Triagem de Ameaças/Malware.

---

## Visão Geral do Projeto

Este repositório contém a evolução do **DIO Agent**, transformando o mentor educacional generalista da DIO em um **Especialista em Segurança de Aplicações (AppSec) e Segurança Defensiva**.

Na arquitetura baseada no padrão aberto `AGENTS.md`, **nenhum modelo de inteligência artificial é treinado do zero**. O agente adquire novos comportamentos, conhecimentos teóricos e metodologias profissionais através de arquivos em Markdown estruturados (skills, base de conhecimento e persona).

---

## Por Que Esta Especialização Foi Criada?

Em cibersegurança e engenharia de software, respostas rápidas e automáticas sem contexto costumam gerar falsos positivos ou introduzir comandos destrutivos. 

A especialização em **Análise de Vulnerabilidades (`vulnerability-analysis`)** foi concebida para que o agente atue exatamente como um profissional sênior de segurança da informação:
1. **Mentalidade Investigativa:** Nunca sugere correções ou comandos sem antes perguntar e entender o ambiente (produção vs laboratório, dados expostos, privilégios).
2. **Avaliação Estruturada de Riscos:** Calcula severidade combinando **Impacto** e **Probabilidade**, correlacionando com a **Tríade CIA** (Confidencialidade, Integridade e Disponibilidade).
3. **Padrões de Mercado:** Mapeia fraquezas no **CWE**, categorias do **OWASP Top 10** e táticas/técnicas do **MITRE ATT&CK**.
4. **Cultura DevSecOps (Secure by Design):** Guia o desenvolvedor a resolver a causa-raiz (ex.: consultas parametrizadas, allowlists) em vez de adotar soluções paliativas frágeis.

---

## A Árvore de Habilidades de Segurança (Skill Tree)

O agente foi dotado de três grandes pilares operacionais dentro da skill `vulnerability-analysis`:

| Habilidade Especializada | Por Que Foi Adicionada? | O Que o Agente Faz? |
| :--- | :--- | :--- |
| **Auditoria Especializada em SQL Injection (SQLi)** | É uma das falhas mais antigas, perigosas e prevalentes da web (OWASP A03:2021 / CWE-89), causando vazamentos em massa e bypass de autenticação. | Detecta interpolações e concatenações inseguras; diferencia injeções In-band (Error e Union), Blind (Booleana/Tempo), injeções em `ORDER BY` e Second-Order; orienta a aplicação de *Prepared Statements* e Allowlists. |
| **Identificação e Triagem de Malware (Threat Triage)** | Analistas de segurança frequentemente precisam avaliar códigos e utilitários suspeitos que tentam se passar por ferramentas legítimas (*Dual-Use*). | Realiza análise estática; detecta ofuscação em Base64, chamadas de sistema (`subprocess`), coleta recursiva de arquivos, compactação não autorizada e exfiltração de dados via canais HTTP. |
| **Exploração Ética & PoC Defensivo** | Em auditorias, é crucial demonstrar o impacto técnico para o time de desenvolvimento sem causar negação de serviço ou danos. | Elabora Provas de Conceito (PoC) didáticas e controladas para laboratório, correlacionando-as com técnicas adversárias do MITRE ATT&CK (ex.: T1190, T1027, T1560, T1567). |

---

## Arquivos Criados e Alterados

Toda a inteligência e o comportamento do agente são governados pelos seguintes arquivos no repositório:

| Arquivo | Tipo | Descrição do Conteúdo |
| :--- | :--- | :--- |
| [`agent/knowledge/security-basics.md`](agent/knowledge/security-basics.md) | **Novo** (Base de Conhecimento) | Fundamentos teóricos: Tríade CIA, equação de risco ($Risco = P \times I$), taxonomia completa de SQL Injection, fundamentos de análise de malware (IOCs, hashes) e Secure by Design. |
| [`skills/vulnerability-analysis/SKILL.md`](skills/vulnerability-analysis/SKILL.md) | **Novo** (Roteiro Operacional) | O fluxo em 6 passos que o agente executa: Investigação de Contexto $\rightarrow$ Classificação CWE/OWASP $\rightarrow$ Matriz de Risco $\rightarrow$ MITRE ATT&CK $\rightarrow$ Playbooks Técnicos $\rightarrow$ Validação. |
| [`skills/vulnerability-analysis/README.md`](skills/vulnerability-analysis/README.md) | **Novo** (Documentação da Skill) | Guia explicativo voltado para pessoas desenvolvedoras e avaliadoras sobre como a skill funciona e como acioná-la. |
| [`agent/persona.md`](agent/persona.md) | **Alterado** (Persona) | Adicionados os traços de comportamento em segurança: postura defensiva, ética inegociável e a proibição explícita de sugerir comandos sem validar o contexto do ambiente. |
| [`AGENTS.md`](AGENTS.md) | **Alterado** (Fonte Única da Verdade) | Registro do arquivo `security-basics.md` na base de conhecimento e inclusão da skill `vulnerability-analysis` na tabela oficial de habilidades do agente. |

---

## Laboratório Prático de Testes

Para validar a atuação do agente em situações reais de laboratório, foram criadas três aplicações em Python:

### 1. `app.py` — Sistema de Login Vulnerável a SQLi Clássico
- **Cenário:** Formulário de login em Flask com SQLite onde a consulta montava a instrução SQL concatenando strings (`WHERE usuario = '...' + usuario`).
- **Falha Demonstrada:** Bypass completo de autenticação com o payload `admin' --`, logando como administrador sem senha legítima.
- **Correção Validada:** Implementação de consulta parametrizada com marcadores `?`.

### 2. `app_sqli_avancado.py` — Loja Virtual com 5 Variantes de SQL Injection
- **Cenário:** API REST com produtos, pedidos e usuários, explorando nuances que passam despercebidas em revisões comuns:
  1. `/produto`: In-band Error-Based e Union-Based SQLi.
  2. `/busca`: SQLi dentro de cláusula `LIKE` via f-string.
  3. `/pedidos`: Injeção na cláusula `ORDER BY` (onde marcadores `?` não funcionam no SQL, exigindo **Allowlist estrita**).
  4. `/api/usuario-existe`: SQLi Cego / Booleano (Boolean Blind).
  5. `/registro` e `/perfil`: Sanitização ingênua com `.replace("--", "")` e **Second-Order SQL Injection**.

### 3. `app_malware_benigno.py` — Triagem de Malware & Exfiltração
- **Cenário:** Utilitário que se apresenta como script de backup, mas possui rotina oculta de *Stealer*.
- **Comportamentos Detectados pelo Agente:**
  - URL de comando e controle (C2) ofuscada em Base64.
  - Varredura recursiva de diretórios (`os.walk`) e compactação em `.zip`.
  - Exfiltração via requisições HTTP POST externas.
  - Mapeamento das técnicas MITRE ATT&CK: T1027, T1083, T1560, T1567 e T1070.

---

## Pasta de Evidências (`evidencias/`)

A pasta [`evidencias/`](evidencias/) reúne os prints e registros de execução que comprovam a atuação do agente e a resolução dos problemas:

1. **Perguntas de Contexto:** Prints do agente questionando sobre ambiente, dados e privilégios antes de emitir qualquer diagnóstico.
2. **PoC de SQL Injection no Login:** Comprovação da autenticação indevida via `admin' --` e sua posterior mitigação.
3. **Análise de SQLi Avançado:** Comparação das respostas das rotas (ex.: `/produto?id=1'` e `-1 UNION SELECT...` retornando `[]` seguro após a parametrização).
4. **Bloqueio de Boolean Blind:** Ambas as requisições (`1=1` e `1=2`) retornando `false`, destruindo o canal de inferência do atacante.
5. **Relatório de Triagem do Malware:** Detecção dos padrões de ofuscação e exfiltração do `app_malware_benigno.py`.

---

## Como Executar o Agente no seu Harness

Este projeto segue o padrão aberto `AGENTS.md` e é compatível com qualquer harness moderno (**Google Antigravity**, **Hermes CLI**, **Claude Code**, **Cursor**, etc.).

### Rodando no Google Antigravity ou Cursor
1. Abra a pasta do projeto no VS Code ou Antigravity IDE:
   ```bash
   git clone https://github.com/<seu-usuario>/<seu-repositorio>.git
   cd <seu-repositorio>
   ```
2. Abra a interface de chat do agente. O harness lerá automaticamente o [AGENTS.md](AGENTS.md) na inicialização.
3. Envie uma mensagem solicitando uma análise de segurança:
   > *"Atue como especialista em AppSec e analise a segurança do arquivo app.py."*

### Rodando no Hermes CLI
1. Certifique-se de que o Hermes está instalado e abra o terminal **exatamente na pasta raiz do projeto**:
   ```bash
   hermes
   ```
2. Converse com o agente e confira o acionamento da skill `vulnerability-analysis`.

---

## Checklist de Conformidade do Desafio

- [x] Skill nova criada em `skills/vulnerability-analysis/` com `SKILL.md` e `README.md`.
- [x] Base teórica criada em `agent/knowledge/security-basics.md`.
- [x] Persona atualizada em `agent/persona.md` com postura investigativa e defensiva.
- [x] Skill registrada na tabela oficial do `AGENTS.md`.
- [x] Testes realizados exclusivamente com códigos e servidores locais de laboratório (`127.0.0.1`).
- [x] Códigos vulneráveis e mitigados documentados e organizados.
- [x] Pasta de evidências estruturada para prints comprobatórios.
- [x] Repositório público no GitHub com nome legível em minúsculas e sem acentos.
