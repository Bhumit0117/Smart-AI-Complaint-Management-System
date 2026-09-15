from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class ComplaintStatus(str, Enum):
    SUBMITTED = "submitted"
    ASSIGNED = "assigned"
    RESOLVED = "resolved"


@dataclass
class Complaint:
    id: str
    student_id: str
    title: str
    description: str
    category: str
    priority: str
    status: ComplaintStatus
    assignee: Optional[str]
    resolution_notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class ComplaintManagementSystem:
    """In-memory complaint manager with lightweight AI-style triage."""

    _CATEGORY_KEYWORDS = {
        "academics": {"exam", "grade", "professor", "class", "course", "assignment"},
        "hostel": {"hostel", "room", "mess", "warden", "water", "electricity"},
        "fees": {"fees", "scholarship", "payment", "refund"},
        "safety": {"harassment", "unsafe", "threat", "violence", "abuse"},
        "facilities": {"library", "lab", "wifi", "internet", "cleaning", "maintenance"},
    }

    _ASSIGNEE_SUGGESTIONS = {
        "academics": "Academic Office",
        "hostel": "Hostel Administration",
        "fees": "Finance Office",
        "safety": "Student Welfare & Security",
        "facilities": "Campus Facilities",
        "general": "Student Affairs",
    }

    def __init__(self) -> None:
        self._complaints: Dict[str, Complaint] = {}

    def submit_complaint(self, student_id: str, title: str, description: str) -> Complaint:
        category, priority = self._triage_complaint(title=title, description=description)
        now = datetime.now(timezone.utc)
        complaint = Complaint(
            id=str(uuid4()),
            student_id=student_id,
            title=title,
            description=description,
            category=category,
            priority=priority,
            status=ComplaintStatus.SUBMITTED,
            assignee=None,
            resolution_notes=None,
            created_at=now,
            updated_at=now,
        )
        self._complaints[complaint.id] = complaint
        return complaint

    def track_complaint(self, complaint_id: str) -> Complaint:
        return self._get_complaint(complaint_id)

    def assign_complaint(self, complaint_id: str, assignee: Optional[str] = None) -> Complaint:
        complaint = self._get_complaint(complaint_id)
        if complaint.status == ComplaintStatus.RESOLVED:
            raise ValueError("Cannot assign a resolved complaint")

        complaint.assignee = assignee or self._ASSIGNEE_SUGGESTIONS[complaint.category]
        complaint.status = ComplaintStatus.ASSIGNED
        complaint.updated_at = datetime.now(timezone.utc)
        return complaint

    def resolve_complaint(self, complaint_id: str, resolution_notes: str) -> Complaint:
        complaint = self._get_complaint(complaint_id)
        complaint.status = ComplaintStatus.RESOLVED
        complaint.resolution_notes = resolution_notes
        complaint.updated_at = datetime.now(timezone.utc)
        return complaint

    def list_student_complaints(self, student_id: str) -> List[Complaint]:
        return sorted(
            (c for c in self._complaints.values() if c.student_id == student_id),
            key=lambda complaint: complaint.created_at,
        )

    def get_ai_routing_suggestion(self, complaint_id: str) -> str:
        complaint = self._get_complaint(complaint_id)
        return self._ASSIGNEE_SUGGESTIONS[complaint.category]

    def _get_complaint(self, complaint_id: str) -> Complaint:
        complaint = self._complaints.get(complaint_id)
        if complaint is None:
            raise KeyError(f"Complaint not found: {complaint_id}")
        return complaint

    def _triage_complaint(self, title: str, description: str) -> tuple[str, str]:
        text = f"{title} {description}".lower()

        category = "general"
        max_matches = 0
        for name, keywords in self._CATEGORY_KEYWORDS.items():
            matches = sum(1 for keyword in keywords if keyword in text)
            if matches > max_matches:
                category = name
                max_matches = matches

        high_priority_signals = {"urgent", "immediately", "asap", "critical", "harassment", "unsafe", "threat"}
        medium_priority_signals = {"soon", "delay", "issue", "problem"}

        if any(signal in text for signal in high_priority_signals):
            priority = "high"
        elif any(signal in text for signal in medium_priority_signals):
            priority = "medium"
        else:
            priority = "low"

        return category, priority
