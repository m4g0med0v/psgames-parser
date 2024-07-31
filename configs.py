import logging


# Кофигкратор логов
def configure_logging(level=logging.INFO) -> None:
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)20s:%(lineno)-3d %(levelname)8s - %(message)s",
    )
