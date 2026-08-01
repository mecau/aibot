from aiohttp import web
import asyncio
import threading
import time
import requests

# ── Web server ────────────────────────────────────────────────────

async def handle(request):
    return web.Response(text="MecauAI Bot is Alive!")

def run():
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(runner.setup())
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    loop.run_until_complete(site.start())
    loop.run_forever()

# ── Self-ping loop ────────────────────────────────────────────────

def self_ping():
    """Ping own endpoint every 47 seconds to prevent container sleep."""
    # Wait for the server to start before pinging
    time.sleep(10)
    while True:
        try:
            requests.get("http://127.0.0.1:8080/", timeout=10)
        except Exception:
            pass  # silently ignore — server may be momentarily unavailable
        time.sleep(47)

# ── Entry point ───────────────────────────────────────────────────

def keep_alive():
    # Start web server thread
    t_server = threading.Thread(target=run, daemon=True)
    t_server.start()

    # Start self-ping thread
    t_ping = threading.Thread(target=self_ping, daemon=True)
    t_ping.start()
