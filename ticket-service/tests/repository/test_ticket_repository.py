from tests.repository.conftest import *
from sqlalchemy import and_, select, update, delete
import pytest


class TestSQLAlchemyTicketRepository:
    async def test_save_new_ticket(self, ticket_repository, sample_ticket_entity, async_session):
        # Test saving a new ticket
        saved_ticket = await ticket_repository.save(sample_ticket_entity)
        
        # Verify the returned ticket has an ID
        assert saved_ticket.id is not None
        
        # Verify the ticket was saved in the database
        stmt = select(TicketModel).where(TicketModel.id == saved_ticket.id)
        result = await async_session.execute(stmt)
        db_ticket = result.scalar_one()
        
        assert db_ticket.movie_id == sample_ticket_entity.movie_id
        assert db_ticket.showtime_id == sample_ticket_entity.showtime_id
        assert db_ticket.user_id == sample_ticket_entity.customer_details.id
        assert db_ticket.customer_email == sample_ticket_entity.customer_details.user_email
        assert float(db_ticket.price) == float(sample_ticket_entity.price_details.price)
        assert db_ticket.price_currency == sample_ticket_entity.price_details.currency
        assert db_ticket.status == sample_ticket_entity.status.value
        assert db_ticket.ticket_type == sample_ticket_entity.ticket_type.value

    async def test_save_existing_ticket(self, ticket_repository, sample_ticket_model, async_session):
        # Create an entity from the existing model
        price_details = PriceDetails(price=Decimal("10.50"), currency="USD")
        customer_details = CustomerDetails(
            user_email="updated@example.com",
            id=1,
            customer_ip_address="0.0.0.0",
        )
        payment_details = PaymentDetails(id=1, transaction_id=123, type="digital", method="card", currency="USD")
        
        existing_ticket = Ticket(
            id=sample_ticket_model.id,
            movie_id=sample_ticket_model.movie_id,
            showtime_id=sample_ticket_model.showtime_id,
            customer_details=customer_details,
            payment_details=payment_details,
            price_details=price_details,
            status=TicketStatus(sample_ticket_model.status),
            ticket_type=TicketType(sample_ticket_model.ticket_type),
        )
        
        # Update the ticket
        updated_ticket = await ticket_repository.save(existing_ticket)
        
        # Verify the changes were saved
        assert updated_ticket.customer_details.user_email == "updated@example.com"
        
        # Verify in database
        stmt = select(TicketModel).where(TicketModel.id == sample_ticket_model.id)
        result = await async_session.execute(stmt)
        db_ticket = result.scalar_one()
        assert db_ticket.customer_email == "updated@example.com"

    async def test_save_non_existing_ticket(self, ticket_repository):
        price_details = PriceDetails(price=Decimal("10.50"), currency="USD")
        customer_details = CustomerDetails(
            user_email="modelcustomer_email@mail.com",
            id=1,
            customer_ip_address="0.0.0.0",
        )
        payment_details = PaymentDetails(id=1, transaction_id=123, type="digital", method="card", currency="USD")

        non_existing_ticket = Ticket(
            id=9999,  # Non-existing ID
            movie_id=1,
            showtime_id=1,
            customer_details=customer_details,
            payment_details=payment_details,
            price_details=price_details,
            status=TicketStatus.RESERVED,
            ticket_type=TicketType.DIGITAL,
        )
 
        
        with pytest.raises(ValueError, match=f"Ticket with ID {non_existing_ticket.id} not found"):
            await ticket_repository.save(non_existing_ticket)

    async def test_get_by_id(self, ticket_repository, sample_ticket_model):
            ticket: Ticket = await ticket_repository.get_by_id(sample_ticket_model.id)
            
            assert ticket is not None
            assert ticket.id == sample_ticket_model.id
            assert ticket.movie_id == sample_ticket_model.movie_id
            assert ticket.showtime_id == sample_ticket_model.showtime_id
            assert ticket.customer_details.id == sample_ticket_model.user_id
            assert ticket.customer_details.user_email == sample_ticket_model.customer_email
            assert float(ticket.price_details.price) == float(sample_ticket_model.price)
            assert ticket.price_details.currency  == sample_ticket_model.price_currency
            assert ticket.status.value == sample_ticket_model.status
            assert ticket.ticket_type.value == sample_ticket_model.ticket_type
            

    async def test_get_by_id_not_found(self, ticket_repository):
            ticket = await ticket_repository.get_by_id(9999)  # Non-existing ID
            assert ticket is None

    async def test_list_by_user_id(self, ticket_repository, sample_ticket_model: TicketModel, async_session):
        # Add another ticket for the same user
        another_ticket = TicketModel(
            movie_id=2,
            showtime_id=2,
            user_id=1,            
            customer_email="another@example.com",
            price=12.50,
            price_currency="USD",
            status=TicketStatus.USED.value,
            ticket_type=TicketType.DIGITAL.value,
        )
        async_session.add(another_ticket)
        await async_session.commit()
        
        tickets = await ticket_repository.list_by_user_id(sample_ticket_model.user_id)
        
        assert len(tickets) == 2
        assert all(ticket.customer_details.id == sample_ticket_model.user_id for ticket in tickets)

    async def test_list_by_user_id_empty(self, ticket_repository):
        tickets = await ticket_repository.list_by_user_id(9999)  # Non-existing user
        assert len(tickets) == 0

    async def test_list_by_showtime_id(self, ticket_repository, async_session):
        # Add another ticket for the same showtime
        another_ticket = TicketModel(
            movie_id=2,
            showtime_id=50,
            user_id=1,            
            customer_email="another@example.com",
            price=12.50,
            price_currency="USD",
            status=TicketStatus.USED.value,
            ticket_type=TicketType.DIGITAL.value,
        )
        async_session.add(another_ticket)
        await async_session.commit()
        
        tickets = await ticket_repository.list_by_showtime_id(50) # 1 with 50
        
        assert len(tickets) == 1
        assert all(ticket.showtime_id == 50 for ticket in tickets)


    async def test_list_by_showtime_id_empty(self, ticket_repository):
            tickets = await ticket_repository.list_by_showtime_id(9999)  # Non-existing showtime
            assert len(tickets) == 0
            
    async def test_delete_ticket(self, ticket_repository, sample_ticket_model):
        result = await ticket_repository.delete(sample_ticket_model.id)
        assert result is True
        
        # Verify ticket is deleted
        ticket = await ticket_repository.get_by_id(sample_ticket_model.id)
        assert ticket is None

    async def test_delete_non_existing_ticket(self, ticket_repository):
        result = await ticket_repository.delete(9999)  # Non-existing ID
        assert result is False
        
