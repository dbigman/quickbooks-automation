---
inclusion: always
---

# Debugging & Troubleshooting

1. **Fix the Root Cause:** Prioritize fixing the underlying issue causing an error, rather than just masking or handling it, unless a temporary workaround is explicitly agreed upon.
2. **Console/Log Analysis:** Always check browser and server console output for errors, warnings, or relevant logs after making changes or when debugging. Report findings.
3. **Targeted Logging:** For persistent or complex issues, add specific `console.log` statements (or use a project logger) to trace execution and variable states. Remember to remove or disable verbose logs after debugging.
4. **Check the `fixes/` Directory:** Before deep-diving into a complex or recurring bug, check `fixes/` for documented solutions to similar past issues.
5. **Document Complex Fixes:** If a bug requires significant effort, create a concise `.md` file in `fixes/` detailing the problem, investigation steps, and the solution.
