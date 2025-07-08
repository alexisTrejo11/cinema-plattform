from typing import Any, Dict
from app.domain.value_objects import UserId,PaymentStatus, PaymentType
from app.domain.repository.payment_repository import PaymentRepository
from .query import GetPaymentHistoryQuery
from .result import PaymentHistoryResult
from ...dto.response import PaymentHistoryItemBuilder

class GetPaymentHistoryQueryHandler:
    """Handler for getting payment history."""
    def __init__(self, payment_repository: PaymentRepository):
        self.payment_repository = payment_repository
    
    async def handle(self, query: GetPaymentHistoryQuery) -> PaymentHistoryResult:
        """
        Handle payment history query.
        
        Args:
            query: Payment history query
            
        Returns:
            Payment history result
        """
        try:
            filters = self._build_filter_criteria(query)
            self._add_pagiantaion_and_sorting(filters, query)
            
            payments = await self.payment_repository.list(**filters)
            
            has_more = len(payments) > query.limit
            if has_more:
                payments = payments[:query.limit]
            
            payment_items = [
                PaymentHistoryItemBuilder()
                .set_payment_id(payment.id.value)
                .set_user_id(payment.user_id.value)
                .set_amount(payment.amount.to_float())
                .set_currency(payment.amount.currency.value)
                .set_payment_method(payment.payment_method.value)
                .set_payment_type(payment.payment_type.value)
                .set_status(payment.status.value)
                .set_timestamps(payment.created_at, payment.updated_at, payment.completed_at)
                .set_refund_details(payment.refunded_amount.to_float() if payment.refunded_amount else 0, payment.refund_reason, payment.refunded_at)
                .set_failure_details(failure_reason=payment.failure_reason)
                .set_metadata(payment.metadata.__dict__ if payment.metadata else None)
                .build()
                
                for payment in payments
            ]
            
            return PaymentHistoryResult(
                payments=payment_items,
                total_count=len(payment_items),
                has_more=has_more,
                limit=query.limit,
                offset=query.offset
            )    
        except Exception as e:
            return PaymentHistoryResult.return_failure(limit=query.limit, offset=query.offset)
 
    def _build_filter_criteria(self, query) -> Dict[str, Any]:
        filters: Dict[str, Any]  = { 'user_id': UserId.from_string(str(query.user_id)) }
        
        if query.status:
            filters['status'] = PaymentStatus(query.status)
        
        if query.payment_type:
            filters['payment_type'] = PaymentType(query.payment_type)
        
        if query.start_date:
            filters['created_after'] = query.start_date
        
        if query.end_date:
            filters['created_before'] = query.end_date
            
        return filters
    
    def _add_pagiantaion_and_sorting(self, filters: Dict[str, Any], query):
        filters.update({
            'limit': query.limit + 1,
            'offset': query.offset,
            'sort_by': query.sort_by.value,
            'sort_order': query.sort_order.value
        })