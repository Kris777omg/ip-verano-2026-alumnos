# capa DAO de acceso/persistencia de datos.
from app.models import Favourite

def getFavouriteByUserAndName(user, name):
    """
    Verifica si un favorito con el mismo nombre ya existe para el usuario.
    Retorna el favorito si existe, o None si no existe.
    """
    return Favourite.objects.filter(user=user, name=name).first()

def saveFavourite(fav):
    fav = Favourite.objects.create(
        name=fav.name,
        gender=fav.gender,
        status=fav.status,
        occupation=fav.occupation,
        phrases=fav.phrases,
        age=fav.age,
        image=fav.image,
        user=fav.user
    )
    return fav

def getAllFavourites(user):
    """
    Obtiene todos los favoritos de un usuario desde la base de datos.
    """
    favourities = Favourite.objects.filter(user=user)
    return favourities

def deleteFavourite(favId):
    favourite = Favourite.objects.get(id=favId)
    favourite.delete()
    return True