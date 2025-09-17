from contextlib import asynccontextmanager
from typing import Sequence

from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.sql.expression import desc

from . import models, schemas
from .database import engine, session


@asynccontextmanager
async def lifespan():
    """
    Обработчик событий запуска и завершения работы приложения.

    При запуске создаёт все таблицы в базе данных,
    определённые в моделях SQLAlchemy.
    По завершении работы закрывает соединение с базой данных
    и освобождает ресурсы движка.
    """
    # код при старте
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # код при завершении
    await session.close()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/recipes", response_model=schemas.RecipeOut)
async def add_recipe(recipe: schemas.RecipeIn) -> models.Recipe:
    """
    Эндпоинт для добавления нового рецепта.

    Принимает данные рецепта в формате schemas.RecipeIn,
    создаёт и сохраняет запись в таблице Recipe.

    Args:
        recipe (schemas.RecipeIn): данные рецепта

    Raises:
        HTTPException: 409 - если рецепт с таким названием уже есть в базе

    Returns:
        models.Recipe: добавленный рецепт
    """
    new_recipe = models.Recipe(**recipe.model_dump())
    try:
        session.add(new_recipe)
        await session.commit()
    except IntegrityError:
        raise HTTPException(
            status_code=409, detail="Recipe with this name already exists"
        )
    return new_recipe


@app.get("/recipes", response_model=list[schemas.RecipesListOut])
async def get_recipes() -> Sequence[models.Recipe]:
    """
    Эндпоинт для получения списка всех рецептов.

    Возвращает список рецептов (метаданные рецептов),
    отсортированных по количеству просмотров (по убыванию),
    а затем по времени приготовления (по возрастанию).

    Returns:
        list[models.Recipe]: список рецептов (метаданные рецептов)
    """
    stmt = select(models.Recipe).order_by(
        desc(models.Recipe.views), models.Recipe.cooking_time
    )
    res = await session.execute(stmt)
    return res.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeOut)
async def get_recipe(recipe_id: int) -> models.Recipe:
    """
    Эндпоинт для получения рецепта по его ID.

    Если рецепт найден, увеличивает счётчик просмотров у этого рецепта.

    Args:
        recipe_id (int): идентификатор рецепта

    Raises:
        HTTPException: 404 - если рецепт не найден

    Returns:
        models.Recipe: данные рецепта
    """
    res = await session.execute(
        select(models.Recipe).where(models.Recipe.id == recipe_id)
    )
    recipe = res.scalars().first()
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    recipe.views += 1
    await session.commit()
    return recipe
