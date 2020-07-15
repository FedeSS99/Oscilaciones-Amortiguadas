import matplotlib.pyplot as plt
from numpy import exp, sqrt, cos, sin
from matplotlib.animation import FuncAnimation
from tkinter import *

# Se declaran los diccionarios que contienen el formato a utilizar para el titulo y datos.
titulo_config = {'family': 'serif',
                 'style': 'oblique',
                 'color': 'white',
                 'weight': 'heavy',
                 'size': 12}
datos_config = {'family': 'serif',
                'color': 'white',
                'weight': 'heavy',
                'size': 9}

# Se fija el backend a utilizar y el estilo a utilizar del entorno de las gráficas.
plt.switch_backend('TkAgg')
plt.style.use('dark_background')


# Se declara la función 'generar datos' que recibe de entrada
# el determinante D, la altura y velocidad inicial, la constante
# de amortiguamiento, la masa del objeto y la constante elástica
# del resorte.
def generar_datos(D, y0, v0, b, M, k):
    def sobreamortiguado(t1, h, v1, b1, d1):
        m1, m2 = (-b1 + sqrt(d1)) / (2 * M), (-b1 - sqrt(d1)) / (2 * M)
        c = ((v1 - h * m1) / (m1 - m2))
        return (h - c) * exp(m1 * t1) + c * exp(m2 * t1)

    def amortiguado_critico(t2, h, b2, m2, v2):
        c1 = -b2 / (2 * m2)
        return h * exp(c1 * t2) + (h * (-c1) + v2) * t2 * exp(c1 * t2)

    def oscilacion_sub(t3, b3, m3, k0, h, v3):
        w = sqrt((k0 / m3) - pow((b3 / (2 * m3)), 2))
        c2 = -b3 / (2 * m3)
        c3 = (b3 * h + 2 * m3 * v3) / (2 * m3 * w)
        return exp(c2 * t3) * (h * cos(w * t3) + c3 * sin(w * t3))

    # Se declaran las listas y variables para generar en un ciclo while los datos de amplitud y tiempo.
    amplitudes, tiempos = [], []
    y = y0
    t = 0
    dt = 0.015
    a = 0.001
    tipo = ''
    amplitudes.append(y)
    tiempos.append(t)
    if y > 0:
        if D > 0:
            tipo = 'Sobreamortiguado'
            while y > a * y0:
                t += dt
                y = sobreamortiguado(t, y0, v0, b, D)
                amplitudes.append(y)
                tiempos.append(t)
        elif D == 0:
            tipo = 'Amortiguado Critico'
            while y > a * y0:
                t += dt
                y = amortiguado_critico(t, y0, b, M, v0)
                amplitudes.append(y)
                tiempos.append(t)
        elif D < 0:
            tipo = 'Subamortiguado'
            k3 = -b / (2 * M)
            y1, y2 = y0 * exp(k3 * t), -y0 * exp(k3 * t)
            dif_y = y1 - y2
            while dif_y > a * y0:
                t += dt
                dif_y = 2 * y0 * exp(k3 * t)
                y = oscilacion_sub(t, b, M, k, y0, v0)
                amplitudes.append(y)
                tiempos.append(t)

    elif y < 0:
        if D > 0:
            tipo = 'Sobreamortiguado'
            while y < a * y0:
                t += dt
                y = sobreamortiguado(t, y0, v0, b, D)
                amplitudes.append(y)
                tiempos.append(t)
        elif D == 0:
            tipo = 'Amortiguado Critico'
            while y < a * y0:
                t += dt
                y = amortiguado_critico(t, y0, b, M, v0)
                amplitudes.append(y)
                tiempos.append(t)
        elif D < 0:
            tipo = 'Subamortiguado'
            k3 = -b / (2 * M)
            y1, y2 = -y0 * exp(k3 * t), y0 * exp(k3 * t)
            dif_y = y1 - y2
            while dif_y > abs(a * y0):
                t += dt
                y1, y2 = -y0 * exp(k3 * t), y0 * exp(k3 * t)
                dif_y = y1 - y2
                y = oscilacion_sub(t, b, M, k, y0, v0)
                amplitudes.append(y)
                tiempos.append(t)

    # Las velocidades se calculan mediante diferencias finitas, se considera que la derivada ha de tener la forma:
    #       dy      y_(i+1)-y_i
    #       -- =   -------------
    #       dt      t_(i+1)-t_i
    velocidades = [(amplitudes[i + 1] - amplitudes[i]) /
                   dt for i in range(len(amplitudes) - 1)]

    # Para el último valor de t, se coonsidera
    #       dy      y_(i)-y_(i-1)
    #       -- =   -------------
    #       dt      t_(i)-t_(i-1)
    velocidades.append(
        (amplitudes[len(amplitudes) - 1] - amplitudes[len(amplitudes) - 2]) / dt)

    return amplitudes, tiempos, tipo, velocidades


def simulacion(m, b, k, v0, y0):
    d = pow(b, 2) - 4 * m * k

    amplitudes, tiempos, tipomoa, velocidades = generar_datos(
        d, y0, v0, b, m, k)

    figura, (sub1, sub2) = plt.subplots(
        1, 2, gridspec_kw={'width_ratios': [10, 8]})

    sub1.set_xlabel('Tiempo (s)')
    sub1.set_ylabel('Y (m)', rotation=0, labelpad=12)
    sub1.spines['top'].set_visible(False)

    sub1_2 = sub1.twinx()
    sub1_2.set_ylabel('V (m/s)', rotation=0, labelpad=20)
    sub1_2.spines['top'].set_visible(False)

    sub2.text(0.65, 0.45, f'Masa={m}kg\n' +
              f'Cte. Amortiguamiento={b}kg/s\n' +
              f'Cte. elastica={k}kg/m\n' +
              f'Velocidad inicial={v0}m/s\n' +
              f'Posición inicial={y0}m\n\n' +
              f'Tiempo final={max(tiempos):.3f}s', transform=sub2.transAxes, fontdict=datos_config)

    sub2.set_ylabel('Y (m)', rotation=0, labelpad=15)
    sub2.spines['right'].set_visible(False)
    sub2.spines['top'].set_visible(False)
    sub2.spines['bottom'].set_visible(False)
    sub2.get_xaxis().set_visible(False)

    sub1.set_xlim(min(tiempos), max(tiempos))
    if min(amplitudes) < max(amplitudes):
        sub1.set_ylim(min(amplitudes) - 0.2, max(amplitudes) + 0.2)
        sub2.set_ylim(min(amplitudes) - 0.2, max(amplitudes) + 0.2)
    elif min(amplitudes) > max(amplitudes):
        sub1.set_ylim(max(amplitudes) - 0.2, min(amplitudes) + 0.2)
        sub2.set_ylim(max(amplitudes) - 0.2, min(amplitudes) + 0.2)

    if min(velocidades) < max(velocidades):
        sub1_2.set_ylim(min(velocidades) - 0.2, max(velocidades) + 0.2)
        sub1_2.set_ylim(min(velocidades) - 0.2, max(velocidades) + 0.2)
    elif min(velocidades) > max(velocidades):
        sub1_2.set_ylim(max(velocidades) - 0.2, min(velocidades) + 0.2)
        sub1_2.set_ylim(max(velocidades) - 0.2, min(velocidades) + 0.2)

    sub1.set_title('Amplitud vs Tiempo y Velocidad vs Tiempo',
                   fontdict=titulo_config)
    sub2.set_title('Simulación', fontdict=titulo_config)
    figura.suptitle(f'Tipo: {tipomoa}', fontsize=18,
                    weight='heavy', style='oblique', family='serif')

    amplitud, = sub1.plot([], [], '-r', linewidth=1, label='Amplitud')
    velocidad, = sub1_2.plot([], [], '-b', linewidth=1, label='Velocidad')
    objeto, = sub2.plot([], [], 'ro', markersize=7)
    texto = sub2.text(0.65, 0.65, '', transform=sub2.transAxes,
                      fontdict=datos_config)

    sub1.legend(bbox_to_anchor=(1.05, 0.7, 0.3, 0.2), loc='upper right')
    sub1_2.legend(bbox_to_anchor=(1.05, 0.6, 0.3, 0.2), loc='upper right')

    plt.subplots_adjust(wspace=0.5, left=0.05)

    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')

    def inicio():
        amplitud.set_data([], [])
        velocidad.set_data([], [])
        objeto.set_data([], [])
        texto.set_text('')
        return amplitud, velocidad, objeto, texto

    def animacion(i):
        amplitud.set_data(tiempos[:i], amplitudes[:i])
        velocidad.set_data(tiempos[:i], velocidades[:i])
        objeto.set_data(0, amplitudes[i])
        texto.set_text(f't={tiempos[i]:.3f}s')
        return amplitud, velocidad, objeto, texto

    FuncAnimation(figura, animacion, init_func=inicio, frames=len(
        amplitudes), interval=0.0001, blit=True, repeat=False)
    plt.show()


def grafica_estatica():
    masa = float(Masa_entrada.get())
    amortiguamiento = float(Amortiguamiento_entrada.get())
    elastica = float(elastica_entrada.get())
    velocidad = float(velocidad_entrada.get())
    posicion = float(Posicion_F.get())

    D = pow(amortiguamiento, 2) - 4 * masa * elastica

    amplitudes, tiempos_2d, tipo_2d, velocidades_2d = generar_datos(D, posicion, velocidad, amortiguamiento, masa,
                                                                    elastica)

    figura2, (sub3, sub4) = plt.subplots(
        1, 2, gridspec_kw={'width_ratios': [12, 3]})

    sub3.plot(tiempos_2d, amplitudes, '-r', linewidth=1, label='Amplitud')
    sub3.spines['top'].set_visible(False)
    sub3.set_xlabel('Tiempo (s)')
    sub3.set_ylabel('Y (m)', rotation=0)

    sub3_2 = sub3.twinx()
    sub3_2.spines['top'].set_visible(False)
    sub3_2.plot(tiempos_2d, velocidades_2d, '-b',
                linewidth=1, label='Velocidad')
    sub3_2.set_ylabel('V (m/s)', rotation=0, labelpad=20)
    sub3.set_xlim(min(tiempos_2d), max(tiempos_2d))

    sub3.legend(bbox_to_anchor=(1, 0.7, 0.3, 0.2), loc='upper right')
    sub3_2.legend(bbox_to_anchor=(1, 0.6, 0.3, 0.2), loc='upper right')

    sub4.text(0.01, 0.5, f'Masa={masa}kg\n' +
              f'Cte. Amortiguamiento={amortiguamiento}kg/s\n' +
              f'Cte. elastica={elastica}kg/m\n' +
              f'Velocidad inicial={velocidad}m/s\n' +
              f'Posición inicial={posicion}m\n\n' +
              f'Tiempo final={max(tiempos_2d):.3f}s', fontdict=datos_config)
    sub4.set_frame_on(False)
    sub4.get_xaxis().set_visible(False)
    sub4.get_yaxis().set_visible(False)

    sub3.set_title('Amplitud vs Tiempo y Velocidad vs Tiempo',
                   fontdict=titulo_config)
    figura2.suptitle(f'Tipo: {tipo_2d}', fontsize=18,
                     weight='heavy', style='oblique', family='serif')

    plt.subplots_adjust(wspace=0.2, left=0.05)
    manager = plt.get_current_fig_manager()
    manager.window.state('zoomed')


# Función para cerrar la ventana y terminar el programa.
def salir():
    ventana_opciones.destroy()
    raise SystemExit(0)


# Función principal que encapsula todos los elementos de texto, cajas de entrada de texto y botones para
# poner en marcha la simulación o salir del programa.
def principal():
    global Masa_entrada, Amortiguamiento_entrada, elastica_entrada, velocidad_entrada, Posicion_F
    Button(ventana_opciones, text=" Salir ", activeforeground='red',
           activebackground='gray', command=salir).grid(row=9, column=1)
    Button(ventana_opciones, text=" Gráfica Estatica ", activeforeground='red',
           activebackground='gray', command=grafica_estatica).grid(row=9, column=2)
    Button(ventana_opciones, text=" Correr Simulacion", activeforeground='red',
           activebackground='gray', command=obtencion_simulacion).grid(row=9, column=3)
    Label(ventana_opciones, text='Ingrese la masa, en kilogramos (kg), del objeto sumergido:').grid(
        row=1, column=0)
    Masa_entrada = Entry(ventana_opciones, width=6)
    Masa_entrada.insert(10, '10')
    Masa_entrada.grid(row=1, column=1)
    Label(ventana_opciones,
          text='Ingrese la constante de amortiguamiento en kilogramos sobre segundo (kg/s):').grid(row=2, column=0)
    Amortiguamiento_entrada = Entry(ventana_opciones, width=6)
    Amortiguamiento_entrada.insert(10, '10')
    Amortiguamiento_entrada.grid(row=2, column=1)
    Label(ventana_opciones,
          text='Ingrese la magnitud de la constante elastica del resorte en Newtons sobre metro (N/m):').grid(
        row=3, column=0)
    elastica_entrada = Entry(ventana_opciones, width=6)
    elastica_entrada.insert(10, '10')
    elastica_entrada.grid(row=3, column=1)
    Label(ventana_opciones,
          text='Ingrese la velocidad inicial en metros sobre segundo (m/s):').grid(row=4, column=0)
    velocidad_entrada = Entry(ventana_opciones, width=6)
    velocidad_entrada.insert(10, '0')
    velocidad_entrada.grid(row=4, column=1)
    Label(ventana_opciones, text='Ingrese la posición inicial en metros (m):').grid(
        row=5, column=0)
    Posicion_F = Entry(ventana_opciones, width=6)
    Posicion_F.insert(10, '10')
    Posicion_F.grid(row=5, column=1)


def obtencion_simulacion():
    # Se asignan los valores escritos en las cajas de entrada de la ventana de Tkinter
    # a las siguientes variables que después seran evaluadas en la función simulación o gráfica.
    masa = float(Masa_entrada.get())
    amortiguamiento = float(Amortiguamiento_entrada.get())
    elastica = float(elastica_entrada.get())
    velocidad = float(velocidad_entrada.get())
    posicion = float(Posicion_F.get())

    if posicion != 0 and masa > 0 and amortiguamiento > 0 and elastica > 0:
        simulacion(masa, amortiguamiento, elastica, velocidad, posicion)


ventana_opciones = Tk()
ventana_opciones.title('Movimiento Oscilatorio Amortiguado')
ventana_opciones.resizable(width=False, height=False)
principal()
ventana_opciones.mainloop()
