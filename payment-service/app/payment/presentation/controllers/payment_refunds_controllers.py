from fastapi import APIRouter


router = APIRouter(prefix="/api/v2/refunds")

@router.get("/")
def create_request(use_case):
    use_case.execute()
    

@router.get("/{refund_id}")
def get_by_id(use_case):
    use_case.execute()


@router.put("/{payment_id}/aprpove") # Admin
def approve(use_case):
    use_case.execute()


@router.put("/{payment_id}/reject") # Admin
def reject(use_case):
    use_case.execute()



