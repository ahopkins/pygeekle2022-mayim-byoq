from pathlib import Path
from sanic import Sanic, html

NAME = "Presentation"
PRESENTATION = Path(__file__).parent / "presentation"


main = Sanic(NAME)
main.static("/assets", PRESENTATION / "assets")


@main.get("/")
def index(_):
    with open(PRESENTATION / "index.html", "r") as f:
        doc = f.read()

    with open(PRESENTATION / "slides.md", "r") as f:
        slides = f.read()

    return html(doc.replace("__SLIDES__", slides))


if __name__ == "__main__":
    main.prepare()
    Sanic.serve()
