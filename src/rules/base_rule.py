"""Base class for APA rules - Scalable rule system."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.models import AnalysisResult, Modification


class BaseRule(ABC):
    """Abstract base class for APA rules."""

    def __init__(self, name: str, description: str) -> None:
        """
        Initialize the rule.

        Args:
            name: Rule name
            description: Rule description
        """
        self.name = name
        self.description = description

    @abstractmethod
    def analyze(
        self, pdf_path: str
    ) -> AnalysisResult:
        """
        Analyze PDF according to this rule.

        Args:
            pdf_path: Path to PDF file

        Returns:
            AnalysisResult with detected issues
        """
        pass

    @abstractmethod
    def apply(
        self,
        pdf_path: str,
        output_path: str,
        modifications: List[Modification],
    ) -> bool:
        """
        Apply rule modifications to PDF.

        Args:
            pdf_path: Input PDF path
            output_path: Output PDF path
            modifications: List of modifications to apply

        Returns:
            True if successful
        """
        pass

    @abstractmethod
    def validate(
        self, modification: Modification
    ) -> bool:
        """
        Validate a modification before applying.

        Args:
            modification: Modification to validate

        Returns:
            True if valid
        """
        pass

    def get_name(self) -> str:
        """Get rule name."""
        return self.name

    def get_description(self) -> str:
        """Get rule description."""
        return self.description

