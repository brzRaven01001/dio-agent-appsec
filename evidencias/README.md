# 📸 Evidências de Teste e Validação

Esta pasta armazena as capturas de tela (prints) e vídeos que comprovam o funcionamento e as validações realizadas durante o desafio:

---

### 1. Postura Investigativa
- **`01_contexto_investigativo.png`**: Demonstração do agente investigando o contexto (ambiente, sensibilidade dos dados e privilégios de execução) antes de emitir qualquer diagnóstico ou sugerir correções.

---

### 2. Prova de Conceito (PoC) de SQL Injection no Login
- **`02_poc_sqli_login.mp4`**: Vídeo demonstrando a exploração prática de bypass de autenticação no login do `app.py` utilizando o payload `admin' --`.

---

### 3. Análise e Raio-X do Laboratório de SQL Injection Avançado (`app_sqli_avancado.py`)
- **`03_analise_sqli_avancado_p1.png`**: Mapeamento inicial das rotas `/produto` (Error/Union-based) e `/busca` (LIKE f-string).
- **`03_analise_sqli_avancado_p2.png`**: Análise da rota `/pedidos` (insegurança no `ORDER BY`) e `/api/usuario-existe` (Boolean Blind).
- **`03_analise_sqli_avancado_p3.png`**: Identificação de Second-Order SQLi nas rotas `/registro` e `/perfil`, acompanhada da Matriz de Avaliação de Risco.

---

### 4. Triagem Estática de Ameaças & Malware (`app_malware_benigno.py`)
- **`04_triagem_malware_mitre_p1.png`**: Detecção de ofuscação em Base64 da URL de comando e controle e rotina de coleta recursiva.
- **`04_triagem_malware_mitre_p2.png`**: Identificação de exfiltração web via HTTPS e execução de comandos nativos do sistema operacional.
- **`04_triagem_malware_mitre_p3.png`**: Matriz completa de correlação de táticas e técnicas com o **MITRE ATT&CK**.
- **`04_triagem_malware_mitre_p4.png`**: Matriz de Risco e recomendações táticas de contenção e resposta a incidentes.
