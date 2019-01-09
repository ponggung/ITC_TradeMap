import logging


def setlog():
    logging.basicConfig(
        # level=logging.DEBUG,
        level=logging.INFO,
        # level=logging.WARNING,
        # level=logging.ERROR,
        format='%(asctime)s %(name)-4s %(levelname)-8s %(message)s',
        datefmt='%m-%d %H:%M:%S',
        # handlers=[
        #     logging.FileHandler('event.log', 'a', 'utf-8'),
        # ],
    )
    return logging


if __name__=="__main__":
    logging = setlog()
    for i in range(10):
        logging.info(i)
