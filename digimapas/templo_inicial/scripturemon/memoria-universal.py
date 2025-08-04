"""
Memória Universal (Mem0) - Sistema unificado de memória para o Digimundo
Integra memória vetorial, semântica e grafo de conhecimento
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import logging

logger = logging.getLogger(__name__)


class MemoriaUniversal:
    """
    Camada universal de memória que unifica e gerencia todos os tipos de memória.
    Implementa o pipeline Mem0: Extração → Deduplicação → Atualização
    """
    
    def __init__(self, 
                 memoria_vetorial=None, 
                 memoria_semantica=None, 
                 grafo_neo4j=None,
                 threshold_similaridade: float = 0.85):
        """
        Inicializa a Memória Universal
        
        Args:
            memoria_vetorial: Instância de MemoriaVetorial (ChromaDB)
            memoria_semantica: Instância de MemoriaSemantica (notas estruturadas)
            grafo_neo4j: Conexão com Neo4j para grafo de conhecimento
            threshold_similaridade: Limiar para considerar memórias como duplicatas
        """
        self.vetorial = memoria_vetorial
        self.semantica = memoria_semantica
        self.grafo = grafo_neo4j
        self.threshold_similaridade = threshold_similaridade
        
        # Cache de memórias recentes para otimização
        self._cache_recente = []
        self._max_cache = 100
        
        # Estatísticas
        self.stats = {
            'total_processado': 0,
            'duplicatas_evitadas': 0,
            'memorias_criadas': 0,
            'memorias_atualizadas': 0
        }
        
    def extrair_e_atualizar(self, 
                           evento: str, 
                           pensamento: str = None,
                           metadata: Dict = None) -> Dict[str, Any]:
        """
        Pipeline principal: extrai fatos relevantes e atualiza memórias
        
        Args:
            evento: Descrição do evento/interação
            pensamento: Pensamento/reflexão do agente sobre o evento
            metadata: Metadados adicionais (emoção, contexto, etc)
            
        Returns:
            Dict com resumo das operações realizadas
        """
        self.stats['total_processado'] += 1
        
        # 1. Fase de Extração
        fatos = self._extrair_fatos(evento, pensamento, metadata)
        logger.info(f"Extraídos {len(fatos)} fatos do evento")
        
        resultado = {
            'fatos_extraidos': len(fatos),
            'operacoes': []
        }
        
        # 2. Fase de Atualização
        for fato in fatos:
            operacao = self._processar_fato(fato)
            resultado['operacoes'].append(operacao)
            
        # 3. Consolidação e manutenção
        self._consolidar_memorias()
        
        return resultado
        
    def _extrair_fatos(self, 
                      evento: str, 
                      pensamento: str = None,
                      metadata: Dict = None) -> List[Dict]:
        """
        Extrai fatos atômicos de um evento/pensamento
        """
        fatos = []
        timestamp = datetime.now().isoformat()
        
        # Fato principal do evento
        if evento and evento.strip():
            fato_evento = {
                'tipo': 'evento',
                'conteudo': evento.strip(),
                'timestamp': timestamp,
                'tags': self._extrair_tags(evento),
                'importancia': metadata.get('importancia', 0.5) if metadata else 0.5,
                'fonte': 'interacao'
            }
            
            # Adicionar emoção se disponível
            if metadata and 'emocao' in metadata:
                fato_evento['emocao'] = metadata['emocao']
                
            fatos.append(fato_evento)
        
        # Fato do pensamento/reflexão
        if pensamento and pensamento.strip():
            fato_pensamento = {
                'tipo': 'reflexao',
                'conteudo': pensamento.strip(),
                'timestamp': timestamp,
                'tags': self._extrair_tags(pensamento) + ['pensamento'],
                'importancia': 0.7,  # Reflexões são geralmente importantes
                'fonte': 'interno'
            }
            fatos.append(fato_pensamento)
            
        # Extrair relações ou entidades mencionadas
        entidades = self._extrair_entidades(evento + ' ' + (pensamento or ''))
        for entidade in entidades:
            fato_entidade = {
                'tipo': 'entidade',
                'conteudo': f"Mencionado: {entidade}",
                'timestamp': timestamp,
                'tags': ['entidade', entidade.lower()],
                'importancia': 0.3,
                'fonte': 'extração'
            }
            fatos.append(fato_entidade)
            
        return fatos
        
    def _processar_fato(self, fato: Dict) -> Dict:
        """
        Processa um fato individual, decidindo se criar, atualizar ou ignorar
        """
        # Gerar hash para identificação única
        fato_hash = self._gerar_hash(fato['conteudo'])
        
        # Verificar duplicatas no cache
        if self._existe_no_cache(fato_hash):
            self.stats['duplicatas_evitadas'] += 1
            return {'acao': 'IGNORADO', 'razao': 'cache', 'fato': fato['conteudo'][:50]}
            
        # Buscar similares na memória vetorial
        if self.vetorial:
            similares = self.vetorial.buscar_contexto(fato['conteudo'], top_k=3)
            
            for similar in similares:
                if self._calcular_similaridade(fato['conteudo'], similar.get('conteudo', '')) > self.threshold_similaridade:
                    # Atualizar memória existente
                    return self._atualizar_memoria_existente(similar, fato)
                    
        # Criar nova memória
        return self._criar_nova_memoria(fato)
        
    def _criar_nova_memoria(self, fato: Dict) -> Dict:
        """
        Cria uma nova entrada de memória em todos os sistemas
        """
        try:
            # Registrar no vetor
            if self.vetorial:
                self.vetorial.registrar_evento(
                    fato['conteudo'],
                    metadata={
                        'tipo': fato['tipo'],
                        'tags': fato['tags'],
                        'importancia': fato['importancia'],
                        'timestamp': fato['timestamp']
                    }
                )
                
            # Registrar na memória semântica
            if self.semantica:
                nota_id = self.semantica.registrar_nota(
                    conteudo=fato['conteudo'],
                    tags=fato['tags'],
                    importancia=fato['importancia']
                )
                
                # Tentar link automático
                if hasattr(self.semantica, 'link_automatico'):
                    self.semantica.link_automatico(nota_id)
                    
            # Registrar no grafo
            if self.grafo and fato['tipo'] == 'entidade':
                self._registrar_no_grafo(fato)
                
            # Adicionar ao cache
            self._adicionar_ao_cache(self._gerar_hash(fato['conteudo']))
            
            self.stats['memorias_criadas'] += 1
            return {'acao': 'CRIADO', 'tipo': fato['tipo'], 'fato': fato['conteudo'][:50]}
            
        except Exception as e:
            logger.error(f"Erro ao criar memória: {e}")
            return {'acao': 'ERRO', 'erro': str(e), 'fato': fato['conteudo'][:50]}
            
    def _atualizar_memoria_existente(self, memoria_existente: Dict, novo_fato: Dict) -> Dict:
        """
        Atualiza uma memória existente com novas informações
        """
        try:
            # Incrementar contadores ou atualizar timestamp
            if self.vetorial and 'id' in memoria_existente:
                # Atualizar metadados
                nova_importancia = min(1.0, memoria_existente.get('importancia', 0.5) + 0.1)
                self.vetorial.atualizar_metadata(
                    memoria_existente['id'],
                    {
                        'ultima_mencao': novo_fato['timestamp'],
                        'importancia': nova_importancia,
                        'mencoes': memoria_existente.get('mencoes', 1) + 1
                    }
                )
                
            self.stats['memorias_atualizadas'] += 1
            return {'acao': 'ATUALIZADO', 'razao': 'similar', 'fato': novo_fato['conteudo'][:50]}
            
        except Exception as e:
            logger.error(f"Erro ao atualizar memória: {e}")
            return {'acao': 'ERRO', 'erro': str(e), 'fato': novo_fato['conteudo'][:50]}
            
    def _consolidar_memorias(self):
        """
        Consolida e otimiza memórias periodicamente
        """
        # Limpar cache se muito grande
        if len(self._cache_recente) > self._max_cache:
            self._cache_recente = self._cache_recente[-self._max_cache:]
            
        # TODO: Implementar consolidação mais avançada
        # - Mesclar memórias muito similares
        # - Arquivar memórias antigas
        # - Gerar resumos de períodos
        
    def buscar_contexto_relevante(self, 
                                  query: str, 
                                  filtros: Dict = None,
                                  limite: int = 10) -> List[Dict]:
        """
        Busca unificada em todas as memórias
        """
        resultados = []
        
        # Buscar no vetor
        if self.vetorial:
            vetor_results = self.vetorial.buscar_contexto(query, top_k=limite)
            for r in vetor_results:
                r['fonte'] = 'vetorial'
                resultados.append(r)
                
        # Buscar na semântica
        if self.semantica and filtros and 'tags' in filtros:
            for tag in filtros['tags']:
                semantica_results = self.semantica.buscar_por_tag(tag)
                for r in semantica_results:
                    resultados.append({
                        'conteudo': r.conteudo,
                        'tags': r.tags,
                        'importancia': getattr(r, 'importancia', 0.5),
                        'fonte': 'semantica'
                    })
                    
        # Ordenar por relevância/importância
        resultados.sort(key=lambda x: x.get('importancia', 0), reverse=True)
        
        return resultados[:limite]
        
    def obter_estatisticas(self) -> Dict:
        """
        Retorna estatísticas de uso da memória
        """
        stats = self.stats.copy()
        
        # Adicionar contagens de cada tipo
        if self.vetorial:
            stats['total_memorias_vetoriais'] = self.vetorial.obter_contagem()
        if self.semantica:
            stats['total_notas_semanticas'] = len(self.semantica.listar_notas())
            
        stats['cache_size'] = len(self._cache_recente)
        
        return stats
        
    # Métodos auxiliares
    
    def _extrair_tags(self, texto: str) -> List[str]:
        """Extrai tags relevantes de um texto"""
        # Implementação simples - pode ser melhorada com NLP
        palavras_chave = []
        
        # Tags baseadas em conteúdo
        if any(word in texto.lower() for word in ['amigo', 'amizade', 'conhecer']):
            palavras_chave.append('social')
        if any(word in texto.lower() for word in ['triste', 'feliz', 'alegre', 'medo']):
            palavras_chave.append('emocional')
        if any(word in texto.lower() for word in ['aprender', 'descobrir', 'entender']):
            palavras_chave.append('conhecimento')
            
        return palavras_chave
        
    def _extrair_entidades(self, texto: str) -> List[str]:
        """Extrai nomes e entidades mencionadas"""
        # Implementação básica - idealmente usar NER
        entidades = []
        
        # Procurar por padrões de nomes próprios (palavras capitalizadas)
        palavras = texto.split()
        for palavra in palavras:
            if palavra and palavra[0].isupper() and len(palavra) > 2:
                if palavra not in ['O', 'A', 'Um', 'Uma', 'De', 'Para']:
                    entidades.append(palavra)
                    
        return list(set(entidades))
        
    def _gerar_hash(self, conteudo: str) -> str:
        """Gera hash único para conteúdo"""
        return hashlib.md5(conteudo.encode()).hexdigest()
        
    def _existe_no_cache(self, fato_hash: str) -> bool:
        """Verifica se fato já existe no cache recente"""
        return fato_hash in self._cache_recente
        
    def _adicionar_ao_cache(self, fato_hash: str):
        """Adiciona hash ao cache recente"""
        self._cache_recente.append(fato_hash)
        
    def _calcular_similaridade(self, texto1: str, texto2: str) -> float:
        """Calcula similaridade simples entre textos"""
        # Implementação básica - idealmente usar embeddings
        palavras1 = set(texto1.lower().split())
        palavras2 = set(texto2.lower().split())
        
        if not palavras1 or not palavras2:
            return 0.0
            
        intersecao = palavras1.intersection(palavras2)
        uniao = palavras1.union(palavras2)
        
        return len(intersecao) / len(uniao) if uniao else 0.0
        
    def _registrar_no_grafo(self, fato: Dict):
        """Registra fato no grafo Neo4j"""
        if not self.grafo:
            return
            
        try:
            # Criar nó para entidade
            query = """
            MERGE (e:Entidade {nome: $nome})
            SET e.ultima_mencao = $timestamp,
                e.mencoes = COALESCE(e.mencoes, 0) + 1
            """
            
            # Extrair nome da entidade do conteúdo
            nome = fato['conteudo'].replace('Mencionado: ', '')
            
            self.grafo.execute_query(
                query,
                nome=nome,
                timestamp=fato['timestamp']
            )
            
        except Exception as e:
            logger.error(f"Erro ao registrar no grafo: {e}")
