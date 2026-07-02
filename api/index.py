from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

BACKEND = "https://athulcode.pythonanywhere.com"


@app.route("/", defaults={"path": ""}, methods=[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
])
@app.route("/<path:path>", methods=[
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS"
])
def gateway(path):
    if not BACKEND:
        return {
            "success": False,
            "message": "BACKEND_URL not configured."
        }, 500

    try:
        url = f"{BACKEND}/{path}"

        headers = {
            k: v
            for k, v in request.headers.items()
            if k.lower() not in (
                "host",
                "content-length"
            )
        }

        response = requests.request(
            method=request.method,
            url=url,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            timeout=20
        )

        excluded = {
            "content-length",
            "connection",
            "content-encoding"
        }

        response_headers = [
            (k, v)
            for k, v in response.headers.items()
            if k.lower() not in excluded
        ]

        return Response(
            response.content,
            status=response.status_code,
            headers=response_headers
        )

    except requests.Timeout:
        return {
            "success": False,
            "message": "Backend timeout."
        }, 504

    except requests.ConnectionError:
        return {
            "success": False,
            "message": "Cannot connect to backend."
        }, 502

    except Exception as e:
        return {
            "success": False,
            "message": "Gateway error.",
            "error": str(e)
        }, 500


app = app
