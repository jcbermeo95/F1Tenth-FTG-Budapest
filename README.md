# Tutorial F1Tenth-FTG-Budapest
Controlador FTG en F1Tenth. Proyecto primer parcial
## Enfoque del controlador (Follow the Gap FTG)
El enfoque del controlador utilizado en el vehìculo fue una modificaciòn del FTG, dado que posee la siguiente estructura base:

**1. Recepción y tratamiento de datos del LiDAR.** Se obtiene informaciòn del LiDAR y se tratan los datos fuera del rango del LiDAR, resultando en valores computables.
**2. Establecer una región de seguridad (safety bubble).** Se establece una regiòn de seguridad basado en el valor mínimo registrado en el LiDAR más un radio de seguridad, transformando datos menores a dicho valor a cero.
**


