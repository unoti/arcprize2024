# ARC Prize
Experiments related to the ARC AGI prize for reasoning on problems the agent has never seen.

![challenge samples](doc/img/2024-06-25-11-48-13.png)

## Challenge description
> The [Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) benchmark](https://arcprize.org/) measures an AI system's ability to efficiently learn new skills. Humans easily score 85% in ARC, whereas the best AI systems only score 34%. The ARC Prize competition encourages researchers to explore ideas beyond LLMs, which depend heavily on large datasets and struggle with novel problems.

> The objective of this competition is to create an algorithm that is capable of solving abstract reasoning tasks. Critically, these are novel tasks: tasks that the algorithm has never seen before. Hence, simply memorizing a set of reasoning templates will not suffice.
![challenge flood fill sample](doc/img/2024-07-15-15-51-27.png)


## Goals
Others have tried LLM's on the arc-prize and obtained poor results as described in [GPT4 ARC Prize Evaluation Paper](https://openreview.net/pdf?id=3rGT5OkzpC).  

> "LLMs like Gemini or ChatGPT [don't work] because they're basically frozen at inference time. They're not actually learning anything." - François Chollet

We think that there are approaches which can make the above statement false and overcome those limitations.  In this repo we will explore some ideas and see what they can do.  Briefly the ideas involve overcoming some of the limitations of LLMs using external storage, loops, [Reflexion](https://arxiv.org/pdf/2303.11366), [chain of thought self-consistency (CoT-SC)](https://arxiv.org/abs/2203.11171), and other ideas.

Although LLM's are frozen at inference time, there are ways to overcome this limitation.  One way that others are working on is data augmentation and fine-tuning at inference time, Test Time Training (TTT).  Another way is Reflexion.

## Brief summary of ideas
* Create a hypothesis on how to solve the task
* Evaluate that hypothesis against the training items, but hold out one of the training items to use for a mini internal evaluation
* If we fail on the task against the held out item, use reflexion to give self-advice. Try the held out item again, and iterate on this up to N times until we succeed.
* If we don't succeed, hold this one out for deeper analysis later.  We will use deeper thinking strategies on these at the end using our remaining processing time. (Note there is a 12 hour processing time limit.)

In the docs folder we have [an example GPT transcript embodying the above ideas](doc/sample-transcript.md).

* Use CoT-SC to run trials multiple times to ensure accuracy.
* Take advantage of the fact that we can try an item up to 3 times.  We can use the additional information we gain from having a failed hypothesis to our advantage.
* We can incorpoate tools to do analysis on the items, for example doing flood fills, copying blocks of data from the input to the output, and other tedious/error prone operations.
* We can do image analysis to gain additional insights during the deeper analysis phase when needed.

## Papers
* [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629)
* [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/pdf/2303.11366)
* Cot-SC: [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)

## Resources
* [ironbar/arc24 repo](https://github.com/ironbar/arc24) Some images came from here
* [Challenge dataset](https://github.com/fchollet/ARC-AGI/tree/master)
* [ARC Prize 2024 Kaggle challenge](https://www.kaggle.com/competitions/arc-prize-2024/overview)
* [ARC Prize Kaggle Leaderboard](https://www.kaggle.com/competitions/arc-prize-2024/leaderboard)
* [Kaggle Arc Prize Discussion Threads](https://www.kaggle.com/competitions/arc-prize-2024/discussion/545671)
* [GPT4 ARC Prize Evaluation Paper](https://openreview.net/pdf?id=3rGT5OkzpC)

## Getting started
### Installation
We used Python 3.9.13 for convenience because that's what we had installed for other projects, but we expect that later versions of Python should work fine.

From the root directory of the project:
```
python -m venv venv
venv\scripts\activate
pip install -e .
```

## Work plan
1. Foundations and infrastructure. Set up libraries and structure.
    * Goal: can run a series of LLM calls directed by code and review the session.
    * Doing LLM calls
    * Storing sessions
    * Clean abstractions
2. Baseline Business Logic
    * Goal: Establish baseline business logic and do an evaluation of the first 10 or so training items.
    * Code to evaluate a single training sample
    * Code to run this across N samples and store the results.
    * CLI program to run it
3. Enhancements
    * Incorporate ideas from the backlog, such as a curated list of strategies, reflexions, and external tools