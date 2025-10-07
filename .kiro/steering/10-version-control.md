---
inclusion: always
---

# Version Control & Environment

1. **Git Hygiene:**

   * Commit frequently with clear, atomic messages.
   * Keep the working directory clean; ensure no unrelated or temporary files are staged or committed.
   * Use `.gitignore` effectively.
2. **Branching Strategy:** Follow the project's established branching strategy. Do not create new branches unless requested or necessary.
3. **.env Files:** **Never** commit `.env` files. Use `.env.example` as templates. Do not overwrite local `.env` files without confirmation.
4. **Environment Awareness:** Ensure code functions correctly across different environments (dev, test, prod). Use environment variables for configuration.
5. **Server Management:** Kill related running servers before starting new ones. Restart servers after relevant configuration or backend changes.
