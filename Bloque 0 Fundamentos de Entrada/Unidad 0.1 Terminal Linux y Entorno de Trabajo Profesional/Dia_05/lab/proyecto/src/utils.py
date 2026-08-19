def vista_persona(request):
    return render(request, 'persona.html')

def vista_producto(request):
    return render(request, 'producto.html')

def vista_pedido(request):
    return render(request, 'pedido.html')

def vista_factura(request):
    return render(request, 'factura.html')

def vista_proveedor(request):
    return render(request, 'proveedor.html')

def vista_categoria(request):
    return render(request, 'categoria.html')

def vista_subcategoria(request):
    return render(request, 'subcategoria.html')

def vista_marca(request):
    return render(request, 'marca.html')

def vista_modelo(request):
    return render(request, 'modelo.html')





























def vista_detalle_pedido(request):
    return render(request, 'detalle_pedido.html')

def vista_detalle_factura(request):
    return render(request, 'detalle_factura.html')

def vista_detalle_proveedor(request):
    return render(request, 'detalle_proveedor.html')

def vista_detalle_categoria(request):
    return render(request, 'detalle_categoria.html')
