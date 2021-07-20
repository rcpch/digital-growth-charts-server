"""
UK-WHO router
"""

from fastapi import APIRouter

# set up the API router
uk_who = APIRouter(
    prefix="/uk-who",
    # tags=["uk90", "uk-who", "WHO", "England"]
)


@uk_who.post("/")
def root_response():
    return {"uk": "who"}
