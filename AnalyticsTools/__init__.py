from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("AnalyticsTools")  # better: explicit package name
except PackageNotFoundError:
    __version__ = "0+unknown"

from .AnalyticsTools import AnalysisTools

__all__ = [
    "__version__",
    "AnalysisTools",
]