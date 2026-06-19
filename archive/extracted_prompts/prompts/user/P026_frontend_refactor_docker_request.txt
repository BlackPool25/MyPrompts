SOURCE: Improving Testing Prompt.pdf, Pages 60-61
TYPE: User Prompt
================================================================================

Give me an agent prompt who will fix this up and refactor the frontend based on the designs I give 
it
  5. Remaining Risks
  
  - qwen3:8b entity extraction quality: The model's <think> tags cause LightRAG's delimiter parser to 
fail on ~2/3 of chunks. Only 6 entities were extracted from the Telegram ToS. Consider using 
qwen3:8b with num_ctx tuning or switching to a model
  without chain-of-thought output for indexing. This is a model behavior issue, not a code bug.
  - Frontend not updated: The frontend's useAppStore.ts and Chat.tsx still use the old API shape (no 
company_id). The frontend needs to be updated to pass company_id in all requests.
  - In-memory indexing_status is lost on restart: After a restart, in-flight status is gone. Documents 
that were indexing when the server restarted will show their persisted status from disk (which may 
be indexing if they didn't finish). This is
  pre-existing behavior.
And also tell it to turn on thinking for the model while infererence. And make sure all this is 
configurable in the .env and also tell it to containerise the entire architecture's backend and 
frontend seperately and allow me to run with a simple docker compose up on any pc with all the 
configs. 
Give it proper frontend thinking and world class thinking and patterns professional web designers 
and implementers follow for making consistent and well make websites. And also tell it to connect 
to neo4j. I will it give my client secret and api key. Give it proper design patterns. 
This was the report the previous agent gave me after it's task
