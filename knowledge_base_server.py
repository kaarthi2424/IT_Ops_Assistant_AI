import sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ITKnowledgeBase")
DB_FILE = "it_knowledge_base.db"

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sops (
            error_code TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            resolution_steps TEXT NOT NULL
        )
    ''')
    
    dummy_sops = [
        ("ERR-MEM-99", "High Memory / Swap Usage Detected", "1. Identify top memory-consuming processes.\n2. Check for zombie processes.\n3. If a known memory leak exists in a specific service, restart that service.\n4. Escalate to Level 3 if memory pressure persists after 15 minutes."),
        ("ERR-DB-01", "SQL Database Locked", "1. Query active transactions to find the blocking session.\n2. Kill the hanging transaction safely.\n3. Verify connection pool limits on internal apps.\n4. Notify the reporting team of potential data delays."),
        ("ERR-CPU-50", "CPU Spikes on Web Nodes", "1. Check incoming network traffic for DDoS patterns.\n2. Review recent code deployments for unoptimized loops.\n3. Temporarily scale up worker nodes if traffic is legitimate.")
    ]
    
    cursor.executemany('''INSERT OR IGNORE INTO sops (error_code, title, resolution_steps) VALUES (?, ?, ?)''', dummy_sops)
    
    conn.commit()
    conn.close()

setup_database()

@mcp.tool()
def search_knowledge_base(keyword: str) -> str:
    """Search the IT Knowledge Base for SOPs using a keyword."""
    search_term = f"%{keyword}%"
    
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT error_code, title FROM sops WHERE title LIKE ? OR resolution_steps LIKE ? ''', (search_term, search_term))
        results = cursor.fetchall()
        
    if not results:
        return f"No SOPs found matching the keyword: '{keyword}'."
    
    output = "Found the following relevant SOPs:\n"
    for row in results:
        output += f"- [{row[0]}] {row[1]}\n"
    
    return output + "\nUse 'get_resolution_steps' with the specific error code to read the full procedure."

@mcp.tool()
def get_resolution_steps(error_code: str) -> str:
    """Fetch the detailed, step-by-step resolution plan for a specific error code."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute('SELECT title, resolution_steps FROM sops WHERE error_code = ?', (error_code.upper(),))
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return f"SOP: {result[0]}\nResolution Steps:\n{result[1]}"
    
    return f"Error: No resolution steps found for error code '{error_code}'."

if __name__ == "__main__":
    mcp.run()