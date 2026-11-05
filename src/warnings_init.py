"""RecallAI — Global warning & logger suppressor.

Silences Transformers 5.x image-processor registry spam, HF hub notices,
and position_id load reports for clean terminal and UI execution.
"""

import os
import sys
import warnings
import logging

# ── 1. Environment variables set before library imports ─────────────────────
os.environ["TRANSFORMERS_VERBOSITY"] = "error"
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ── 2. Comprehensive Warning Filters ─────────────────────────────────────────
warnings.filterwarnings("ignore", message=r".*Accessing `__path__`.*")
warnings.filterwarnings("ignore", message=r".*`huggingface_hub` cache-system uses symlinks.*")
warnings.filterwarnings("ignore", message=r".*unauthenticated requests.*")
warnings.filterwarnings("ignore", message=r".*get_sentence_embedding_dimension.*")
warnings.filterwarnings("ignore", message=r".*position_ids.*")
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# ── 3. Silence Loggers ───────────────────────────────────────────────────────
for name in [
    "transformers",
    "transformers.modeling_utils",
    "transformers.configuration_utils",
    "transformers.tokenization_utils_base",
    "transformers.pipeline",
    "transformers.pipelines",
    "sentence_transformers",
    "sentence_transformers.SentenceTransformer",
    "huggingface_hub",
    "huggingface_hub.file_download",
    "huggingface_hub.utils",
    "filelock",
    "urllib3",
    "PIL",
]:
    logger = logging.getLogger(name)
    logger.setLevel(logging.ERROR)
    logger.propagate = False

# Try disabling progress bar in transformers directly if already loaded
try:
    import transformers.utils.logging as hf_logging
    hf_logging.set_verbosity_error()
    hf_logging.disable_progress_bar()
except Exception:
    pass
