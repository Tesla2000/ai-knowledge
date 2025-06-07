from pydantic import BaseModel


class LanggraphModel(BaseModel):
    def missing_fields(self) -> set[str]:
        return {k for k, v in self.model_dump().items() if v is not None}

    def missing_fields_string(self) -> str:
        return "\n".join(
            f"{k}: {self.model_fields[k].description}" for k in self.missing_fields()
        )

    def is_complete(self) -> bool:
        return not self.missing_fields()
