# Tutorial F1Tenth-FTG-Budapest
Controlador FTG en F1Tenth. Proyecto primer parcial
## Enfoque del controlador (Follow the Gap FTG)
El enfoque del controlador utilizado en el vehìculo es una modificaciòn del FTG, dado que posee la siguiente estructura base:

**1. Recepción y tratamiento de datos del LiDAR.** Se obtiene informaciòn del LiDAR y se tratan los datos fuera del rango del LiDAR, resultando en valores computables.

**2. Establecer una región de seguridad (safety bubble).** Se establece una regiòn de seguridad basado en el valor mínimo registrado en el LiDAR más un radio de seguridad, transformando datos menores a dicho valor a cero.

**3. Obtener arreglos de los valores del LiDAR.** Se obtienen subarreglos de los datos del LiDAR para cadenas consecutivas cuyos valores son distintos de 0. Además, se obtienen subarreglos de los índices.

**4. Elección del objetivo** Se realiza la selección de un subarreglo basado en casos: Si existen subarreglos que se encuentren dentro de un barrido angular de 30º, se lo agrega a un nuevo arreglo. A partir de allí, se selecciona el punto medio. Caso contrario, se selecciona el arreglo que tenga el valor máximo dentro de los subarreglos disponibles y se selecciona su punto medio.

**5. Selección de las velocidades lineales y ángulos de giro.** Basado en la distancia del objetivo, se establece distintas velocidades lineales y ángulos de giro controlados.

## Organizaciòn del código##

El código se encuentra disponible en
```
src/controllers/controllers/competition.py
```
Este código tiene los siguientes elementos:

**`__init__`**. Se crean dentro de esta los subscribers `/scan` del LiDAR, `/ego_racecar/odom`. del Odómetro y el publisher (`/drive`). Además se establecen variables internas de la clase RaceFTG.

**`odom_callback`**.  Función que registra la posición del vehiculo y determina el tiempo de vueltas y total del vehículo.

**`lidar_callback`**. Función que determina el objetivo dentro de los subarreglos tratados según el caso y publica la velocidad y ángulo de giro de las ruedas basado en la distancia del objetivo.

**`max_distance_chain`**. Función que determina el arreglo que tenga la distancia máxima dentro de un conjunto de un subarreglos.

**`find_longest_chain`**. Función que determina el arreglo con longitud más larga dentro de un conjunto de un subarreglos.

**`get_wide_arrays`**. Función que determina subarreglos dentro de un subarreglo, cuyos elementos se encuentran en un ángulo de barrido de 30º.

**`main`**. Ejecuta el programa dentro del terminal. Contiene un objeto de la clase RaceFTG.



