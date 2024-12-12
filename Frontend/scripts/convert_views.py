from click import command, option
from pathlib import Path
from services.logging import Logger, LoggingService
from subprocess import CalledProcessError, run


@command()
@option("--path", default="./ui/views/generated")
def convert(path: str, logger: Logger = LoggingService.get_logger(__name__)):
    for ui_file in Path(path).glob("*.ui"):
        py_file = ui_file.parent / f"{ui_file.stem}.py"
        logger.info("Converting UI file", ui_file=ui_file, py_file=py_file)

        try:
            run(
                ["poetry", "run", "pyside6-uic", "-o", str(py_file), str(ui_file)],
                check=True,
            )
        except CalledProcessError as ex:
            logger.error(
                "Failed to convert UI file", ui_file=ui_file, py_file=py_file, error=ex
            )


if __name__ == "__main__":
    convert()
