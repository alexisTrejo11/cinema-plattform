class CreatePaymentMethodUseCase:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self, command: CreatePaymentMethodCommand) -> PaymentMethodDTO:

        card = Card(
            card_holder=command.card_holder,
            card_number=command.card_number,
            cvv=command.cvv,
            expiration_month=command.expiration_month,
            expiration_year=command.expiration_year,
        )

        payment_method = PaymentMethod(
            id=ID.generate(),
            user_id=command.user_id,
            card=card,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        self.payment_method_repository.add(payment_method)

        return PaymentMethodDTO.from_entity(payment_method)


class ListPaymentMethodsQuery:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self) -> List[PaymentMethodDTO]:
        payment_methods = self.payment_method_repository.find_all()
        return [PaymentMethodDTO.from_entity(pm) for pm in payment_methods]


class SoftDeletePaymentMethodUseCase:
    def __init__(self, payment_method_repository: IRepository):
        self.payment_method_repository = payment_method_repository

    def execute(self, command: SoftDeletePaymentMethodCommand):
        payment_method = self.payment_method_repository.find_by_id(command.id)

        if not payment_method:
            raise Exception("Payment method not found")

        payment_method.deleted_at = datetime.now()
        payment_method.updated_at = datetime.now()

        self.payment_method_repository.update(payment_method)
