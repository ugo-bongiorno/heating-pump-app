"""
Definition of the REST API, using FastAPI
"""

import ctypes
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


# define the wrappers for our .c functions
HP_TOOLS = ctypes.CDLL(str((Path(__file__).parent / "hp_tools/hp_tools.so").resolve()))


# define templates for our input / output specifications
class TargetTemperature(BaseModel):
    target_water_temperature: int


class WaterTemperature(BaseModel):
    current_water_temperature: int


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


@app.get("/get_water_temperature/", response_model=WaterTemperature)
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

    return {"current_water_temperature": current_water_temp}


@app.get("/get_target_water_temperature/", response_model=TargetTemperature)
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

    return {"target_water_temperature": target_water_temp}


@app.post("/set_target_water_temperature/", response_model=TargetTemperature)
async def set_target_water_temperature(
    target_temperature: TargetTemperature,
) -> Dict[str, int]:
    """
    Set the target water temperature.

    :param target_temperature: The user query target temperature.
    :type target_temperature: TargetTemperature

    :raises HTTPException: if an error occurred when communicating
        with the heat pump

    :return: The newly set value of target temperature
    :rtype: Dict[str, int]
    """
    new_target_water_temp = HP_TOOLS.set_target_water_temperature(
        target_temperature.target_water_temperature
    )
    if new_target_water_temp == -1:
        raise HTTPException(
            status_code=500,
            detail="Unable to communicate with the heat pump",
        )

    return {"target_water_temperature": new_target_water_temp}
