from app.extensions import ma
from app.models import ServiceTicket
from app.blueprints.mechanics.schemas import MechanicSchema

class ServiceTicketSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ServiceTicket

    customer_id = ma.auto_field()
    mechanics = ma.Nested(MechanicSchema, many=True, only=('id', 'name'))
    
service_ticket_schema = ServiceTicketSchema()
service_tickets_schema = ServiceTicketSchema(many=True)