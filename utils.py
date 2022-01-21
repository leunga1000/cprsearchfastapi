import string
def transform_text(text: str) -> str:
    return text.translate(str.maketrans('', '', string.punctuation)).lower()

try:
    import spacy
    spacy_nlp = spacy.load("en_core_web_md")
except ImportError:
    spacy_nlp = None




import json as json, typing
from starlette.responses import Response

class PrettyJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: typing.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=4,
            separators=(", ", ": "),
        ).encode("utf-8")