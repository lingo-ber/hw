from pydantic import BaseModel, ConfigDict, Field


class RecipeBase(BaseModel):
    """
    Базовая модель данных рецепта.

    Attributes:
        dish_name (str): название блюда (ограничение длины - 100 символов)
        cooking_time (int): время приготовления в минутах
        ingredients (str): список ингредиентов
        description (str): описание рецепта
    """

    dish_name: str = Field(max_length=100)
    cooking_time: int = Field(gt=0)
    ingredients: str
    description: str


class RecipeIn(RecipeBase):
    """
    Модель-наследник от RecipeBase,
    используется при приёме данных рецепта от клиента.
    """

    pass


class RecipeOut(RecipeBase):
    """
    Модель-наследник от RecipeBase,
    используется при выводе данных рецепта клиенту.

    Attributes:
        id (int): идентификатор рецепта
    """

    id: int

    model_config = ConfigDict(from_attributes=True)


class RecipesListBase(BaseModel):
    """
    Базовая модель метаданных рецепта (для списка рецептов).

    Attributes:
        dish_name (str): название блюда (ограничение длины - 100 символов)
        views (int): количество просмотров рецепта
        cooking_time (int): время приготовления в минутах
    """

    dish_name: str = Field(max_length=100)
    views: int = Field(ge=0)
    cooking_time: int = Field(gt=0)


class RecipesListOut(RecipesListBase):
    """
    Модель-наследник от RecipesListBase,
    используется при выводе списка рецептов клиенту.

    Attributes:
        id (int): идентификатор записи
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
