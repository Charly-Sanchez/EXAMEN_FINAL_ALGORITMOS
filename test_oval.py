import turtle
import math

# Configurar
screen = turtle.Screen()
screen.setup(1000, 700)
screen.bgcolor('#1a1a2e')

# Crear tortuga de dibujo
dibujante = turtle.Turtle()
dibujante.speed(0)
dibujante.hideturtle()

# Parámetros
ancho = 700
alto = 400
radio_curva = alto / 2
offset = 0  # Primera tortuga

# Dibujar el óvalo como en el código original
dibujante.penup()
dibujante.goto(-ancho/2 + offset, alto/2 - offset)
print(f"Inicio: {dibujante.position()}")
dibujante.setheading(0)
dibujante.pendown()
dibujante.color('white')
dibujante.width(3)

# Recta superior
dibujante.forward(ancho - 2*offset)
print(f"Después recta superior: {dibujante.position()}, heading: {dibujante.heading()}")

# Curva derecha
dibujante.circle(-(radio_curva - offset), 180)
print(f"Después curva derecha: {dibujante.position()}, heading: {dibujante.heading()}")

# Recta inferior
dibujante.setheading(180)
dibujante.forward(ancho - 2*offset)
print(f"Después recta inferior: {dibujante.position()}, heading: {dibujante.heading()}")

# Curva izquierda
dibujante.circle(-(radio_curva - offset), 180)
print(f"Después curva izquierda: {dibujante.position()}, heading: {dibujante.heading()}")

# Marcar puntos clave
marker = turtle.Turtle()
marker.hideturtle()
marker.penup()

# Punto inicial
marker.goto(-ancho/2 + offset, alto/2 - offset)
marker.dot(10, 'green')
marker.write("Inicio", font=('Arial', 10))

# Después de recta superior
marker.goto(-ancho/2 + offset + (ancho - 2*offset), alto/2 - offset)
marker.dot(10, 'yellow')
marker.write("Fin recta sup", font=('Arial', 10))

# Después de curva derecha
marker.goto(-ancho/2 + offset + (ancho - 2*offset), -alto/2 + offset)
marker.dot(10, 'red')
marker.write("Fin curva der", font=('Arial', 10))

screen.mainloop()
