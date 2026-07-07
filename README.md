# Tutorial F1Tenth-FTG-Budapest
Controlador FTG en F1Tenth. Proyecto primer parcial
## Enfoque del controlador (Follow the Gap FTG)
El enfoque del controlador utilizado en el vehìculo es una modificaciòn del FTG, dado que posee la siguiente estructura base:

**1. Recepción y tratamiento de datos del LiDAR.** Se obtiene informaciòn del LiDAR y se tratan los datos fuera del rango del LiDAR, resultando en valores computables.

**2. Establecer una región de seguridad (safety bubble).** Se establece una regiòn de seguridad basado en el valor mínimo registrado en el LiDAR más un radio de seguridad, transformando datos menores a dicho valor a cero.

**3. Obtener arreglos de los valores del LiDAR.** Se obtienen subarreglos de los datos del LiDAR para cadenas consecutivas cuyos valores son distintos de 0. Además, se obtienen subarreglos de los índices.

**4. Elección del objetivo** Se realiza la selección de un subarreglo basado en casos: Si existen subarreglos que se encuentren dentro de un barrido angular de 30º, se lo agrega a un nuevo arreglo. A partir de allí, se selecciona el punto medio. Caso contrario, se selecciona el arreglo que tenga el valor máximo dentro de los subarreglos disponibles y se selecciona su punto medio.


