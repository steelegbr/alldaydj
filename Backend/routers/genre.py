from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Security, status
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from models.genre import Genre, GenreUpdate
from pymongo import ReturnDocument
from services.database import genre_collection
from services.security import TokenVerifier

router = APIRouter(prefix="/genre", tags=["genre"])

token_verifier = TokenVerifier()


@router.post(
    "/",
    response_description="Create a genre",
    response_model=Genre,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_genre(
    genre: GenreUpdate = Body(...), auth_result: str = Security(token_verifier.verify)
):
    new_genre = await genre_collection.insert_one(genre.model_dump(by_alias=True))
    created_genre = await genre_collection.find_one({"_id": new_genre.inserted_id})
    return created_genre


@router.get(
    "/{id}",
    response_description="Get a genre",
    response_model=Genre,
    response_model_by_alias=False,
)
async def get_genre(id: str, auth_result: str = Security(token_verifier.verify)):
    if not (genre := await genre_collection.find_one({"_id": ObjectId(id)})):
        raise HTTPException(status_code=404, detail=f"Genre {id} not found")
    return genre


@router.delete("/{id}", response_description="Delete a genre", status_code=204)
async def delete_genre(id: str, auth_result: str = Security(token_verifier.verify)):
    delete_result = await genre_collection.delete_one({"_id": ObjectId(id)})

    if not delete_result.deleted_count == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre {id} not found"
        )


@router.put(
    "/{id}",
    response_description="Update a genre",
    response_model=Genre,
    response_model_by_alias=False,
)
async def update_genre(
    id: str,
    genre: GenreUpdate = Body(...),
    auth_result: str = Security(token_verifier.verify),
):
    update_result = await genre_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": genre.model_dump(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    if not update_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Genre {id} not found"
        )
    return update_result


@router.get(
    "/",
    response_description="List genres",
    response_model=Page[Genre],
    response_model_by_alias=False,
)
async def list_geres(auth_result: str = Security(token_verifier.verify)) -> Page[Genre]:
    return await paginate(genre_collection)
