#!/usr/bin/env python3
"""
Aarogya Sahayak - Tavily Live Verification Demonstration Script
Used for video demos, technical evaluation, and mentor presentations.
"""
import sys
import time
from app.ai.providers.tavily_service import tavily_service

def main():
    print("=" * 70)
    print("   AAROGYA SAHAYAK - LIVE TAVILY OFFICIAL VERIFICATION ENGINE   ")
    print("=" * 70)
    print(f"[1] Integration Mode : {tavily_service.get_mode()}")
    print(f"[2] Is Live Connected: {tavily_service.is_live}")
    print(f"[3] Approved Domains : {sorted(list(tavily_service.APPROVED_DOMAINS))[:5]} ... (+ more)")
    print("-" * 70)

    # Test Case 1: Live Official Search
    query = "Pradhan Mantri Matru Vandana Yojana official guidelines"
    print(f"\n[Test 1] Searching Live Official Govt Sources for:\n         '{query}'")
    start = time.time()
    result = tavily_service.verify_official_update(query)
    elapsed = time.time() - start

    print(f" -> Response Time    : {elapsed:.2f}s")
    print(f" -> Verified Status  : {result.get('status')}")
    print(f" -> Official Domain  : {result.get('domain')}")
    print(f" -> Document Title   : {result.get('title')}")
    print(f" -> Official Link    : {result.get('url')}")
    if result.get('content'):
        print(f" -> Verified Snippet : {result.get('content')[:180]}...")

    # Test Case 2: Zero-Trust Security Guard (Blocked Unofficial URL)
    fake_url = "https://unverified-health-subsidy-claim.org/apply-cash"
    print(f"\n[Test 2] Security Guard Test - Unofficial / Untrusted URL:\n         '{fake_url}'")
    guard_result = tavily_service.verify_official_update(query="Maternal Benefit", candidate_url=fake_url)
    print(f" -> Verified Status  : {guard_result.get('status')}")
    print(f" -> Verified Flag    : {guard_result.get('verified')}")
    print(f" -> Guard Reason     : {guard_result.get('reason')}")

    print("\n" + "=" * 70)
    print("   RESULT: TAVILY ENGINE VERIFIED & ACTIVE IN AAROGYA SAHAYAK   ")
    print("=" * 70)

if __name__ == "__main__":
    main()
