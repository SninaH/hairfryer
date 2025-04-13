import asyncio
import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import HttpUrl
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.api.pydantic_schemas import UploadYouTubeRequest, UploadYouTubeResponse, SubmitCoordinatesRequest, \
    SubmitCoordinatesResponse, StatusResults, StatusProcessingResponse, ErrorResponse, ThrowResult
from src.database.database import get_db
from src.database.models.game_session import GameSession
from src.utils import get_query_param_value
from src.video_utils.get_numbers_frames import get_data_from_frames, get_data
from src.video_utils.save_youtube_video import save_youtube_video, video_to_images

api_router = APIRouter()


@api_router.get("/")
async def hello():
    return {"message": "Hello World"}


@api_router.post("/upload-youtube", response_model=UploadYouTubeResponse)
async def upload_youtube(body: UploadYouTubeRequest, db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())

    video_url = str(body.youtube_url)
    video_id = get_query_param_value(video_url, 'v')
    if not video_id:
        raise HTTPException(status_code=400, detail="Invalid YouTube URL.")

    result = await db.execute(select(GameSession).where(GameSession.youtube_url == video_id))
    existing_session = result.scalar_one_or_none()
    if not existing_session:
        await asyncio.create_task(save_youtube_video(video_url, "/data/videos/"))

    await video_to_images(video_id, "mkv", "/data/videos/", "/data/images/", every_n_seconds=10, for_frontend=True)

    preview_image_url = f"http://localhost:8000/images/{video_id}/frame0.jpg"

    new_session = GameSession(
        id=session_id,
        youtube_url=video_url,
        preview_image_url=preview_image_url,
        status="waiting-coordinates",
    )
    db.add(new_session)
    await db.commit()

    return UploadYouTubeResponse(
        session_id=session_id,
        preview_image_url=HttpUrl(preview_image_url)
    )


@api_router.post('/submit-coordinates', response_model=SubmitCoordinatesResponse)
async def submit_coordinates(body: SubmitCoordinatesRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(GameSession).where(GameSession.id == body.session_id))
    game_session = result.scalar_one_or_none()

    if not game_session:
        raise HTTPException(status_code=404, detail="Session not found.")

    if game_session.status != "waiting-coordinates":
        raise HTTPException(status_code=400, detail="Session is not in a state to receive coordinates.")

    game_session.coordinates_throw_order = body.coordinates.throw_order.model_dump()
    game_session.coordinates_pins_fallen_in_throw = body.coordinates.pins_fallen_in_throw.model_dump()
    game_session.coordinates_pins_fallen_on_lane = body.coordinates.pins_fallen_on_lane.model_dump()
    game_session.coordinates_pin_1 = body.coordinates.pins["pin_1"].model_dump()
    game_session.coordinates_pin_1 = body.coordinates.pins["pin_1"].model_dump()
    game_session.coordinates_pin_2 = body.coordinates.pins["pin_2"].model_dump()
    game_session.coordinates_pin_3 = body.coordinates.pins["pin_3"].model_dump()
    game_session.coordinates_pin_4 = body.coordinates.pins["pin_4"].model_dump()
    game_session.coordinates_pin_5 = body.coordinates.pins["pin_5"].model_dump()
    game_session.coordinates_pin_6 = body.coordinates.pins["pin_6"].model_dump()
    game_session.coordinates_pin_7 = body.coordinates.pins["pin_7"].model_dump()
    game_session.coordinates_pin_8 = body.coordinates.pins["pin_8"].model_dump()
    game_session.coordinates_pin_9 = body.coordinates.pins["pin_9"].model_dump()

    # todo: poženi async task
    coordinates = [
        [*game_session.coordinates_throw_order, "int"],
        [*game_session.coordinates_pins_fallen_in_throw, "int"],
        [*game_session.coordinates_pins_fallen_on_lane, "int"],
        [*game_session.coordinates_pin_1, "bool"],
        [*game_session.coordinates_pin_2, "bool"],
        [*game_session.coordinates_pin_3, "bool"],
        [*game_session.coordinates_pin_4, "bool"],
        [*game_session.coordinates_pin_5, "bool"],
        [*game_session.coordinates_pin_6, "bool"],
        [*game_session.coordinates_pin_7, "bool"],
        [*game_session.coordinates_pin_8, "bool"],
        [*game_session.coordinates_pin_9, "bool"]
    ]

    video_id = get_query_param_value(game_session.youtube_url, 'v')

    total_throws, total_pins_fallen, throws = await get_data('/data/images/', video_id, coordinates)
    game_session.total_throws = total_throws
    game_session.total_pins_fallen = total_pins_fallen
    game_session.throws = throws

    # game_session.total_throws
    # game_session.total_pins_fallen
    # game_session.throws


    # game_session.status = "processing"
    game_session.status = "done"
    await db.commit()

    response = SubmitCoordinatesResponse(
        status="coordinates_received",
        message="Coordinates successfully received, processing will continue."
    )
    return response


@api_router.get("/status/{session_id}", response_model=StatusResults)
async def get_result(session_id: str, db: AsyncSession = Depends(get_db)):
    # 1. Check if session exists
    result = await db.execute(select(GameSession).where(GameSession.id == session_id))
    game_session = result.scalar_one_or_none()

    if not game_session:
        raise HTTPException(status_code=404, detail="Session not found.")
    if game_session.status == "waiting-coordinates" or game_session.status == "processing":
        return StatusProcessingResponse()
    if game_session.status == "error":
        return ErrorResponse(message=game_session.error_message)

    if game_session.status != "done":
        raise HTTPException(status_code=500, detail="Something went wrong.")

    results = StatusResults(
        total_throws=game_session.total_throws,
        total_pins_fallen=game_session.total_pins_fallen,
        throws=[ThrowResult(**throw) for throw in game_session.throws]
    )
    return results
