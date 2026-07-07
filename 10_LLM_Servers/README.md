

## # Session 10: LLM Servers


| 📰 Session Sheet                                                                                                                            | ⏺️ Recording                                                                                                                                           | 🖼️ Slides                                              | 👨‍💻 Repo    | 📝 Homework                                                  | 📁 Feedback                                         |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------- | ------------- | ------------------------------------------------------------ | --------------------------------------------------- |
| [Session 10: LLM Servers](https://github.com/AI-Maker-Space/The-AI-Engineering-Certification-v1.0/tree/main/00_Docs/Modules/10_LLM_Servers) | [Recording!](https://us02web.zoom.us/rec/share/zXd6__uO2RwCmJUmNyGKY01sbwYjjrkpDDNPbfK_Es0MANaqRpFOqqYX4sEVYY1d.gJwTZk1729siXnjj) passcode: `^1$@$R@.` | [Session 10 Slides](https://canva.link/953giejzt5igxvw) | You are here! | [Session 10 Assignment](https://forms.gle/hKxFnEM8U16fCCnG8) | [Feedback 7/2](https://forms.gle/uj2QvYjHfHKFFQ8a6) |


**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU'RE FINISHED YOUR ASSIGNMENT !!!⚠️**

# Build 🏗️

In today's assignment, we'll be creating Fireworks AI endpoints, and then building a RAG application.

- 🤝 Breakout Room #1
  - Set-up Open Source Endpoint (Instructions [here](./ENDPOINT_SETUP.md)) ((This process may take 15-20min.))
  - Test Endpoint and Embeddings with the `endpoint_slammer.ipynb` notebook.
- 🤝 Breakout Room #2
  - Use the Open Source Endpoints to build a RAG LangGraph application

# Ship 🚢

The completed notebook and your RAG app/notebook!

### Deliverables

- A short Loom of either:
  - the notebook and the RAG application you built for the Main Homework Assignment; or
  - the notebook you created for the Advanced Build

# Share 🚀

Make a social media post about your final application!

### Deliverables

- Make a post on any social media platform about what you built!

Here's a template to get you started:

```
🚀 Exciting News! 🚀

I am thrilled to announce that I have just built and shipped a RAG application powered by open-source endpoints! 🎉🤖

🔍 Three Key Takeaways:
1️⃣
2️⃣
3️⃣

Let's continue pushing the boundaries of what's possible in the world of AI and question-answering. Here's to many more innovations! 🚀
Shout out to @AIMakerspace !

#LangChain #QuestionAnswering #RetrievalAugmented #Innovation #AI #TechMilestone

Feel free to reach out if you're curious or would like to collaborate on similar projects! 🤝🔥
```

# Submitting You Homework

## Main Homework Assignment

Follow these steps to prepare and submit your homework assignment:

1. Follow the instructions in `ENDPOINT_SETUP.md`
2. Replace both `model` values in `endpoint_slammer.ipynb` with the `gpt-oss` endpoint you created in Step 1
3. Run the code cells in `endpoint_slammer.ipynb`
4. Respond to the questions in the section below
5. Build a sample RAG
6. Record a Loom video reviewing what you have learned from this session

**⚠️!!! PLEASE BE SURE TO SHUTDOWN YOUR DEDICATED ENDPOINT ON FIREWORKS AI WHEN YOU HAVE FINISHED YOUR ASSIGNMENT !!!⚠️**

## Questions

### ❓ Question #1:

What is the difference between serverless and dedicated endpoints?

#### ✅ Answer:

Serverless and dedicated are two ways to run a model behind an endpoint. With serverless you pay by usage. The provider spins the model up when you send a request, runs it, and spins it back down when you are done, so there is no server sitting there that belongs to you. You share capacity with other people, which keeps it cheap and makes it a good fit for light or spiky traffic. With a dedicated endpoint you rent a server that stays running and is yours alone. It can take a minute to set up, and the first request after it has been idle can be slow while it warms back up, but once it is going you get consistent speed because nobody else is using it. You pay by the hour whether or not you are sending requests, so it makes sense when you have steady heavy usage or a big batch job like running evaluations, where you want to hit it hard for a flat cost.

### ❓ Question #2:

Why is it important to consider token throughput and latency when choosing an LLM for user-facing applications?

#### ✅ Answer:

Throughput and latency matter because they decide how the app actually feels to the person using it. Latency is how long the user waits before the answer starts showing up, and if that wait is long the app feels broken and people give up and leave. Throughput is how many tokens per second the model can produce and how many users it can handle at the same time. On a single GPU the throughput drops as more people use it at once, so an app that feels fast for a few users can slow to a crawl once a lot of people are on it. This is why you cannot just pick the biggest, smartest model. A large model that takes a minute to answer can be a worse experience than a smaller model that responds right away, so for anything a real person is waiting on you have to balance quality against speed and how many users you need to serve.

## Activity 1: RAGAS Evaluation with Cost Analysis

Use RAGAS to evaluate your open-source Fireworks AI powered RAG app against an OpenAI `gpt-4.1-mini` powered equivalent. Compare retrieval quality, answer faithfulness, and end-to-end accuracy across both providers.

Additionally, instrument both pipelines with **LangSmith** to capture token usage and cost per query. Use LangSmith's tracing and cost dashboards to compare the total cost of running each provider at scale. Include your evaluation results, cost breakdown, and analysis in your Loom video.

## Advanced Activity: Local Models

Swap out the Fireworks AI endpoints for **locally-running open-source models** using [Ollama](https://ollama.com/) or another local inference server of your choice. Run both your embedding model and your chat model locally, and rebuild the RAG pipeline on top of them.

- Compare quality and latency between the local setup and your Fireworks AI hosted endpoint.
- Reflect: what are the trade-offs of local models vs. managed endpoints in a production setting?

Include your findings and a demo in your Loom video.

### Results

My implementation is in `activity1_ragas_eval.ipynb`.

Setup: I built two RAG pipelines over the same feline-health PDF with the same prompt, chunking, and retrieval settings, so the only difference is the models. The open-source stack uses Fireworks gpt-oss-20b for generation and qwen3-embedding-8b for retrieval. The OpenAI stack uses gpt-4.1-mini for generation and text-embedding-3-small for retrieval. I scored both with RAGAS using a single gpt-4.1-mini judge, and I traced every call to LangSmith to capture token usage and cost.

Quality (RAGAS, 0 to 1, higher is better):


| Metric                   | Fireworks (open-source) | OpenAI (gpt-4.1-mini) |
| ------------------------ | ----------------------- | --------------------- |
| Context precision        | 0.72                    | 0.92                  |
| Context recall           | 1.00                    | 1.00                  |
| Faithfulness             | 0.80                    | 1.00                  |
| Answer relevancy         | 0.74                    | 0.76                  |
| Factual correctness (F1) | 0.49                    | 0.54                  |


Cost:


|                     | Fireworks (open-source) | OpenAI (gpt-4.1-mini) |
| ------------------- | ----------------------- | --------------------- |
| Cost per query      | $0.0003                 | $0.0011               |
| Cost per 1M queries | $280.82                 | $1,128.32             |


Findings: the OpenAI stack scored higher on most quality metrics or tied, and it clearly won on faithfulness and context precision. The open-source stack was more conservative and answered "I don't know" on one question when its retrieval missed the exact chunk, which keeps it honest but lowers its accuracy. On cost the open-source stack was about four times cheaper per query, and that gap grows at scale. The takeaway is a quality versus cost tradeoff. The closed model is a bit more accurate, but the open-source stack is much cheaper and can also be run privately, so for a high-volume or privacy-sensitive app it is a reasonable choice even at slightly lower accuracy. All runs are traced in LangSmith under the session10-ragas-eval project.