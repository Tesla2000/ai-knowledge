from dnd.character.blueprint.building_blocks import (
    AnyBuildingBlock,
)
from dnd.character.blueprint.building_blocks.building_block import (
    BuildingBlock,
)
from dnd.character.builder import Builder
from dnd.character.checkpoint import IncrementChain
from dnd.character.checkpoint import IncrementStorage
from dnd.character.checkpoint import MemoryStorage
from dnd.character.presentable_character import (
    PresentableCharacter,
)
from dnd.server.example_generators.example_building_blocks import (
    example_building_blocks,
)
from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import Field
from pydantic import TypeAdapter
from pydantic import ValidationError
from starlette.responses import Response


class _CreateCharacterResponse(BaseModel):
    character: PresentableCharacter | None = None
    increment_chain: IncrementChain
    error: str | None = None


_building_blocks_creator: TypeAdapter[tuple[BuildingBlock, ...]] = TypeAdapter(
    tuple[AnyBuildingBlock, ...]
)

EXAMPLES = (
    _building_blocks_creator.dump_python(example_building_blocks(), mode="json"),
)


class _CreateCharacterRequestSchema(BaseModel):
    building_blocks: list[dict[str, object]] = Field(examples=list(EXAMPLES))
    increment_chain: dict[str, object] = Field(examples=[IncrementChain()])


def create_app(storage: IncrementStorage) -> FastAPI:
    app_ = FastAPI()

    @app_.post(
        "/create_character",
        response_model=_CreateCharacterResponse,
    )
    def create_character(
        request: _CreateCharacterRequestSchema, response: Response
    ) -> _CreateCharacterResponse:
        errors = []
        building_blocks: tuple[BuildingBlock, ...]
        try:
            building_blocks = _building_blocks_creator.validate_python(
                request.building_blocks
            )
        except ValidationError as e:
            errors.append(e)
        try:
            increment_chain = IncrementChain.model_validate(request.increment_chain)
        except ValidationError as e:
            errors.append(e)
        if errors:
            raise HTTPException(status_code=422, detail="\n\n".join(map(str, errors)))
        builder = Builder(
            building_blocks=building_blocks,
            increment_storage=storage,
        )
        result = builder.build(increment_chain)
        output_increment_chain = storage.load_chain(result.chain_id)
        response.status_code = 422 if result.error else 200
        return _CreateCharacterResponse(
            character=result.character,
            increment_chain=output_increment_chain,
            error=str(result.error) if result.error else None,
        )

    return app_


app = create_app(MemoryStorage())
