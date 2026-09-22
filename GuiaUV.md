# Guía Completa: Manim Community + Typst + Manim-Slides con `uv`

Esta guía documenta la configuración, flujo de trabajo, comandos y buenas prácticas para crear animaciones y presentaciones interactivas de física/matemáticas en CachyOS/Arch Linux usando la sintaxis de **Typst** y el gestor de paquetes **`uv`**.

---

## 1. Fundamentos y Decisiones Técnicas

* **ManimCE vs Motion Canvas:** Manim posee herramientas y abstracciones nativas especializadas en matemáticas y física (cálculo, campos vectoriales, coordenadas, transformaciones algebraicas complejas) que reducen el tiempo de desarrollo frente a librerías genéricas de animación.
* **Typst en lugar de LaTeX:** Evita la instalación pesada de TeX Live (ahorrando gigabytes de espacio). Typst ofrece compilación en milisegundos y una sintaxis matemática limpia y directa (`nabla times bold(E)` en lugar de macros complejas).
* **Gestión con `uv`:** Todo el proyecto vive aislado en su propio directorio. No ensucia el sistema, no requiere activar entornos manualmente y se elimina borrando una sola carpeta.
* **Presentaciones interactivas (`manim-slides`):** Permite pausar la animación por etapas (`self.next_slide()`) y avanzar con las flechas del teclado, exportando a HTML interactivo para proyectar directamente en el navegador.

---

## 2. Dependencias del Sistema en CachyOS / Arch Linux

Typst ya se encuentra instalado. Solo se requieren las dependencias gráficas y de procesamiento multimedia:

```bash
sudo pacman -S --needed ffmpeg cairo pango pkgconf
```

---

## 3. Inicialización del Proyecto con `uv`

Configura el directorio y descarga las librerías necesarias con soporte para Typst y exportación de diapositivas:

```bash
# 1. Crear el proyecto
uv init manim_fisica_slides
cd manim_fisica_slides

# 2. Agregar Manim con soporte nativo de Typst
uv add "manim[typst]"

# 3. Agregar Manim-Slides para el flujo de diapositivas
uv add manim-slides
```

---

## 4. Plantilla Reutilizable con Encabezado Persistente

Para no repetir la creación del avatar y el nombre en cada diapositiva, se define una clase base (`BasePhysicsSlide`) que hereda de `Slide`. Al usar el método del ciclo de vida `setup()`, el encabezado se renderiza automáticamente en la esquina superior izquierda antes de que comience el contenido de `construct()`.

Crea un archivo llamado `plantilla_slides.py`:

```python
from pathlib import Path
from manim import *
from manim_slides import Slide

class BasePhysicsSlide(Slide):
    """
    Clase base que inyecta automáticamente un encabezado persistente
    con foto de perfil circular y el rótulo 'Físico Juan Diego'.
    """
    def setup(self):
        super().setup()
        
        # 1. Configuración del Avatar Circular
        avatar_path = Path("avatar.png")
        radio_avatar = 0.45
        
        if avatar_path.exists():
            # Cargar imagen y aplicar máscara circular
            img = ImageMobject(str(avatar_path))
            img.height = radio_avatar * 2
            
            # Máscara circular
            mascara = Circle(radius=radio_avatar)
            avatar = Group(img)
            avatar.add(mascara)
        else:
            # Respaldo visual estilizado si no existe avatar.png
            circulo_base = Circle(
                radius=radio_avatar, 
                color=TEAL, 
                fill_opacity=0.3, 
                stroke_width=2.5
            )
            iniciales = Text("JD", font_size=20, weight=BOLD, color=WHITE)
            avatar = VGroup(circulo_base, iniciales)

        # Borde decorativo alrededor del avatar
        borde_avatar = Circle(
            radius=radio_avatar, 
            color=BLUE_C, 
            stroke_width=2
        ).move_to(avatar)

        # 2. Texto con sintaxis Typst
        nombre = Typst("*Físico Juan Diego*", font_size=22)
        nombre.next_to(borde_avatar, RIGHT, buff=0.25)

        # 3. Agrupar y anclar en la esquina superior izquierda
        self.header_badge = Group(avatar, borde_avatar, nombre)
        self.header_badge.to_corner(UL, buff=0.35)
        
        # Fijar en la escena sin animación de entrada
        self.add(self.header_badge)


# ==============================================================================
# EJEMPLO DE USO: Hereda de BasePhysicsSlide en lugar de Slide o Scene
# ==============================================================================
class DemostracionClase(BasePhysicsSlide):
    def construct(self):
        # Diapositiva 1: Título central
        titulo = Typst("*Ley de Faraday-Lenz*", font_size=42)
        titulo.shift(UP * 1.2)
        self.play(Write(titulo))
        
        # Pausa interactiva (espera tecla para avanzar)
        self.next_slide()

        # Diapositiva 2: Ecuación en sintaxis matemática de Typst
        eq_faraday = MathTypst(
            "nabla times bold(E) = - (partial bold(B)) / (partial t)",
            font_size=48
        )
        self.play(FadeIn(eq_faraday, shift=UP * 0.3))
        
        # Pausa interactiva
        self.next_slide()

        # Diapositiva 3: Transformación a caso electrostático
        eq_estatica = MathTypst(
            "nabla times bold(E) = 0", 
            font_size=48
        )
        nota = Typst(
            "_Régimen estacionario: campo conservativo_", 
            font_size=26
        ).next_to(eq_estatica, DOWN, buff=0.6)

        self.play(
            Transform(eq_faraday, eq_estatica),
            FadeIn(nota, shift=UP * 0.2)
        )
        
        # Pausa interactiva
        self.next_slide()

        # Salida limpia (el encabezado permanece fijo)
        self.play(
            FadeOut(titulo),
            FadeOut(eq_faraday),
            FadeOut(nota)
        )
```

> **Nota sobre el avatar:** Guarda tu foto de perfil con el nombre `avatar.png` en la misma raíz del proyecto. Si el archivo no existe, la plantilla creará automáticamente un círculo con las iniciales **JD** para evitar errores de compilación.

---

## 5. Renderizado y Presentación en el Navegador

El flujo para compilar y reproducir la presentación sin depender de ventanas Qt es:

```bash
# 1. Renderizar los fragmentos de video
uv run manim-slides render plantilla_slides.py DemostracionClase

# 2. Convertir y abrir directamente en el navegador web predeterminado
uv run manim-slides convert DemostracionClase presentacion.html --open
```

### Controles durante la presentación en el navegador:
* **`Espacio` o `Flecha derecha`:** Reproduce la animación y avanza a la siguiente pausa.
* **`Flecha izquierda`:** Regresa al estado de la diapositiva anterior.
* **`F`:** Alternar pantalla completa.
* **`R`:** Reiniciar la diapositiva actual.

---

## 6. Comandos Clave de Manim con Typst

Para renders rápidos de prueba que no sean diapositivas interactivas:

```bash
# Render rápido en baja calidad (480p) con vista previa automática
uv run manim -pql archivo.py NombreEscena

# Render en alta calidad (1080p a 60 fps)
uv run manim -pqh archivo.py NombreEscena

# Renderizar solo el último fotograma como imagen PNG
uv run manim -s -qh archivo.py NombreEscena
```

---

## 7. Eliminación Completa del Entorno

Dado que `uv` mantiene todo autocontenido dentro de la carpeta del proyecto, para desinstalar o limpiar todo el laboratorio basta con eliminar la carpeta:

```bash
cd ..
rm -rf manim_fisica_slides
```

Para liberar espacio de descargas cacheadas por `uv` a nivel de usuario (opcional):

```bash
uv cache clean
```