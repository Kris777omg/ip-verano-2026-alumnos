# capa de servicio/lógica de negocio

import random
from ..transport import transport
from ..persistence import repositories
from ..utilities import translator
from django.contrib.auth import get_user

def getAllImages():
    """
    Obtiene todas las imágenes de personajes desde la API y las convierte en objetos Card.  
    Esta función debe obtener los datos desde transport, transformarlos en Cards usando 
    translator y retornar una lista de objetos Card.
    """
    json_collection = transport.getAllImages() 
    images = []
    for object_api in json_collection:
        card = translator.fromRequestIntoCard(object_api)
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
    fav_card = translator.requesttoCard(request)
    fav_card.user = get_user(request)
    repositories.saveFavourite(fav_card)

def getAllFavourites(request):
    """
    Obtiene todos los favoritos del usuario autenticado.
    
    Si el usuario está autenticado, se deben obtener sus favoritos desde el repositorio,
    transformarlos en Cards usando translator y retornar la lista. Si no está autenticado, se retorna una lista vacía.
    """
    if not request.user .is_authenticated:
        return []
    user = get_user(request)
    favourites_data = repositories.getAllFavouritesByUser(user)
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
    fav_id = request.POST.get(id)
    repositories.deleteFavourite(fav_id)
## El request.POST.get(id) obtiene el id del favorito que se quiere eliminar, y luego se llama a la función deleteFavourite del repositorio para eliminarlo de la base de datos.

    
    