import pydantic

if pydantic.__version__.startswith("2"):
    def to_dict(model: pydantic.BaseModel, **kwargs):
        return model.model_dump(**kwargs)
else:
    def to_dict(model: pydantic.BaseModel, **kwargs):
        return model.dict(**kwargs)
