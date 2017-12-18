import logging

logging.basicConfig(
    filename='blockchain.log', level=logging.DEBUG, filemode='w',
    format='%(levelno)d [%(asctime)s.%(msecs)03d] %(message)s',
    datefmt='%H:%M:%S'
)
