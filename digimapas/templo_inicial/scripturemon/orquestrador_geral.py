"""
Orquestrador Geral - Sistema nervoso central do Digimundo
Coordena múltiplos agentes, gerencia o ambiente e facilita interações
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import threading
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)


class TipoEvento(Enum):
    """Tipos de eventos no Digimundo"""
    GLOBAL = "global"
    LOCAL = "local"
    MENSAGEM = "mensagem"
    SISTEMA = "sistema"
    RITUAL = "ritual"


@dataclass
class Evento:
    """Estrutura de um evento no mundo"""
    tipo: TipoEvento
    conteudo: str
    origem: Optional[str] = None
    destino: Optional[str] = None
    metadata: Optional[Dict] = None
    timestamp: Optional[str] = None
    
    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class OrquestradorGeral:
    """
    Orquestrador central que gerencia todos os agentes e o ambiente do Digimundo
    """
    
    def __init__(self, config: Dict = None):
        """
        Inicializa o Orquestrador
        
        Args:
            config: Configurações do mundo (tick_rate, max_agentes, etc)
        """
        self.config = config or self._config_padrao()
        
        # Agentes registrados
        self.agentes = {}
        self.agentes_ativos = set()
        
        # Sistemas auxiliares
        self.orquestrador_contexto = None
        self.fisica_digital = None
        self.grafo_global = None
        
        # Fila de eventos
        self.fila_eventos = asyncio.Queue() if asyncio.get_event_loop().is_running() else []
        
        # Estado do mundo
        self.tempo_mundo = 0
        self.rodando = False
        self.paused = False
        
        # Localização dos agentes
        self.localizacoes = {}
        self.mapa_mundo = self._criar_mapa_inicial()
        
        # Estatísticas
        self.stats = {
            'ciclos_executados': 0,
            'eventos_processados': 0,
            'interacoes_agentes': 0,
            'tempo_execucao_total': 0
        }
        
        # Thread pool para execução paralela
        self.executor = ThreadPoolExecutor(max_workers=self.config['max_workers'])
        
        logger.info("Orquestrador Geral inicializado")
        
    def _config_padrao(self) -> Dict:
        """Configurações padrão do orquestrador"""
        return {
            'tick_rate': 1.0,  # segundos entre ciclos
            'max_agentes': 20,
            'max_workers': 4,
            'auto_save_interval': 300,  # 5 minutos
            'locais_iniciais': ['praca_central', 'templo', 'floresta', 'laboratorio']
        }
        
    def _criar_mapa_inicial(self) -> Dict:
        """Cria estrutura inicial do mundo"""
        mapa = {}
        
        for local in self.config['locais_iniciais']:
            mapa[local] = {
                'nome': local.replace('_', ' ').title(),
                'descricao': f"Um lugar no Digimundo: {local}",
                'agentes_presentes': set(),
                'propriedades': {}
            }
            
        # Definir conexões entre locais
        mapa['praca_central']['conexoes'] = ['templo', 'floresta', 'laboratorio']
        mapa['templo']['conexoes'] = ['praca_central']
        mapa['floresta']['conexoes'] = ['praca_central', 'laboratorio']
        mapa['laboratorio']['conexoes'] = ['praca_central', 'floresta']
        
        return mapa
        
    def inicializar_sistemas(self, 
                           orquestrador_contexto=None,
                           fisica_digital=None,
                           grafo_global=None):
        """
        Inicializa sistemas auxiliares
        
        Args:
            orquestrador_contexto: Instância de OrquestradorContexto
            fisica_digital: Instância de FisicaDigital
            grafo_global: Conexão com Neo4j para grafo compartilhado
        """
        self.orquestrador_contexto = orquestrador_contexto
        self.fisica_digital = fisica_digital
        self.grafo_global = grafo_global
        
        logger.info("Sistemas auxiliares inicializados")
        
    def adicionar_agente(self, 
                        nome: str, 
                        agente: Any,
                        local_inicial: str = 'praca_central') -> bool:
        """
        Adiciona um novo agente ao mundo
        
        Args:
            nome: Identificador único do agente
            agente: Instância do agente (DigimonConsciente)
            local_inicial: Local onde o agente começa
            
        Returns:
            bool: Sucesso da operação
        """
        if len(self.agentes) >= self.config['max_agentes']:
            logger.warning(f"Limite de agentes atingido ({self.config['max_agentes']})")
            return False
            
        if nome in self.agentes:
            logger.warning(f"Agente {nome} já existe")
            return False
            
        # Registrar agente
        self.agentes[nome] = agente
        self.agentes_ativos.add(nome)
        
        # Definir localização inicial
        if local_inicial in self.mapa_mundo:
            self.localizacoes[nome] = local_inicial
            self.mapa_mundo[local_inicial]['agentes_presentes'].add(nome)
        else:
            self.localizacoes[nome] = 'praca_central'
            self.mapa_mundo['praca_central']['agentes_presentes'].add(nome)
            
        # Criar contexto se orquestrador de contexto disponível
        if self.orquestrador_contexto:
            self.orquestrador_contexto.criar_contexto(nome)
            
        # Evento de nascimento
        self.adicionar_evento(Evento(
            tipo=TipoEvento.SISTEMA,
            conteudo=f"{nome} entrou no Digimundo",
            origem="sistema",
            metadata={'agente': nome, 'local': self.localizacoes[nome]}
        ))
        
        logger.info(f"Agente {nome} adicionado ao mundo em {local_inicial}")
        return True
        
    def remover_agente(self, nome: str) -> bool:
        """Remove um agente do mundo"""
        if nome not in self.agentes:
            return False
            
        # Remover de localização
        local_atual = self.localizacoes.get(nome)
        if local_atual and local_atual in self.mapa_mundo:
            self.mapa_mundo[local_atual]['agentes_presentes'].discard(nome)
            
        # Remover registros
        del self.agentes[nome]
        self.agentes_ativos.discard(nome)
        if nome in self.localizacoes:
            del self.localizacoes[nome]
            
        # Evento de saída
        self.adicionar_evento(Evento(
            tipo=TipoEvento.SISTEMA,
            conteudo=f"{nome} deixou o Digimundo",
            origem="sistema"
        ))
        
        logger.info(f"Agente {nome} removido do mundo")
        return True
        
    def adicionar_evento(self, evento: Evento):
        """Adiciona um evento à fila de processamento"""
        if asyncio.get_event_loop().is_running():
            asyncio.create_task(self.fila_eventos.put(evento))
        else:
            if isinstance(self.fila_eventos, list):
                self.fila_eventos.append(evento)
                
    async def executar_async(self):
        """Execução assíncrona do loop principal"""
        self.rodando = True
        logger.info("Iniciando execução assíncrona do Orquestrador")
        
        try:
            while self.rodando:
                if not self.paused:
                    await self._executar_ciclo_async()
                    
                await asyncio.sleep(self.config['tick_rate'])
                
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
            self.rodando = False
            
    def executar_sync(self, num_ciclos: int = -1):
        """
        Execução síncrona do loop principal
        
        Args:
            num_ciclos: Número de ciclos a executar (-1 para infinito)
        """
        self.rodando = True
        ciclos = 0
        
        logger.info(f"Iniciando execução síncrona do Orquestrador ({'infinito' if num_ciclos == -1 else f'{num_ciclos} ciclos'})")
        
        try:
            while self.rodando and (num_ciclos == -1 or ciclos < num_ciclos):
                if not self.paused:
                    self._executar_ciclo_sync()
                    ciclos += 1
                    
                time.sleep(self.config['tick_rate'])
                
        except KeyboardInterrupt:
            logger.info("Execução interrompida pelo usuário")
        except Exception as e:
            logger.error(f"Erro no loop principal: {e}")
        finally:
            self.rodando = False
            
    async def _executar_ciclo_async(self):
        """Executa um ciclo completo (versão assíncrona)"""
        inicio = time.time()
        
        # 1. Atualizar física do mundo
        eventos_mundo = await self._atualizar_mundo_async()
        
        # 2. Processar eventos pendentes
        await self._processar_eventos_async()
        
        # 3. Executar agentes em paralelo
        tasks = []
        for nome in list(self.agentes_ativos):
            task = asyncio.create_task(self._executar_agente_async(nome))
            tasks.append(task)
            
        await asyncio.gather(*tasks)
        
        # 4. Atualizar estatísticas
        self._atualizar_estatisticas(time.time() - inicio)
        
    def _executar_ciclo_sync(self):
        """Executa um ciclo completo (versão síncrona)"""
        inicio = time.time()
        
        # 1. Atualizar física do mundo
        eventos_mundo = self._atualizar_mundo_sync()
        
        # 2. Processar eventos pendentes
        self._processar_eventos_sync()
        
        # 3. Executar cada agente
        for nome in list(self.agentes_ativos):
            self._executar_agente_sync(nome)
            
        # 4. Atualizar estatísticas
        self._atualizar_estatisticas(time.time() - inicio)
        
    def _atualizar_mundo_sync(self) -> List[Evento]:
        """Atualiza o estado do mundo e gera eventos globais"""
        eventos = []
        self.tempo_mundo += 1
        
        # Atualizar física digital se disponível
        if self.fisica_digital:
            eventos_fisica = self.fisica_digital.atualizar(self.tempo_mundo)
            eventos.extend(eventos_fisica)
            
        # Eventos baseados no tempo
        if self.tempo_mundo % 100 == 0:  # A cada 100 ciclos
            hora_dia = self._calcular_hora_dia()
            eventos.append(Evento(
                tipo=TipoEvento.GLOBAL,
                conteudo=f"O tempo passa no Digimundo. Agora é {hora_dia}",
                origem="mundo"
            ))
            
        # Adicionar eventos à fila
        for evento in eventos:
            self.adicionar_evento(evento)
            
        return eventos
        
    async def _atualizar_mundo_async(self) -> List[Evento]:
        """Versão assíncrona de atualizar mundo"""
        return self._atualizar_mundo_sync()
        
    def _processar_eventos_sync(self):
        """Processa eventos pendentes na fila"""
        if isinstance(self.fila_eventos, list):
            eventos = self.fila_eventos.copy()
            self.fila_eventos.clear()
            
            for evento in eventos:
                self._processar_evento(evento)
                
    async def _processar_eventos_async(self):
        """Versão assíncrona de processar eventos"""
        while not self.fila_eventos.empty():
            evento = await self.fila_eventos.get()
            self._processar_evento(evento)
            
    def _processar_evento(self, evento: Evento):
        """Processa um evento individual"""
        self.stats['eventos_processados'] += 1
        
        # Registrar no grafo global se disponível
        if self.grafo_global and evento.tipo in [TipoEvento.GLOBAL, TipoEvento.SISTEMA]:
            self._registrar_evento_grafo(evento)
            
        # Log de eventos importantes
        if evento.tipo in [TipoEvento.SISTEMA, TipoEvento.RITUAL]:
            logger.info(f"Evento {evento.tipo.value}: {evento.conteudo}")
            
    def _executar_agente_sync(self, nome: str):
        """Executa o ciclo de um agente específico"""
        try:
            agente = self.agentes[nome]
            
            # Carregar contexto se disponível
            if self.orquestrador_contexto:
                self.orquestrador_contexto.carregar_estado(nome)
                
            # Coletar percepções
            percepcoes = self._coletar_percepcoes(nome)
            
            # Enviar percepções ao agente
            for percepcao in percepcoes:
                agente.consciencia.perceive(percepcao)
                
            # Executar ciclo do agente
            acoes = agente.viver()
            
            # Processar ações
            self._processar_acoes(nome, acoes)
            
            # Salvar contexto
            if self.orquestrador_contexto:
                self.orquestrador_contexto.salvar_estado(nome)
                
        except Exception as e:
            logger.error(f"Erro ao executar agente {nome}: {e}")
            
    async def _executar_agente_async(self, nome: str):
        """Versão assíncrona de executar agente"""
        # Por ora, delega para versão síncrona
        await asyncio.get_event_loop().run_in_executor(
            self.executor,
            self._executar_agente_sync,
            nome
        )
        
    def _coletar_percepcoes(self, nome_agente: str) -> List[Dict]:
        """Coleta percepções relevantes para um agente"""
        percepcoes = []
        local_agente = self.localizacoes.get(nome_agente)
        
        if not local_agente:
            return percepcoes
            
        # Percepção do ambiente
        local_info = self.mapa_mundo.get(local_agente, {})
        percepcoes.append({
            'tipo': 'ambiente',
            'local': local_agente,
            'descricao': local_info.get('descricao', ''),
            'agentes_presentes': list(local_info.get('agentes_presentes', set()) - {nome_agente})
        })
        
        # Eventos globais recentes
        # TODO: Implementar buffer de eventos por localização
        
        return percepcoes
        
    def _processar_acoes(self, nome_agente: str, acoes: Optional[List[Dict]]):
        """Processa as ações executadas por um agente"""
        if not acoes:
            return
            
        for acao in acoes:
            tipo_acao = acao.get('tipo')
            
            if tipo_acao == 'mover':
                self._processar_movimento(nome_agente, acao.get('destino'))
            elif tipo_acao == 'falar':
                self._processar_fala(nome_agente, acao.get('mensagem'))
            elif tipo_acao == 'interagir':
                self._processar_interacao(nome_agente, acao.get('alvo'), acao.get('tipo_interacao'))
                
    def _processar_movimento(self, agente: str, destino: str):
        """Processa movimento de um agente"""
        local_atual = self.localizacoes.get(agente)
        
        if not local_atual or destino not in self.mapa_mundo:
            return
            
        # Verificar se movimento é válido
        if destino not in self.mapa_mundo[local_atual].get('conexoes', []):
            return
            
        # Atualizar localização
        self.mapa_mundo[local_atual]['agentes_presentes'].discard(agente)
        self.mapa_mundo[destino]['agentes_presentes'].add(agente)
        self.localizacoes[agente] = destino
        
        # Evento de movimento
        self.adicionar_evento(Evento(
            tipo=TipoEvento.LOCAL,
            conteudo=f"{agente} moveu-se para {destino}",
            origem=agente,
            metadata={'local_anterior': local_atual, 'local_novo': destino}
        ))
        
    def _processar_fala(self, emissor: str, mensagem: str):
        """Processa uma mensagem falada por um agente"""
        local_emissor = self.localizacoes.get(emissor)
        
        if not local_emissor:
            return
            
        # Criar evento de mensagem para agentes no mesmo local
        agentes_local = self.mapa_mundo[local_emissor]['agentes_presentes']
        
        for receptor in agentes_local:
            if receptor != emissor:
                evento = Evento(
                    tipo=TipoEvento.MENSAGEM,
                    conteudo=mensagem,
                    origem=emissor,
                    destino=receptor,
                    metadata={'local': local_emissor}
                )
                
                # Enviar diretamente ao agente
                if receptor in self.agentes:
                    self.agentes[receptor].consciencia.perceive({
                        'tipo': 'mensagem',
                        'emissor': emissor,
                        'conteudo': mensagem
                    })
                    
        self.stats['interacoes_agentes'] += 1
        
    def _processar_interacao(self, agente: str, alvo: str, tipo_interacao: str):
        """Processa interação entre agentes"""
        if alvo not in self.agentes:
            return
            
        # Registrar interação
        self.adicionar_evento(Evento(
            tipo=TipoEvento.LOCAL,
            conteudo=f"{agente} {tipo_interacao} {alvo}",
            origem=agente,
            destino=alvo
        ))
        
        # Atualizar conexões simbióticas se disponível
        if hasattr(self.agentes[agente], 'rede'):
            self.agentes[agente].rede.registrar_interacao(alvo, tipo_interacao)
        if hasattr(self.agentes[alvo], 'rede'):
            self.agentes[alvo].rede.registrar_interacao(agente, tipo_interacao)
            
    def _calcular_hora_dia(self) -> str:
        """Calcula a hora do dia no mundo baseado no tempo"""
        hora = (self.tempo_mundo // 10) % 24
        periodos = {
            (5, 12): "manhã",
            (12, 18): "tarde",
            (18, 22): "noite",
            (22, 5): "madrugada"
        }
        
        for (inicio, fim), periodo in periodos.items():
            if inicio <= hora < fim or (inicio > fim and (hora >= inicio or hora < fim)):
                return periodo
                
        return "dia"
        
    def _registrar_evento_grafo(self, evento: Evento):
        """Registra evento no grafo global Neo4j"""
        try:
            query = """
            CREATE (e:Evento {
                tipo: $tipo,
                conteudo: $conteudo,
                origem: $origem,
                timestamp: $timestamp
            })
            """
            
            self.grafo_global.execute_query(
                query,
                tipo=evento.tipo.value,
                conteudo=evento.conteudo,
                origem=evento.origem or "desconhecido",
                timestamp=evento.timestamp
            )
            
        except Exception as e:
            logger.error(f"Erro ao registrar evento no grafo: {e}")
            
    def _atualizar_estatisticas(self, tempo_ciclo: float):
        """Atualiza estatísticas do orquestrador"""
        self.stats['ciclos_executados'] += 1
        self.stats['tempo_execucao_total'] += tempo_ciclo
        
        # Log periódico
        if self.stats['ciclos_executados'] % 100 == 0:
            tempo_medio = self.stats['tempo_execucao_total'] / self.stats['ciclos_executados']
            logger.info(f"Estatísticas: {self.stats['ciclos_executados']} ciclos, "
                       f"tempo médio: {tempo_medio:.3f}s, "
                       f"agentes ativos: {len(self.agentes_ativos)}")
            
    def pausar(self):
        """Pausa a execução do mundo"""
        self.paused = True
        logger.info("Mundo pausado")
        
    def retomar(self):
        """Retoma a execução do mundo"""
        self.paused = False
        logger.info("Mundo retomado")
        
    def parar(self):
        """Para completamente a execução"""
        self.rodando = False
        self.executor.shutdown(wait=True)
        logger.info("Orquestrador parado")
        
    def salvar_estado(self, caminho: str):
        """Salva o estado completo do mundo"""
        estado = {
            'tempo_mundo': self.tempo_mundo,
            'agentes': list(self.agentes.keys()),
            'localizacoes': self.localizacoes,
            'stats': self.stats,
            'config': self.config
        }
        
        try:
            with open(caminho, 'w') as f:
                json.dump(estado, f, indent=2)
            logger.info(f"Estado do mundo salvo em {caminho}")
        except Exception as e:
            logger.error(f"Erro ao salvar estado: {e}")
            
    def carregar_estado(self, caminho: str):
        """Carrega estado do mundo de arquivo"""
        try:
            with open(caminho, 'r') as f:
                estado = json.load(f)
                
            self.tempo_mundo = estado.get('tempo_mundo', 0)
            self.localizacoes = estado.get('localizacoes', {})
            self.stats = estado.get('stats', self.stats)
            
            logger.info(f"Estado do mundo carregado de {caminho}")
        except Exception as e:
            logger.error(f"Erro ao carregar estado: {e}")


# Exemplo de uso:
if __name__ == "__main__":
    # Criar orquestrador
    orq = OrquestradorGeral()
    
    # Adicionar agentes (assumindo que existem)
    # orq.adicionar_agente("scripturemon", scripturemon_instance)
    # orq.adicionar_agente("reflectimon", reflectimon_instance)
    
    # Executar mundo
    # orq.executar_sync(num_ciclos=100)  # Ou usar async com asyncio.run(orq.executar_async())
