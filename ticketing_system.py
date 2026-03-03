from mcp.server.fastmcp import FastMCP

mcp = FastMCP("TicketingSystem")

MOCK_TICKETS = {
    "INC-101": {"status": "Open", "priority": "High", "issue": "Main SQL database is locked, affecting internal apps."},
    "INC-102": {"status": "Closed", "priority": "Low", "issue": "User password reset for email access."},
    "INC-103": {"status": "Open", "priority": "Critical", "issue": "Production deployment failed, high CPU usage detected."}
}

@mcp.tool()
def get_open_tickets() -> str:
    """Fetch a list of all currently open IT support tickets."""
    open_tickets_gen = (
        f"[{t_id}] Priority: {details['priority']} - {details['issue']}" 
        for t_id, details in MOCK_TICKETS.items() 
        if details['status'].lower() == 'open'
    )
    
    result = "\n".join(open_tickets_gen)
    if not result:
        return "There are currently no open tickets."
    
    return "Open IT Tickets:\n" + result

@mcp.tool()
def get_ticket_details(ticket_id: str) -> str:
    """Get the full details for a specific ticket ID (e.g., INC-101)."""
    ticket_id = ticket_id.upper()
    ticket = MOCK_TICKETS.get(ticket_id)
    
    if ticket:
        return f"Details for {ticket_id}:\nStatus: {ticket['status']}\nPriority: {ticket['priority']}\nIssue: {ticket['issue']}"
    return f"Error: Ticket {ticket_id} could not be found."

@mcp.tool()
def update_ticket_status(ticket_id: str, new_status: str) -> str:
    """Update the status of a specific ticket (e.g., change 'Open' to 'Closed')."""
    ticket_id = ticket_id.upper()
    if ticket_id in MOCK_TICKETS:
        old_status = MOCK_TICKETS[ticket_id]['status']
        MOCK_TICKETS[ticket_id]['status'] = new_status
        return f"Successfully updated {ticket_id} from '{old_status}' to '{new_status}'."
    return f"Error: Ticket {ticket_id} not found. Cannot update status."

if __name__ == "__main__":
    print("Starting IT Ticketing System on HTTP (Streamable) at http://127.0.0.1:8000/mcp ...")
    mcp.run(transport='streamable-http')