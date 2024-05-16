import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tqdm import tqdm
import sys

sys.path.append("discrete-radon-transform/discrete_radon_transform")
from . import __version__
import click


class Discrete_Radon_Transform:
    def __init__(self, path_to_picture: str, angle_acc=500, shift_acc=500) -> None:
        """main calculations"""
        # open picture with PILL
        input_img = Image.open(path_to_picture)
        # transform picture to grayscale: (black: 0, white: 255)
        input_img = input_img.convert("L")
        # picture to matrix with negative values (black: 255, white: 0)
        input_img = self.negative(np.matrix(input_img))

        # (x,y) rectangle size
        (N, M) = input_img.shape
        # the sampling rate of the slope angle tangent and linear shift
        H = shift_acc
        K = angle_acc
        self.H = H
        self.K = K
        # x: linspace(-1, 1, M)
        dx = 2 / (M - 1)
        xmin = -1
        # y: linspace(-1, 1, N)
        dy = 2 / (N - 1)
        ymin = -1

        # f'(p(k), t(h)) = dx * Σf(x(m), p(k)*x(m)+t(h))
        self.tg = np.tan(np.pi * 89 / 180)
        p = np.linspace(-self.tg, self.tg, K)
        t = np.linspace(-5, 5, H)
        self.Transformed = np.zeros((H, K))

        # nearest neighbour approximation
        for k in tqdm(range(K)):
            for h in range(H):
                sum = 0
                alpha = p[k] * dx / dy
                beta = (p[k] * xmin + t[h] - ymin) / dy
                for m in range(M):
                    n = int(np.round(alpha * m + beta))
                    if (n > 0) and (n < N):
                        sum = sum + input_img[n, m]
                self.Transformed[h, k] = dx * sum

    def negative(self, M: np.matrix) -> np.matrix:
        """Reverses matrixs' values |value - 255|"""
        # m_ij = |m_ij - 255|
        return np.ones(M.shape) * 255 - M

    def get_transform(self) -> np.matrix:
        """returnes result of transformation"""
        return self.Transformed

    def get_params(self):
        raise NotImplementedError

    def display_result(self, name="radon_result", dir="./") -> plt.figure:
        """returns heatmap of the result"""
        fig = plt.figure()
        plt.title(
            "$\\tilde F (p(k), t(h)) = \Delta x * \sum_{m=0}^{M-1}F(x(m), p(k)*x(m)+t(h))$"
        )
        plt.imshow(self.Transformed)
        plt.xticks([1, self.K // 2, self.K - 1], ["-tg($89^o$)", "0", "tg($89^o$)"])
        plt.xlabel("p(k) slope")
        plt.yticks([1, self.H // 2, self.H - 1], [-self.H * 5 // 2, 0, self.H * 5 // 2])
        plt.ylabel("t(h) offset")
        plt.savefig(dir + name + ".png")
        return fig


if __name__ == "__main__":
    drdt = Discrete_Radon_Transform("straight_lines_samples.JPG")
    drdt.display_result()


@click.command()
@click.option(
    "--path_to_picture",
    "-p",
    default="./discrete_radon_transform/straight_lines_samples.JPG",
    help="path to picture",
    show_default=True,
)
@click.option(
    "--angle_accuracy",
    "-a",
    default=500,
    help="angle_accuracy",
    show_default=True,
)
@click.option(
    "--shift_accuracy",
    "-s",
    default=500,
    help="shift accuracy",
    show_default=True,
)
@click.option(
    "--save_to_dir",
    "-d",
    default="./discrete_radon_transform",
    help="saves result heatmap to the directory",
    show_default=True,
)
@click.version_option(version=__version__)
def main(
    path_to_picture: str, angle_accuracy: int, shift_accuracy: int, save_to_dir: str
) -> None:
    """The Discrete Radon Transform project."""
    drdt = Discrete_Radon_Transform(
        path_to_picture=path_to_picture,
        angle_acc=angle_accuracy,
        shift_acc=shift_accuracy,
    )
    drdt.display_result(dir=save_to_dir)
