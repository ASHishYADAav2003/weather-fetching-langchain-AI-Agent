# LangChain Master Q&A Guide

Here are the complete answers to all 150 of your LangChain questions, structured logically by topic and including necessary code examples.

## 1. LangChain Fundamentals

**1. What is LangChain?**
LangChain is an open-source framework designed to simplify the creation of applications using large language models (LLMs). It provides standard interfaces for components like memory, agents, chains, and document loaders to build complex AI applications easily.

**2. Why do we need LangChain if we can directly call an LLM API?**
While you can call LLM APIs directly, LangChain provides a structured way to chain multiple calls together, connect LLMs to external data sources (like databases or APIs), manage conversational memory, parse outputs into structured data, and orchestrate complex workflows using agents, which would otherwise require a lot of boilerplate code.

**3. What are the core components of LangChain?**
Models (LLMs, Chat Models, Embeddings), Prompts (Prompt Templates, Example Selectors), Output Parsers, Memory, Chains, Agents, and Retrievers (Document Loaders, Text Splitters, Vector Stores).

**4. What is LCEL (LangChain Expression Language)?**
LCEL is a declarative way to compose chains in LangChain. It uses the pipe operator (`|`) to pass the output of one component as the input to the next, making it easier to build, stream, batch, and trace complex processing pipelines.

**5. Explain the architecture of a LangChain application.**
It typically involves Data ingestion (Document loaders → Text splitters → Embeddings → Vector Store) and Execution flow (User Input → Prompt Template → LLM → Output Parser). For complex logic, it uses Agents (User Input → Agent → executes Tools → LLM → final output).

**6. Difference between LangChain and LlamaIndex?**
LangChain is a general-purpose framework for building LLM applications, focusing on chains, agents, and versatile tooling. LlamaIndex (formerly GPT Index) is specifically optimized for data ingestion, indexing, and advanced RAG (Retrieval-Augmented Generation) pipelines.

**7. What problems does LangChain solve?**
Context limitations (via RAG and memory), reasoning constraints (via agents and tool usage), formatting issues (via output parsers), and state management in stateless LLM APIs.

---

## 2. Models

**8. What is a Chat Model?**
A variation of an LLM that is fine-tuned specifically for conversational interactions. It takes a sequence of messages (System, Human, AI) as input rather than a single raw string, and outputs an AI message.

**9. Difference between LLM and Chat Model?**
An LLM (Text LLM) takes a string as input and returns a string (text completion). A Chat Model takes a list of chat messages as input and returns a chat message.

**10. What is ChatOpenAI?**
A LangChain wrapper class for OpenAI's chat models (like `gpt-4o`), allowing them to be integrated seamlessly into LangChain workflows.

**11. How do you connect NVIDIA/OpenAI/Groq models in LangChain?**
By installing their respective integration packages (e.g., `langchain-openai`, `langchain-groq`, `langchain-nvidia-ai-endpoints`) and instantiating their specific model classes (e.g., `ChatOpenAI()`, `ChatGroq()`, `ChatNVIDIA()`).

**12. What are temperature and max_tokens?**
`temperature` controls the randomness of the output (0 is deterministic/focused, 1+ is creative/random). `max_tokens` sets the hard limit on the number of tokens the model is allowed to generate in its response.

**13. What is streaming in LangChain?**
Receiving the output of the LLM token-by-token as it is being generated via the `.stream()` method, rather than waiting for the entire response to finish before displaying it.

**14. What is model binding?**
Attaching persistent arguments (like tool definitions, stop words, or specific kwargs) to a model so that every time the model is invoked, those arguments are automatically applied (e.g., `model.bind_tools(tools)`).

**15. What are embeddings and why are they important?**
Embeddings are numerical array representations (vectors) of text. They capture the semantic meaning of the text, allowing computers to measure the similarity between different pieces of text mathematically (crucial for RAG and search).

---

## 3. Prompts

**16. What is PromptTemplate?**
A template for creating raw string prompts with placeholders for dynamic variables. Used primarily for standard text LLMs.

**17. What is ChatPromptTemplate?**
A template specifically designed for Chat Models. It formats dynamic variables into a sequence of structured messages (System Message, Human Message, AI Message).

**18. Difference between PromptTemplate and ChatPromptTemplate?**
`PromptTemplate` outputs a single formatted string. `ChatPromptTemplate` outputs a list of formatted message objects.

**19. What are System, Human, and AI messages?**
- **System messages**: Set the behavior/persona of the AI.
- **Human messages**: Represent user inputs.
- **AI messages**: Represent the LLM's previous responses (used for conversational history).

**20. What is prompt engineering?**
The practice of designing, refining, and optimizing text inputs (prompts) to guide an LLM to produce the most accurate, relevant, and high-quality outputs.

**21. How do you pass dynamic variables to prompts?**
By defining placeholders in the template (e.g., `{topic}`) and passing a dictionary of values when formatting or invoking the template (e.g., `prompt.invoke({"topic": "AI"})`).

**22. What is partial prompting?**
Formatting a prompt template with some of its variables ahead of time, leaving the remaining variables to be filled in later in the execution chain.

**23. What are few-shot prompts?**
Prompts that include a few examples of the desired input-output behavior to guide the LLM on how to respond to the final, actual input.

**24. What are example selectors?**
Components that dynamically select the most relevant few-shot examples from a larger pool based on the user's current input (often using semantic similarity), keeping the prompt size manageable.

---

## 4. Output Parsers

**25. What is an Output Parser?**
A component that takes the raw text output from an LLM and converts it into a structured data format (like JSON, a Python dictionary, or a Pydantic model).

**26. Why do we need output parsers?**
LLMs naturally output raw unstructured text. Applications often require structured data (like objects or arrays) to trigger programmatic actions or insert into databases.

**27. What is StrOutputParser?**
A simple parser that extracts the raw string content from an AI message object, commonly used as the final step in an LCEL chain to get clean text.

**28. What is JsonOutputParser?**
A parser that forces the LLM to output valid JSON and parses that JSON string into a Python dictionary.

**29. How do structured outputs work?**
They combine prompting instructions (telling the LLM to output a specific format) with parsing logic. Modern models utilize "tool calling" or "JSON mode" APIs natively to enforce this.

**30. What is PydanticOutputParser?**
A parser that uses Pydantic schemas to define the exact structure, types, and validation rules for the expected output, ensuring the LLM returns data strictly matching the model.

**31. How do you force LLM output into JSON format?**
By using a `JsonOutputParser` or `PydanticOutputParser`, passing the parser's formatting instructions into the prompt, and enabling JSON mode on the model itself.

---

## 5. Chains

**32. What is a Chain?**
A sequence of calls to components (like prompts, models, and parsers) linked together to perform a specific task.

**33. Why are Chains useful?**
They modularize complex workflows, making them repeatable, easier to test, and allowing the output of one step to seamlessly flow as the input to the next.

**34. Difference between Sequential Chain and Agent?**
A Sequential Chain follows a strictly predefined, hardcoded path of execution. An Agent uses an LLM to dynamically decide which steps (tools) to take and in what order based on the user's input.

**35. What is the Pipe Operator (|)?**
Used in LangChain Expression Language (LCEL) to compose chains. `A | B` means the output of component A is passed as input to component B.

**36. How does LCEL create chains?**
By defining components that implement the `Runnable` protocol and chaining them using the `|` operator, automatically handling execution flows (sync, async, batch, stream).

**37. Explain: prompt | llm | parser**
A basic LCEL chain. The prompt template formats the input variables into a prompt, the formatted prompt is sent to the LLM, and the LLM's raw response is passed to the parser to extract the final output.

**38. What is RunnableSequence?**
The underlying class created when you chain multiple Runnables together using the `|` operator.

**39. What are parallel chains?**
Executing multiple chains or Runnables simultaneously (using `RunnableParallel` or a dictionary in LCEL) and combining their results.

**40. What are conditional chains?**
Chains that branch their execution path based on the output of a previous step or specific conditions (achieved using `RunnableBranch`).

---

## 6. Runnables

**41. What is Runnable in LangChain?**
The core interface of LCEL. Any component (prompt, model, parser, chain) that implements standard methods like `invoke`, `batch`, and `stream` is a Runnable.

**42. What methods are available in Runnables?**
`invoke`, `batch`, `stream`, `ainvoke`, `abatch`, `astream`, `astream_log`, `astream_events`.

**43. Difference between invoke(), batch(), stream(), ainvoke()?**
- `invoke()`: Synchronous run on a single input.
- `batch()`: Runs on a list of inputs in parallel.
- `stream()`: Returns an iterator yielding chunks of output as they are generated.
- `ainvoke()`: Asynchronous version of invoke.

**44. What is RunnableLambda?**
A wrapper that converts any standard Python function into a LangChain Runnable so it can be used inside an LCEL chain.

**45. What is RunnablePassthrough?**
A Runnable that passes its input through to the next step unchanged. Used to pass original user input alongside newly generated data.

**46. What is RunnableParallel?**
A Runnable that executes a dictionary of Runnables concurrently, taking the same input for all of them and returning a dictionary of their respective outputs.

**47. Explain RunnableBranch.**
A Runnable that allows conditional routing. It evaluates conditions sequentially and executes the runnable associated with the first true condition.

---

## 7. Document Loaders

**48. What is a Document Loader?**
A component that ingests data from various sources (files, websites) and converts it into LangChain `Document` objects containing text (`page_content`) and `metadata`.

**49. Why do we need document loaders?**
LLMs cannot natively read files from your hard drive or scrape websites. Document loaders extract the text in a standardized format so it can be processed.

**50. Name some commonly used document loaders.**
`PyPDFLoader`, `TextLoader`, `CSVLoader`, `WebBaseLoader`, `DirectoryLoader`.

**51. Explain PyPDFLoader, CSVLoader, TextLoader, WebBaseLoader.**
- `PyPDFLoader`: Extracts text from PDF files.
- `CSVLoader`: Loads CSV files, converting rows into separate documents.
- `TextLoader`: Loads plain text files (.txt).
- `WebBaseLoader`: Scrapes text content from HTML web pages.

**52. How do loaders fit into RAG?**
They are the very first step in the ingestion phase of RAG. They gather the external knowledge base that will be split, embedded, and stored in a vector DB.

---

## 8. Text Splitters

**53. Why is text splitting necessary?**
LLMs have strict context window limits. Splitting breaks large documents into smaller, manageable chunks that fit within the prompt.

**54. What happens if you don't split large documents?**
You will hit the model's token limit error, or the model might suffer from the "lost in the middle" phenomenon, ignoring information in the center of the text block.

**55. What is RecursiveCharacterTextSplitter?**
The recommended text splitter. It tries to split text on logical boundaries (paragraphs `\n\n`, then sentences `\n`, then spaces) recursively to keep related text together.

**56. Difference between chunk_size and chunk_overlap?**
`chunk_size` is the maximum length of a single chunk. `chunk_overlap` is the number of characters/tokens shared between two adjacent chunks.

**57. Why do we use chunk overlap?**
To prevent splitting a continuous thought or sentence right down the middle, ensuring context is not lost at the boundaries.

**58. Best chunk size for RAG?**
Typically 500 to 1000 tokens (or ~1000-2000 characters) with a 10-20% overlap is a solid starting point, depending on the embedding model.

**59. Token-based vs Character-based splitting?**
Character-based counts literal text characters. Token-based splits based on how the LLM tokenizes the text. Token-based is safer for strict context limits.

---

## 9. Embeddings

**60. What are embeddings?**
High-dimensional vectors (arrays of floating-point numbers) that mathematically represent the semantic meaning and context of text.

**61. Why can't we directly search text?**
Keyword search only finds exact word matches. It fails to understand synonyms or intent (e.g., searching "car" won't match a document talking exclusively about "automobiles").

**62. What is vector representation?**
Translating text into a point in an n-dimensional geometric space, where texts with similar meanings are located close to each other.

**63. How are embeddings generated?**
By passing text through a specialized neural network model trained to map semantic relationships into vector space.

**64. Examples of embedding models?**
OpenAI Embeddings, HuggingFace BGE models, Cohere Embeddings, Google Vertex AI Embeddings.

**65. Difference between OpenAI embeddings and HuggingFace embeddings?**
OpenAI embeddings require an API key and cloud costs but perform exceptionally well. HuggingFace embeddings are open-source and can be run entirely locally for free.

---

## 10. Vector Databases

**66. What is a Vector Database?**
A database specifically designed to store, manage, and query high-dimensional vector embeddings efficiently using similarity search algorithms.

**67. Why do we need vector databases?**
Standard SQL databases are terrible at computing mathematical similarities between massive arrays. Vector DBs use specialized indexes to search millions of vectors in milliseconds.

**68. Difference between SQL database and Vector Database?**
SQL databases store tabular data and query via exact matches. Vector DBs store unstructured data as vectors and query via mathematical similarity (nearest neighbors).

**69. What is indexing in a vector DB?**
Organizing vectors into data structures (like graphs) that allow for Approximate Nearest Neighbor (ANN) search, trading a tiny bit of accuracy for massive speed.

**70. Explain FAISS.**
(Facebook AI Similarity Search) An open-source library for efficient similarity search, highly performant for local, in-memory vector storage.

**71. Explain ChromaDB.**
A lightweight, open-source vector database designed specifically for building LLM apps. Easy to run locally or as a client/server.

**72. Explain Pinecone.**
A fully managed, cloud-native vector database. Serverless, highly scalable, and excellent for production deployments.

**73. Explain Weaviate.**
An open-source vector database offering powerful hybrid search (vector + keyword) capabilities natively.

**74. Explain Milvus.**
A highly scalable, open-source vector database built for massive enterprise-scale data.

**75. Explain Qdrant.**
An open-source vector similarity search engine written in Rust, known for high performance and excellent metadata filtering.

---

## 11. Similarity Search

**76. What is Semantic Search?**
Searching for information based on the intent and contextual meaning of the query, rather than exact keywords.

**77. Difference between Keyword Search and Semantic Search?**
Keyword search looks for exact string matches. Semantic search converts the query to a vector and finds nearest neighbor vectors in the database.

**78. What is Similarity Search?**
Finding items in a database that are mathematically most similar to a given query, usually calculated using vector distance metrics.

**79. What is Vector Similarity?**
A numerical score representing how close two vectors are to each other in a multi-dimensional space.

**80. Explain Cosine Similarity.**
A metric that measures the cosine of the angle between two vectors, focusing on orientation rather than magnitude.

**81. Formula of Cosine Similarity?**
Cosine Similarity (A, B) = (A · B) / (||A|| * ||B||)

**82. Why is cosine similarity preferred?**
Text length shouldn't drastically affect semantic meaning. Cosine similarity is robust against document length variations.

**83. Difference between Cosine Similarity, Euclidean Distance, Dot Product?**
- Cosine: Measures angle (direction).
- Euclidean: Measures physical straight-line distance.
- Dot Product: Combines both angle and magnitude.

**84. What is ANN (Approximate Nearest Neighbor)?**
Algorithms that quickly find an approximation of the nearest vectors rather than exhaustively comparing the query to every single vector.

**85. Why is ANN used in vector databases?**
Exact nearest neighbor search is too slow for massive datasets. ANN provides sub-millisecond search times with high accuracy.

---

## 12. Retrievers

**86. What is a Retriever?**
An interface in LangChain that takes a string query and returns a list of relevant `Document` objects, abstracting away the search mechanism.

**87. Difference between Retriever and Vector Store?**
A Vector Store saves the embeddings. A Retriever is the search interface used to query that database.

**88. What does `vectorstore.as_retriever()` do?**
Wraps a VectorStore object into a Retriever interface, allowing it to be easily integrated into RAG chains.

**89. What is Top-K retrieval?**
Returning the exact `k` most similar documents to the query based on the similarity score.

**90. What is MMR Retrieval?**
Maximal Marginal Relevance. It attempts to maximize both relevance to the query AND diversity among retrieved documents.

**91. What is Hybrid Search?**
Combining semantic vector search with traditional keyword search (e.g., BM25) and merging the results.

**92. What is Metadata Filtering?**
Applying traditional database filters (e.g., `date > 2023`) to the vector search to narrow down the search space.

---

## 13. RAG (Retrieval Augmented Generation)

**93. What is RAG?**
A framework where the LLM is provided with external, verified context (retrieved from a database) to ground its generation, preventing hallucinations.

**94. Why is RAG better than fine-tuning for many applications?**
RAG is cheaper, faster to update, provides citations/sources, and stops the model from hallucinating facts.

**95. Explain the complete RAG pipeline.**
1. Ingest: Load Docs → Split → Embed → Store in Vector DB.
2. Retrieve: Query → Embed Query → Similarity Search → Fetch Top-K.
3. Generate: Pass Query + Context into Prompt → LLM → Answer.

**96. What are the steps involved in RAG?**
Ingestion, Retrieval, Augmentation, Generation.

**97. What is Retrieval?**
Fetching the most relevant chunks of text from the knowledge base.

**98. What is Augmentation?**
Injecting the retrieved text chunks into the prompt alongside the user query.

**99. What is Generation?**
The LLM reading the augmented prompt and generating a final answer.

**100. What problem does RAG solve?**
The LLM's lack of knowledge about private or recent data, and hallucination.

**101. Hallucination vs RAG?**
Hallucination is inventing false facts. RAG mitigates this by instructing the LLM to only use the provided context.

**102. What are common RAG challenges?**
Poor retrieval quality, chunking strategy failures, losing context in long prompts, and complex multi-hop reasoning.

**103. What is Context Window?**
The maximum number of tokens an LLM can process in a single request (e.g., GPT-4 has 128k).

**104. What is Context Injection?**
The physical act of inserting retrieved document chunks into the prompt template.

---

## 14. Tools

**105. What is a Tool?**
A specific capability given to an Agent (like web search or a calculator) that it can invoke to interact with the outside world.

**106. Why do agents need tools?**
LLMs cannot browse the web or execute code natively. Tools act as the LLM's "hands" to gather live data or perform actions.

**107. How do you create a custom tool?**
Using the `@tool` decorator on a Python function, providing a clear docstring and type hints.

**108. Purpose of `@tool`?**
Converts a Python function into a LangChain `Tool` object, automatically extracting the schema required by the LLM.

**109. Difference between Tool and Function?**
A Tool wraps a Python Function with a specific schema (name, description, arguments) required by the LLM.

**110. Examples of tools used in production?**
Web search, SQL executors, GitHub API readers, Calculators, Slack/Jira integrations.

**111. Explain DuckDuckGoSearchRun.**
A built-in tool that performs a web search using DuckDuckGo and returns text snippets without requiring API keys.

**112. Explain Tavily Search.**
A search engine built specifically for AI agents, extracting clean, relevant content formatted for LLM consumption.

**113. Explain Weather Tool implementation.**
A custom tool taking a `location`, making an HTTP request to OpenWeatherMap, and returning current weather conditions.

---

## 15. Tool Calling

**114. What is Tool Calling?**
A capability of modern LLMs where the model outputs a structured JSON command specifying exactly which tool to run and with what arguments.

**115. How does tool calling work internally?**
You pass a JSON schema of your tools to the LLM. The LLM halts generation, outputs a `tool_call` object, your code executes the local function, and returns the result to the LLM.

**116. What happens when the LLM decides to call a tool?**
Execution stops, the LLM returns the tool name and arguments. LangChain runs the tool, wraps the result in a `ToolMessage`, and sends it back to the LLM to continue.

**117. Explain tool schema.**
A JSON definition describing the tool's name, purpose, and the exact names, types, and descriptions of its arguments.

**118. What is function calling?**
The original terminology introduced by OpenAI for Tool Calling. They mean the same thing.

**119. Difference between Tool Calling and API Calling?**
Tool calling is the LLM generating the instructions (JSON) to execute a function. API calling is the actual execution of an HTTP request.

---

## 16. Agents

**120. What is an Agent?**
A system where an LLM acts as a reasoning engine to dynamically determine which tools to take, execute them, and loop until a goal is reached.

**121. Difference between Agent and Chain?**
A Chain is deterministic (A → B → C). An Agent is non-deterministic (LLM decides steps dynamically).

**122. Why are Agents powerful?**
They solve complex, multi-step problems, recover from errors, and interact with multiple external systems dynamically.

**123. What is AgentExecutor?**
The runtime component that manages the Agent Loop. It takes the agent and tools, handles the while loop, and manages execution.

**124. Explain `create_tool_calling_agent()`.**
A LangChain constructor that builds an agent specifically optimized to utilize native LLM Tool Calling capabilities.

**125. What is `agent_scratchpad`?**
A section of the prompt where the AgentExecutor stores the history of tools called so far and their outputs.

**126. What is ReAct Agent?**
Reason + Act. A prompting strategy where the LLM outputs a "Thought", an "Action", and waits for an "Observation".

**127. What is Tool Calling Agent?**
An agent relying on the LLM's native ability to output JSON tool calls rather than strict text parsing.

**128. What is an Agent Loop?**
Prompt LLM → Return Tool Call → Execute Tool → Append Result to Scratchpad → Re-prompt LLM → Repeat until final answer.

**129. How does an Agent decide which tool to use?**
By reading the highly descriptive tool schemas provided in the prompt.

**130. What are the limitations of agents?**
Can get stuck in infinite loops, hallucinate inputs, are slower, more expensive, and require highly capable LLMs.

---

## 17. Advanced LangChain

**131. What is LangSmith?**
A unified platform for debugging, testing, evaluating, and monitoring LLM applications.

**132. Why use LangSmith?**
Provides visual tracing of chains, tracks token costs, logs errors, and allows dataset creation for prompt evaluation.

**133. What is tracing?**
Logging the entire execution graph showing prompt inputs, LLM responses, tool calls, and latency.

**134. What is observability?**
Monitoring the internal state and performance of AI applications in production.

**135. What is LangServe?**
A library turning LangChain runnables into production-ready REST APIs via FastAPI.

**136. How do you deploy a LangChain application?**
Wrap in LangServe/FastAPI, containerize with Docker, deploy to AWS/GCP/Vercel.

**137. How would you build a PDF Chatbot?**
Load PDF → Split text → Embed → Store in ChromaDB → Setup ConversationalRetrievalChain.

**138. How would you build a Resume Analyzer?**
Load Resume → PydanticOutputParser (Schema: Name, Skills) → LLM → JSON Profile → Evaluate against job description.

**139. How would you build a Weather Agent?**
Create OpenWeatherMap `@tool` → Instantiate ChatOpenAI → `create_tool_calling_agent` → `AgentExecutor` → Query.

**140. How would you build a Multi-Tool AI Assistant?**
Define tools (Search, Calendar) → Bind to Chat Model → Agent Executor → ChatMessageHistory → Deploy via LangServe.

---

## 18. Coding Questions

**141. Create a PromptTemplate.**
```python
from langchain_core.prompts import PromptTemplate
prompt = PromptTemplate.from_template("Translate the following English word to {language}: {word}")
```

**142. Build a Chain using LCEL.**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

chain = prompt | model | parser
print(chain.invoke({"topic": "bears"}))
```

**143. Create a custom weather tool.**
```python
from langchain_core.tools import tool

@tool
def get_weather(location: str) -> str:
    """Returns the current weather for a given city."""
    return f"The weather in {location} is 72°F and sunny."
```

**144. Implement a DuckDuckGo search tool.**
```python
from langchain_community.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()
print(search_tool.invoke("Who won the world series in 2023?"))
```

**145. Create an Agent using two tools.**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression."""
    return str(eval(expression))

tools = [DuckDuckGoSearchRun(), calculator]
model = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}")
])

agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

**146. Load a PDF and split it into chunks.**
```python
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = PyPDFLoader("document.pdf")
docs = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = splitter.split_documents(docs)
```

**147. Store embeddings in FAISS.**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings)
vector_store.save_local("faiss_index")
```

**148. Retrieve top 5 similar chunks.**
```python
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
results = retriever.invoke("What is the main topic of the document?")
```

**149. Build a complete RAG pipeline.**
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

template = """Answer the question based only on the following context:
{context}

Question: {question}"""
prompt = ChatPromptTemplate.from_template(template)
model = ChatOpenAI(model="gpt-4o")

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
print(rag_chain.invoke("What is RAG?"))
```

**150. Explain your project architecture using LangChain.**
```text
Project Architecture Example (RAG + Agentic App):
1. Data Ingestion: Scheduled jobs use `WebBaseLoader` and `PyPDFLoader` to scrape documentation.
2. Processing: `RecursiveCharacterTextSplitter` chunks the text (size 1000, overlap 150).
3. Embedding & Storage: `OpenAIEmbeddings` convert text to vectors, stored in a managed `Pinecone` vector DB.
4. Core Logic: A `create_tool_calling_agent` acts as the brain, equipped with:
   - A retriever tool connected to Pinecone for knowledge retrieval.
   - A Jira API custom tool for creating support tickets.
5. Deployment: The agent is served via `LangServe` as a REST API, consumed by a React frontend.
6. Monitoring: `LangSmith` traces all LLM calls to monitor token usage, latency, and retrieval accuracy.
```
