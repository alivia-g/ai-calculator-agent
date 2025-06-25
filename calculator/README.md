Automated bug fixer for arithmetic expressions

This project develops an AI agent to autonomously identify and resolve code bugs within a Python-based calculator application.

Sample Challenge:
The calculator was intentionally configured with an incorrect operator precedence for the addition operator (+), causing expressions like 3 + 7 * 2 to evaluate incorrectly (e.g., yielding 20 instead of the mathematically correct 17). This mimics a common real-world debugging scenario.

The Solution:
The AI agent was tasked with debugging this specific issue. By analyzing the problem (the incorrect calculation output) and the codebase, the agent successfully located the wrongly-configured operator precedence in pkg/calculator.py and applied the necessary correction in file. This restored the calculator's ability to correctly evaluate arithmetic expressions, adhering to standard order of operations.