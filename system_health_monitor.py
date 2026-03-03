import psutil
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("SystemHealthMonitor")

@mcp.tool()
def get_cpu_usage() -> str:
    cpu_percent = psutil.cpu_percent(interval=1)
    return f"Current CPU usage is {cpu_percent}%."

@mcp.tool()
def get_memory_usage() -> str:
    memory = psutil.virtual_memory()
    total_gb = round(memory.total / (1024**3), 2)
    used_gb = round(memory.used / (1024**3), 2)
    percent = memory.percent
    
    return f"Memory Usage: {percent}% ({used_gb}GB used out of {total_gb}GB total)."

@mcp.tool()
def get_disk_space() -> str:
    disk = psutil.disk_usage('/')
    free_gb = round(disk.free / (1024**3), 2)
    total_gb = round(disk.total / (1024**3), 2)
    
    return f"Disk Space: {free_gb}GB free out of {total_gb}GB total ({disk.percent}% used)."

if __name__ == "__main__":
    mcp.run()