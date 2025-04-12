from pydantic import BaseModel, HttpUrl
from typing import List, Dict
from pydantic import RootModel


class UploadYouTubeRequest(BaseModel):
    youtube_url: HttpUrl


class UploadYouTubeResponse(BaseModel):
    session_id: str
    preview_image_url: HttpUrl


class CoordinateBox(RootModel[list[float]]):
    def __len__(self) -> int:
        return len(self.root) == 4


class PinCoordinates(BaseModel):
    throw_order: CoordinateBox
    pins_fallen_in_throw: CoordinateBox
    pins_fallen_on_lane: CoordinateBox
    pins: Dict[str, CoordinateBox]  # e.g., "pin_1", "pin_2", ...


class SubmitCoordinatesRequest(BaseModel):
    session_id: str
    coordinates: PinCoordinates


class SubmitCoordinatesResponse(BaseModel):
    status: str = "coordinates_received"
    message: str


class StatusProcessingResponse(BaseModel):
    status: str = "processing"


class ThrowResult(BaseModel):
    pins_fallen: int
    pins_hit: List[int]


class StatusResults(BaseModel):
    total_throws: int
    total_pins_fallen: int
    throws: List[ThrowResult]


class StatusDoneResponse(BaseModel):
    status: str = "done"
    results: StatusResults


class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
