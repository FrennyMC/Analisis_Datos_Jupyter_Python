# Importar librerías necesarias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

# Ignorar advertencias específicas
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Cargar el dataset
data = pd.read_csv("IMDB_top_1000v2.csv")

# Mostrar una vista preliminar de los datos y las columnas
print(data.head())
print(data.columns)  # Verificar nombres exactos de las columnas

# Función para limpieza de datos (manejo de nulos, etc.)
def limpiar_datos(df):
    # Ajustar nombres de columnas según el dataset
    df = df.dropna(subset=['Director', 'Star1', 'Gross', 'No_of_Votes', 'Genre'])
    return df

# Limpiar el dataset
data = limpiar_datos(data)

    """
        Permite visualizar las ganancias de todas las películas de un director
        específico mediante un gráfico de barras. El usuario introduce el nombre
        del director y la función muestra las ganancias de cada película dirigida
        por esa persona.
    """
# 1. Análisis de las ganancias de una película en función de su director (Intervención del usuario)
def ganancias_por_director(df):
    director = input("Ingrese el nombre de un director para ver sus ganancias promedio: ")
    director_data = df[df['Director'] == director]
    if director_data.empty:
        print("No se encontraron datos para el director ingresado.")
    else:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=director_data['Gross'], y=director_data['Series_Title'], palette="viridis")
        plt.title(f"Ganancias de las películas de {director}", fontsize=16)
        plt.xlabel("Ganancias", fontsize=14)
        plt.ylabel("Película", fontsize=14)
        plt.tight_layout()
        plt.show()
ganancias_por_director(data)

    """
        Busca las películas donde el actor aparece (ya sea como Star1, Star2,
        Star3 o Star4) y muestra las ganancias de cada una en un gráfico de
        barras.
    """

# 2. Análisis de las ganancias de una película en función de los actores en la misma 
def ganancias_por_actor(df):
    actor = input("Ingrese el nombre de un actor para ver sus ganancias promedio: ")
    actor_data = df[(df['Star1'] == actor) | (df['Star2'] == actor) | (df['Star3'] == actor) | (df['Star4'] == actor)]
    if actor_data.empty:
        print("No se encontraron datos para el actor ingresado.")
    else:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=actor_data['Gross'], y=actor_data['Series_Title'], palette="plasma")
        plt.title(f"Ganancias de las películas de {actor}", fontsize=16)
        plt.xlabel("Ganancias", fontsize=14)
        plt.ylabel("Película", fontsize=14)
        plt.tight_layout()
        plt.show()

ganancias_por_actor(data)

    """
        Visualiza el número de votos recibidos en IMDb para cada película de
        un director específico. Ayuda a entender la popularidad de las
        películas de cada director.
    """

# 3. Análisis del número de votos de una película en función de su director (Intervención del usuario)
def votos_por_director(df):
    director = input("Ingrese el nombre de un director para ver el promedio de votos de sus películas: ")
    director_data = df[df['Director'] == director]
    if director_data.empty:
        print("No se encontraron datos para el director ingresado.")
    else:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=director_data['No_of_Votes'], y=director_data['Series_Title'], palette="coolwarm")
        plt.title(f"Votos de las películas de {director}", fontsize=16)
        plt.xlabel("Número de Votos", fontsize=14)
        plt.ylabel("Película", fontsize=14)
        plt.tight_layout()
        plt.show()

votos_por_director(data)

    """
        Muestra el número de votos en IMDb para todas las películas
        en las que participa un actor específico, permitiendo ver qué
        películas del actor fueron más populares.
    """
# 4. Análisis del número de votos de una película en función de los actores en la misma (Intervención del usuario)
def votos_por_actor(df):
    actor = input("Ingrese el nombre de un actor para ver el promedio de votos de sus películas: ")
    actor_data = df[(df['Star1'] == actor) | (df['Star2'] == actor) | (df['Star3'] == actor) | (df['Star4'] == actor)]
    if actor_data.empty:
        print("No se encontraron datos para el actor ingresado.")
    else:
        plt.figure(figsize=(10, 6))
        sns.barplot(x=actor_data['No_of_Votes'], y=actor_data['Series_Title'], palette="magma")
        plt.title(f"Votos de las películas de {actor}", fontsize=16)
        plt.xlabel("Número de Votos", fontsize=14)
        plt.ylabel("Película", fontsize=14)
        plt.tight_layout()
        plt.show()

votos_por_actor(data)

    """    
        Crea un gráfico de barras apiladas que muestra los géneros
        más frecuentes en los que trabajan los actores más prolíficos.
        Visualiza los top 10 actores y los 5 géneros más comunes.
    """
# 5. ¿Cuál actor prefiere cuál género? (Gráfico de barras apiladas)
def genero_preferido_por_actor_barras(df, top_n=10, top_genres=5):
    # Crear una lista con todos los actores de cada película, una fila por actor y género
    actores_genero = df.melt(
        id_vars=['Genre'],
        value_vars=['Star1', 'Star2', 'Star3', 'Star4'],
        var_name='StarPosition', 
        value_name='Actor'
    )
    
    # Contar la frecuencia de cada género por actor
    actor_genero = actores_genero.groupby(['Actor', 'Genre']).size().unstack(fill_value=0)
    
    # Seleccionar los actores con más apariciones
    top_actors = actor_genero.sum(axis=1).sort_values(ascending=False).head(top_n).index
    actor_genero_top = actor_genero.loc[top_actors]
    
    # Seleccionar los géneros más frecuentes para simplificar el gráfico
    top_genres = actor_genero_top.sum(axis=0).sort_values(ascending=False).head(top_genres).index
    actor_genero_top = actor_genero_top[top_genres]
    
    # Crear el gráfico de barras apiladas
    ax = actor_genero_top.plot(kind="bar", stacked=True, figsize=(12, 8), colormap="viridis")
    plt.title("Preferencias de Género por Actor (Top 10 Actores, Top 5 Géneros)", fontsize=16)
    plt.xlabel("Actor", fontsize=14)
    plt.ylabel("Frecuencia de Género", fontsize=14)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Género", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.show()

# Llamada a la función, limitando a los 10 actores más frecuentes y los 5 géneros más populares
genero_preferido_por_actor_barras(data, top_n=10, top_genres=5)

    """
        Analiza qué combinaciones de 4 actores obtienen las mejores
        calificaciones promedio en IMDb, mostrando las 10 mejores combinaciones.
    """
# 6. ¿Cuál combinación de actores obtiene buenos ratings más a menudo?
def combinacion_actores_mejores_ratings(df):
    df['Actors'] = df['Star1'] + ", " + df['Star2'] + ", " + df['Star3'] + ", " + df['Star4']
    actor_combos = df.groupby('Actors')['IMDB_Rating'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=actor_combos.values, y=actor_combos.index, palette="cubehelix", dodge=False)
    plt.title("Combinación de Actores con Mejores Ratings", fontsize=16)
    plt.xlabel("Rating Promedio", fontsize=14)
    plt.ylabel("Combinación de Actores", fontsize=14)
    plt.tight_layout()
    plt.show()

combinacion_actores_mejores_ratings(data)

    """
        enfocada en ganancias. Muestra las 10
        combinaciones de actores que generan mayores ingresos en promedio.
    """

# 7. ¿Cuál combinación de actores obtiene las máximas ganancias?
def combinacion_actores_mayor_ganancia(df):
    df['Actors'] = df['Star1'] + ", " + df['Star2'] + ", " + df['Star3'] + ", " + df['Star4']
    actor_combos_ganancias = df.groupby('Actors')['Gross'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=actor_combos_ganancias.values, y=actor_combos_ganancias.index, palette="viridis", dodge=False)
    plt.title("Combinación de Actores con Máximas Ganancias", fontsize=16)
    plt.xlabel("Ganancia Promedio", fontsize=14)
    plt.ylabel("Combinación de Actores", fontsize=14)
    plt.tight_layout()
    plt.show()

combinacion_actores_mayor_ganancia(data)

    """
        Analiza qué géneros de películas son más rentables,
        mostrando las ganancias promedio por género en un gráfico de barras.
    """

# 8. Análisis del género de las películas en función de las ganancias obtenidas
def genero_por_ganancias(df):
    genero_ganancias = df.groupby('Genre')['Gross'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=genero_ganancias.values, y=genero_ganancias.index, palette="Set2", dodge=False)
    plt.title("Ganancias Promedio por Género", fontsize=16)
    plt.xlabel("Ganancia Promedio", fontsize=14)
    plt.ylabel("Género", fontsize=14)
    plt.tight_layout()
    plt.show()

genero_por_ganancias(data)

    """
        Visualiza cómo ha evolucionado la distribución de
        géneros cinematográficos a lo largo de las décadas,
        mostrando el porcentaje de cada género por década.
    """

# 9. ¿Cuál es la distribución porcentual de las películas por género y por década?
def distribucion_por_genero_decada(df):
    df['Decade'] = (df['Released_Year'] // 10) * 10
    genero_decada = df.groupby(['Decade', 'Genre']).size().unstack().fillna(0)
    genero_decada_percentage = genero_decada.apply(lambda x: x / x.sum() * 100, axis=1)
    genero_decada_percentage.plot(kind="bar", stacked=True, figsize=(14, 10), colormap="tab20")
    plt.title("Distribución Porcentual de Películas por Género y Década", fontsize=16)
    plt.xlabel("Década", fontsize=14)
    plt.ylabel("Porcentaje", fontsize=14)
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
    plt.tight_layout()
    plt.show()

distribucion_por_genero_decada(data)

    """
        Identifica qué películas generan más ingresos por minuto de
        duración, dividiendo las ganancias totales entre la duración
        de la película.
    """

# 10. ¿Cuáles son las 10 películas más rentables por minuto?
def peliculas_mas_rentables_por_minuto(df):
    df['Revenue_per_minute'] = df['Gross'] / df['Runtime']
    rentables_por_minuto = df.sort_values(by='Revenue_per_minute', ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=rentables_por_minuto['Revenue_per_minute'], y=rentables_por_minuto['Series_Title'], palette="summer")
    plt.title("Top 10 Películas Más Rentables por Minuto", fontsize=16)
    plt.xlabel("Ganancia por Minuto", fontsize=14)
    plt.ylabel("Título", fontsize=14)
    plt.tight_layout()
    plt.show()

peliculas_mas_rentables_por_minuto(data)

#---------------------------------------------------------------------------------------------------
#Preguntas Extra

    """
        Calcula y muestra la calificación promedio de
        IMDb para todas las películas de un director específico.
    """

def calificacion_promedio_por_director(df):
    director = input("Ingrese el nombre de un director para ver la calificación promedio de sus películas: ")
    director_data = df[df['Director'] == director]
    if director_data.empty:
        print("No se encontraron películas para el director ingresado.")
    else:
        promedio_calificacion = director_data['IMDB_Rating'].mean()
        print(f"La calificación promedio para las películas de {director} es: {promedio_calificacion:.2f}")

calificacion_promedio_por_director(data)

    """
        Muestra qué géneros tienen las mejores calificaciones promedio en IMDb,
        ayudando a identificar los géneros más apreciados por los usuarios.
    """

def genero_mejor_calificacion(df):
    genero_calificacion = df.groupby('Genre')['IMDB_Rating'].mean().sort_values(ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=genero_calificacion.values, y=genero_calificacion.index, palette="Blues")
    plt.title("Géneros con Mejor Calificación Promedio en IMDb", fontsize=16)
    plt.xlabel("Calificación Promedio", fontsize=14)
    plt.ylabel("Género", fontsize=14)
    plt.tight_layout()
    plt.show()

genero_mejor_calificacion(data)

    """
        Identifica las 10 películas que han recibido más votos en IMDb,
        lo que puede indicar su popularidad general entre los espectadores.
    """

def peliculas_mas_votadas(df):
    peliculas_votadas = df.sort_values(by='No_of_Votes', ascending=False).head(10)
    plt.figure(figsize=(12, 8))
    sns.barplot(x=peliculas_votadas['No_of_Votes'], y=peliculas_votadas['Series_Title'], palette="magma")
    plt.title("Top 10 Películas Más Populares por Número de Votos", fontsize=16)
    plt.xlabel("Número de Votos", fontsize=14)
    plt.ylabel("Título de la Película", fontsize=14)
    plt.tight_layout()
    plt.show()

peliculas_mas_votadas(data)



