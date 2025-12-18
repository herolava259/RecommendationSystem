import json
from typing import Callable


from fastapi import Request, Response


from fastapi.routing import APIRoute



class PythonConventionRoute(APIRoute):

    def _convert_in(self, body: bytes) -> bytes:
        json_object = json.loads(body.decode("utf-8"))

        def recursive_convert(json_element: dict) -> dict:

            convention_element = dict()

            for k, v in json_element.items():
                new_k = ""
                for c in k:
                    if c.isupper():
                        new_k += f"_{c.lower()}"
                    else:
                        new_k += c
                if isinstance(v, dict):
                    v = recursive_convert(v)

                convention_element[new_k] = v

            return convention_element



        convention_obj = recursive_convert(json_element=json_object)

        return json.dumps(convention_obj).encode("utf-8")

    def _convert_out(self, response: Response) -> Response:

        if response.charset != "utf-8":
            return response

        if response.media_type != "application/json":
            return response

        json_object = json.loads(response.body.decode("utf-8"))

        def recursive_convert(json_element: dict) -> dict:
            convention_element = dict()
            for k, v in json_element.items():
                new_k = ""
                has_delimiter = False
                for c in k:
                    if c == "_":
                        has_delimiter = True
                    elif has_delimiter:
                        new_k += c.upper()
                        has_delimiter = False
                    else:
                        new_k += c
                if isinstance(v, dict):
                    v = recursive_convert(v)
                convention_element[new_k] = v
            return convention_element

        convention_obj = recursive_convert(json_element=json_object)

        response.body = json.dumps(convention_obj).encode("utf-8")
        return response



    def get_route_handler(self) -> Callable:

        original_route_handler = super().get_route_handler()


        async def convert_to_python_convention(request: Request) -> Response:

            if request.method in "GET":
                return await original_route_handler(request)

            if request.headers.get("content-type") != "application/json":
                return await original_route_handler(request)

            body = await request.body()

            if body is None:
                return self._convert_out(await original_route_handler(request))

            request._body = self._convert_in(body)
            return self._convert_out(await original_route_handler(request))

        return convert_to_python_convention






