# capa de servicio/lógica de negocio

import random

from app.layers.utilities.card import Card
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages(input=None, status=None):
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.  
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """
    json_collection = transport.getAllImages()
    images = []
    
    for object_api in json_collection:
        card = translator.fromRequestIntoCard(object_api)
        
        # FILTRO RÁPIDO: Si mandaste un status, solo guardamos los que coinciden
        if status:
            if card.status.lower() == status.lower():
                images.append(card)
        else:
            images.append(card)

    return images

def filterByCharacter(name):
    """
    Filtra las cards de personajes según el nombre proporcionado.
    
    Se debe filtrar los personajes cuyo nombre contenga el parámetro recibido. Retorna una lista de Cards filtradas.
    """
    cards = getAllImages()
    filtered_card = []
    
    for card in cards:
        if name.lower() in card.name.lower():
            filtered_card.append(card)
                
    return filtered_card

def filterByStatus(status_name):
    """
    Filtra las cards de personajes según su estado (Alive/Deceased).
    
    Se deben filtrar los personajes que tengan el estado igual al parámetro 'status_name'. Retorna una lista de Cards filtradas.
    """
    cards = getAllImages()
    filtered_card = []
    
    for card in cards:
        if card.status == status_name:
            filtered_card.append(card)
            
    return filtered_card



# añadir favoritos (usado desde el template 'home.html')
def saveFavourite(request):
    """
    Guarda un favorito en la base de datos.
    
    Se deben convertir los datos del request en una Card usando el translator,
    asignarle el usuario actual, y guardarla en el repositorio.
    """
    name = request.POST.get('name')
    image = request.POST.get('image')
    status = request.POST.get('status')
    gender = request.POST.get('gender')      
    phrases = request.POST.get('phrases')      
    occupation = request.POST.get('occupation')
    age = request.POST.get('age')
    
    already_exists = repositories.getFavouriteByUserAndName(request.user, name)
    if already_exists:
        return None  # Si ya existe, no lo guardamos de nuevo

    fav = Card(
        name=name,
        image=image,
        status=status,
        gender=gender,
        phrases=phrases,
        occupation=occupation,
        age=age,    
        user=request.user
    )
    return repositories.saveFavourite(fav)

def getAllFavourites(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    user = request.user
    favourites_data = repositories.getAllFavourites(user)
    if favourites_data is None:
        favourites_data = []
    cards = []
    for data in favourites_data:
        card = translator.fromRepositoryIntoCard(data)
        cards.append(card)
    return cards

def deleteFavourite(request):
    """
    Elimina un favorito de la base de datos.
    
    Se debe obtener el ID del favorito desde el POST y eliminarlo desde el repositorio.
    """
    fav_id = request.POST.get('id')
    repositories.deleteFavourite(fav_id)
## El request.POST.get(id) obtiene el id del favorito que se quiere eliminar, y luego se llama a la función deleteFavourite del repositorio para eliminarlo de la base de datos.

    
    