from bson import ObjectId
from fastapi import APIRouter, Body, HTTPException, Security, status
from fastapi_pagination import Page
from fastapi_pagination.ext.motor import paginate
from models.tag import Tag, TagUpdate
from pymongo import ReturnDocument
from services.database import tag_collection
from services.security import TokenVerifier

router = APIRouter(prefix="/tag", tags=["tag"])

token_verifier = TokenVerifier()


@router.post(
    "/",
    response_description="Create a tag",
    response_model=Tag,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_tag(
    tag: TagUpdate = Body(...), auth_result: str = Security(token_verifier.verify)
):
    new_tag = await tag_collection.insert_one(tag.model_dump(by_alias=True))
    created_tag = await tag_collection.find_one({"_id": new_tag.inserted_id})
    return created_tag


@router.get(
    "/{id}",
    response_description="Get a tag",
    response_model=Tag,
    response_model_by_alias=False,
)
async def get_tag(id: str, auth_result: str = Security(token_verifier.verify)):
    if not (tag := await tag_collection.find_one({"_id": ObjectId(id)})):
        raise HTTPException(status_code=404, detail=f"Tag {id} not found")
    return tag


@router.delete("/{id}", response_description="Delete a tag", status_code=204)
async def delete_tag(id: str, auth_result: str = Security(token_verifier.verify)):
    delete_result = await tag_collection.delete_one({"_id": ObjectId(id)})

    if not delete_result.deleted_count == 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag {id} not found"
        )


@router.put(
    "/{id}",
    response_description="Update a tag",
    response_model=Tag,
    response_model_by_alias=False,
)
async def update_tag(
    id: str,
    tag: TagUpdate = Body(...),
    auth_result: str = Security(token_verifier.verify),
):
    update_result = await tag_collection.find_one_and_update(
        {"_id": ObjectId(id)},
        {"$set": tag.model_dump(by_alias=True)},
        return_document=ReturnDocument.AFTER,
    )
    if not update_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Tag {id} not found"
        )
    return update_result


@router.get(
    "/",
    response_description="List tags",
    response_model=Page[Tag],
    response_model_by_alias=False,
)
async def list_tags(auth_result: str = Security(token_verifier.verify)) -> Page[Tag]:
    return await paginate(tag_collection)
