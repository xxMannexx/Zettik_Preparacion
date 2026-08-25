## raise ... from ... transforma un error conservando el original

def parsear(t):
    try:
        return int(t)
    except ValueError as e:
        raise RuntimeError(f"no se pudo parsear {t!r}") from e

try:
    parsear("xyz")
except RuntimeError as e:
    print(f"{e} (causa: {type(e.__cause__).__name__})")  ## Cause da de donde viene el error este runtimeerror provino o lo mandamos de un valueError