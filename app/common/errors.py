from fastapi import HTTPException, status

def not_found(detail: str = "Not found"):
    """
    Return error response with Not Found. 404
    """
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

def conflict(detail: str):
    """
    Return error response with conflict details. 409
    """
    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=detail)

def bad_request(detail: str):
    """
    Return error response with bad request. 400
    """
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
