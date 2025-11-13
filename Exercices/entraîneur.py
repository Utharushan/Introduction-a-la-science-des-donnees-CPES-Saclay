import glob
from ipywidgets import interactive         # type: ignore
from jupylates.jupylates import Exerciser  # type: ignore
from IPython.display import display        # type: ignore

thèmes = {
    'Tableaux Numpy': 'numpyarray/*.md',
}


def entraîneur(Thème=[(a, b) for a, b in thèmes.items()]) -> None:
    exercises = glob.glob(Thème)
    display(Exerciser(exercises, lrs_url=".lrs.json", mode="train"))


entraîneur = interactive(entraîneur)
