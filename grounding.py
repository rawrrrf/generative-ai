from langchain.chains import RetrievalQA
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from langchain_google_vertexai import VertexAI
from langchain_google_community import VertexAISearchRetriever
from langchain_google_community import VertexAIMultiTurnSearchRetriever
import IPython
import vertexai
import langchain
from langchain_google_vertexai import VertexAI
from vertexai.generative_models import (
    GenerativeModel,
    GenerationResponse,
    Tool,
    grounding,
)
from vertexai.preview.generative_models import grounding as preview_grounding
from IPython.display import display, Markdown
PROJECT_ID = 'ai-sandbox-company-18'
REGION = 'us-central1'
MODEL_NAME = "gemini-1.5-pro-001"
vertexai.init(project=PROJECT_ID, location=REGION)
llm = VertexAI(model_name=MODEL_NAME, max_output_tokens=1000)
model = GenerativeModel(MODEL_NAME)


def print_grounding_response(response: GenerationResponse):
    """Prints Gemini response with grounding citations."""
    grounding_metadata = response.candidates[0].grounding_metadata

    # Citation indices are in byte units
    ENCODING = "utf-8"
    text_bytes = response.text.encode(ENCODING)

    prev_index = 0
    markdown_text = ""

    sources: dict[str, str] = {}
    footnote = 1
    for attribution in grounding_metadata.grounding_attributions:
        context = attribution.web or attribution.retrieved_context
        if not context:
            print(f"Skipping Grounding Attribution {attribution}")
            continue

        title = context.title
        uri = context.uri
        end_index = int(attribution.segment.end_index)

        if uri not in sources:
            sources[uri] = {"title": title, "footnote": footnote}
            footnote += 1

        text_segment = text_bytes[prev_index:end_index].decode(ENCODING)
        markdown_text += f"{text_segment} [[{sources[uri]['footnote']}]]({uri})"
        prev_index = end_index

    if prev_index < len(text_bytes):
        markdown_text += str(text_bytes[prev_index:], encoding=ENCODING)

    markdown_text += "\n## Grounding Sources:"

    if grounding_metadata.web_search_queries:
        markdown_text += (
            f"\n**Web Search Queries:** {grounding_metadata.web_search_queries}\n"
        )
    elif grounding_metadata.retrieval_queries:
        markdown_text += (
            f"\n**Retrieval Queries:** {grounding_metadata.retrieval_queries}\n"
        )

    for uri, source in sources.items():
        markdown_text += f"{source['footnote']}. [{source['title']}]({uri})\n"

    print(markdown_text)
    #display(Markdown(markdown_text))

DATA_STORE_PROJECT_ID = 'ai-sandbox-company-18'  # @param {type:"string"}
DATA_STORE_REGION = "global"  # @param {type:"string"}
# Replace this with your data store ID from Vertex AI Search
DATA_STORE_ID = "ra-selection-guide_1716893896897"  # @param {type:"string"}

datastore = f"projects/{DATA_STORE_PROJECT_ID}/locations/{DATA_STORE_REGION}/collections/default_collection/dataStores/{DATA_STORE_ID}"
tool = Tool.from_retrieval(
    preview_grounding.Retrieval(preview_grounding.VertexAISearch(datastore=datastore))
)
chat = model.start_chat(response_validation=False)
datastore = f"projects/{DATA_STORE_PROJECT_ID}/locations/{DATA_STORE_REGION}/collections/default_collection/dataStores/{DATA_STORE_ID}"
tool = Tool.from_retrieval(
    preview_grounding.Retrieval(preview_grounding.VertexAISearch(datastore=datastore))
)

PROMPT = "List all the names of the products in the datastore"
PROMPT_FOLLOWUP = "From the selection in the datastore recommend products to build a conveyor belt"

#response = chat.send_message("list the title of the files in the current datastore", tools=[tool])
#print_grounding_response(response)

i = 10
try:
    while i > 0:
        print ("Question: ")
        question = input()
        print ("Response: ")
        response = chat.send_message(question, tools=[gh.tool])
        print_grounding_response(response)
        i -= 1
except Exception as e:
    print(e)