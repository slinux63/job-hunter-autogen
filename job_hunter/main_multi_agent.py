from __future__ import annotations

import argparse
from pathlib import Path
from job_hunter.orchestrator import JobHuntOrchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Multi-Agent Local AI Job Hunter with AutoGen"
    )
    parser.add_argument(
        "--keywords",
        default=None,
        help="Job keywords to search",
    )
    parser.add_argument(
        "--location",
        default=None,
        help="Job location to search",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of jobs to analyze",
    )
    parser.add_argument(
        "--chat",
        action="store_true",
        help="Run interactive group chat mode",
    )
    parser.add_argument(
        "--chat-query",
        default="""I need help with my job search. Please:
1. Collect relevant job opportunities
2. Analyze my CV and strengths
3. Match jobs to my profile
4. Generate a daily job hunting strategy
5. Create personalized outreach messages for top opportunities""",
        help="Query for interactive chat mode",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    # Ensure data directory exists
    Path("data").mkdir(exist_ok=True)
    
    # Initialize orchestrator
    orchestrator = JobHuntOrchestrator()
    
    if args.chat:
        # Run interactive group chat
        orchestrator.run_group_chat_workflow(args.chat_query)
    else:
        # Run full automated workflow
        results = orchestrator.run_full_workflow(
            keywords=args.keywords,
            location=args.location,
            limit=args.limit,
        )
        
        print("\n📊 WORKFLOW RESULTS:")
        print("-" * 70)
        print(f"Jobs Collected: {results['jobs_collected']}")
        print(f"Jobs Matched: {results['matches']}")
        print(f"CV Skills Identified: {len(results['cv_skills'])}")
        print(f"Outreach Messages Generated: {len(results['outreach_messages'])}")
        print("\n" + "-" * 70)
        print("📋 DAILY DIGEST:")
        print("-" * 70)
        print(results['digest'][:500] + "...")
        print("-" * 70)


if __name__ == "__main__":
    main()
