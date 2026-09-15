import unittest

from complaint_system import ComplaintManagementSystem, ComplaintStatus


class ComplaintSystemTests(unittest.TestCase):
    def setUp(self) -> None:
        self.system = ComplaintManagementSystem()

    def test_submit_complaint_generates_tracking_data_and_ai_triage(self) -> None:
        complaint = self.system.submit_complaint(
            student_id="stu-1",
            title="Urgent hostel water issue",
            description="Hostel room has no water supply and this is critical",
        )

        self.assertEqual(complaint.student_id, "stu-1")
        self.assertEqual(complaint.status, ComplaintStatus.SUBMITTED)
        self.assertEqual(complaint.category, "hostel")
        self.assertEqual(complaint.priority, "high")

    def test_assign_and_resolve_flow(self) -> None:
        complaint = self.system.submit_complaint(
            student_id="stu-2",
            title="WiFi not working in library",
            description="Internet issue in central library",
        )

        assigned = self.system.assign_complaint(complaint.id)
        self.assertEqual(assigned.status, ComplaintStatus.ASSIGNED)
        self.assertEqual(assigned.assignee, "Campus Facilities")

        resolved = self.system.resolve_complaint(complaint.id, "Router replaced and connection restored")
        self.assertEqual(resolved.status, ComplaintStatus.RESOLVED)
        self.assertIn("restored", resolved.resolution_notes)

    def test_track_unknown_complaint_raises(self) -> None:
        with self.assertRaises(KeyError):
            self.system.track_complaint("missing-id")

    def test_list_student_complaints_returns_only_student_records(self) -> None:
        self.system.submit_complaint("stu-1", "Exam issue", "Exam hall seat mismatch")
        self.system.submit_complaint("stu-2", "Fee query", "Payment reflected late")
        self.system.submit_complaint("stu-1", "Mess complaint", "Mess food quality problem")

        complaints = self.system.list_student_complaints("stu-1")
        self.assertEqual(len(complaints), 2)
        self.assertTrue(all(complaint.student_id == "stu-1" for complaint in complaints))


if __name__ == "__main__":
    unittest.main()
