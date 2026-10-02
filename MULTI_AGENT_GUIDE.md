# 🤖 Multi-Agent AutoGen Job Hunter Guide

## Architecture Overview

This is a sophisticated multi-agent system where different AI agents collaborate to help you find and apply for jobs.

### The 5 Agents

#### 1. **JobCollectorAgent** 🔍
- **Role**: Searches and collects job offers from public sources
- **Responsibilities**:
  - Find relevant job listings
  - Analyze search strategies
  - Recommend optimal search terms
  - Suggest job sources

#### 2. **CVAnalyzerAgent** 📄
- **Role**: Analyzes your CV and professional profile
- **Responsibilities**:
  - Extract key skills from your CV
  - Assess experience level
  - Identify skill gaps
  - Recommend improvements

#### 3. **MatcherAgent** ⚡
- **Role**: Matches jobs to your profile
- **Responsibilities**:
  - Score job fit (0-100%)
  - Identify relevant skills
  - Highlight missing skills
  - Rank opportunities

#### 4. **DigestGeneratorAgent** 📋
- **Role**: Creates daily job search digest
- **Responsibilities**:
  - Synthesize matching results
  - Prioritize opportunities
  - Create action plans
  - Provide strategy recommendations

#### 5. **RecruiterOutreachAgent** 💼
- **Role**: Generates personalized outreach messages
- **Responsibilities**:
  - Write application emails
  - Create cover letters
  - Generate LinkedIn messages
  - Tailor communication per opportunity

## Setup

### 1. Install AutoGen

```bash
pip install autogen
```

### 2. Start LM Studio

1. Open LM Studio
2. Load a model (Mistral 7B recommended)
3. Go to Server tab
4. Enable "Local API Server"
5. Keep running in background

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your preferences
```

### 4. Run the Multi-Agent System

#### Automated Workflow

```bash
# Run full workflow with defaults
python -m job_hunter

# With custom parameters
python -m job_hunter --keywords "DevOps engineer" --location "Paris" --limit 15
```

#### Interactive Group Chat

```bash
# Run in group chat mode (agents discuss strategy)
python -m job_hunter --chat

# With custom query
python -m job_hunter --chat --chat-query "Find me backend positions in Paris that pay 80k+"
```

## How It Works

### Automated Workflow (Default)

```
┌─────────────────────────┐
│  JobCollectorAgent      │
│  Collect job offers     │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  CVAnalyzerAgent        │
│  Analyze your profile   │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  MatcherAgent           │
│  Match jobs to CV       │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  DigestGeneratorAgent   │
│  Create daily digest    │
└────────────┬────────────┘
             │
             ↓
┌─────────────────────────┐
│  RecruiterOutreachAgent │
│  Generate messages      │
└─────────────────────────┘
```

### Interactive Group Chat

All 5 agents participate in a group discussion:

```
┌─────────────────────────────────────────┐
│        Multi-Agent Group Chat           │
├─────────────────────────────────────────┤
│ • JobCollector suggests search strategy │
│ • CVAnalyzer highlights strengths       │
│ • Matcher ranks opportunities           │
│ • DigestGenerator creates action plan   │
│ • Recruiter prepares outreach           │
└─────────────────────────────────────────┘
```

## Example Usage

### Run Automated Workflow

```bash
$ python -m job_hunter --keywords "python backend" --location "Paris" --limit 10

======================================================================
🚀 STARTING MULTI-AGENT JOB HUNT WORKFLOW
======================================================================

[Step 1] Job Collection
----------------------------------------------------------------------
✅ Collected 10 job opportunities

[Step 2] CV Analysis
----------------------------------------------------------------------
✅ CV analyzed. Found 14 key skills

[Step 3] Job Matching
----------------------------------------------------------------------
✅ Matched 10 jobs against profile

[Step 4] Digest Generation
----------------------------------------------------------------------
✅ Daily digest generated

[Step 5] Recruiter Outreach Generation
----------------------------------------------------------------------
✅ Generated 3 outreach messages

======================================================================
✅ WORKFLOW COMPLETE
======================================================================
```

### Run Interactive Chat

```bash
$ python -m job_hunter --chat

======================================================================
🗣️ STARTING MULTI-AGENT GROUP CHAT
======================================================================

HRManager: I need help with my job search...

JobCollector: Great! I recommend searching for...
CVAnalyzer: Based on your profile, your strengths are...
Matcher: These jobs match your skills: ...
DigestGenerator: Here's your action plan for today: ...
RecruiterOutreach: For your top opportunity, here's the message...
```

## Output Files

- `data/job_hunter.db` - SQLite database with all job offers and matches
- `data/daily_digest.md` - Today's job hunting digest and action plan
- `data/cv.md` - Your CV/profile

## Agent Communication

### How Agents Collaborate

1. **JobCollector** finds opportunities → passes to **Matcher**
2. **CVAnalyzer** analyzes profile → passes to **Matcher** and **Recruiter**
3. **Matcher** scores jobs → passes to **DigestGenerator**
4. **DigestGenerator** creates strategy → passes to **Recruiter**
5. **Recruiter** personalizes messages → final output

### In Group Chat Mode

Agents can discuss and refine their analysis:
- "I found 10 jobs, but only 3 match the skills requirement"
- "Your CV shows strong backend experience. Let's focus on senior roles."
- "These are the top 3 opportunities. Here are personalized messages."

## Customization

### Change Agent Behavior

Edit system messages in each agent class:

```python
self.agent = autogen.AssistantAgent(
    name="CustomAgent",
    system_message="Your custom instructions here...",
    llm_config=llm_config,
)
```

### Add New Agents

1. Create new agent class in `job_hunter/agents/`
2. Add to `job_hunter/agents/__init__.py`
3. Initialize in `JobHuntOrchestrator.__init__()`
4. Integrate in workflow

### Modify Workflow

Edit `job_hunter/orchestrator.py` to change the order or add steps:

```python
def run_full_workflow(self, ...):
    # Step 1: Collect
    # Step 2: Analyze
    # Step 3: Match
    # Step 4: Digest
    # Step 5: Outreach
    # Add Step 6: Your custom step
```

## Tips & Best Practices

### For Better Results

1. **Update your CV regularly** - More details = Better matches
2. **Use specific keywords** - "Python backend" vs "programming"
3. **Set realistic expectations** - Agent analysis is probabilistic
4. **Review agent outputs** - Always verify recommendations
5. **Customize outreach** - Use agent messages as templates

### Performance Optimization

- Use smaller models for faster responses (TinyLlama, Phi)
- Reduce `max_turns` in group chat for quicker cycles
- Cache CV analysis if it doesn't change daily
- Run during off-peak hours for better LM Studio performance

## Troubleshooting

### "Connection refused" error

```bash
# Make sure LM Studio is running
# Check: http://localhost:1234/v1/models
```

### Agents not responding

```bash
# Increase timeout in config.py
LMSTUDIO_TIMEOUT=120  # seconds
```

### Low quality responses

- Update your CV with more details
- Use a larger language model
- Specify more context in chat queries

## Advanced Features

### 1. Email Integration

Send daily digest via email:

```python
from job_hunter.utils import send_email_digest
send_email_digest(digest, "your@email.com")
```

### 2. Slack Integration

Post digest to Slack:

```python
from job_hunter.utils import post_to_slack
post_to_slack(digest, "#job-search")
```

### 3. Schedule Daily Runs

**Linux/Mac (Cron)**:
```bash
0 8 * * * cd /path/to/job-hunter && python -m job_hunter >> logs/daily.log 2>&1
```

**Windows (Task Scheduler)**:
```
Action: Start program
Program: C:\Python\python.exe
Arguments: -m job_hunter
Start in: C:\path\to\job-hunter
```

## Next Steps

1. ✅ Run automated workflow
2. ✅ Review daily digest
3. ✅ Try interactive chat mode
4. ✅ Customize for your needs
5. ✅ Automate daily execution
6. ✅ Add Slack/email notifications

## Contributing

Want to improve the agents? Consider:
- Adding new data sources
- Improving matching algorithm
- Creating new specialized agents
- Building a web dashboard

## License

MIT License - Free to use and modify
