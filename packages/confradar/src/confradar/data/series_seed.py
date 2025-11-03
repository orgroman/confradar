"""Canonical data for conference series seeding.

This module contains the authoritative list of major conference series
that should be seeded into the database. Both the seed script and tests
import from this module to ensure consistency.
"""

from __future__ import annotations

# Major conference series to seed with (short_name, full_name, homepage)
# This is the single source of truth for conference series seeding
MAJOR_SERIES = [
    ("NeurIPS", "Conference on Neural Information Processing Systems", "https://neurips.cc"),
    ("ICML", "International Conference on Machine Learning", "https://icml.cc"),
    ("ICLR", "International Conference on Learning Representations", "https://iclr.cc"),
    ("ACL", "Annual Meeting of the Association for Computational Linguistics", "https://aclweb.org"),
    ("EMNLP", "Conference on Empirical Methods in Natural Language Processing", "https://aclweb.org"),
    ("NAACL", "North American Chapter of the Association for Computational Linguistics", "https://aclweb.org"),
    ("COLING", "International Conference on Computational Linguistics", "https://www.aclweb.org/anthology/venues/coling/"),
    ("EACL", "European Chapter of the Association for Computational Linguistics", "https://aclweb.org"),
]
