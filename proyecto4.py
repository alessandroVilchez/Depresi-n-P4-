"""
    Tareas a Realizar: 
        - cual es la ciudad que tiene la mayor cantidad de casos de depresión 
        - cual es el rango de edades de personas que sufren de depresión 
        - el porcentaje de personas que han tenido pensamientos suicidas 
        - qué género es el que más estres financiero tiene  
"""
import pandas as pd 
import mysql.connector  

conn= mysql.connector.connect(
    host="localhost",
    user="root", 
    password="aleyolen24"
)

cursor=conn.cursor(buffered=True)

df=pd.read_csv("student_depression_dataset.csv")      

#REVISAR EL NOMBRE DE LAS COLUMNAS, LOS TIPOS DE DATOS QUE POSEE Y VERIFICAR QUE NO HAYA DATOS NULOS
df.info()
 
#REVISAR QUE NO HAYA FILAS DUPLICADAS 
df.duplicated().any()

#REVISAR QUE NO HAYA CELDAS VACIAS O DATOS NULOS
df.isnull().any()

#REVISAR SI HAY VALORES "UNKNOWN"
(df == "unknown").any()

#REVISAR SI HAY VALORES DUPLICADOS EN LA COLUMNA ID, YA QUE ES LA UNICA COLUMNA LA CUAL NO DEBERIA TENER VALORES DOBLES
df["id"].nunique()

# CONVERTIR A MINUSCULAS TODOS LOS VALORES DE LAS COLUMNAS CON TIPO STRING:

for x in df.columns:
    if df[x].dtypes==object:
        if df[x].str.isalpha().all():
            df[x]=df[x].str.lower()


#EN EL BLOQUE DE CODIGO ANTERIOR NO SE PUDO CONVERTIR LOS STRINGS DE LA COLUMNA "CITY" A LETRAS MINUSCULAS PORQUE HABIA 
#UNA FILA CON EL VALOR MEZCLADO ENTRE INT Y STR ASI QUE SE TUVO QUE HACER UN FILTRO EXCLUSIVO  

df.drop(df[df["City"].astype(str).str.contains(r'(?=.*[A-Za-z])(?=.*\d)', regex=True)].index, inplace=True)
df["City"]=df["City"].str.lower()



#EN LA COLUMNA FINANCIAL STRESS SE TUVO QUE CREAR UN FILTRO PARTICULAR PORQUE HABIA UN CARACTER EL CUAL NO IBA A PERMITIR 
#LA CONVERSION DE LA COLUMNA A INT

b=df[df["Financial Stress"].str.contains(r'\?', regex=True)].index
df.drop(b, inplace=True)
df["Financial Stress"]=df["Financial Stress"].astype(float).astype(int)


#PASANDO A INT SOLO LOS VALORES DE COLUMNAS DE TIPO FLOAT CON UN CERO FLOTANTE. POR EJEMPLO: 1.0 SE CONVERTIRÁ A 1

floats=df.select_dtypes(include="float64")
a=floats.columns[floats.mod(1).ne(00).any()].to_list()
floats.drop(a, axis=1, inplace=True)
floatsColumns=floats.astype(int)
df[floatsColumns.columns]=floatsColumns


#RESETEAR EL INDEX PORQUE SE ELIMINARON 3 FILAS

df.reset_index(drop=True, inplace=True)


#RESETEAR EL ID YA QUE SE ELIMINARON FILAS. 

df["id"]=[x for x in range(1,len(df["id"]) + 1)]


#SE HA LIMPIADO TODO EL DATAFRAME PERO EN REALIDAD SOLO SE VA A TRABAJAR EN POWER BI CON  
#LAS COLUMNAS: CITY, AGE, GENDER ,SUICIDAL THOUGHTS, FINANCIAL STRESS. 

df["Suicidal Thoughts"]=df["Have you ever had suicidal thoughts ?"]
analisis= df.loc[:, ["City", "Age", "Gender","Financial Stress", "Suicidal Thoughts"]]




#CONEXION A BASE DE DATOS, CREACION DE TABLA CON LA DATA EN LA CUAL SE VA A TRABAJAR EN POWER BI

# cursor.execute("USE db")
# cursor.execute("""CREATE TABLE proyecto4(
#                id INT AUTO_INCREMENT PRIMARY KEY,
#                city VARCHAR(60),
#                age INT,
#                gender VARCHAR(30),
#                financialStress INT,
#                suicidalThoughts VARCHAR(10) 
# )""")

# cursor.execute("SELECT * FROM proyecto4")

# for i,v in df.iterrows():
#     sql="INSERT INTO proyecto4(city, age, gender, financialStress, suicidalThoughts) VALUES (%s, %s, %s, %s, %s)"
#     valor=(v["City"], v["Age"], v["Gender"], v["Financial Stress"], v["Suicidal Thoughts"] )

#     cursor.execute(sql, valor)
# conn.commit()
