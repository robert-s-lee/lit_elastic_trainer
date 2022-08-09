import streamlit as st

def run(state):
	st.markdown("""
	# Lightning is the "glue" layer of ML.
	- Build models.
	- Research Workflows.
	- Production Pipeline.

	# Wrap existing code to get started fast
	- Take the existing code
	- Wrap it with Lightning Work
	- Run it with Lightning Flow
	- Lightning App created.
	[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggUkw7XG4gIEFQKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-QXBwKVxuICBzdWJncmFwaCBTdGF0ZSBUcmFuc2l0aW9uIHZpYSBFdmVudCBMb29wXG4gICAgTEYoKE9yY2hlc3RyYXRlIDxicj48YnI-TGlnaHRuaW5nIDxicj5GbG93KSlcbiAgICBMV1tSdW4gPGJyPjxicj5MaWdodG5pbmcgPGJyPldvcmtdXG4gICAgQVAgLS0gcnVuIC0tPiBMRlxuICAgIExGIC0tIHJ1biAtLT4gTFdcbiAgICBMVyAtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICBlbmQgIFxuICBzdWJncmFwaCBleGlzdGluZyBzY3JpcHRzXG4gICAgU1tleGlzdGluZyAucHkgLnNoIC4uIGNvZGVdXG4gIGVuZFxuICBMVyAtLS0-IFNcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)](https://mermaid-js.github.io/docs/mermaid-live-editor-beta/#/edit/eyJjb2RlIjoiZ3JhcGggUkw7XG4gIEFQKEFwcCA8YnI-PGJyPkxpZ2h0bmluZyA8YnI-QXBwKVxuICBzdWJncmFwaCBTdGF0ZSBUcmFuc2l0aW9uIHZpYSBFdmVudCBMb29wXG4gICAgTEYoKE9yY2hlc3RyYXRlIDxicj48YnI-TGlnaHRuaW5nIDxicj5GbG93KSlcbiAgICBMV1tSdW4gPGJyPjxicj5MaWdodG5pbmcgPGJyPldvcmtdXG4gICAgQVAgLS0gcnVuIC0tPiBMRlxuICAgIExGIC0tIHJ1biAtLT4gTFdcbiAgICBMVyAtLSBzdGF0ZSBjaGFuZ2VzIC0tPiBMRlxuICBlbmQgIFxuICBzdWJncmFwaCBleGlzdGluZyBzY3JpcHRzXG4gICAgU1tleGlzdGluZyAucHkgLnNoIC4uIGNvZGVdXG4gIGVuZFxuICBMVyAtLS0-IFNcbiIsIm1lcm1haWQiOnsidGhlbWUiOiJkZWZhdWx0In0sInVwZGF0ZUVkaXRvciI6ZmFsc2V9)

	# Research Workflow:
	- Scale out and scale in the number of trainer VMs

	# Production Pipeline:
	- Deploy on the Cloud `lightning run app app.py --cloud`

	# Source Code:
	- [Source Code](https://github.com/robert-s-lee/lai-train-eval)
	""")  

