import os

def contar_carpetas_en_directorio(directorio):
    # Inicializamos un contador para las carpetas
    contador_carpetas = 0

    # Iteramos sobre los elementos en el directorio
    for elemento in os.listdir(directorio):
        # Comprobamos si el elemento es una carpeta
        if os.path.isdir(os.path.join(directorio, elemento)):
            contador_carpetas += 1

    return contador_carpetas

# Directorio en el que quieres contar las carpetas
directorio_padre = './train_images'

# Llamamos a la función para contar las carpetas en ese directorio
cantidad_carpetas = contar_carpetas_en_directorio(directorio_padre)

print(f'La cantidad de carpetas en el directorio {directorio_padre} es: {cantidad_carpetas}')
