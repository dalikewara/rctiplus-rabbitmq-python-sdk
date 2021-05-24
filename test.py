import sys

if __name__ == '__main__':
    try:
        test_name = sys.argv[1]
    except:
        test_name = None
    if test_name == 'send':
        import tests.send
    if test_name == 'receive':
        import tests.receive
    if test_name == 'aio_send':
        import tests.aio_send
    if test_name == 'aio_receive':
        import tests.aio_receive
