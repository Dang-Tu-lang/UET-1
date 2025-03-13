from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from loguru import logger
from schema.request import MatchingRequest
from schema.response import AlertResp
from service.alert_matching import AlertMatching

router = APIRouter()

alert_matching = AlertMatching()


@router.get("/", response_model=AlertResp)
def matching(request: MatchingRequest):
    logger.info(f"Request: {request}")
    try:
        alerts_matched = alert_matching.match_alert(
            event=request.event, alerts=request.alerts
        )
        logger.info(f"Alerts matched: {alerts_matched}")
        return alerts_matched
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Bad request: {e}")
    except Exception as e:
        msg = f"Internal server error: {e}"
        logger.error(msg)
        return JSONResponse(
            status_code=500, content=AlertResp(message=msg, alerts=[]).model_dump()
        )
