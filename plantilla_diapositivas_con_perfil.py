from manim import *
from manim_slides import Slide
import os

class BasePhysicsSlide(Slide):
    """
    Clase base que añade automáticamente la foto de perfil circular
    y el rótulo de autor en la esquina superior izquierda en todas las diapositivas.
    """
    AUTHOR_NAME = "Físico Juan Diego"
    AVATAR_PATH = "avatar.png"  # Coloca tu imagen en la misma carpeta o ajusta la ruta

    def setup(self):
        super().setup()
        self.header_group = self._crear_avatar_header()
        # Se añade directamente a la escena para que esté presente sin animar
        self.add(self.header_group)

    def _crear_avatar_header(self) -> Group:
        radio = 0.45
        
        # 1. Foto de perfil circular o fallback si no existe el archivo
        if os.path.exists(self.AVATAR_PATH):
            img = ImageMobject(self.AVATAR_PATH)
            img.height = radio * 2

            # Máscara circular para recortar la imagen redonda
            mascara = Circle(radius=radio)
            # En Manim los ImageMobjects se pueden recortar asignando máscara o envoltorio
            # Para máxima compatibilidad visual vectorizada:
            avatar_visual = Group(img)
        else:
            # Placeholder elegante si aún no has colocado la imagen 'avatar.png'
            avatar_visual = Circle(
                radius=radio,
                color=TEAL_B,
                fill_opacity=0.2,
                stroke_width=2.5
            )
            iniciales = Typst("*JD*", font_size=20).move_to(avatar_visual.get_center())
            avatar_visual = Group(avatar_visual, iniciales)

        # Borde decorativo alrededor del avatar
        borde_avatar = Circle(
            radius=radio,
            color=TEAL_C,
            stroke_width=2.5
        ).move_to(avatar_visual.get_center())

        # 2. Nombre del autor utilizando Typst
        etiqueta_nombre = Typst(
            f"*{self.AUTHOR_NAME}*",
            font_size=22
        )
        etiqueta_nombre.next_to(borde_avatar, RIGHT, buff=0.25)

        # 3. Subtítulo opcional (puedes descomentarlo si deseas)
        # sub_titulo = Typst("_Física & Matemáticas_", font_size=16).next_to(etiqueta_nombre, DOWN, buff=0.1, aligned_edge=LEFT)

        # Agrupar elementos del encabezado
        encabezado = Group(avatar_visual, borde_avatar, etiqueta_nombre)
        
        # Posicionar en la esquina superior izquierda con margen
        encabezado.to_corner(UL, buff=0.4)
        return encabezado


# ==============================================================================
# EJEMPLO DE USO: Hereda de BasePhysicsSlide en lugar de Slide
# ==============================================================================
class DemostracionClase(BasePhysicsSlide):
    def construct(self):
        # Diapositiva 1: Título centrado
        titulo = Typst("*Termodinámica: Entropía y Microestados*", font_size=36)
        titulo.to_edge(UP, buff=1.2)

        formula_boltzmann = MathTypst("S = k_B ln Omega")
        
        self.play(Write(titulo))
        self.play(FadeIn(formula_boltzmann, shift=UP * 0.3))
        
        # Pausa 1
        self.next_slide()

        # Diapositiva 2: Explicación de variables
        explicacion = Typst(
            "- $S$: Entropía del sistema\n"
            "- $k_B$: Constante de Boltzmann\n"
            "- $Omega$: Número de microestados accesibles",
            font_size=26
        ).next_to(formula_boltzmann, DOWN, buff=0.8)

        self.play(formula_boltzmann.animate.shift(UP * 0.5))
        self.play(Write(explicacion))

        # Pausa 2
        self.next_slide()

        # Diapositiva 3: Transformación a forma diferencial
        eq_termo = MathTypst("d S = (delta Q) / T")
        self.play(
            FadeOut(explicacion),
            Transform(formula_boltzmann, eq_termo)
        )
        
        # Pausa final
        self.next_slide()
        self.play(FadeOut(formula_boltzmann), FadeOut(titulo))