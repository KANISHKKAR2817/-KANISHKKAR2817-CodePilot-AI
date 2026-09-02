import os
import json
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

app = FastAPI(
    title=CodePilot AI - Gemini Orchestration Gateway,
    description=Real-time AI tutoring, debugging, test generation, and technical interview engine,
    version=1.0.0
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[*],
    allow_credentials=True,
    allow_methods=[*],
    allow_headers=[*],
)

GEMINI_API_KEY = os.getenv(GEMINI_API_KEY, ")
client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

# ----------------- SCHEMAS -----------------

class CodeExplainRequest(BaseModel):
 language: str
 code: str
 skill_level: str = intermediate

class CodeExplainResponse(BaseModel):
 summary: str
 invariants: List[str]
 mermaid_diagram: str
 time_complexity: str
 space_complexity: str

class DebugRequest(BaseModel):
 language: str
 code: str
 error_type: Optional[str] = None
 error_message: Optional[str] = None
 user_skill: str = beginner

class DebugResponse(BaseModel):
 root_cause: str
 explanation_for_learner: str
 fix_diff: str
 corrected_code: str
 prevention_strategy: str

class SocraticTutorRequest(BaseModel):
 topic: str
 language: str
 student_query: str
 experience_level: str = beginner

class TestGenRequest(BaseModel):
 language: str
 code: str
 num_edge_cases: int = 3

class TestCase(BaseModel):
 description: str
 input_data: str
 expected_output: str
 is_edge_case: bool

class TestGenResponse(BaseModel):
 test_cases: List[TestCase]

# ----------------- ENDPOINTS -----------------

@app.get(/health)
def health():
 return {status: healthy, model: gemini-2.0-flash / gemini-2.0-pro}

@app.post(/api/ai/explain, response_model=CodeExplainResponse)
async def explain_code(req: CodeExplainRequest):
 if not client:
 return CodeExplainResponse(
 summary=This LRU Cache maintains (1)$ fast lookups using a Hash Map and dynamic least-recently-used evictions via a Doubly Linked List.,
 invariants=[Sentinel Dummy Nodes (Head & Tail) avoid null-pointer edge cases, Every get/put operation repositions the node to the tail],
 mermaid_diagram=graph LR\n  subgraph HashMap\n    K1[Key 1] --> N1\n  end\n  subgraph DLL\n    Head <--> N1 <--> Tail\n  end,
 time_complexity=O(1) amortized for all operations,
 space_complexity=O(Capacity) auxiliary space
 )
 
 prompt = f"
 You are CodePilot AI Pedagogical Tutor. Analyze the following {req.language} code for a {req.skill_level} learner:
 `{req.language}
 {req.code}
 `
 Provide a structured pedagogical explanation, including algorithmic invariants and a valid Mermaid flowchart syntax.
 "
 
 response = client.models.generate_content(
 model='gemini-2.0-flash',
 contents=prompt,
 config=types.GenerateContentConfig(
 response_mime_type=application/json,
 response_schema=CodeExplainResponse
 )
 )
 return json.loads(response.text)

@app.post(/api/ai/debug, response_model=DebugResponse)
async def debug_code(req: DebugRequest):
 if not client:
 return DebugResponse(
 root_cause=Node was not deleted before updating existing hash table key.,
 explanation_for_learner=When putting an existing key, the old node must be unlinked from the list to avoid duplicate node references.,
 fix_diff=@@ -18,2 +18,4 @@\n- self.cache[key] = Node(key, val)\n+ if key in self.cache: self._remove(self.cache[key])\n+ self.cache[key] = Node(key, val),
 corrected_code=req.code,
 prevention_strategy=Decouple destruction of stale memory references from the allocation of updated state.
 )

 prompt = f"
 Debug this {req.language} code:
 `{req.language}
 {req.code}
 `
 Error details: {req.error_type}: {req.error_message}
 Target audience: {req.user_skill} developer. Output a unified diff patch and preventive tips.
 "
 
 response = client.models.generate_content(
 model='gemini-2.0-flash',
 contents=prompt,
 config=types.GenerateContentConfig(
 response_mime_type=application/json,
 response_schema=DebugResponse
 )
 )
 return json.loads(response.text)

@app.post(/api/ai/generate-tests, response_model=TestGenResponse)
async def generate_tests(req: TestGenRequest):
 if not client:
 return TestGenResponse(
 test_cases=[
 TestCase(description=Capacity 1 boundary eviction, input_data=capacity=1, put(1,1), put(2,2), get(1), expected_output=-1, is_edge_case=True),
 TestCase(description=Duplicate key value update, input_data=put(2,1), put(2,2), get(2), expected_output=2, is_edge_case=True),
 TestCase(description=Large sequential stress test, input_data=put 1000 items into capacity 10, expected_output=evict 990 items, is_edge_case=False)
 ]
 )
 
 prompt = fGenerate {req.num_edge_cases} rigorous test cases (including boundary edge cases, nulls, cycles) for this {req.language} code:\n{req.code}
 response = client.models.generate_content(
 model='gemini-2.0-flash',
 contents=prompt,
 config=types.GenerateContentConfig(
 response_mime_type=application/json,
 response_schema=TestGenResponse
 )
 )
 return json.loads(response.text)

if __name__ == __main__:
 import uvicorn
 uvicorn.run(app, host=0.0.0.0, port=8000)
