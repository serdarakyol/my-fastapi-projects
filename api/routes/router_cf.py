from starlette.requests import Request
from fastapi import APIRouter, Depends

from api.core import security
from api.models.model_cf import CFRequest, CFResponse
from api.services.service_cf import Recommendation

router = APIRouter()

@router.post("/collaborativeFilter", response_model=CFResponse, name="collaborative filter")
async def post_recommend(
    request: Request,
    authenticated: bool = Depends(security.validate_request),
    request_data: CFRequest = None,
    ) -> CFResponse:

    recommendation_service = Recommendation(
        cf_matrix=request.app.state.cf_matrix, 
        products_info=request.app.state.product_info
    )
    # get similar top n item
    results = recommendation_service.recommend(items=request_data.item, n_item=request_data.n_item)
    input_data = recommendation_service.find_products_by_id(
        recommended_product_ids=request_data.item
    )
    return CFResponse(input_item=input_data, similar_items=results)
