from PIL import Image
import os

def create_icon():
    try:
        # Cargar la imagen PNG desde la carpeta assets
        png_path = os.path.join('assets', 'icon.png')
        if not os.path.exists(png_path):
            print(f"Error: No se encontró el archivo {png_path}")
            return
            
        # Abrir la imagen PNG
        img = Image.open(png_path)
        
        # Asegurarse de que la imagen sea cuadrada
        size = max(img.size)
        new_img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        new_img.paste(img, ((size - img.size[0]) // 2, (size - img.size[1]) // 2))
        
        # Redimensionar a 256x256 para el icono
        new_img = new_img.resize((256, 256), Image.Resampling.LANCZOS)
        
        # Guardar como ICO
        new_img.save('icon.ico', format='ICO', sizes=[(256, 256)])
        print("Icono creado exitosamente.")
        
    except Exception as e:
        print(f"Error al crear el icono: {str(e)}")

if __name__ == "__main__":
    create_icon() 