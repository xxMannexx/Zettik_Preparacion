it = iter("abc") ## Un for no conoce de listas ni nada genera iteradores con los datos que le damos un solo uso

while True:
    try:
        print(next(it))  ## Next es como avanza sobre el iterador hasta que llegeu a una except StopIteration ahi para
    except StopIteration:
        break
