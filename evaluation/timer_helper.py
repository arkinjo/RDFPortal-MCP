#!/usr/bin/env python3
"""
Simple Timer for Manual Validation
===================================
Run this script alongside your browser testing.

Usage:
    python timer_helper.py
    
Commands:
    s or start  - Start timer for a question
    e or end    - Stop timer and record
    q or quit   - Save results and exit
    l or list   - Show all recorded times
"""

import time
import csv
from datetime import datetime

class ValidationTimer:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.current_question = None
        self.question_count = 0
        
    def start(self):
        """Start timing a question."""
        self.question_count += 1
        self.current_question = f"Q{self.question_count:03d}"
        self.start_time = time.time()
        print(f"\n⏱️  Timer STARTED for {self.current_question}")
        print(f"   Started at: {datetime.now().strftime('%H:%M:%S')}")
        
    def end(self, notes: str = ""):
        """Stop timer and record result."""
        if self.start_time is None:
            print("❌ No timer running! Use 's' to start first.")
            return
            
        elapsed = time.time() - self.start_time
        
        result = {
            "question": self.current_question,
            "time_sec": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        }
        self.results.append(result)
        
        print(f"\n⏹️  Timer STOPPED for {self.current_question}")
        print(f"   Elapsed: {elapsed:.2f} seconds")
        
        self.start_time = None
        self.current_question = None
        
    def list_results(self):
        """Show all recorded times."""
        if not self.results:
            print("\nNo results recorded yet.")
            return
            
        print("\n" + "=" * 50)
        print("RECORDED TIMES")
        print("=" * 50)
        for r in self.results:
            print(f"  {r['question']}: {r['time_sec']:.2f}s  {r['notes']}")
        print("=" * 50)
        total = sum(r['time_sec'] for r in self.results)
        avg = total / len(self.results)
        print(f"  Total: {total:.1f}s | Avg: {avg:.1f}s | Count: {len(self.results)}")
        
    def save(self, filename: str = "timing_results.csv"):
        """Save results to CSV."""
        if not self.results:
            print("No results to save.")
            return
            
        with open(filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["question", "time_sec", "timestamp", "notes"])
            writer.writeheader()
            writer.writerows(self.results)
        print(f"\n✅ Saved {len(self.results)} results to {filename}")

def main():
    timer = ValidationTimer()
    
    print("""
╔═══════════════════════════════════════════════════════╗
║         RDF Portal Validation Timer Helper            ║
╠═══════════════════════════════════════════════════════╣
║  Commands:                                            ║
║    s / start  - Start timer for next question         ║
║    e / end    - Stop timer and record time            ║
║    n [note]   - End timer with a note                 ║
║    l / list   - Show all recorded times               ║
║    r / reset  - Reset question counter                ║
║    q / quit   - Save and exit                         ║
╚═══════════════════════════════════════════════════════╝
    """)
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if not cmd:
                continue
            elif cmd in ['s', 'start']:
                timer.start()
            elif cmd in ['e', 'end']:
                timer.end()
            elif cmd.startswith('n '):
                note = cmd[2:].strip()
                timer.end(note)
            elif cmd in ['l', 'list']:
                timer.list_results()
            elif cmd in ['r', 'reset']:
                timer.question_count = 0
                print("Question counter reset to 0")
            elif cmd in ['q', 'quit', 'exit']:
                timer.save()
                print("Goodbye!")
                break
            else:
                print("Unknown command. Use s/e/l/q")
                
        except KeyboardInterrupt:
            print("\n")
            timer.save()
            break

if __name__ == "__main__":
    main()
