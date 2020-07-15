# Oscilaciones-Amortiguadas

Codigo Python para visualizar gráficas de amplitud y velocidad de un oscilador amortiguado, además de una animación simulando este mismo movimiento.

Está escrito en Python 3.8.2 y con los módulos matplotlib, tkinter y numpy.

El evento a simular es el movimiento amortiguado de una esfera bajo la influencia de un resorte que la traslada a traves de un fluido viscoso.

El usuario define en una ventana de tkinter las mangitudes principales del sistema tales como la constante de amortiguamiento del fluido, la constante elástica del resorte y la masa de la esfera; cada uno en unidades de kg/s, N/m y kg. También ingresa los valores de las condiciones iniciales tales como la posición y velocidad de la esfera sumergida en un tiempo t=0s.

Tras esto, se puede seleccionar una de las dos opciones a querer visualizar:
-Visualizar una gráfica estática que muestre las curvas de amplitud y velocidad contra el tiempo sin ninguna animación (mejor opción para propositos de imagenes)
-Visualizar una gráfica animada que muestre la evolución de las curvas de amplitud y velocidad contra el tiempo además de una animación de una "bolita" que se traslada a traves de un eje vertical acorde a las variables ingresadas.

Se eligió intervalos de tiempo de 15 milisegundos para la gráfica animada para una mejor fluidez sin sacrificar tiempo de ejecución hasta la última posición calculada.

<a href="https://www.codecogs.com/eqnedit.php?latex=m\frac{d^2y}{dt^2}&plus;v\frac{dy}{dt}&plus;ky=0" target="_blank"><img src="https://latex.codecogs.com/gif.latex?m\frac{d^2y}{dt^2}&plus;v\frac{dy}{dt}&plus;ky=0" title="m\frac{d^2y}{dt^2}+v\frac{dy}{dt}+ky=0" /></a>
