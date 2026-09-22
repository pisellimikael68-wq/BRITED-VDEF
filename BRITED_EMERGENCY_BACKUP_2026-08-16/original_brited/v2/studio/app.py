from pathlib import Path
import sys

# ---------------------------------------------------------------------
# Permet d'importer le package "v2" lorsque Streamlit lance l'application
# ---------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from v2.knowledge.io.compiled_knowledge_loader import (
    CompiledKnowledgeLoader,
)
from v2.knowledge.io.knowledge_catalog import (
    KnowledgeCatalog,
)
from v2.knowledge.services.corpus_service import (
    CorpusService,
)

from v2.studio.components.dashboard import (
    render_dashboard,
)
from v2.studio.components.corpus_selector import (
    render_corpus_selector,
)
from v2.studio.components.knowledge_inspector import (
    render_knowledge_inspector,
)

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------

st.set_page_config(
    page_title="BRITED Studio V2",
    layout="wide",
)

st.title("BRITED Studio V2")

# ---------------------------------------------------------------------
# Services
# ---------------------------------------------------------------------

corpus_service = CorpusService()
catalog = KnowledgeCatalog()
loader = CompiledKnowledgeLoader()

# ---------------------------------------------------------------------
# Dashboard
# ---------------------------------------------------------------------

summary = corpus_service.summary()

render_dashboard(summary)

# ---------------------------------------------------------------------
# Sélection du corpus
# ---------------------------------------------------------------------

family, chapter = render_corpus_selector(
    catalog,
)

if family is None:
    st.stop()

# ---------------------------------------------------------------------
# Chargement du chapitre
# ---------------------------------------------------------------------

if st.button(
    "Ouvrir le chapitre",
    type="primary",
):
    knowledge = loader.load(
        family=family,
        chapter=chapter,
    )

    render_knowledge_inspector(
        knowledge,
    )
    