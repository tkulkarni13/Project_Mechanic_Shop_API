from .schemas import service_ticket_schema, service_tickets_schema
from flask import jsonify, request
from marshmallow import ValidationError
from sqlalchemy import select
from app.models import ServiceTicket, Mechanic, db
from . import service_tickets_bp

# Create new service ticket
@service_tickets_bp.route('/', methods=['POST'])
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    new_ticket = ServiceTicket(**data)
    db.session.add(new_ticket)
    db.session.commit()
    
    return service_ticket_schema.jsonify(new_ticket), 201

# Get all service tickets
@service_tickets_bp.route('/', methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    tickets = db.session.execute(query).scalars().all()
    
    return service_tickets_schema.jsonify(tickets), 200

# Add mechanic to service ticket
@service_tickets_bp.route('/<int:id>/add_mechanic/<int:mechanic_id>', methods=['PUT'])
def add_mechanic_to_service_ticket(id, mechanic_id):
    ticket = db.session.get(ServiceTicket, id)
    
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    ticket.mechanics.append(mechanic)
    db.session.commit()
    
    return service_ticket_schema.jsonify(ticket), 200

# Remove mechanic from service ticket
@service_tickets_bp.route('/<int:id>/remove_mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic_from_service_ticket(id, mechanic_id):
    ticket = db.session.get(ServiceTicket, id)
    
    if not ticket:
        return jsonify({"message": "Service ticket not found"}), 404
    
    mechanic = db.session.get(Mechanic, mechanic_id)
    if not mechanic:
        return jsonify({"message": "Mechanic not found"}), 404
    
    if mechanic not in ticket.mechanics:
        return jsonify({"message": "Mechanic not assigned to this service ticket"}), 400
    
    ticket.mechanics.remove(mechanic)
    db.session.commit()

    return service_ticket_schema.jsonify(ticket), 200