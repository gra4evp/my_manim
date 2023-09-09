from manim import *
import numpy as np
import random


# manim -pql -i -r 2000,2000 matrix_scene.py MinkowskiNorm


config.background_color = WHITE

config.frame_width = 6
config.frame_height = 6

# config.pixel_width = 1080
# config.frame_height = 1080


def generate_matrix(rows, cols):
    matrix = MathTable(
        [[random.randint(1, 5) for _ in range(cols)] for _ in range(rows)],
        h_buff=0.4,
        v_buff=0.4,
        include_outer_lines=True
    )
    matrix.get_horizontal_lines().set_color(BLACK)
    matrix.get_vertical_lines().set_color(BLACK)
    matrix.set_fill(BLACK)
    return matrix


class MatrixNumbers(Scene):
    def construct(self):
        matrixs = [generate_matrix(10, 20) for _ in range(10)]
        self.add(matrixs[0])
        for i in range(len(matrixs) - 1):
            self.play(ReplacementTransform(matrixs[i], matrixs[i+1]))


class MinkowskiNorm(Scene):
    def construct(self):

        grid = NumberPlane(x_range=(-2, 2), y_range=(-2, 2), axis_config={"color": BLACK})

        p_num = ValueTracker(0.3)

        func = ImplicitFunction(lambda x, y: abs(x)**p_num.get_value() + abs(y)**p_num.get_value() - 1, color=RED)
        func.add_updater(
            lambda m: m.become(
                ImplicitFunction(lambda x, y: abs(x)**p_num.get_value() + abs(y)**p_num.get_value() - 1, color=RED)
            )
        )

        # text_up = MathTex(r"\rho (x,\hat{x})=\sqrt[p]{|x_{1}-\hat{x}_{1}|^{p} + |x_{2}-\hat{x}_{2}|^{p}}", color=BLACK)
        # text_up.shift(DOWN*2)

        text_down = MathTex('1')

        def updater_tex_formula(mobject: Mobject):
            p = round(p_num.get_value(), 1)
            if p == 1.0:
                p = 1
            if p == 2.0:
                p = 2
            if p == 5.0:
                p = 5
            sqrt = r"\sqrt[" + f"{p}" + "]"
            brc1 = r"|x_{1}|^{"+f"{p}"+"}"
            brc2 = r"|x_{2}|^{"+f"{p}"+"}"
            return mobject.become(MathTex(sqrt + "{" + brc1 + " + " + brc2 + "} = 1", color=RED).shift(DOWN*2.5))

        text_down.add_updater(updater_tex_formula)

        self.add(grid, text_down, func)
        self.play(p_num.animate.set_value(1), run_time=2)
        self.wait(0.1)
        self.play(p_num.animate.set_value(2), run_time=2)
        self.wait(0.1)
        self.play(p_num.animate.set_value(5), run_time=3)
        self.play(p_num.animate.set_value(0.3), run_time=3)
