---
name: retro
description: "Facilitate a structured sprint retrospective — what went well, what didn't, and prioritized action items with owners and deadlines. Use when running a retrospective, reflecting on a sprint, creating action items from team feedback, or learning how to run effective retros."
---

## Sprint Retrospective Facilitator

Run a structured retrospective that surfaces insights and produces actionable improvements.

### Context

You are facilitating a retrospective for **the subject described in the conversation**.

If the user provides files (sprint data, velocity charts, team feedback, or previous retro notes), read them first.

### Instructions

1. **Choose a retro format** based on context (or let the user pick):

   **Format A — Start / Stop / Continue**:
   - **Start**: What should we begin doing?
   - **Stop**: What should we stop doing?
   - **Continue**: What's working well that we should keep?

   **Format B — 4Ls (Liked / Learned / Lacked / Longed For)**:
   - **Liked**: What did the team enjoy?
   - **Learned**: What new knowledge was gained?
   - **Lacked**: What was missing?
   - **Longed For**: What do we wish we had?

   **Format C — Sailboat**:
   - **Wind (propels us)**: What's driving us forward?
   - **Anchor (holds us back)**: What's slowing us down?
   - **Rocks (risks)**: What dangers lie ahead?
   - **Island (goal)**: Where are we trying to get to?

2. **If the user provides raw feedback** (e.g., sticky notes, survey responses, Slack messages):
   - Group similar items into themes
   - Identify the most frequently mentioned topics
   - Note sentiment patterns (frustration, energy, confusion)

   If there is no input yet, collect it anonymously before the discussion, so the first or most senior voice doesn't set the agenda: a word cloud or a 1–5 rating for the mood, and written items others can upvote for what went well and what didn't. The live-polls and live-qa skills cover both.

3. **Analyze the sprint performance**:
   - Sprint goal: achieved or not?
   - Velocity vs. commitment (over-committed? under-committed?)
   - Blockers encountered and how they were resolved
   - Collaboration patterns (what worked, what didn't)

4. **Generate prioritized action items**:

   | Priority | Action Item | Owner | Deadline | Success Metric |
   |---|---|---|---|---|
   | 1 | [Specific, actionable improvement] | [Name/Role] | [Date] | [How we'll know it worked] |

   - Limit to 2-3 action items (more won't get done)
   - Each must be specific, assignable, and measurable
   - Reference previous retro actions if available — were they completed?

5. **Create the retro summary**:
   ```
   ## Sprint [X] Retrospective — [Date]

   ### Sprint Performance
   - Goal: [Achieved / Partially / Missed]
   - Committed: [X pts] | Completed: [Y pts]

   ### Key Themes
   1. [Theme] — [summary]

   ### Action Items
   1. [Action] — [Owner] — [By date]

   ### Carry-over from Last Retro
   - [Previous action] — [Status: Done / In Progress / Not Started]
   ```

Save as markdown. Keep the tone constructive — the goal is improvement, not blame.
## 中文执行导读

这是 `retro` 的中文 runtime 入口。

中文产品管理请求命中本 skill 时，先确认目标产出和适用的 PM framework，再按下方上游流程执行。输出说明使用简体中文；framework 名称、公式、字段、命令、路径、模板结构、引用和代码保持原样，法律与合规内容不替代专业意见。

## Sprint Retrospective Facilitator

本次上游补充：如果还没有输入，先在讨论前匿名收集，避免第一个发言或职级最高的人设定议程——用词云或 1–5 分情绪评分，再让大家书面写下做得好与不好的事项并互相投票（见 `live-polls` 与 `live-qa`）。
