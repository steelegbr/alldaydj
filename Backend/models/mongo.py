from pydantic.functional_validators import BeforeValidator
from typing import Annotated

PyObjectId = Annotated[str, BeforeValidator]
