import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

def interfaz_usuario():
    print("-----------Bienvenido----------")
    n_requerimientos = int(input('Por favor, ingrese la cantidad de requerimientos de su propuesta: '))
    secc_BI = [0]*8 #si usará el Dataframe_estimaciones, cambiar el valor de 8 a 14
    secc_ETL = [0]*5
    if n_requerimientos == 0:
        n_procesos =  int(input('\nPor favor, ingrese la cantidad de procesos de su propuesta: '))
        if n_procesos == 0:
            pass
        else:
            c_lbaja = int(input("Cantidad de procesos de baja prioridad: "))
            c_baja = int(input("Cantidad de procesos de media prioridad: "))
            c_media = int(input("Cantidad de procesos de alta prioridad: "))
            c_alta = int(input("Cantidad de procesos de muy alta prioridad: "))
    else:
            for i in range(n_requerimientos):
                print(f"\nIngrese los detalles del requerimiento {i+1}:")
                panel = int(input("Cantidad de vistas: "))
                panel2 = int(input("Cantidad de vistas PDF: "))
                reporte = int(input("Cantidad de reportes S: "))
                reporte2 = int(input("Cantidad de reportes M: "))
                reporte3 = int(input("Cantidad de reportes C: "))
                indicador = int(input("Cantidad de indicadores S: "))
                indicador2 = int(input("Cantidad de indicadores M: "))
                indicador3 = int(input("Cantidad de indicadores C: "))
                """
                bt = int(input("Cantidad de Bt S: "))
                bt2 = int(input("Cantidad de Bt M: "))
                bt3 = int(input("Cantidad de Bt C: "))
                lk = int(input("Cantidad de Lk S: "))
                lk2 = int(input("Cantidad de Lk M: "))
                lk3 = int(input("Cantidad de Lk C: "))
                """
                secc_BI[0] += panel
                secc_BI[1] += panel2
                secc_BI[2] += reporte
                secc_BI[3] += reporte2
                secc_BI[4] += reporte3
                secc_BI[5] += indicador
                secc_BI[6] += indicador2
                secc_BI[7] += indicador3
                """
                secc_BI[8] += bt
                secc_BI[9] += bt2
                secc_BI[10] += bt3
                secc_BI[11] += lk
                secc_BI[12] += lk2
                secc_BI[13] += lk3
                """
            c_lbaja = int(input("Cantidad de procesos de Lkbaja prioridad: "))
            c_baja = int(input("Cantidad de procesos de baja prioridad: "))
            c_media = int(input("Cantidad de procesos de media prioridad: "))
            c_alta = int(input("Cantidad de procesos de muy alta prioridad: "))
            n_proceso = c_lbaja + c_baja + c_media + c_alta
            secc_ETL[0] += c_lbaja
            secc_ETL[1] += c_baja
            secc_ETL[2] += c_media
            secc_ETL[3] += c_alta
            secc_ETL[4] += n_proceso

    return[secc_BI+secc_ETL]

def main():

    df = pd.read_csv('prueba7.csv')
    X = df[['Panel vista','Panel pdf','Reporte S','Reporte M','Reporte C','Indicador S','Indicador M','Indicador C','Cantidad_Lbaja','Cantidad_Baja','Cantidad_Media','Cantidad_Alta','Cantidad de procesos']] #si desea usar el dataframe_estimaciones agregar 'Bt S','Bt M','Bt C','Lk S','Lk M','Lk C' entre 'Indicador C' y 'Cantidad_Lbaja'
    y = df['Total_TOTAL']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Entrenar el modelo
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Realizar predicciones Base del modelo
    y_pred = model.predict(X_test)
    r2 = r2_score(y_test, y_pred)
    r2 = max(0, min(1, r2))
    r2 = r2_score(y_test, y_pred)
    r2 = max(0, min(1, r2))
    r2_percent = r2 * 100

    #interfaz de usuario
    interfaz = interfaz_usuario()
    
    print(interfaz) 
    total_total = model.predict(interfaz)[0]
    print(total_total*0.6)
    print(f"Coeficiente de determinación (R^2): {r2_percent:.2f}%")


    
if __name__== "__main__":
    main()
