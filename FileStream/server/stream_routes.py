import time
import math
import logging
import mimetypes
import traceback
from aiohttp import web
from aiohttp.http_exceptions import BadStatusLine
from FileStream.bot import multi_clients, work_loads, FileStream
from FileStream.config import Telegram, Server
from FileStream.server.exceptions import FIleNotFound, InvalidHash
from FileStream import utils, StartTime, __version__
from FileStream.utils.render_template import render_page

routes = web.RouteTableDef()

@routes.get("/", allow_head=True)
async def home_page(_):
    # Serve the HTML page as the response
    html_content = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="File Stream and Share Bot - Instant Streaming and Sharing Links">
    <title>File Stream | Share Bot</title>

    <!-- Favicon -->
    <link rel="icon" href="https://iili.io/2Kb8u6u.md.png" type="image/x-icon">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">

    <!-- FontAwesome Icons -->
    <script src="https://kit.fontawesome.com/a076d05399.js" crossorigin="anonymous"></script>

    <!-- Styling -->
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #000000, #1a1a1d);
            color: #fff;
            overflow-x: hidden;
            line-height: 1.6;
        }

        header {
            background: linear-gradient(135deg, #e50914, #b81d24);
            padding: 15px 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
            position: sticky;
            top: 0;
            z-index: 1000;
            transition: all 0.3s ease;
        }

        header:hover {
            background: linear-gradient(135deg, #b81d24, #e50914);
        }

        header h1 {
            font-size: 32px;
            letter-spacing: 1px;
            color: white;
            animation: slideIn 1s ease-in-out;
            font-weight: 600;
            text-align: center;
        }

        .menu {
            position: absolute;
            right: 20px;
        }

        .menu-btn {
            background: none;
            border: none;
            font-size: 24px;
            color: white;
            cursor: pointer;
            transition: transform 0.3s ease, color 0.3s ease;
        }

        .menu-btn:hover {
            transform: rotate(90deg);
            color: #ff7373;
        }

        .menu-content {
            display: none;
            position: absolute;
            right: 0;
            background: rgba(0, 0, 0, 0.8);
            border-radius: 5px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
            z-index: 10;
        }

        .menu-content a {
            display: block;
            padding: 10px 20px;
            color: white;
            text-decoration: none;
            font-weight: 500;
            transition: background-color 0.3s ease, padding-left 0.3s ease;
        }

        .menu-content a:hover {
            background-color: #e50914;
            padding-left: 30px;
        }

        .menu-btn:focus + .menu-content, .menu-content:hover {
            display: block;
        }

        .container {
            max-width: 1200px;
            margin: auto;
            padding: 50px 20px;
        }

        h2 {
            font-size: 32px;
            margin-bottom: 20px;
            text-align: center;
            color: #e50914;
            animation: fadeInUp 1s ease;
        }

        h2::after {
            content: '';
            width: 100px;
            height: 3px;
            background-color: #e50914;
            display: block;
            margin: 10px auto 0;
            animation: growLine 0.6s ease-in-out;
        }

        .section {
            margin-bottom: 50px;
        }

        .about, .features, .privacy {
            background-color: rgba(255, 255, 255, 0.05);
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.5);
            transition: transform 0.3s ease, background-color 0.3s ease;
        }

        .about:hover, .features:hover, .privacy:hover {
            transform: translateY(-10px);
            background-color: rgba(255, 255, 255, 0.1);
        }

        p {
            font-size: 18px;
            margin-bottom: 20px;
            text-align: justify;
        }

        .cta-container {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 30px;
            animation: fadeInUp 1.2s ease;
        }

        .cta-button {
            display: inline-block;
            padding: 15px 30px;
            background-color: #e50914;
            color: white;
            font-size: 18px;
            border-radius: 30px;
            text-decoration: none;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }

        .cta-button:hover {
            background-color: #b81d24;
            transform: scale(1.1);
        }

        footer {
            background-color: #1a1a1d;
            padding: 20px;
            font-size: 16px;
            color: #fff;
            text-align: center;
            margin-top: 50px;
            transition: background-color 0.3s ease;
        }

        footer:hover {
            background-color: #2a2a2d;
        }

        footer a {
            color: #e50914;
            text-decoration: none;
            font-weight: bold;
        }

        footer a:hover {
            text-decoration: underline;
        }

        /* Animations */
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes growLine {
            from { width: 0; }
            to { width: 100px; }
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            header h1 {
                font-size: 28px;
            }

            .cta-button {
                font-size: 16px;
                padding: 10px 20px;
            }

            .menu-content {
                right: 10px;
            }
        }

        @media (max-width: 480px) {
            header h1 {
                font-size: 24px;
            }

            .container {
                padding: 15px;
            }

            .about, .features, .privacy {
                padding: 20px;
            }

            .cta-container {
                flex-direction: column;
                gap: 20px;
            }
        }
    </style>
</head>
<body>

    <header>
        <h1>File Stream | Share Bot</h1>
        <div class="menu">
            <button class="menu-btn">&#x22EE;</button>
            <div class="menu-content">
                <a href="#about">About</a>
                <a href="#features">Features</a>
                <a href="#privacy">Privacy Policy</a>
            </div>
        </div>
    </header>

    <!-- Container for all content -->
    <div class="container">
        <!-- About Section -->
        <section id="about" class="section about">
            <h2>About This Bot</h2>
            <p>
                Welcome to the File Streaming and Sharing Bot. This advanced tool enables seamless streaming and sharing of various file types, including documents, photos, GIFs, audio, and video. It generates instant links for easy access and distribution, ensuring swift and smooth streaming to enhance your file management experience!
            </p>
        </section>

        <!-- Features Section -->
        <section id="features" class="section features">
            <h2>Features</h2>
            <ul>
                <li>Instant file streaming and download links for any media.</li>
                <li>Supports files, photos, GIFs, audio, and video up to 4GB.</li>
                <li>Enables quick video streaming for efficient access.</li>
                <li>Enjoy fast speeds and a seamless streaming experience.</li>
                <li>Simple and user-friendly interface with easy commands.</li>
            </ul>
        </section>

        <!-- Privacy Policy Section -->
        <section id="privacy" class="section privacy">
            <h2>Privacy Policy</h2>
            <p>
            At our service, we prioritize user privacy and have implemented stringent measures to ensure data protection. We do not collect, store, or keep a record of any user-specific identifiers, such as chat ID, username, or personal information. The bot is designed to function without the necessity of logging any data related to individual users
            </p>
        </section>

        <!-- Call to Action Section -->
        <section class="section contact">
            <h2>Get Started Now!</h2>
            <div class="cta-container">
                <a href="https://t.me/Fast_FileStreamBot" target="_blank" class="cta-button">Use @Fast_FileStreamBot</a>
                <a href="https://t.me/AR_File_To_Link_Bot" target="_blank" class="cta-button">Use @AR_File_To_Link_Bot</a>
            </div>
        </section>
    </div>

    <!-- Footer Section -->
    <footer>
        Made with ❤️ by <a href="https://t.me/Ashlynn_Repository" target="_blank">Ashlynn Repository</a>
    </footer>

</body>
</html>            
    """
    return web.Response(text=html_content, content_type="text/html")

@routes.get("/host", allow_head=True)
async def host_embed(_):
    # Serves a fullscreen embedded page
    return web.Response(
        text=f"""
        <html>
        <head>
            <style>
                /* Remove margin and padding to ensure the iframe fills the viewport */
                body, html {{
                    margin: 0;
                    padding: 0;
                    width: 100%;
                    height: 100%;
                }}
                iframe {{
                    width: 100%;
                    height: 100%;
                    border: none;
                }}
            </style>
        </head>
        <body>
            <iframe src="https://ar-hosting.pages.dev/"></iframe>
        </body>
        </html>
        """,
        content_type="text/html"
    )

@routes.get("/status", allow_head=True)
async def root_route_handler(_):
    return web.json_response(
        {
            "server_status": "running",
            "uptime": utils.get_readable_time(time.time() - StartTime),
            "telegram_bot": "@" + FileStream.username,
            "connected_bots": len(multi_clients),
            "loads": dict(
                ("bot" + str(c + 1), l)
                for c, (_, l) in enumerate(
                    sorted(work_loads.items(), key=lambda x: x[1], reverse=True)
                )
            ),
            "version": __version__,
        }
    )

@routes.get("/watch/{path}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        return web.Response(text=await render_page(path), content_type='text/html')
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass


@routes.get("/dl/{path}", allow_head=True)
async def stream_handler(request: web.Request):
    try:
        path = request.match_info["path"]
        return await media_streamer(request, path)
    except InvalidHash as e:
        raise web.HTTPForbidden(text=e.message)
    except FIleNotFound as e:
        raise web.HTTPNotFound(text=e.message)
    except (AttributeError, BadStatusLine, ConnectionResetError):
        pass
    except Exception as e:
        traceback.print_exc()
        logging.critical(e.with_traceback(None))
        logging.debug(traceback.format_exc())
        raise web.HTTPInternalServerError(text=str(e))

class_cache = {}

async def media_streamer(request: web.Request, db_id: str):
    range_header = request.headers.get("Range", 0)
    
    index = min(work_loads, key=work_loads.get)
    faster_client = multi_clients[index]
    
    if Telegram.MULTI_CLIENT:
        logging.info(f"Client {index} is now serving {request.headers.get('X-FORWARDED-FOR',request.remote)}")

    if faster_client in class_cache:
        tg_connect = class_cache[faster_client]
        logging.debug(f"Using cached ByteStreamer object for client {index}")
    else:
        logging.debug(f"Creating new ByteStreamer object for client {index}")
        tg_connect = utils.ByteStreamer(faster_client)
        class_cache[faster_client] = tg_connect
    logging.debug("before calling get_file_properties")
    file_id = await tg_connect.get_file_properties(db_id, multi_clients)
    logging.debug("after calling get_file_properties")
    
    file_size = file_id.file_size

    if range_header:
        from_bytes, until_bytes = range_header.replace("bytes=", "").split("-")
        from_bytes = int(from_bytes)
        until_bytes = int(until_bytes) if until_bytes else file_size - 1
    else:
        from_bytes = request.http_range.start or 0
        until_bytes = (request.http_range.stop or file_size) - 1

    if (until_bytes > file_size) or (from_bytes < 0) or (until_bytes < from_bytes):
        return web.Response(
            status=416,
            body="416: Range not satisfiable",
            headers={"Content-Range": f"bytes */{file_size}"},
        )

    chunk_size = 1024 * 1024
    until_bytes = min(until_bytes, file_size - 1)

    offset = from_bytes - (from_bytes % chunk_size)
    first_part_cut = from_bytes - offset
    last_part_cut = until_bytes % chunk_size + 1

    req_length = until_bytes - from_bytes + 1
    part_count = math.ceil(until_bytes / chunk_size) - math.floor(offset / chunk_size)
    body = tg_connect.yield_file(
        file_id, index, offset, first_part_cut, last_part_cut, part_count, chunk_size
    )

    mime_type = file_id.mime_type
    file_name = utils.get_name(file_id)
    disposition = "attachment"

    if not mime_type:
        mime_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"

    # if "video/" in mime_type or "audio/" in mime_type:
    #     disposition = "inline"

    return web.Response(
        status=206 if range_header else 200,
        body=body,
        headers={
            "Content-Type": f"{mime_type}",
            "Content-Range": f"bytes {from_bytes}-{until_bytes}/{file_size}",
            "Content-Length": str(req_length),
            "Content-Disposition": f'{disposition}; filename="{file_name}"',
            "Accept-Ranges": "bytes",
        },
    )
