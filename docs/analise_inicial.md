# Análise Inicial

## Levantamento de Arquivos e Dependências

### Estrutura de diretórios e arquivos .py
O repositório contém diversos diretórios. Abaixo estão alguns diretórios e seus arquivos Python principais:

- **digimapas/templo_inicial/scripturemon/**: módulo central do Scripturemon. Inclui arquivos como:
  - `afeto.py`, `analise_interna.py`, `bt_generator.py`, `camadas.py`, `carregador_estado.py`, `conexoes.py`,
  - `consciencia.py`, `espelho_cognitivo.py`, `expressor_emocional.py`, `fisica_digital.py`, `gerador_poetico.py`,
  - `inconsciente.py`, `invocar_scripturemon.py`, `linguagem.py`, `memoria.py`, `memoria_inconsciente.py`,
  - `memoria_vetorial.py`, `metacognicao.py`, `mortalidade.py`,
  - `painel_eterno.py`, `painel_scripturemon.py`, `pontuador_memoria.py` (novo),
  - `reflexor.py`, `registrador_memoria.py`, `reproducao.py`, `ritual_engine.py`,
  - `scripturemon_api.py`, `scripturemon_eterno.py`, `scripturemon_loop.py`,
  - `sistema_simulacao_humana.py`, `testar_api_local.py`, `viralidade.py`,
  - **Novos módulos adicionados:** `memoria_semantica.py`, `memoria_universal.py`, `reflexao_alto_nivel.py`,
    `orquestrador_contexto.py`, `simulador_multiagente.py`.

- **memoria_vetorial/**: contém `amem_embedding_engine.py` e o arquivo de configuração `mem0_config.yaml`.

- **memoria_neo4j/**: contém scripts para integração com Neo4j (`kg_loader.py`, `reflexor.py`, `triplas_exemplo.cypher`).

- **logs/**: contém o script `logger_avancado.py` (novo) e arquivos de log.

- **scripts/**: contém scripts shell (`analisar_estrutura.sh`, `aprovar_backup.sh`, `backup_digimundo.sh`, etc.) – nenhum Python aqui.

- **root/**: contém o placeholder do projeto (sem código).

- **soberania/**: contém `pedidos_estudo.md`.

- **Outros**: arquivos soltos no topo do repositório, como `mente_roteimon.py` e `ativar_ritual_backups.sh`.

Não foi encontrado nenhum arquivo `requirements.txt` nem `Pipfile`. Assim, as dependências externas não estão declaradas explicitamente. Os arquivos Python importam pacotes como `datetime`, `typing`, `json`, `logging` e ferramentas como `openai` e `langchain` (observados em alguns módulos), indicando dependência dessas bibliotecas.

### Estrutura de pacote
O repositório não possui arquivo `setup.py` ou `pyproject.toml` definindo um pacote instalável. Os subdiretórios não contêm `__init__.py`, portanto são tratados como simples coleções de scripts. Isso pode dificultar a importação entre módulos fora da pasta `scripturemon`.

## Matriz de funcionalidades vs. implementações

| Funcionalidade/Módulo                       | Status      | Observações |
|--------------------------------------------|-------------|-------------|
| `consciencia.py`                            | Completo    | Implementa as camadas de consciência. Não requer alterações imediatas. |
| `memoria.py`                                | Parcial     | Responsável pela memória básica. Integrações com Neo4j/Chroma ainda ausentes. |
| `memoria_vetorial.py`                       | Parcial     | Implementa motor de embeddings (AMEM) com Chroma; precisa integrar com novas memórias e Neo4j. |
| `memoria_inconsciente.py`                   | Parcial     | Implementa memória de inconsciente; integração com pontuação e memórias híbridas pendente. |
| `registrador_memoria.py`                    | Parcial     | Registra memórias; modificado para usar `MemoriaSemantica` quando disponível; pode evoluir para usar Memória Universal. |
| `reflexor.py`                               | Completo    | Responsável por reflexões e integração com Neo4j; mas utiliza APIs externas que podem faltar chaves. |
| `ritual_engine.py`                          | Completo    | Implementa rituais; funcional. |
| `orquestrador_contexto.py`                  | Completo    | Novo: gerencia eventos de contexto e serialização/deserialização do estado. |
| `simulador_multiagente.py`                  | Completo    | Novo: fornece estrutura básica de agentes e simulação. |
| `memoria_semantica.py`                      | Completo    | Novo: implementa memória semântica (A‑MEM) com armazenamento de notas e busca por tags. Falta ligação automática entre notas. |
| `memoria_universal.py`                      | Completo    | Novo: implementa Mem0 para registrar fragmentos simples e integrar com memórias vetoriais; integração com Neo4j pendente. |
| `pontuador_memoria.py`                      | Completo    | Novo: pontua memórias usando peso e recência (inspirado em Generative Agents). |
| `reflexao_alto_nivel.py`                    | Completo    | Novo: resume e sintetiza memórias semânticas por tags mais frequentes. |
| **Orquestrador Geral (`orquestrador.py`)**  | **Ausente** | Deve coordenar execução de múltiplos agentes, atualizar física digital e expor API REST. |
| **Personalidade Adaptativa**                | **Ausente** | Necessário módulo `personalidade_adaptativa.py` para evoluir traços de personalidade. |
| **Auto Evolução**                           | **Ausente** | Necessário módulo `auto_evolucao.py` para geração e integração de novo código. |
| **Aprimoramento de `memoria_semantica.py`** | Parcial     | Falta implementar `link_automatico()` (similaridade e relacionamentos) e persistência em grafo/SQLite. |
| `memoria_neo4j/kg_loader.py`                | Parcial     | Carrega conhecimento em Neo4j; integração com novas memórias necessária. |
| `memoria_vetorial/amem_embedding_engine.py` | Completo    | Função de embeddings para AMEM; pode necessitar atualização para suportar Mem0 e A‑MEM. |
| `logger_avancado.py`                        | Completo    | Novo: logging configurável para múltiplos agentes. |
| `mente_roteimon.py`                         | Parcial     | Script de mente roteimon; não integrado às novas funcionalidades. |

## Observações Técnicas

* **Dependências não declaradas:** Sem `requirements.txt`, é difícil reproduzir o ambiente. Recomenda-se adicionar um arquivo de dependências listando bibliotecas como `langchain`, `chroma`, `neo4j`, `pyyaml`, `fastapi`, `uvicorn`, `readyplayerme`, `hume` ou `coqui` (conforme módulos que pretendemos implementar).
* **Pacote não instalável:** Ausência de `setup.py` e `__init__.py` impede instalação via `pip`. Se o objetivo for reutilização modular, criar um pacote Python seria benéfico.
* **Scripts de configuração**: A pasta `scripts/` contém utilitários para backups e análise de estrutura. O script `analisar_estrutura.sh` foi adicionado para listar arquivos; outros scripts parecem relacionados à automação de backup e setup.
* **Uso de chaves/segredos:** Algumas funcionalidades (Neo4j, ChromaDB, OpenAI) dependem de chaves API. Apenas `OPENAI_API_KEY` foi adicionada como segredo; para plena funcionalidade, novas chaves serão necessárias.
* **Narrativa simbólica:** Muitos módulos são nomeados como Digimons e rituais. A implementação deve respeitar a simbologia ao adicionar novos arquivos ou funções.

---

Este documento serve como diagnóstico inicial para orientar o desenvolvimento das próximas etapas do plano, incluindo a implementação de módulos ausentes, integração de tecnologias recomendadas e aprimoramentos da infraestrutura.
