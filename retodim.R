setwd("/home/arwin/Hackaton/Reto Dimension/")
options(scipen=999) #Permite al usuario establecer opciones globales

#Paso 1 Lectura de la data.
data = read.csv("SALDOS1.csv", header = T, stringsAsFactors = F)
buro = read.csv("BUROCREDITO1.csv", header = T, stringsAsFactors = F)
cfe = read.csv("RFCUsuariosyconsumoapartir2018.csv", header = T, stringsAsFactors = F)

#Paso 2 Analisis de data.
str(data)
head(data)
head(buro)
head(cfe)

library(reshape2)# Facilita la transformacion de datos entre formatos.
library(dplyr) # Ayuda a transformar y resumir datos en filas y columnas.

ventas = apply(data[4:27], 1, function(x){return(12*mean(x)/0.3)}) #Devuelve un vector con al aplicar la funcion dada.
ventas[is.na(ventas)] = 0
saldo = apply(data[28:51], 1, function(x){return(12*mean(x))})
saldo[is.na(saldo)] = 0

## paso 3 Homologar la data
data2 = data.frame(NU_CTE=data$NU_CTE,rfc=data$RFC, sector=data$NB_SECTOR, antiguedad=2018-as.numeric(substr(data$FH_ANTIGUEDAD, 1,4)), saldo, ventas)
head(data2)

str(buro)
buro[is.na(buro)] = 0
summaryburo = as.data.frame(group_by(buro, NU_CTE) %>% summarise(AVGDIAS29 = mean(DIAS29), AVGDIAS59 = mean(DIAS59),AVGDIAS89 = mean(DIAS89),AVGDIAS119 = mean(DIAS119), AVGDIAS179 = mean(DIAS179), AVGDIASMAS180 = mean(DIASMAS180), sumsaldoinicial = sum(SALDOINICIAL)))

df=merge(data2,summaryburo, by = "NU_CTE",all.x=TRUE)
head(df)
dim(df)

train = df[,4:13]
str(train)

# Paso 4 Usar tecnica de machine learning para predecir la venta, Usamos SVM.
library(e1071)

modelsvm = svm(ventas ~ . , train,kernel="radial")

pred = predict(modelsvm, train)

#Paso 5 Calculamos el error cuadratico.
rmse = function(error){return(sqrt(mean(error^2)))}#calculo del error cuadratico

error = train$ventas - pred
svrPredictionRMSE = rmse(error)
svrPredictionRMSE

result = data.frame(cliente_id=df$NU_CTE,ventas=pred)
head(result)
write.table(result,"result_dimension.csv",row.names=F,sep=",")
