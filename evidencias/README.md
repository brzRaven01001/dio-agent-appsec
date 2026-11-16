# Evidências de Teste e Validação

Esta pasta armazena as capturas de tela (prints) que comprovam o funcionamento e as validações realizadas durante o desafio:

1. **`01_contexto_investigativo.png`**: Print do agente perguntando o contexto (ambiente, sensibilidade dos dados e privilégios) antes de sugerir comandos ou correções.
2. **`02_poc_sqli_login.mp4`**: Demonstração em vídeo da falha de SQL Injection no login do `app.py` utilizando o payload `admin' --`.
3. **`03_mitigacao_sqli_login.png`**: Comprovação de bloqueio da injeção após a aplicação de consultas parametrizadas.
4. **`04_sqli_avancado_error_union.png`**: Teste de exploração e mitigação no endpoint `/produto` do `app_sqli_avancado.py` (retorno seguro de `[]`).
5. **`05_sqli_avancado_boolean_blind.png`**: Teste do endpoint `/api/usuario-existe` retornando `false` para ambas as queries, eliminando o oráculo booleano.
6. **`06_analise_estatica_malware.png`**: Relatório do agente identificando ofuscação em Base64, coleta recursiva e exfiltração web no `app_malware_benigno.py`.
