

# Session 1: Dense Vector Retrieval

### [Quicklinks]()


| 📰 Module Sheet                                                                  | ⏺️ Recording                                                                                                                                           | 🖼️ Slides                                             | 👨‍💻 Repo    | 📝 Homework                                                 | 📁 Feedback                                         |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| [Dense Vector Retrieval](../00_Docs/Modules/01_Dense_Vector_Retrieval/README.md) | [Recording!](https://us02web.zoom.us/rec/share/sHWvo0Nd1aI0SEhKecOLEX9kFGVJJAdYfsKiuTmm8t85W48Z2lnjpnzTy8jAd8R5.PwuqibGwAZhvDd8c) passcode: `C62n^@Q!` | [Session 1 Slides](https://canva.link/htfqf8i39yejyhn) | You are here! | [Session 1 Assignment](https://forms.gle/Z9qskfVaAvPjn6gz8) | [Feedback 6/2](https://forms.gle/21a2uoL9DVZPwgJP6) |


## 🏗️ How AIM Does Assignments

> 📅 **Assignments will always be released to students as live class begins.** We will never release assignments early.

Each assignment will have a few of the following categories of exercises:

- ❓ **Questions** - these will be questions that you will be expected to gather the answer to. These can appear as general questions, or questions meant to spark a discussion in your breakout rooms.
- 🏗️ **Activities** - these will be work or coding activities meant to reinforce specific concepts or theory components.
- 🚧 **Advanced Builds (optional)** - Take on a challenge. These builds require you to create something with minimal guidance outside of the documentation.

## Main Assignment

In this assignment, you will build a vector RAG application using LangChain v1, OpenAI embeddings, and Qdrant.

The main notebook is:

```text
01_Cat_Health_Vector_RAG_LangChain_Qdrant.ipynb
```

The notebook uses the bundled cat health guideline PDF in `data/cat_health_guidelines.pdf`.

### Setup

From this folder, install the environment with uv:

```bash
uv sync
```

Then open the notebook in Cursor or VS Code and select the Python/Jupyter environment created by uv.

You will also need an OpenAI API key available when running the notebook.

---

## 🏗️ Activity #1: Embedding Similarity

Run the embedding similarity primer in the notebook.

You will compare embeddings for terms like:

- `king`
- `queen`
- `banana`
- `cat`
- `veterinarian`
- `cat health guidelines`

#### ❓Question #1

Why is cosine similarity useful for dense vector retrieval?

##### ✅ Answer:

Cosine similarity measures how aligned two embedding vectors are by direction, ignoring their length. It is useful for dense vector retrieval because it reliably ranks semantically related text above unrelated text. In the primer, king and queen (0.591) and cat and cat health guidelines (0.496) scored well above king and banana (0.310), and an identical pair like king and king scored 1.000. That ranking is what lets us embed a query and pull the chunks whose vectors point in the most similar direction. The absolute values are model dependent and not meaningful on their own, so they are best used for ranking rather than as a fixed measure of meaning.

---

## 🏗️ Activity #2: Build the Vector RAG Pipeline

Run the notebook sections that:

1. Load the PDF into LangChain `Document` objects
2. Split the document into chunks
3. Embed the chunks
4. Store the chunk embeddings in in-memory Qdrant
5. Retrieve relevant chunks with similarity scores
6. Generate an answer grounded in retrieved context

#### ❓Question #2

Why is metadata important for a RAG application?

##### ✅ Answer:

Metadata matters because each chunk carries information about where it came from, not just the text itself. In the cat health PDF, every page came with a source filename, a page number, and a total page count, plus PDF details like title and author, along with the document_type tag we added in code. That extra information is useful in a few ways. It lets us cite sources, so when the model answers we can point back to the exact page the answer came from instead of asking the user to trust a black box. It lets us filter what we search, for example restricting a search to chunks where document_type is cat_health_guideline if we later mix in other documents. And it helps us trust and debug results, because we can see which page a retrieved chunk came from and go check it. So metadata is what turns a loose pile of text into pieces we can trace, filter, and cite.

#### ❓Question #3

What tradeoff do we make when choosing chunk size and chunk overlap?

##### ✅ Answer:

Chunk size and chunk overlap trade off precision against context, not speed. Retrieval always returns a fixed number of chunks (k) no matter how many chunks exist in total, so having more chunks does not make the model read more. What changes is how good each chunk is as a match.

Larger chunks carry more context, so a single chunk is more likely to contain a complete answer and there are fewer boundary problems. The cost is that each chunk's vector becomes a blurry average of several topics, so it matches a specific query less precisely, and we feed more text, including more unrelated text, into the prompt, which adds cost and noise. Taken to the extreme, making the whole PDF one chunk would defeat retrieval entirely, because there would be one vector that matches every query equally and no way to locate the relevant passage.

Smaller chunks are sharply focused, so each vector matches a query more precisely. The cost is that a chunk may be too small to hold a full answer, so the answer gets split across several chunks and one retrieved chunk may lack enough surrounding context, which can push us to retrieve more chunks to compensate.

Chunk overlap protects ideas that fall on a boundary. More overlap means neighboring chunks share more text, so an idea split across the seam still appears whole in at least one chunk. The cost is more chunks to embed and store and some duplicated text in results.

#### ❓Question #4

What does a similarity score help you understand, and what does it not prove by itself?

##### ✅ Answer:

A similarity score tells you how close a chunk is to the query in meaning, measured by cosine similarity on the same embedding map. It is useful for ranking, so the chunk with the highest score is the system's best guess at the most related passage. For the query about signs a cat should see a veterinarian, Source 1 scored highest at 0.584.

What it does not prove: it does not prove the chunk actually contains the answer, because a high score only means the passage is about a similar topic, not that the specific fact is present, so judging that still requires reading the chunk and the generated answer. It is also a relative ranking, not an absolute measure of truth or confidence, so 0.584 does not mean 58 percent correct.

---

## 🏗️ Activity #3: Vibe Check Retrieval Quality

Run the notebook's vibe check queries and inspect both:

- The retrieved context
- The generated answer

#### ❓Question #5

For the vibe check queries, did the retrieved context seem relevant before generation? Why or why not?

##### ✅ Answer:

Based on the code as written, we do not actually see the retrieved context for the vibe check questions, since the cell only prints the generated answer. We could add code to display the retrieved chunks for each question if we wanted to inspect it directly. That said, based on the answers that were generated, the context seemed relevant, because the assistant did a good job answering each question and cited specific sources for its claims. The off-topic question about filing taxes is a useful contrast, since no relevant context could be retrieved and the assistant correctly said it did not have enough information instead of making something up.

---

## 🏗️ Activity #4: Tune Retrieval

Improve retrieval quality by changing one or more of:

- Chunk size
- Chunk overlap
- Retrieval `k`
- Query wording

Document what changed and whether retrieval improved.

##### Settings Changed:

- Chunk size: 1000 to 500 characters
- Chunk overlap: 200 to 100 characters
- Retrieval k and the query wording were kept the same, so only chunk size and overlap changed

##### Results:

1. Halving the chunk size roughly doubled the number of chunks, from 135 to 263.
2. The smaller chunks surfaced more specific and more varied warning signs for the same query, for example a passage tying litter box changes to urinary disease, constipation, or diabetes. That added specificity was a real gain.
3. The smaller chunks were truncated too aggressively, which cost more than the specificity gained. One retrieved chunk began with "is noted by the owner, the kitten should be evaluated for underlying conditions," with the actual sign cut off the front, so the most important part of the passage was missing. Overall the smaller chunks returned less usable context, so for this query the original 1000 / 200 setting gave better retrieval.

---

## Optional Deep Dive: RAG From Scratch

If you want to look underneath the library abstractions, run the optional reference notebook:

```text
02_Cat_Health_Vector_RAG_From_Scratch.ipynb
```

It builds the same retrieval pipeline again with only:

- `pypdf` for extracting text from the PDF
- Python standard-library HTTP requests for calling OpenAI
- Handcrafted document, chunking, embedding, similarity-search, vector-store, and generation primitives

This notebook is a reference walkthrough, not an additional assignment. Its purpose is to make the responsibilities hidden by LangChain, Qdrant, and provider SDKs visible.

---

## Submitting Your Homework

### Main Assignment

Follow these steps to prepare and submit your homework:

1. Pull the latest updates from upstream into the main branch of your AIE9 repo:

```bash
git checkout main
git pull upstream main
git push origin main
```

1. Start Cursor from the `01_Dense_Vector_Retrieval` folder.
2. Complete the notebook.
3. Answer the questions in this `README.md`.
4. Add, commit, and push your modified work to your origin repository.

When submitting your homework, provide the GitHub URL to your AIE9 repo.