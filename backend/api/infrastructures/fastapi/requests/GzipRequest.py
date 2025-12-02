import gzip
from fastapi import  Request


class GzipRequest(Request):

    async def body(self) -> bytes:

        if not hasattr(self, "_body"):
            body = await super().body()
            if "gzip" in self.headers.get("Content-Encoding"):
                body = gzip.decompress(body)
            self._body = body
        return self._body

