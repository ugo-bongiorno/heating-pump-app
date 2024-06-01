"""
Definition of the REST API, using FastAPI
"""

import ctypes
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator


# define the wrappers for our .c functions
HP_TOOLS = ctypes.CDLL(str((Path(__file__).parent / "hp_tools/hp_tools.so").resolve()))


# define templates for our input / output specifications
class NewTargetTemperature(BaseModel):
    target_water_temperature: float = Field(
        title="Target Water Temperature",
        description="The target water temperature to be set, in °C. It must be a multiple of 0.5 °C",
        ge=12,
        le=40,
    )

    @field_validator("target_water_temperature", mode="after")
    @classmethod
    def must_be_multiple_of_half(cls, input_value: float) -> float:
        """
        Validates that the input target_water_temperature is a multiple of a half Celsius degree

        :param input_value: The input value to check
        :type input_value: float

        :raises ValueError: if the input value is not a multiple of 0.5

        :return: The validated value
        """
        if input_value % 0.5 != 0:
            raise ValueError("target_water_temperature must be a multiple of 0.5 °C")
        return input_value


class CurrentTargetTemperature(BaseModel):
    target_water_temperature: float = Field(
        title="Current Target Water Temperature",
        description="The current target water temperature, in °C",
    )


class CurrentWaterTemperature(BaseModel):
    current_water_temperature: float = Field(
        title="Current Water Temperature",
        description="The current water temperature, in °C",
    )


app = FastAPI()

# allow specific CORS origins (so that requests
# from the frontend pass through)
allowed_cors_origins = [
    "http://localhost",
    "http://localhost:4200",
    "http://raspberrypi-garage",
    "http://raspberrypi-garage.local",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_water_temperature/", response_model=CurrentWaterTemperature)
async def get_water_temperature() -> Dict[str, int]:
    """
    Get the current water temperature.

    :raises HTTPException: if an error occurred when communicating
        with the heat pump

    :return: The current value of target temperature
    :rtype: Dict[str, int]
    """
    current_water_temp = HP_TOOLS.read_water_temperature()
    if current_water_temp == -1:
        raise HTTPException(
            status_code=500,
            detail="Unable to communicate with the heat pump",
        )
    # convert the temperature to °C
    current_water_temp = round(current_water_temp / 10, 1)

    return {"current_water_temperature": current_water_temp}


@app.get("/get_target_water_temperature/", response_model=CurrentTargetTemperature)
async def get_target_water_temperature() -> Dict[str, int]:
    """
    Get the target water temperature.

    :raises HTTPException: if an error occurred when communicating
        with the heat pump

    :return: The current value of target temperature
    :rtype: Dict[str, int]
    """
    target_water_temp = HP_TOOLS.read_target_water_temperature()
    if target_water_temp == -1:
        raise HTTPException(
            status_code=500,
            detail="Unable to communicate with the heat pump",
        )
    # convert the temperature to °C
    target_water_temp = round(target_water_temp / 10, 1)

    return {"target_water_temperature": target_water_temp}


@app.post("/set_target_water_temperature/", response_model=NewTargetTemperature)
async def set_target_water_temperature(
    target_temperature: NewTargetTemperature,
) -> Dict[str, int]:
    """
    Set the target water temperature. The target temperature must be a multiple of 0.5 °C.
    The minimum allowed value is 12, and the maximum allowed value is 40.

    :param target_temperature: The user query target temperature.
    :type target_temperature: TargetTemperature

    :raises HTTPException: if an error occurred when communicating
        with the heat pump

    :return: The newly set value of target temperature
    :rtype: Dict[str, int]
    """
    new_target_water_temp = HP_TOOLS.set_target_water_temperature(
        int(target_temperature.target_water_temperature * 10)
    )
    if new_target_water_temp == -1:
        raise HTTPException(
            status_code=500,
            detail="Unable to communicate with the heat pump",
        )

    return {"target_water_temperature": new_target_water_temp}
