from manim import *
import numpy as np
import random

col1 = '#B1CE96'
col2 = '#EA8E8B'


config.background_color = WHITE


class MatrixSquare(MovingCameraScene):
    def construct(self):
        squares = VGroup()
        for i in range(10):
            for j in range(8):
                square = Square(0.7)
                square.shift(i * RIGHT*0.8, j * UP*0.8)
                square.set_stroke(BLACK)
                squares.add(square)
        squares.move_to(ORIGIN)

        nums = VGroup()
        for square in squares:
            num = round(np.random.randint(0, 5)*np.random.random(), 1)
            if num:
                num = MathTex(f'{num}', color=BLACK, font_size=33)
                square.set_fill(col1, 1)
            else:
                num = MathTex(r'\times', color=BLACK, font_size=50)
                square.set_fill(col2, 1)
            num.move_to(square)
            nums.add(num)

        self.add(squares, nums)
        self.wait()

        for k in range(10):
            nums_to_rewrite = []
            for _ in range(20):
                index = np.random.randint(0, len(squares) - 1)
                num = round(np.random.randint(0, 5) * np.random.random(), 1)
                if num:
                    num = MathTex(f'{num}', color=BLACK, font_size=33)
                    squares[index].set_fill(col1, 1)
                else:
                    num = MathTex(r'\times', color=BLACK, font_size=50)
                    squares[index].set_fill(col2, 1)
                num.move_to(squares[index])
                nums[index].replace(num)
                nums_to_rewrite.append(FadeIn(nums[index]))
            self.play(*nums_to_rewrite, run_time=1)

        # counter = 0
        # while counter <= 10:
        #     index1 = np.random.randint(0, len(squares) - 1)
        #     index2 = np.random.randint(0, len(squares) - 1)
        #
        #     if index1 != index2:
        #         sq1 = squares[index1]
        #         sq2 = squares[index2]
        #
        #         num1 = nums[index1]
        #         num2 = nums[index2]
        #         self.play(
        #             sq1.animate.move_to(sq2),
        #             num1.animate.move_to(sq2),
        #             sq2.animate.move_to(sq1),
        #             num2.animate.move_to(sq1),
        #             run_time=0.8)
        #
        #         counter += 1


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
        self.camera.frame_width = 15
        self.camera.frame_height = 9

        grid = NumberPlane(x_range=(-3, 3), y_range=(-3, 3), axis_config={"color": BLACK})

        p_num = ValueTracker(0.3)

        func = ImplicitFunction(lambda x, y: abs(x)**p_num.get_value() + abs(y)**p_num.get_value() - 1, color=BLACK)
        func.add_updater(
            lambda m: m.become(
                ImplicitFunction(lambda x, y: abs(x)**p_num.get_value() + abs(y)**p_num.get_value() - 1, color=BLACK)
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
            return mobject.become(MathTex(sqrt + "{" + brc1 + " + " + brc2 + "} = 1", color=BLACK).shift(DOWN*3.5))

        text_down.add_updater(updater_tex_formula)

        self.add(grid, text_down, func)
        # self.play(p_num.animate.set_value(1), run_time=2)
        # self.wait(0.1)
        # self.play(p_num.animate.set_value(2), run_time=2)
        # self.wait(0.1)
        # self.play(p_num.animate.set_value(5), run_time=3)
        # self.play(p_num.animate.set_value(0.3), run_time=3)
