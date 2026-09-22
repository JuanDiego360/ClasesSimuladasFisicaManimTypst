# Guía Práctica: Manim Community + Typst con `uv`

Este documento resume el flujo de trabajo moderno para generar animaciones matemáticas y presentaciones interactivas en **CachyOS / Arch Linux**, combinando la potencia de **Manim Community**, la sintaxis moderna de **Typst** para fórmulas y la gestión de proyectos de **`uv`**.

---

## 1. Conceptos Clave Aprendidos

* **Manim vs. Typst:** Typst es un motor de composición tipográfica de alto rendimiento (escrito en Rust), no un motor de animación por sí mismo. Manim es el motor de animación procedural. Al unirlos (`MathTypst`), Typst se encarga de renderizar la tipografía matemática a vectores instantáneamente, mientras Manim anima las transformaciones.
* **Sin TeX Live gigante:** Usar Typst evita instalar múltiples gigabytes de LaTeX (`texlive-*`), acelerando los tiempos de compilación de fórmulas a SVG de forma drástica.
* **Gestión con `uv`:** Al usar `uv init` y `uv run`, todo el entorno virtual (`.venv`) y las dependencias quedan aislados en la carpeta del proyecto. No se ensucia el sistema operativo y para desinstalar todo basta con eliminar la carpeta del proyecto.
* **Presentaciones interactivas (`manim-slides`):** Permite pausar animaciones con `self.next_slide()` para avanzar término a término con el teclado, ideal para clases y conferencias.

---

## 2. Dependencias de Sistema (CachyOS / Arch)

Solo se requieren las librerías gráficas de compilación y multimedia. LaTeX **no** es necesario:

```bash
sudo pacman -S --needed typst ffmpeg cairo pango pkgconf
```

---

## 3. Inicialización del Proyecto con `uv`

```bash
# 1. Crear el proyecto tipo aplicación
uv init mi_proyecto_animaciones
cd mi_proyecto_animaciones

# 2. Agregar Manim con soporte oficial para Typst y diapositivas
uv add "manim[typst]" manim-slides
```

---

## 4. Estructura de Código: Diapositiva Interactiva con Typst

Crea un archivo llamado `escena.py`:

```python
from manim import *
from manim_slides import Slide

class ClaseFisica(Slide):
    def construct(self):
        # 1. Título estructurado con sintaxis Typst
        titulo = Typst("*Demostración: Ley de Faraday*").to_edge(UP)
        self.play(Write(titulo))
        
        # Pausa: espera tecla de avance (Espacio o Flecha derecha)
        self.next_slide()

        # 2. Ecuación en sintaxis nativa de Typst:
        # Se escribe directo: bold(), vec(), partial, etc. (sin barras invertidas)
        eq_campo = MathTypst("nabla times bold(E) = - (partial bold(B)) / (partial t)")
        self.play(FadeIn(eq_campo, shift=UP * 0.3))
        
        # Pausa
        self.next_slide()

        # 3. Transformación matemática
        eq_estatico = MathTypst("nabla times bold(E) = 0")
        nota = Typst("_Caso electrostático (campo conservativo)_", font_size=28).next_to(eq_estatico, DOWN)
        
        self.play(
            Transform(eq_campo, eq_estatico),
            FadeIn(nota, shift=UP * 0.2)
        )
        
        # Pausa final
        self.next_slide()
        self.play(FadeOut(eq_campo), FadeOut(nota), FadeOut(titulo))
```

---

## 5. Comandos de Renderizado y Presentación

### Renderizado de los fragmentos de la presentación
```bash
uv run manim-slides render escena.py ClaseFisica
```

### Visualización en el Navegador Web (Recomendado)
Convierte la presentación a Reveal.js / HTML autocontenido y la abre directamente en tu navegador (evita depender de ventanas Qt):

```bash
uv run manim-slides convert ClaseFisica presentacion.html --open
```

**Controles en el navegador:**
* **`Flecha derecha` / `Espacio`:** Avanza al siguiente fragmento animado.
* **`Flecha izquierda`:** Retrocede a la diapositiva anterior.
* **`F`:** Modo pantalla completa.

---

## 6. Renderizado de Video Tradicional (MP4 directo)

Si en lugar de diapositivas quieres exportar un video continuo convencional:

* **Vista previa rápida en baja resolución (480p):**
  ```bash
  uv run manim -pql escena.py ClaseFisica
  ```

* **Calidad de producción (1080p, 60 FPS):**
  ```bash
  uv run manim -pqh escena.py ClaseFisica
  ```

* **Guardar solo el último fotograma como imagen:**
  ```bash
  uv run manim -s -qh escena.py ClaseFisica
  ```

---

## 7. Notas Técnicas y Resolución de Problemas

1. **Error `qtpy.QtBindingsNotFoundError`:**
   * Ocurre si intentas ejecutar el visor de escritorio `manim-slides present` sin un backend Qt instalado.
   * **Solución A (preferida):** Presentar en el navegador con `uv run manim-slides convert ClaseFisica presentacion.html --open`.
   * **Solución B:** Si quieres la ventana nativa de escritorio, instala PySide:
     ```bash
     uv add "manim-slides[pyside6]"
     ```
     *(En Wayland/Hyprland, si no abre la ventana, ejecutar con: `QT_QPA_PLATFORM=wayland uv run manim-slides present ClaseFisica`).*

2. **Limpieza completa del proyecto:**
   Como todo está confinado al directorio del proyecto:
   ```bash
   cd ..
   rm -rf mi_proyecto_animaciones
   ```
   No deja residuos ni en los paquetes del sistema ni en bibliotecas globales.