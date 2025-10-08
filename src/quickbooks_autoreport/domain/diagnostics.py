"""Diagnostic result domain model.

This module defines the DiagnosticResult dataclass for structured
diagnostic information about the system and QuickBooks installation.
"""

from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass
class DiagnosticResult:
    """Result of system diagnostics.
    
    This dataclass encapsulates comprehensive diagnostic information about
    the system, QuickBooks installation, SDK, and connectivity.
    
    Attributes:
        timestamp: When diagnostics were run (ISO format)
        system_info: System information (OS, Python version, etc.)
        quickbooks_installation: QuickBooks installation details
        sdk_installation: SDK installation details
        connectivity_test: Connection test results
        recommendations: List of recommended actions
    """

    timestamp: str
    system_info: Dict[str, Any]
    quickbooks_installation: Dict[str, Any]
    sdk_installation: Dict[str, Any]
    connectivity_test: Dict[str, Any]
    recommendations: List[str]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization.
        
        Returns:
            Dictionary representation of diagnostic results
        """
        return asdict(self)

    def get_summary(self) -> str:
        """Get a human-readable summary of diagnostics.
        
        Returns:
            Multi-line summary string
        """
        lines = [
            "=== QuickBooks Auto Reporter Diagnostics ===",
            f"Timestamp: {self.timestamp}",
            "",
            "System Information:",
        ]
        
        for key, value in self.system_info.items():
            lines.append(f"  {key}: {value}")
        
        lines.append("")
        lines.append("QuickBooks Installation:")
        qb_status = self.quickbooks_installation.get("status", "Unknown")
        lines.append(f"  Status: {qb_status}")
        if "version" in self.quickbooks_installation:
            lines.append(f"  Version: {self.quickbooks_installation['version']}")
        
        lines.append("")
        lines.append("SDK Installation:")
        sdk_status = self.sdk_installation.get("status", "Unknown")
        lines.append(f"  Status: {sdk_status}")
        if "version" in self.sdk_installation:
            lines.append(f"  Version: {self.sdk_installation['version']}")
        
        lines.append("")
        lines.append("Connectivity Test:")
        conn_status = self.connectivity_test.get("status", "Unknown")
        lines.append(f"  Status: {conn_status}")
        if "message" in self.connectivity_test:
            lines.append(f"  Message: {self.connectivity_test['message']}")
        
        if self.recommendations:
            lines.append("")
            lines.append("Recommendations:")
            for i, rec in enumerate(self.recommendations, 1):
                lines.append(f"  {i}. {rec}")
        
        return "\n".join(lines)

    def has_issues(self) -> bool:
        """Check if diagnostics found any issues.
        
        Returns:
            True if any component has issues, False otherwise
        """
        qb_ok = self.quickbooks_installation.get("status") == "OK"
        sdk_ok = self.sdk_installation.get("status") == "OK"
        conn_ok = self.connectivity_test.get("status") == "OK"
        
        return not (qb_ok and sdk_ok and conn_ok)

    def get_error_count(self) -> int:
        """Get count of errors found.
        
        Returns:
            Number of components with errors
        """
        error_count = 0
        
        if self.quickbooks_installation.get("status") != "OK":
            error_count += 1
        if self.sdk_installation.get("status") != "OK":
            error_count += 1
        if self.connectivity_test.get("status") != "OK":
            error_count += 1
        
        return error_count
