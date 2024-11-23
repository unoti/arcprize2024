# ARC Prize
Experiments related to the ARC AGI prize for reasoning on problems the agent has never seen.

![challenge samples](doc\img\2024-06-25-11-48-13.png)

## Challenge description
![challenge flood fill sample](doc\img\2024-07-15-15-51-27.png)
> The [Abstraction and Reasoning Corpus for Artificial General Intelligence (ARC-AGI) benchmark](https://arcprize.org/) measures an AI system's ability to efficiently learn new skills. Humans easily score 85% in ARC, whereas the best AI systems only score 34%. The ARC Prize competition encourages researchers to explore ideas beyond LLMs, which depend heavily on large datasets and struggle with novel problems.

> The objective of this competition is to create an algorithm that is capable of solving abstract reasoning tasks. Critically, these are novel tasks: tasks that the algorithm has never seen before. Hence, simply memorizing a set of reasoning templates will not suffice.

## Goals
Others have tried LLM's on the arc-prize and obtained poor results as described in [GPT4 ARC Prize Evaluation Paper](https://openreview.net/pdf?id=3rGT5OkzpC).  

In this repo we will explore some ideas and see what they can do.  Briefly the ideas involve overcoming some of the limitations of LLMs using external storage, loops, [Reflexion](https://arxiv.org/pdf/2303.11366), [chain of thought self-consistency (CoT-SC)](https://arxiv.org/abs/2203.11171), and other ideas.

> "LLMs like Gemini or ChatGPT [don't work] because they're basically frozen at inference time. They're not actually learning anything." - François Chollet

Although LLM's are frozen at inference time, there are ways to overcome this limitation.  One way that others are working on is data augmentation and fine-tuning at inference time, Test Time Training (TTT).  Another way is Reflexion.

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