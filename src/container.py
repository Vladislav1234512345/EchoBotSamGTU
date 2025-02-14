from pathlib import Path
import logging

BASE_DIR = Path(__file__).parent.parent


def configure_logging(level: int = logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)s:%(lineno)d %(levelname)s - %(message)s",
    )


with open(BASE_DIR / "memes.txt", "r", encoding="utf-8") as file:
    memes = file.read().splitlines()


with open(BASE_DIR / "jokes.txt", "r", encoding="utf-8") as file:
    jokes = file.read().splitlines()
