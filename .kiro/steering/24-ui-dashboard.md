---
inclusion: fileMatch
fileMatchPattern: ['apps/dashboard/**']
---

# Streamlit (apps/dashboard)

**Structure**
- Multipage: `Home.py` + `pages/*.py`. Wide layout.

**State & Caching**
- `st.session_state` for UI state (filters/selections).
- `st.cache_resource` for clients/repos; `st.cache_data` for expensive reads.
- After writes, refresh via `st.rerun()` or cache invalidation.

**Rules**
- Thin callbacks; call services for work.
- Stable widget keys; prefer forms for create/edit flows.
- Config from env; no hardcoded paths.

**Accessibility**
- Clear labels, keyboard-friendly controls, and helpful empty states.
