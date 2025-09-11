# AI Application Developer Labs - Curriculum

> **🏠 [README.md](README.md)** - Quick start and setup instructions

# Course Details
This is an upskilling track at AmaliTech with weekly sessions and hands-on labs building incrementally over 10 weeks. It focuses on practical development skills for production AI applications.

Successful completion will equip learners with foundational skills as **AI Engineers**.
## Resources
- Registration: [Signup link](https://forms.office.com/e/kHpdHcQJev)
- Feedback (after each session): [Survey link](https://forms.office.com/e/kYuGZHBdh5)
- Lab repository: [GitHub link](https://github.com/Amali-Tech/ai-application-developer-labs)
- Primary learning resource: [OpenAI Platform Docs - Overview](https://platform.openai.com/docs/overview)
- *Optional* resources, especially for those with knowledge in other fields:
	- Data science: [HuggingFace LLM Course](https://huggingface.co/learn/llm-course/chapter1/1)
	- AWS: [Claude in Amazon Bedrock](https://anthropic.skilljar.com/claude-in-amazon-bedrock)
	- Software architecture: [Patterns for LLM Systems](https://eugeneyan.com/writing/llm-patterns/)
	- Cybersecurity: [OWASP LLM Top 10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
	- Frontend: [Vercel AI SDK](https://ai-sdk.dev/docs/ai-sdk-ui)
	- UI/UX: [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/haxtoolkit/ai-guidelines/)
	- QA: [Your AI product needs evals](https://hamel.dev/blog/posts/evals/)
## Structure
- **Cadence**: Weekly 2h live session plus minimum 6h self study
- **Session flow**: instructor walkthrough, rotating learner demos, open discussion
- **Coordination**: Slack channel, all online sessions recorded
- **Assessment criteria**:
	- **Lab Completion (60%)**: Working code meeting weekly specifications
	- **Dodokpo Assessment (20%)**: Online test covering core concepts
	- **Participation (20%)**: weekly session participation and slack engagement
## Prerequisites
- Junior L1 to associate Y2 (any specialisation or chapter)
- Comfortable with REST, JSON, CLI.
- Preinstalled on machine:
	- Python 3.10+ or Node 20+
	- git (v2.48.0+)
	- Official OpenAI SDK: [Libraries](https://platform.openai.com/docs/libraries).
## Expectations
- Study all weekly docs and pre-reads for the next session
- Attend and participate in all live sessions
- Commit frequently to git, demo weekly labs
- Share knowledge in Slack (*#ai-application-development*)
	- One helpful post per week that includes a code snippet or a reading summary
	- Comments on posts that provides additional feedback or reflection
- Participate and contribute with integrity
	- All labs are to be completed individually
	- AI assistance is allowed via [approved tools](https://amali-tech.atlassian.net/wiki/spaces/AH/pages/1777008661/AI+Tools+and+Access), but prompts must be captured either as code comments or in documentation
	- You must be able to explain any non-trivial code in your labs
## Schedule

| Week | Name | Areas of focus | Pre-read | Lab (minimum) |
|------|------|----------------|----------|---------------|
| [Week 1](https://amalitech-my.sharepoint.com/:v:/p/nachiket_apte/EWlzSIp3OxZKt-cLraZ62JoBDZ4bswgSxkGeKv6-3CyuOQ?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D&e=54lua1) | Foundations with Completions + Responses API | - [How LLMs work](https://platform.openai.com/docs/concepts)<br>- [OpenAI quick-start](https://platform.openai.com/docs/quickstart) | [Karpathy: 1 hr intro to LLMs](https://www.youtube.com/watch?v=zjkBMFhNj_g) | Build a basic Q&A app that answers questions |
| Week 2 | Streaming response and conversations | - [Streaming API](https://platform.openai.com/docs/guides/streaming-responses)<br>- [Managing state and conversations](https://platform.openai.com/docs/guides/conversation-state)<br>- [Background mode](https://platform.openai.com/docs/guides/background) | - | Add conversation memory and streaming so users can ask follow-up questions naturally |
| Week 3 | Prompting and reasoning | - [Prompt engineering](https://platform.openai.com/docs/guides/prompt-engineering)<br>- [Reasoning best practices](https://platform.openai.com/docs/guides/reasoning-best-practices) | [Anthropic AI Fluency: Framework & Foundations](https://anthropic.skilljar.com/ai-fluency-framework-foundations) | Create a prompt template system for different query types, add reasoning controls |
| Week 4 | Function calling and structured outputs | - [Web search tool](https://platform.openai.com/docs/guides/tools-web-search)<br>- [Structured outputs](https://platform.openai.com/docs/guides/structured-outputs) | - | Extend the app to call a tool (ex: web search) when needed and return validated JSON that matches a schema |
| Week 5 | Responses API and tool use | - [Code Interpreter tool](https://platform.openai.com/docs/guides/tools-code-interpreter) (demo only)<br>- [Remote MCP](https://platform.openai.com/docs/guides/tools-remote-mcp) | [Model Context Protocol overview](https://modelcontextprotocol.io/) | Implement one remote tool and call it through function calling. Log tool latency and failures. Note: code interpreter not part of core labs |
| Week 6 | Retrieval-Augmented Generation | - [File search tool](https://platform.openai.com/docs/guides/tools-file-search)<br>- [Embeddings](https://platform.openai.com/docs/guides/embeddings)<br>- [Retrieval guide](https://platform.openai.com/docs/guides/retrieval) | [RAG introduction](https://www.pinecone.io/learn/retrieval-augmented-generation/) | Implement a narrow RAG flow that answers questions over your docs |
| Week 7 | Model portability and vendor choice | - Google Gemini<br>- [Self-hosting with Ollama](https://ollama.readthedocs.io/en/)<br>- [Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html) | [Gemini quick-start](https://ai.google.dev/gemini-api/docs/quickstart) | Add fallback to alternative models (Gemini or local ollama model) |
| Week 8 | Quality Assurance at scale | - [Evals guide](https://platform.openai.com/docs/guides/evals) | [Evaluating LLMs](https://medium.com/data-science-at-microsoft/evaluating-llm-systems-metrics-challenges-and-best-practices-664ac25be7e5); [SWE-Bench](https://www.swebench.com/) | Create test suite validating accuracy on common questions and edge cases (at least 10 test cases) |
| Week 9 | Production ops | - [Prompt caching](https://platform.openai.com/docs/guides/prompt-caching)<br>- [Batch API](https://platform.openai.com/docs/guides/batch)<br>- [Flex processing](https://platform.openai.com/docs/guides/flex-processing)<br>- [Safety best practices](https://platform.openai.com/docs/guides/safety-best-practices) | - | Add caching for repeated prompts. Implement one batch or flex workflow. Add tracing / safety checks. Write a 1 page incident playbook |
| Week 10 | Wrap up | Summarise learnings; clarify outstanding topics; lab demos; assessment preparation | - | Package everything as a shareable tool. Include architecture diagram, eval results, and runbook |
### Ongoing topics
The following cross-functional topics will be integrated throughout the course:
- **Cost optimisation**: Token usage monitoring, model selection, caching
- **Error handling**: Rate limits, retries, timeouts, graceful degradation
- **Security**: API key management, input sanitisation, prompt injection
- **Observability**: Logging, metrics, debugging
- **Deployment**: Environment configuration, API design patterns, containerisation

---
## Onboarding instructions (for instructors)
1. Ensure learner is [signed up](https://forms.office.com/e/kHpdHcQJev)
2. Add learner to [Slack channel](https://amalitech-workspace.slack.com/archives/C09BHH7FQ48)
3. Add learner to [GitHub team](https://github.com/orgs/Amali-Tech/teams/ai-application-developer-labs)
4. Invite learner to weekly meeting in Outlook.
5. Issue an [OpenAI API key](https://platform.openai.com/settings/proj_qDHGPSZUpKpdbTRuW8QbFXv4/api-keys).
