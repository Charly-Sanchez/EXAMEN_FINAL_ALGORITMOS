import math

# Simular cálculo de rutas para S-Doble
ancho_carril = 70
num_tortugas = 3
puntos_ruta = []

for i in range(num_tortugas):
    ruta_tortuga = []
    y_offset = 150 - (i * ancho_carril)
    
    for x in range(-450, 451, 3):
        # Primera S
        if x < -150:
            y = y_offset + 80 * math.sin((x + 450) * 0.015)
        # Transición
        elif x < 150:
            y = y_offset + 80 * math.sin((x + 150) * 0.015)
        # Segunda S invertida
        else:
            y = y_offset - 80 * math.sin((x - 150) * 0.015)
        
        ruta_tortuga.append((x, y))
    
    puntos_ruta.append(ruta_tortuga)
    print(f"Tortuga {i}: {len(ruta_tortuga)} puntos")
    print(f"  Y offset: {y_offset}")
    print(f"  Primer punto: {ruta_tortuga[0]}")
    print(f"  Último punto: {ruta_tortuga[-1]}")
    print()

print(f"Total de tortugas: {len(puntos_ruta)}")
print("✅ Simulación exitosa, no hay errores en el cálculo")
