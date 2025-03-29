# comunidades_calculo_autoconsumo
**calculo_autoconsumido_v11.py**

Este escript calcula la energía consumida, autoconsumida y exportada cada hora partiendo de un servidor emonCMS

Se parte de dos registros de energía, la energía consumida y la energía generada, entendiendo como energía generada la correspondinte incluyendo el coeficiente de reparto

El resultado se trasmite al servidor con la información de la hora para que se pueda guardar y posteriormete visualizar

La configuración necesita:
* **config_sensores.ini** con la información del servidor para extraer los datos necesarios
* **comunidad.sql** una base de datos con el esquema incluido en fichero

El escript esta hecho para ejecutarse automaticamente desde el crontab de un servidor aunque también se puede hacer manualmente
