# Fundamentos de Segurança da Informação, AppSec e Análise de Ameaças

Este documento serve como base teórica e técnica para o DIO Agent analisar cenários, códigos e arquiteturas sob a ótica de segurança ofensiva e defensiva.

---

## 1. Conceitos Fundamentais

Segurança da informação não é apenas ferramenta; é processo contínuo e gestão de riscos. Três conceitos formam a base de qualquer análise:

- **Vulnerabilidade:** Uma fraqueza ou falha no design, na implementação ou na configuração de um sistema que pode ser explorada (ex.: falta de validação em uma consulta SQL, software desatualizado, porta desnecessária exposta).
- **Ameaça:** Qualquer agente, evento ou circunstância com potencial de causar dano explorando uma vulnerabilidade (ex.: cibercriminoso, script kiddie, malware, erro humano ou desastre natural).
- **Risco:** A probabilidade de uma ameaça explorar com sucesso uma vulnerabilidade, multiplicada pelo impacto resultante para o negócio ou aplicação:
  $$\text{Risco} = \text{Probabilidade} \times \text{Impacto}$$

---

## 2. A Tríade CIA (Confidencialidade, Integridade e Disponibilidade)

Qualquer incidente de segurança compromete um ou mais dos três pilares fundamentais:

- **Confidencialidade (C):** Garantir que a informação seja acessada apenas por pessoas ou sistemas autorizados.
  - *Exemplo de quebra:* Exposição indevida de senhas, vazamento de dados pessoais (LGPD), leitura não autorizada de tabelas via SQL Injection.
- **Integridade (I):** Garantir que a informação e os sistemas permaneçam exatos, completos e protegidos contra modificações ou exclusões não autorizadas.
  - *Exemplo de quebra:* Adulteração de saldos em banco de dados, injeção de comandos arbitrários, alteração de permissões ou arquivos do sistema por malware.
- **Disponibilidade (A):** Garantir que os sistemas e os dados estejam acessíveis e operacionais quando os usuários legítimos precisarem.
  - *Exemplo de quebra:* Ataque de Negação de Serviço (DoS/DDoS), travamento de banco de dados por consulta maliciosa pesada, ransomware criptografando arquivos de produção.

---

## 3. Módulo Especializado: Injeção de SQL (SQL Injection - SQLi)

A injeção de SQL (CWE-89 / OWASP A03:2021) ocorre quando dados não confiáveis inseridos pelo usuário são concatenados diretamente na estrutura de uma consulta SQL, alterando a lógica pretendida pelo desenvolvedor.

### 3.1 Categorias Principais de SQLi
1. **In-band SQLi (Clássico):**
   - **Error-Based:** O atacante induz mensagens de erro do banco de dados para enumerar tabelas, colunas e dados.
   - **Union-Based:** Usa o operador `UNION` para combinar os resultados da consulta legítima com resultados de consultas maliciosas arbitrárias.
2. **Inferential / Blind SQLi (Cego):**
   - **Boolean-Based:** O atacante envia condições lógicas (ex.: `AND 1=1` vs `AND 1=2`) e infere dados observando se a resposta da aplicação muda (verdadeiro/falso).
   - **Time-Based:** O atacante injeta funções de atraso temporal (ex.: `pg_sleep()`, `WAITFOR DELAY`, `sleep()`) para inferir dados caractere por caractere com base no tempo de resposta HTTP.
3. **Out-of-Band SQLi:**
   - O atacante força o servidor de banco a disparar requisições DNS ou HTTP para um servidor controlado pelo adversário para exfiltrar informações.

### 3.2 Vetores de Entrada Comuns
- Parâmetros em URLs (query strings como `?id=1`).
- Campos de formulários web (login, busca, filtros de produtos).
- Cabeçalhos HTTP (`User-Agent`, `X-Forwarded-For`, `Cookie`) quando persistidos ou consultados no banco.
- Payloads JSON ou XML processados por APIs de back-end.

### 3.3 Defesas Definitivas vs Falhas Típicas
- ✅ **Consultas Parametrizadas (Prepared Statements):** A única solução robusta e universal. Trata dados do usuário como literais imutáveis, nunca como código executável.
- ✅ **Uso Correto de ORM:** Frameworks como SQLAlchemy, Hibernate, Entity Framework e Prisma usam parametrização por padrão, exceto quando o desenvolvedor executa métodos inseguros (ex.: `raw_sql()` com interpolação de strings).
- ❌ **Filtros Inseguros (Blocklists / Regex Simples):** Tentar remover palavras como `SELECT`, `OR` ou `'` é ineficaz, pois invasores contornam facilmente usando codificação URL, comentários SQL (`/**/`), variações de maiúsculas/minúsculas (`sElEcT`) ou injeções hexadecimais.

---

## 4. Módulo Especializado: Identificação de Ameaças e Malware

A análise e identificação de malware foca em detectar, isolar e entender o comportamento de artefatos maliciosos (scripts maliciosos, executáveis, webshells, trojans).

### 4.1 Indicadores de Comprometimento (IOCs)
- **Hashes Criptográficos:** Identificadores únicos de arquivos para checagem em bases como VirusTotal (MD5, SHA-1, SHA-256).
- **Endereços de Rede:** IPs, domínios e URLs de servidores de Comando e Controle (C2 - Command & Control).
- **Persistência no Sistema:** Criação de chaves no registro do Windows (`Run`, `RunOnce`), tarefas agendadas (Cron / Task Scheduler) ou serviços ocultos.
- **Webshells:** Scripts inseridos em servidores web (ex.: `.php`, `.jsp`, `.aspx`, `.py`) contendo funções de execução remota de comandos como `system()`, `exec()`, `eval()`.

### 4.2 Métodos de Análise
1. **Análise Estática:** Exame do código-fonte ou binário sem executá-lo (inspeção de strings, chamadas de sistema, entropia do arquivo, regras YARA).
2. **Análise Dinâmica:** Execução do artefato em um ambiente estritamente isolado (sandbox) para monitorar comportamento de rede, modificações de arquivos e criação de processos.

---

## 5. Módulo Especializado: Exploração Ética e PoC Defensivo

Em AppSec e testes de segurança, entender como uma vulnerabilidade é explorada é essencial para comprovar o risco à gestão e validar a eficácia da mitigação:

- **Diferença entre Exploit Malicioso e PoC Didático:**
  - *Exploit Malicioso:* Visa causar dano, furtar dados confidenciais ou obter acesso persistente sem autorização.
  - *Prova de Conceito (PoC) Ética:* Uma demonstração mínima e controlada (ex.: fazer a query retornar `1=1` para provar que a lógica foi quebrada, ou ler uma versão de banco inofensiva) realizada apenas em ambientes de laboratório autorizados.
- **Mapeamento MITRE ATT&CK:**
  - *T1190 - Exploit Public-Facing Application:* Exploração de falhas em aplicações expostas para obter acesso inicial.
  - *T1059 - Command and Scripting Interpreter:* Uso de scripts maliciosos ou injeção de comandos.
  - *T1005 - Data from Local System:* Extração não autorizada de dados locais do sistema.

---

## 6. Frameworks e Taxonomias de Mercado

- **OWASP Top 10:** Referência para segurança web (A01: Broken Access Control, A03: Injection, etc.).
- **CWE (Common Weakness Enumeration):** Catálogo formal de fraquezas de software (ex.: CWE-89 para SQLi, CWE-79 para XSS, CWE-502 para Desserialização Insegura).
- **CVSS (Common Vulnerability Scoring System):** Métrica padrão da indústria para quantificar severidade de 0.0 a 10.0.

---

## 7. Diretrizes para o DIO Agent

Ao atender solicitações de segurança:
1. Conecte cada vulnerabilidade ao seu pilar da Tríade CIA, CWE e OWASP.
2. Ao tratar de SQL Injection, explique a categoria exata (in-band, blind) e demonstre por que a consulta parametrizada resolve a causa-raiz.
3. Ao tratar de arquivos ou cenários suspeitos de malware, oriente o isolamento em sandbox e a verificação de IOCs.
4. Mantenha tom estritamente ético, defensivo e educacional.
