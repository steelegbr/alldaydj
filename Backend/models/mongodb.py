from typing_extensions import Annotated
from pydantic import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
