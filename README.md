# Smart-AI-Complaint-Management-System

Minimal Python implementation of an **AI-powered university complaint management system** for:
- submitting student complaints,
- tracking complaint status,
- assigning complaints to responsible departments,
- resolving complaints with resolution notes.

## Implemented Components

- `complaint_system.py`
  - `ComplaintManagementSystem.submit_complaint(...)`
  - `ComplaintManagementSystem.track_complaint(...)`
  - `ComplaintManagementSystem.assign_complaint(...)`
  - `ComplaintManagementSystem.resolve_complaint(...)`
  - `ComplaintManagementSystem.list_student_complaints(...)`
  - `ComplaintManagementSystem.get_ai_routing_suggestion(...)`
- Lightweight AI triage:
  - category detection from complaint text (academics, hostel, fees, safety, facilities, general)
  - priority prediction (`high`, `medium`, `low`)
  - routing suggestion to likely department

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Quick Usage

```python
from complaint_system import ComplaintManagementSystem

system = ComplaintManagementSystem()

complaint = system.submit_complaint(
    student_id="stu-1001",
    title="Urgent hostel water issue",
    description="No water in room since morning, please resolve ASAP"
)

system.assign_complaint(complaint.id)  # Uses AI routing suggestion
system.resolve_complaint(complaint.id, "Plumbing issue fixed")
```
