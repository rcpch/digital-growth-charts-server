from fastapi import Request

def get_reference(reference: str):
    def dependency(request: Request):
        return reference
    return dependency