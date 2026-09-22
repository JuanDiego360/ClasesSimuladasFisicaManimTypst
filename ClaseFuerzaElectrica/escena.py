from pathlib import Path
from manim import *
from manim_slides import Slide


# ==============================================================================
# CLASE BASE CON AVATAR CIRCULAR REAL + BADGE
# ==============================================================================
class BasePhysicsSlide(Slide):
    def setup(self):
        super().setup()
        # Avatar con recorte circular REAL (hecho con PIL en make_avatar.py)
        avatar_path = Path("avatar_circle.png")
        radio_avatar = 0.42

        if avatar_path.exists():
            img = ImageMobject(str(avatar_path))
            img.height = radio_avatar * 2
            # Borde decorativo alrededor del avatar (visible encima de la imagen)
            borde_avatar = Circle(
                radius=radio_avatar + 0.01,
                color=BLUE_C,
                stroke_width=2.5,
            )
            avatar = Group(img, borde_avatar)
        else:
            circulo_base = Circle(
                radius=radio_avatar, color=TEAL, fill_opacity=0.3, stroke_width=2.5
            )
            iniciales = Text("JD", font_size=20, weight=BOLD, color=WHITE)
            avatar = VGroup(circulo_base, iniciales)

        nombre = Text("Físico Juan Diego", font_size=22, weight=BOLD)
        nombre.next_to(avatar, RIGHT, buff=0.25)
        self.header_badge = Group(avatar, nombre)
        self.header_badge.to_corner(UL, buff=0.35)
        # Fijar en la escena sin animación de entrada
        self.add(self.header_badge)


# Helper: aplica to_edge con margen suficiente para no chocar con el badge
def title(mob):
    mob.to_edge(UP, buff=1.1)
    return mob


# Helper: crea un panel cartesiano pequeño para mostrar vectores
def panel_vectores(self, posiciones, vectores_fuerza, vectores_posicion=None, titulo_panel="", factor=0.5):
    """
    Crea un Axes pequeño a la derecha con puntos en `posiciones` (dict nombre->(x,y)),
    vectores POSICIÓN (desde origen) en `vectores_posicion` (dict nombre->(x,y)),
    y vectores FUERZA (desde la posición de cada carga) en `vectores_fuerza` (dict nombre->(dx,dy)).
    Los vectores fuerza se dibujan escalados por `factor` para que quepan en el plano.
    Devuelve el group (ejes+puntos+vectores).
    """
    # Calcular bounds incluyendo los extremos de los vectores
    xs = [p[0] for p in posiciones.values()]
    ys = [p[1] for p in posiciones.values()]
    if vectores_posicion:
        for v in vectores_posicion.values():
            xs.append(v[0])
            ys.append(v[1])
    if vectores_fuerza:
        for n, v in vectores_fuerza.items():
            xs.append(posiciones[n][0] + v[0] * factor)
            ys.append(posiciones[n][1] + v[1] * factor)
    x_min, x_max = min(min(xs), 0) - 1.0, max(max(xs), 0) + 1.5
    y_min, y_max = min(min(ys), 0) - 1.0, max(max(ys), 0) + 1.5

    ejes = Axes(
        x_range=[int(x_min) - 1, int(x_max) + 1, 1],
        y_range=[int(y_min) - 1, int(y_max) + 1, 1],
        x_length=4.4,
        y_length=4.4,
        axis_config={"include_numbers": True, "font_size": 14},
    )
    ejes.to_edge(RIGHT, buff=0.6).shift(DOWN * 0.4)

    grupo = VGroup(ejes)

    # Título pequeño del panel
    if titulo_panel:
        t = Typst(titulo_panel, font_size=18, color=YELLOW).next_to(ejes, UP, buff=0.25)
        grupo.add(t)

    colores = {"q1": RED, "q2": BLUE, "q3": GREEN, "q4": YELLOW}
    nombres = list(posiciones.keys())

    # 1) Vectores POSICIÓN (desde el origen hacia la carga) — finos y punteados
    if vectores_posicion:
        for nombre, v in vectores_posicion.items():
            if v == (0, 0):
                continue
            col = colores.get(nombre, WHITE)
            arr = DashedLine(
                ejes.c2p(0, 0),
                ejes.c2p(v[0], v[1]),
                color=col,
                stroke_width=2,
                dash_length=0.1,
            )
            # Etiqueta a mitad de la línea
            label = Typst(nombre, font_size=14, color=col).move_to(
                ejes.c2p(v[0] / 2, v[1] / 2)
            ).shift(LEFT * 0.15)
            grupo.add(arr, label)

    # 2) Puntos (cargas) + etiquetas
    for nombre in nombres:
        pos = posiciones[nombre]
        col = colores.get(nombre, WHITE)
        d = Dot(ejes.c2p(pos[0], pos[1]), color=col, radius=0.09)
        l = Typst(nombre, font_size=16, color=WHITE).next_to(d, UR, buff=0.05)
        grupo.add(d, l)

    # 3) Vectores FUERZA (desde cada carga, escalados) — más elegantes
    if vectores_fuerza:
        for nombre, v in vectores_fuerza.items():
            if v == (0, 0):
                continue
            pos = posiciones[nombre]
            col = colores.get(nombre, WHITE)
            origen = ejes.c2p(pos[0], pos[1])
            destino = ejes.c2p(pos[0] + v[0] * factor, pos[1] + v[1] * factor)
            arrow = Arrow(
                origen, destino,
                color=col,
                buff=0,
                stroke_width=3.5,
                max_tip_length_to_length_ratio=0.25,
            )
            # Etiqueta al final de la flecha (escalada)
            f_label = Typst(
                f"${factor}$×$F$",
                font_size=12,
                color=col,
            ).move_to(destino).shift(UR * 0.2)
            grupo.add(arrow, f_label)

    return grupo


# ==============================================================================
# SLIDE 1: TITULO
# ==============================================================================
class Slide01_Titulo(BasePhysicsSlide):
    def construct(self):
        titulo = Text(
            "Problema de Electrostática", font_size=52, weight=BOLD, color=BLUE_C
        ).shift(UP * 1.5)
        subtitulo = Text(
            "Fuerza Eléctrica sobre una carga", font_size=30
        ).next_to(titulo, DOWN, buff=0.4)
        linea = Line(LEFT * 4, RIGHT * 4, color=BLUE_C, stroke_width=2).next_to(
            subtitulo, DOWN, buff=0.6
        )
        self.play(Write(titulo))
        self.play(FadeIn(subtitulo, shift=UP * 0.3))
        self.play(Create(linea))
        self.next_slide()


# ==============================================================================
# SLIDE 2: PLANTEAMIENTO
# ==============================================================================
class Slide02_Planteamiento(BasePhysicsSlide):
    def construct(self):
        # Título arriba
        titulo = title(Text("Planteamiento del Problema", font_size=38, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # Descripción a la IZQUIERDA (no en cascada vertical con el título)
        desc = Typst(
            "*4 cargas están en el plano XY*",
            font_size=24,
        )
        desc.to_edge(LEFT, buff=0.7).shift(UP * 1.0)
        self.play(FadeIn(desc, shift=UP * 0.2))
        self.next_slide()

        # Ejes a la derecha
        ejes = Axes(
            x_range=[-0.5, 5.5, 1],
            y_range=[-0.5, 5.5, 1],
            x_length=4.5,
            y_length=4.5,
            axis_config={"include_numbers": True, "font_size": 18},
        ).to_edge(RIGHT, buff=0.7).shift(DOWN * 0.3)
        self.play(Create(ejes))
        self.next_slide()

        def dot(pos, color, label):
            d = Dot(ejes.c2p(pos[0], pos[1]), color=color, radius=0.1)
            l = Typst(label, font_size=16).next_to(d, RIGHT, buff=0.1)
            return d, l

        q1d, q1l = dot((0, 0), RED, "$q_1 = 8 mu C$")
        q2d, q2l = dot((0, 3), BLUE, "$q_2 = -2 mu C$")
        q3d, q3l = dot((3, 0), GREEN, "$q_3 = 4 mu C$")
        q4d, q4l = dot((3, 3), YELLOW, "$q_4 = 2 mu C$")
        for d, l in [(q1d, q1l), (q2d, q2l), (q3d, q3l), (q4d, q4l)]:
            self.play(FadeIn(d, scale=0.5), Write(l))
            self.wait(0.3)
        self.next_slide()

        # Objetivo en la parte inferior, ancho completo
        objetivo = Typst(
            "*Calcular:* $arrow(F)_4 = arrow(F)_(41) + arrow(F)_(42) + arrow(F)_(43)$",
            font_size=26,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(objetivo, shift=UP * 0.2))
        self.next_slide()


# ==============================================================================
# SLIDE 3: LEY DE COULOMB
# ==============================================================================
class Slide03_LeyCoulomb(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Ley de Coulomb", font_size=40, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        eq = MathTypst(
            "arrow(F)_(i j) = K_e (q_i q_j) / r_(i j)^2 dot hat(r)_(i j)",
            font_size=48,
        )
        self.play(FadeIn(eq, shift=UP * 0.3))
        self.next_slide()

        significado = VGroup(
            Typst("$K_e = 9 times 10^9$ *N·m²/C²*", font_size=24),
            Typst("$q_i, q_j$: *magnitudes de las cargas (C)*", font_size=24),
            Typst("$r_(i j)$: *distancia entre las cargas (m)*", font_size=24),
            Typst("$hat(r)_(i j)$: *vector unitario dirección*", font_size=24),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.6)
        for item in significado:
            self.play(FadeIn(item, shift=UP * 0.15))
            self.wait(0.2)
        self.next_slide()


# ==============================================================================
# SLIDE 4: F41 - PLANTEAMIENTO
# ==============================================================================
class Slide04_F41_Plant(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Fuerza sobre q₄ debido a q₁", font_size=34, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # Panel cartesiano: posiciones, vectores POSICIÓN desde origen y FUERZA escalada
        panel = panel_vectores(
            self,
            posiciones={"q1": (0, 0), "q4": (3, 3)},
            vectores_posicion={"q1": (0, 0), "q4": (3, 3)},
            vectores_fuerza={"q4": (3, 3)},  # dirección r_41 escalada
            titulo_panel="Plano XY: $arrow(r)_(41)$",
            factor=0.45,
        )
        self.play(Create(panel[0]), FadeIn(panel[1:]))
        self.next_slide()

        # Ecuación a la IZQUIERDA
        eq = MathTypst(
            "arrow(F)_(41) = K_e (q_4 q_1) / r_(41)^2 dot hat(r)_(41)",
            font_size=36,
        )
        eq.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        self.play(FadeIn(eq, shift=UP * 0.3))
        self.next_slide()

        datos = VGroup(
            MathTypst("arrow(r)_4 = 3 hat(i) + 3 hat(j) space (m)", font_size=22),
            MathTypst("arrow(r)_1 = 0 hat(i) + 0 hat(j) space (m)", font_size=22),
            MathTypst("q_4 = 2 times 10^(-6) space C", font_size=22),
            MathTypst("q_1 = 8 times 10^(-6) space C", font_size=22),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.5).align_to(eq, LEFT)
        for d in datos:
            self.play(FadeIn(d, shift=UP * 0.15))
            self.wait(0.2)
        self.next_slide()


# ==============================================================================
# SLIDE 5: F41 - CALCULO DE r
# ==============================================================================
class Slide05_F41_R(BasePhysicsSlide):
    def construct(self):
        titulo = title(Typst("*Cálculo de* $hat(r)_(41)$", font_size=38))
        self.play(Write(titulo))
        self.next_slide()

        paso1 = MathTypst(
            "arrow(r)_4 - arrow(r)_1 = (3 hat(i) + 3 hat(j)) - (0 + 0) = 3 hat(i) + 3 hat(j) space (m)",
            font_size=28,
        )
        self.play(FadeIn(paso1, shift=UP * 0.2))
        self.next_slide()

        paso2 = MathTypst(
            "|arrow(r)_4 - arrow(r)_1| = sqrt(3^2 + 3^2) = sqrt(18) = 3 sqrt(2) space (m)",
            font_size=28,
        )
        paso2.next_to(paso1, DOWN, buff=0.4)
        self.play(FadeIn(paso2, shift=UP * 0.2))
        self.next_slide()

        paso3 = MathTypst(
            "hat(r)_(41) = (3 hat(i) + 3 hat(j)) / (3 sqrt(2)) = 1/sqrt(2) hat(i) + 1/sqrt(2) hat(j)",
            font_size=26,
            color=YELLOW,
        )
        paso3.next_to(paso2, DOWN, buff=0.4)
        self.play(FadeIn(paso3, shift=UP * 0.2))
        self.next_slide()


# ==============================================================================
# SLIDE 6: F41 - RESULTADO
# ==============================================================================
class Slide06_F41_Resultado(BasePhysicsSlide):
    def construct(self):
        titulo = title(Typst("*Resultado:* $arrow(F)_(41)$", font_size=38))
        self.play(Write(titulo))
        self.next_slide()

        calc = MathTypst(
            "arrow(F)_(41) = 9 times 10^9 dot (2 times 10^(-6))(8 times 10^(-6)) / 18 dot (1/sqrt(2) hat(i) + 1/sqrt(2) hat(j))",
            font_size=22,
        )
        self.play(FadeIn(calc, shift=UP * 0.2))
        self.next_slide()

        resultado = MathTypst(
            "arrow(F)_(41) = 5.6568 times 10^(-3) hat(i) + 5.6568 times 10^(-3) hat(j) space (N)",
            font_size=32,
            color=PINK,
        )
        resultado.next_to(calc, DOWN, buff=0.5)
        self.play(FadeIn(resultado, shift=UP * 0.3))
        self.next_slide()


# ==============================================================================
# SLIDE 7: F42 - PLANTEAMIENTO
# ==============================================================================
class Slide07_F42_Plant(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Fuerza sobre q₄ debido a q₂", font_size=34, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # Panel cartesiano: posiciones, vectores POSICIÓN y FUERZA (atracción hacia -î)
        panel = panel_vectores(
            self,
            posiciones={"q2": (0, 3), "q4": (3, 3)},
            vectores_posicion={"q2": (0, 3), "q4": (3, 3)},
            vectores_fuerza={"q4": (-3, 0)},
            titulo_panel="Plano XY: $arrow(F)_(42)$",
            factor=0.55,
        )
        self.play(Create(panel[0]), FadeIn(panel[1:]))
        self.next_slide()

        eq = MathTypst(
            "arrow(F)_(42) = K_e (q_4 q_2) / r_(42)^2 dot hat(r)_(42)",
            font_size=36,
        )
        eq.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        self.play(FadeIn(eq, shift=UP * 0.3))
        self.next_slide()

        datos = VGroup(
            MathTypst("arrow(r)_2 = 0 hat(i) + 3 hat(j) space (m)", font_size=22),
            MathTypst("arrow(r)_4 - arrow(r)_2 = 3 hat(i) space (m)", font_size=22),
            MathTypst("|arrow(r)_4 - arrow(r)_2| = 3 space (m)", font_size=22),
            MathTypst("hat(r)_(42) = hat(i)", font_size=22),
            Typst(
                "$q_2 = -2 times 10^(-6) space C$ → *atracción* → dir. $-hat(i)$",
                font_size=20,
                color=RED,
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.5).align_to(eq, LEFT)
        for d in datos:
            self.play(FadeIn(d, shift=UP * 0.15))
            self.wait(0.2)
        self.next_slide()


# ==============================================================================
# SLIDE 8: F42 - RESULTADO
# ==============================================================================
class Slide08_F42_Resultado(BasePhysicsSlide):
    def construct(self):
        titulo = title(Typst("*Resultado:* $arrow(F)_(42)$", font_size=38))
        self.play(Write(titulo))
        self.next_slide()

        calc = MathTypst(
            "arrow(F)_(42) = 9 times 10^9 dot (2 times 10^(-6))(-2 times 10^(-6)) / 9 dot hat(i)",
            font_size=26,
        )
        self.play(FadeIn(calc, shift=UP * 0.2))
        self.next_slide()

        resultado = MathTypst(
            "arrow(F)_(42) = -4 times 10^(-3) hat(i) space (N)",
            font_size=36,
            color=PINK,
        )
        resultado.next_to(calc, DOWN, buff=0.5)
        self.play(FadeIn(resultado, shift=UP * 0.3))
        self.next_slide()


# ==============================================================================
# SLIDE 9: F43 - PLANTEAMIENTO
# ==============================================================================
class Slide09_F43_Plant(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Fuerza sobre q₄ debido a q₃", font_size=34, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # Panel cartesiano: posiciones, vectores POSICIÓN y FUERZA (repulsión hacia +ĵ)
        panel = panel_vectores(
            self,
            posiciones={"q3": (3, 0), "q4": (3, 3)},
            vectores_posicion={"q3": (3, 0), "q4": (3, 3)},
            vectores_fuerza={"q4": (0, 3)},
            titulo_panel="Plano XY: $arrow(F)_(43)$",
            factor=0.55,
        )
        self.play(Create(panel[0]), FadeIn(panel[1:]))
        self.next_slide()

        eq = MathTypst(
            "arrow(F)_(43) = K_e (q_4 q_3) / r_(43)^2 dot hat(r)_(43)",
            font_size=36,
        )
        eq.to_edge(LEFT, buff=0.5).shift(UP * 1.5)
        self.play(FadeIn(eq, shift=UP * 0.3))
        self.next_slide()

        datos = VGroup(
            MathTypst("arrow(r)_3 = 3 hat(i) + 0 hat(j) space (m)", font_size=22),
            MathTypst("arrow(r)_4 - arrow(r)_3 = 3 hat(j) space (m)", font_size=22),
            MathTypst("|arrow(r)_4 - arrow(r)_3| = 3 space (m)", font_size=22),
            MathTypst("hat(r)_(43) = hat(j)", font_size=22),
            Typst(
                "$q_3 = 4 times 10^(-6) space C$ → *repulsión* → dir. $+hat(j)$",
                font_size=20,
                color=GREEN,
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT).next_to(eq, DOWN, buff=0.5).align_to(eq, LEFT)
        for d in datos:
            self.play(FadeIn(d, shift=UP * 0.15))
            self.wait(0.2)
        self.next_slide()


# ==============================================================================
# SLIDE 10: F43 - RESULTADO
# ==============================================================================
class Slide10_F43_Resultado(BasePhysicsSlide):
    def construct(self):
        titulo = title(Typst("*Resultado:* $arrow(F)_(43)$", font_size=38))
        self.play(Write(titulo))
        self.next_slide()

        calc = MathTypst(
            "arrow(F)_(43) = 9 times 10^9 dot (2 times 10^(-6))(4 times 10^(-6)) / 9 dot hat(j)",
            font_size=26,
        )
        self.play(FadeIn(calc, shift=UP * 0.2))
        self.next_slide()

        resultado = MathTypst(
            "arrow(F)_(43) = 8 times 10^(-3) hat(j) space (N)",
            font_size=36,
            color=PINK,
        )
        resultado.next_to(calc, DOWN, buff=0.5)
        self.play(FadeIn(resultado, shift=UP * 0.3))
        self.next_slide()


# ==============================================================================
# SLIDE 11: SUPERPOSICION
# ==============================================================================
class Slide11_Superposicion(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Principio de Superposición", font_size=36, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # Ecuación a la IZQUIERDA, panel cartesiano a la DERECHA
        eq = MathTypst(
            "arrow(F)_4 = arrow(F)_(41) + arrow(F)_(42) + arrow(F)_(43)",
            font_size=34,
        )
        eq.to_edge(LEFT, buff=0.5).shift(UP * 1.3)
        self.play(FadeIn(eq, shift=UP * 0.3))
        self.next_slide()

        # Panel cartesiano con los 3 vectores sumándose desde q4=(3,3)
        # Magnitudes reales (×10^-3 N): F41=(5.657, 5.657), F42=(-4, 0), F43=(0, 8)
        # F4_total = (1.6568, 13.6568). Rango en y llega hasta 3 + 13.66 = 16.66;
        # en x llega hasta 3 + 5.66 = 8.66 y baja hasta 3 - 4 = -1. Todo escalado por ESCALA.
        ESCALA = 0.2  # unidades de gráfico por (10^-3 N) — chico para que todo quepa
        f41 = (5.6568, 5.6568)
        f42 = (-4.0, 0.0)
        f43 = (0.0, 8.0)
        f4_total = (f41[0] + f42[0] + f43[0], f41[1] + f42[1] + f43[1])  # (1.6568, 13.6568)

        # Bounds generosos para que todos los vectores quepan
        # F4_total en y = 13.66*ESCALA = 2.73 unidades arriba de q4 (3,3) → y=5.73
        # F4_total en x = 1.66*ESCALA = 0.33 → x=3.33
        # F42 en x = -4*ESCALA = -0.8 → x=2.2
        ejes = Axes(
            x_range=[-1, 6, 1],
            y_range=[-2, 7, 1],
            x_length=3.6,
            y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 12},
        )
        ejes.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        # Marcar q4 en (3,3) como punto de aplicación de las fuerzas
        q4_pos = ejes.c2p(3, 3)
        q4_dot = Dot(q4_pos, color=YELLOW, radius=0.09)
        q4_label = Typst("q4", font_size=14, color=YELLOW).next_to(q4_dot, UR, buff=0.05)

        titulo_panel = Typst(
            "*Vectores sobre* $q_4$ *(×10⁻³ N)*",
            font_size=14, color=YELLOW
        ).next_to(ejes, UP, buff=0.2)

        self.play(Create(ejes), FadeIn(titulo_panel), FadeIn(q4_dot), Write(q4_label))
        self.next_slide()

        # Vector F41 (verde-azulado): desde q4 hacia (3+5.657·E, 3+5.657·E)
        def flecha(origen_graf, dx_N, dy_N, color, etiqueta, factor=ESCALA):
            destino_graf = origen_graf + RIGHT * dx_N * factor + UP * dy_N * factor
            arr = Arrow(
                origen_graf, destino_graf,
                color=color, buff=0, stroke_width=4,
                max_tip_length_to_length_ratio=0.25,
            )
            lab = Typst(etiqueta, font_size=12, color=color).move_to(destino_graf).shift(UR * 0.15)
            return arr, lab

        v41, l41 = flecha(q4_pos, *f41, TEAL, "F41")
        self.play(GrowArrow(v41), FadeIn(l41))
        self.wait(0.4)
        self.next_slide()

        v42, l42 = flecha(q4_pos, *f42, BLUE, "F42")
        self.play(GrowArrow(v42), FadeIn(l42))
        self.wait(0.4)
        self.next_slide()

        v43, l43 = flecha(q4_pos, *f43, GREEN, "F43")
        self.play(GrowArrow(v43), FadeIn(l43))
        self.wait(0.5)
        self.next_slide()

        # Vector suma F4 (rojo) — desde q4 al final de la suma
        v4, l4 = flecha(q4_pos, *f4_total, RED, "F4")
        self.play(GrowArrow(v4), FadeIn(l4))
        self.wait(0.6)
        self.next_slide()

        # Componentes a la izquierda
        comp = MathTypst(
            "arrow(F)_4 = (5.6568 - 4) times 10^(-3) hat(i) + (5.6568 + 8) times 10^(-3) hat(j)",
            font_size=20,
        )
        comp.next_to(eq, DOWN, buff=0.35).align_to(eq, LEFT)
        self.play(FadeIn(comp, shift=UP * 0.2))
        self.next_slide()

        resultado = MathTypst(
            "arrow(F)_4 = 1.6568 times 10^(-3) hat(i) + 13.6568 times 10^(-3) hat(j) space (N)",
            font_size=24,
            color=YELLOW,
        )
        resultado.next_to(comp, DOWN, buff=0.35).align_to(eq, LEFT)
        self.play(FadeIn(resultado, shift=UP * 0.3))
        self.next_slide()


# ==============================================================================
# SLIDE 12: MAGNITUD Y DIRECCION
# ==============================================================================
class Slide12_MagnitudDireccion(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Magnitud y Dirección", font_size=36, weight=BOLD))
        self.play(Write(titulo))
        self.next_slide()

        # --- LADO IZQUIERDO: cálculos de magnitud y ángulo ---
        mag = MathTypst(
            "|arrow(F)_4| = sqrt((1.6568)^2 + (13.6568)^2) times 10^(-3)",
            font_size=22,
        )
        mag.to_edge(LEFT, buff=0.45).shift(UP * 1.3)
        self.play(FadeIn(mag, shift=UP * 0.2))
        self.next_slide()

        mag_res = MathTypst(
            "|arrow(F)_4| = 13.76 times 10^(-3) space (N)",
            font_size=28,
            color=PINK,
        )
        mag_res.next_to(mag, DOWN, buff=0.3).align_to(mag, LEFT)
        self.play(FadeIn(mag_res, shift=UP * 0.2))
        self.next_slide()

        theta = MathTypst(
            "theta = arctan((13.6568) / (1.6568))",
            font_size=22,
        )
        theta.next_to(mag_res, DOWN, buff=0.45).align_to(mag, LEFT)
        self.play(FadeIn(theta, shift=UP * 0.2))
        self.next_slide()

        theta_res = MathTypst(
            "theta approx 83.08°",
            font_size=28,
            color=YELLOW,
        )
        theta_res.next_to(theta, DOWN, buff=0.3).align_to(mag, LEFT)
        self.play(FadeIn(theta_res, shift=UP * 0.2))
        self.next_slide()

        # --- LADO DERECHO: plano cartesiano con q4 y F4 escalada, más el ángulo ---
        # F4_total = (1.6568, 13.6568) × 10⁻³ N, va casi vertical (83°)
        ESCALA = 0.22  # unidades de gráfico por (10⁻³ N)
        ESCALA_GRAF_X = 0.04  # conversión a unidades del gráfico (eje_x_length / x_range)

        ejes = Axes(
            x_range=[-1, 5, 1],
            y_range=[-1, 7, 1],
            x_length=3.8,
            y_length=4.2,
            axis_config={"include_numbers": True, "font_size": 12},
        )
        ejes.to_edge(RIGHT, buff=0.4).shift(DOWN * 0.3)
        # Marcar q4 en (3,3)
        q4_pos = ejes.c2p(3, 3)
        q4_dot = Dot(q4_pos, color=YELLOW, radius=0.09)
        q4_label = Typst("q4", font_size=14, color=YELLOW).next_to(q4_dot, UR, buff=0.05)

        titulo_panel = Typst(
            "*Vector* $arrow(F)_4$ *sobre* $q_4$",
            font_size=14, color=YELLOW,
        ).next_to(ejes, UP, buff=0.2)

        # Vector F4 escalada — desde q4 hacia (1.6568, 13.6568) × 10⁻³ N
        fx_N, fy_N = 1.6568, 13.6568
        # En unidades del gráfico: dx_graf = fx_N * ESCALA, dy_graf = fy_N * ESCALA
        destino = q4_pos + RIGHT * fx_N * ESCALA + UP * fy_N * ESCALA
        f4_arrow = Arrow(
            q4_pos, destino,
            color=RED, buff=0, stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
        )
        f4_label = Typst("F4", font_size=14, color=RED).move_to(destino).shift(UR * 0.18)

        # Arco del ángulo (entre +X y el vector F4) usando Angle
        eje_x_pos = q4_pos + RIGHT * 1.0  # Un punto a la derecha de q4 a lo largo del eje +X
        angle_arc = Angle(
            Line(q4_pos, eje_x_pos),
            Line(q4_pos, destino),
            radius=0.6,
            color=YELLOW,
            stroke_width=2.5,
        )
        angle_label = MathTypst(
            "theta = 83.08°", font_size=14, color=YELLOW,
        ).move_to(Angle(Line(q4_pos, eje_x_pos), Line(q4_pos, destino), radius=0.6).point_from_proportion(0.6))

        self.play(Create(ejes), FadeIn(titulo_panel), FadeIn(q4_dot), Write(q4_label))
        self.next_slide()

        self.play(GrowArrow(f4_arrow), FadeIn(f4_label))
        self.wait(0.4)
        self.next_slide()

        self.play(Create(angle_arc), FadeIn(angle_label))
        self.wait(0.5)
        self.next_slide()


# ==============================================================================
# SLIDE 13: RESULTADO FINAL
# ==============================================================================
class Slide13_ResultadoFinal(BasePhysicsSlide):
    def construct(self):
        titulo = title(Text("Resultado Final", font_size=46, weight=BOLD, color=YELLOW))
        self.play(Write(titulo))
        self.next_slide()

        eq1 = MathTypst(
            "arrow(F)_4 = (1.6568 hat(i) + 13.6568 hat(j)) times 10^(-3) space (N)",
            font_size=32,
            color=YELLOW,
        )
        self.play(FadeIn(eq1, shift=UP * 0.2))
        self.next_slide()

        eq2 = MathTypst("|arrow(F)_4| = 13.76 times 10^(-3) space (N)", font_size=32)
        eq2.next_to(eq1, DOWN, buff=0.4)
        self.play(FadeIn(eq2, shift=UP * 0.2))
        self.next_slide()

        eq3 = Typst(
            "$theta approx 83.08°$ *respecto al eje* $+hat(i)$",
            font_size=28,
        )
        eq3.next_to(eq2, DOWN, buff=0.4)
        self.play(FadeIn(eq3, shift=UP * 0.2))
        self.next_slide()
