import logging
import vars

logging.basicConfig(filename=(vars.PATH_TO_PARENT_DIRECTORY + 'led.log'),
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)
def my_print(*args, **kwargs):
    print(*args, *kwargs)
    logging.info(str(args))