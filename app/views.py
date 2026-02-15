# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

##Se deja de utilizar el pass ya que esta funcion servia para mostrar la estructura y que no tire error el codigo al

def index_page(request):
    return render(request, 'index.html')

def home(request):
    """
    Vista principal que muestra la galería de personajes de Los Simpsons.
    
    Esta función debe obtener el listado de imágenes desde la capa de servicios
    y también el listado de favoritos del usuario, para luego enviarlo al template 'home.html'.
    Recordar que los listados deben pasarse en el contexto con las claves 'images' y 'favourite_list'.
    """
    images = services.getAllImages()
    favourite_list = []

    return render(request, 'home.html', { 'images': images,'layout': 'horizontal', 'favourite_list': favourite_list })

def search(request):
    """
    Busca personajes por nombre.
    
    Se debe implementar la búsqueda de personajes según el nombre ingresado.
    Se debe obtener el parámetro 'query' desde el POST, filtrar las imágenes según el nombre
    y renderizar 'home.html' con los resultados. Si no se ingresa nada, redirigir a 'home'.
    """
    search_msg = request.POST.get('query', '')
    
    if not search_msg:
        return redirect('home')
    
    images = services.filterByCharacter(search_msg)
    favourite_list = services.getAllFavourites(request)
    
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })
        

def filter_by_status(request):
    """
    Filtra personajes por su estado (Alive/Deceased).
    
    Se debe implementar el filtrado de personajes según su estado.
    Se debe obtener el parámetro 'status' desde el POST, filtrar las imágenes según ese estado
    y renderizar 'home.html' con los resultados. Si no hay estado, redirigir a 'home'.
    """
    status = request.POST.get('status', '')
    if not status:
        return redirect('home')
    
    images = services.filterByStatus(status) 
    favourite_list = services.getAllFavourites(request)
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    """
    favourite_list = services.getAllFavourites(request)
    return render(request, 'home.html', { 'images': services.getAllImages(), 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    """
    Guarda un personaje como favorito.
    """
    services.saveFavourite(request)
    return redirect('home')
## se usa el redirect para no tener que recargar la pagina y asi poder ver el personaje agregado


@login_required
def deleteFavourite(request):
    """
    Elimina un favorito del usuario.
    """
    services.deleteFavourite(request)
    return redirect('home')


@login_required
def exit(request):
    logout(request)
    return redirect('home')