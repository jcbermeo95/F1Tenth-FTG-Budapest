# Tutorial F1Tenth-FTG-Budapest
Controlador FTG en F1Tenth. Proyecto primer parcial
## Enfoque del controlador (Follow the Gap FTG)
El enfoque del controlador utilizado en el vehìculo es una modificaciòn del FTG, dado que posee la siguiente estructura base:

**1. Recepción y tratamiento de datos del LiDAR.** Se obtiene informaciòn del LiDAR y se tratan los datos fuera del rango del LiDAR, resultando en valores computables.

**2. Establecer una región de seguridad (safety bubble).** Se establece una regiòn de seguridad basado en el valor mínimo registrado en el LiDAR más un radio de seguridad, transformando datos menores a dicho valor a cero.

**3. Obtener arreglos de los valores del LiDAR.** Se obtienen subarreglos de los datos del LiDAR para cadenas consecutivas cuyos valores son distintos de 0. Además, se obtienen subarreglos de los índices.

**4. Elección del objetivo** Se realiza la selección de un subarreglo basado en casos: Si existen subarreglos que se encuentren dentro de un barrido angular de 30º, se lo agrega a un nuevo arreglo. A partir de allí, se selecciona el punto medio. Caso contrario, se selecciona el arreglo que tenga el valor máximo dentro de los subarreglos disponibles y se selecciona su punto medio.

**5. Selección de las velocidades lineales y ángulos de giro.** Basado en la distancia del objetivo, se establece distintas velocidades lineales y ángulos de giro controlados.

## Organizaciòn del código

El código se encuentra disponible en
```
src/controllers/controllers/competition.py
```
Este código tiene los siguientes elementos:

Tòpicos usados:

`/scan` (`sensor_msgs/LaserScan`). Detecta datos del LiDAR.
`/ego_racecar/odom` (`nav_msgs/Odometry`). Obtiene posición del vehículo para determinar tiempos de vuelta y total. El cronómetro determina el tiempo de vueltas cuando el vehículo cruza la posición X=0.
`/drive` (`ackermann_msgs/AckermannDriveStamped`). Envía datos para mover el vehículo.

Funciones:

**`__init__`**. Se crean dentro de esta los subscribers `/scan` del LiDAR, `/ego_racecar/odom`. del Odómetro y el publisher (`/drive`). Además se establecen variables internas de la clase RaceFTG.

**`odom_callback`**.  Función que registra la posición del vehiculo y determina el tiempo de vueltas y total del vehículo.

**`lidar_callback`**. Función que determina el objetivo dentro de los subarreglos tratados según el caso y publica la velocidad y ángulo de giro de las ruedas basado en la distancia del objetivo. Para modificar el movimiento del vehículo se recomienda modificar las variables `self.safety_bubble`,`drive_msg.drive.speed` y `steering_angle`.

**`max_distance_chain`**. Función que determina el arreglo que tenga la distancia máxima dentro de un conjunto de un subarreglos.

**`find_longest_chain`**. Función que determina el arreglo con longitud más larga dentro de un conjunto de un subarreglos.

**`get_wide_arrays`**. Función que determina subarreglos dentro de un subarreglo, cuyos elementos se encuentran en un ángulo de barrido de 30º.

**`main`**. Ejecuta el programa dentro del terminal. Contiene un objeto de la clase RaceFTG.

## Guía de instalación

Sigue estos pasos para configurar el entorno en **Ubuntu 22.04** con **ROS2 Humble**.

### 1. Prerrequisitos
Asegúrate de tener ROS2 Humble instalado. Carga el entorno:
```bash
source /opt/ros/humble/setup.bash
```

### 2. Instalar F1Tenth Gym
Seguir la guía de instalación de ROS 2 Humble y dado en:

```bash
https://github.com/widegonz/F1Tenth-Repository
```
Asegúrate de seguir los pasos correctamente.

### 3. Descargar la carpeta src/controllers del repositorio.

Descarga la carpeta src/controllers dentro de este repositorio. Copie el archivo competition.py dentro de src/controllers/controllers a la carpeta respectiva de home/F1Tenth-Repository/src/controllers/controllers y péguelo dentro de dicha carpeta con los demás documentos con extensión de Python. 

Use el siguiente comando en el terminal para que el archivo.py se pueda ejecutar:
```bash
cd F1Tenth-Repository/src/controllers/controllers
colcon build
chmod +x competition.py
```
Modifica la posición inicial del vehículo en el archivo sim.yaml de la siguiente manera:

```bash
# ego starting pose on map
    sx: 0.0
    sy: 0.0
    stheta: -0.702474197
```

### 4. Cambiar el mapa.

Descarga el mapa Budapest_map y Budapest_map_obstacle con extensiones png y sus respecto archivos yaml dentro de la carpeta `src/controllers/maps` del repositorio de esta página y péguelos en la carpeta de home/F1Tenth-Repository/src/f1tenth_gym_ros/maps. 
Abre `src/f1tenth_gym_ros/config/sim.yaml` y cambia la ruta del mapa para la carrera sin obstáculo en Budapest por :

```yaml
map_path: '/home/<tu_usuario>/F1Tenth-Repository/src/f1tenth_gym_ros/maps/Budapest_map'
```
y la mapa de la carrera con obstáculo por 

```yaml
map_path: '/home/<tu_usuario>/F1Tenth-Repository/src/f1tenth_gym_ros/maps/Budapest_map_obstacle'
```
### 5. Añade el respectivo del archivo para ejecutar.

Añade el nombre del respectivo archivo competition en el archivo setup.py ubicado en home/F1Tenth-Repository/src/controllers

```bash
...
tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'competition = controllers.competition:main',
...
```


## Ejecución


Abre la terminal y ejecuta el siguiente comando.


```bash
cd ~/F1Tenth-Repository
source install/setup.bash
colcon build
ros2 launch f1tenth_gym_ros gym_bridge_launch.py
```

En otra ventana del terminal ejecuta el siguiente comando

```bash
source install/setup.bash
ros2 run controllers competition
```

El tiempo se mostrará al ejecutar el archivo de competition.py dado por este último comando. Aproximadamente se espera un tiempo promedio de cada vuelta de 43s. En caso de que el vehículo choque debido a variaciones de mediciones del LiDAR u otro asuntos cierre toda la terminal y ejecute los últimos dos pasos del comando. No se recomienda cambio de vista, debido que esto produce crasheo del sistema. 
NOTA: No se ha realizado la simulación en F1Tenth para 2 o más vehículos.

Autor: Julio Bermeo


