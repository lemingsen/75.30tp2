from math import isinf
import pycountry_convert as pc
import networkx as nx
import pandas as pd
import metricas
import homofilia
import modelos

def armar_grafo():
    df = pd.read_csv('World.csv')
    df = df.drop(columns='ConexionAeropuertos')
    g = nx.from_pandas_edgelist(df, 'Origen', 'Destino')
    # Obtengo lista de paises
    paises = pd.concat([df['Origen'],df['Destino']]).unique()
    # Agrego los paises que no encuentra pycountry_convert
    continente_por_pais = {
        "Cote d'Ivoire": 'Africa',
        'Congo (Brazzaville)': 'Africa', 
        'Congo (Kinshasa)': 'Africa', 
        'Reunion': 'Africa', 
        'Virgin Islands': 'North America', 
        'Netherlands Antilles': 'North America', 
        'Burma': 'Asia', 
        'East Timor': 'Asia', 
        'Saint Helena': 'Africa', 
        'Western Sahara': 'Africa'
    }    
    for pais in paises:
        try:
            codigo_pais = pc.country_name_to_country_alpha2(pais, cn_name_format="default")
            codigo_continente = pc.country_alpha2_to_continent_code(codigo_pais)
            continent_name = pc.convert_continent_code_to_continent_name(codigo_continente)
            continente_por_pais[pais] = continent_name
        except KeyError:
            pass
    # Agrego el continente a cada nodo en el atributo 'type'
    nx.set_node_attributes(g, continente_por_pais, 'type')
    return g

def metrics(grafo):    
    print(f'Cantidad de Nodos: {grafo.number_of_nodes()}')
    print(f'Cantidad de Aristas: {grafo.number_of_edges()}')
    print(f'Tipo de grafo: {"Dirigido" if nx.is_directed(grafo) else "No Dirigido"}')
    print(f'Cantidad de componentes: {nx.number_connected_components(grafo)}')
    print(f'Diámetro: {nx.diameter(grafo)}')
    print(f'Distancia Promedio: {nx.average_shortest_path_length(grafo)}')
    print(f'Grado promedio: {metricas.grado_promedio(grafo)}')
    print(f'Coeficiente de clustering promedio: {metricas.clustering(grafo)[1]}')

def homofilia_por_continente(grafo):
    print(f'Proporcion cruzan continente: {homofilia.proporcion_cruzan_campo(grafo)}')
    print(f'Proporcion por continente: {homofilia.proporcion_por_tipo(grafo)}')
    print(f'Probabilidad de cruzar continente: {homofilia.probabilidad_tipos_distintos(grafo)}')
    continentes = ['North America', 'South America', 'Africa', 'Asia', 'Oceania', 'Europe']
    for continente in continentes:
        print(f'Proporcion cruzan {continente}: {homofilia.proporcion_cruzan_campo_de_tipo(grafo, continente)}')

def puentes(grafo):
    print(f'Puentes Globales: {list(nx.bridges(grafo))}')
    # filtro los puentes globales de los locales
    puentes_locales = filter(lambda puente: not isinf(puente[2]), list(nx.local_bridges(grafo)))    
    print(f'Puentes Locales: {list(puentes_locales)}')


def betweenness_centrality(grafo):
    bc = sorted(nx.betweenness_centrality(grafo).items(), key=lambda i:i[1], reverse=True)
    print(f'Betweenness Centrality: {bc}')


grafo = armar_grafo()
print('*************************** 1 *****************************')
metrics(grafo)
print('*************************** 2 *****************************')
homofilia_por_continente(grafo)
print('*************************** 3 *****************************')
puentes(grafo)
print('*************************** 4 *****************************')
betweenness_centrality(grafo)
print('*************************** 5 *****************************')
erdos_renyi = modelos.erdos_renyi(229, 24.908)
print('Metricas Erdos Renyi n=229 k=24.908:')
metrics(erdos_renyi)
print('***********************************************************')
alfa = metricas.alfa_preferential_attachment(grafo, 10 )
preferential_attachment = modelos.preferential_attachment(False, alfa, 229, 24.908)
print(f'Metricas Preferential Attachment α={alfa} n=229 k=24.908:')
metrics(preferential_attachment)





