from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Security, status
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from models.type import CartType, CartTypeUpdate
from pymongo import ReturnDocument
from services.database import type_collection
from services.security import TokenVerifier

router = APIRouter(prefix="/type", tags=["type"])

token_verifier = TokenVerifier()


@router.post(
    "/",
    response_description="Create a type",
    response_model=CartType,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_type(
    cart_type: CartTypeUpdate = Body(...), auth_result: str = Security(token_verifier.verify)
):
    new_cart_type = await type_collection.insert_one(cart_type.model_dump(by_alias=True))
    created_cart_type = await type_collection.find_one({"_id": new_cart_type.inserted_id})
    return created_cart_type


@router.get(
    "/{id}",
    response_description="Get a type",
    response_model=CartType,
    response_model_by_alias=False,
)
async def get_type(id: str, auth_result: str = Security(token_verifier.verify)):
    if not (cart_type := await type_collection.find_one({"_id": ObjectId(id)})):
        raise HTTPException(status_code=404, detail=f"Type {id} not found")
    return cart_type


@router.delete("/{id}", response_description="Delete a type", status_code=204)
async def delete_type(id: str, auth_result: str = Security(token_verifier.verify)):
    delete_result = await type_collection.delete_one({"_id": ObjectId(id)})

    if not delete_result.deleted_count == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Type {id} not found"
        )


@router.put(
    "/{id}",
    response_description="Update a type",
    response_model=CartType,
    response_model_by_alias=False,
)
async def update_type(
    id: str,
    cart_type: CartTypeUpdate = Body(...),
    auth_result: str = Security(token_verifier.verify),
):
    update_result = await type_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": cart_type.model_dump(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    if not update_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Type {id} not found"
        )
    return update_result


@router.get(
    "/",
    response_description="List types",
    response_model=Page[CartType],
    response_model_by_alias=False,
)
async def list_types(auth_result: str = Security(token_verifier.verify)) -> Page[CartType]:
    return await paginate(type_collection)
