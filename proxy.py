from aiohttp import web
import aiohttp

async def handle(request):
    url = request.query.get("url")
    if not url:
        return web.Response(text="Missing ?url= parameter", status=400)

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=url,
            headers=request.headers,
            data=await request.read()
        ) as resp:
            body = await resp.read()
            return web.Response(body=body, status=resp.status, headers=resp.headers)

app = web.Application()
app.router.add_route("*", "/proxy", handle)

if __name__ == "__main__":
    web.run_app(app, host="0.0.0.0", port=8080)