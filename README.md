# RETO-5-grupo-azul-oscuro-
Guion para seguir los cuadernos en orden: qué se hace en cada uno y por qué. Trabajamos con préstamos de tipo «Negocios» y cada cuaderno usa el resultado del anterior.

1. Preprocesamiento
Se carga el Excel con todos los préstamos y nos quedamos solo con los de Negocios (76.515). Se revisan nulos y duplicados y se eliminan las 2 filas con datos incompletos.

2. Análisis descriptivo
Se estudian las variables una a una y frente al impago (11,6 % de los préstamos). Se limpian 3 duplicados y la columna Proposito, que es igual en todos. Se ve que impagan más los jóvenes, con menos antigüedad laboral y con interés alto. También se descubre que la prima tiene un tope según la duración del préstamo y que no depende del riesgo.

3. VAN y TIR
Se ve cada préstamo como una inversión del banco: presta el capital hoy y cobra cuotas después. Se calcula el VAN y la TIR de cada uno para decidir si es viable (VAN > 0) y se comprueba que la TIR coincide con la TAE. Incluye ejemplos de descuento y de rentas (constantes, geométricas, perpetuas).

4 y 5. Amortización alemana y francesa
Se programan los dos sistemas de pago. En el alemán se amortiza lo mismo cada mes y las cuotas bajan; en el francés la cuota es fija. Después se crea un modelo de puntos que asigna cada cliente a un sistema: el alemán solo para quien puede asumir cuotas altas y el francés para el resto.

6. Valor presente
Para cada préstamo se toman las cuotas que quedan por cobrar a mitad del plazo y se traen a valor de hoy. Genera las columnas Valor_Presente y Valor_Final.

7 y 8. Modelo de impago
Se entrena una regresión logística para predecir la probabilidad de impago. Como hay pocos impagos, se duplican al azar solo en entrenamiento. Con validación cruzada se optimizan los parámetros del modelo y se ajusta el umbral de decisión. Se evalúa al final con datos que el modelo no ha visto: detecta el 47 % de los impagos.

9 y 10. Modelo del coste del seguro
Se predice la prima del seguro. Se parte de un modelo lineal, se eligen 6 variables (monto, duración, scoring, interés, deuda/ingresos e ingresos) y se mejora con un polinomio de grado 5 con regularización Ridge. Las predicciones se limitan al mínimo y al tope de cada duración. En test el error medio es de 38,7 € y explica el 95,5 % de la variación de la prima.
