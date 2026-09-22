# Clases Simuladas de Física — Manim + Typst

Repositorio de **ejercicios y slides animados** de la clase de Física,
construidos con [Manim](https://www.manim.community/) y renderizados con
[Typst](https://typst.app/) para una tipografía matemática de calidad.

## Estructura

```
ClasesSimuladas/
├── README.md                        # Este archivo
├── avatar.png                       # Foto de perfil usada en los slides
├── plantilla_diapositivas_con_perfil.py
├── Guia_manim.md                    # Guía rápida de manim + manim-slides
├── GuiaUV.md                        # Notas sobre el gestor uv
└── ClaseFuerzaElectrica/            # Ejemplo: clase sobre fuerza eléctrica
    ├── problemaFuerzaElectrica.typ  # Planteamiento original en Typst
    ├── escena.py                    # Código manim-slides (13 slides)
    ├── make_avatar.py               # Script para recortar avatar circular
    ├── avatar_circle.png            # Avatar ya recortado en círculo
    ├── presentacion.html            # HTML autocontenido generado
    ├── slides/                      # JSONs de cada slide
    └── pyproject.toml               # Dependencias uv (manim, manim-slides, pillow)
```

Cada nueva clase se guarda en su propia carpeta siguiendo este patrón.

## Stack

- **uv** — gestor de paquetes y entorno virtual
- **manim** + **manim-slides** — motor de animaciones y exportación a HTML
- **MathTypst / Typst** — ecuaciones tipográficas de alta calidad (subíndices,
  superíndices, vectores, fracciones, unidades)
- **Pillow + NumPy** — recorte circular del avatar de perfil

## Cómo trabajar

```bash
cd ClaseFuerzaElectrica
uv sync
uv run manim-slides render escena.py Slide01_Titulo Slide02_Planteamiento ...
uv run manim-slides convert --folder slides --one-file --to html \
    Slide01_Titulo ... presentacion.html
xdg-open presentacion.html
```

Para profundizar:
- [`Guia_manim.md`](Guia_manim.md) — chuleta de manim-slides y Typst
- [`GuiaUV.md`](GuiaUV.md) — comandos habituales de uv

## Ejemplo: Fuerza eléctrica sobre 4 cargas

La carpeta `ClaseFuerzaElectrica/` contiene una clase completa paso a paso:

1. Planteamiento del problema (4 cargas en cuadrado 3×3)
2. Ley de Coulomb y vectores unitarios
3. Cálculo de F₄₁ (fuerza sobre q₄ debido a q₁)
4. Cálculo de F₄₂
5. Cálculo de F₄₃
6. Superposición vectorial
7. Magnitud y dirección finales

Ver `presentacion.html` para el resultado.

## Autor

**Físico Juan Diego** — clases simuladas para visualización de conceptos
de física con animaciones 2D.
