from fastapi import APIRouter


router = APIRouter(prefix="/api/v2/payments/products/food")

@router.post("/")
def purchase(use_case):
    use_case.execute()
    

@router.post("/{payment_id}")
def details(use_case):
    use_case.execute()


@router.post("/{payment_id}/refund")
def refund(use_case):
    use_case.execute()
