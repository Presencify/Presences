import time
import psutil

while running:
    ram = psutil.virtual_memory()
    update_rpc(
        state=f"RAM Usage: {ram.percent}%",
        details=f"Total: {ram.total / 1024 / 1024 / 1024:.2f} GB",
    )
    time.sleep(10)
