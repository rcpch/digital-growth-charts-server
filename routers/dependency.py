from fastapi import Request, Depends

def get_reference(reference: str):
    def dependency(request: Request):
        return reference
    return dependency