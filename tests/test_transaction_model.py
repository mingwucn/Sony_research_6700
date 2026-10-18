"""Synthetic OFF-12/13 coverage, without camera or durable journal claims."""

from dataclasses import FrozenInstanceError
import unittest

from tools.transaction_model import Operation, OwnershipRegistry, TransactionError, TransactionSimulator


class TransactionModelTests(unittest.TestCase):
    def setUp(self):
        self.registry = OwnershipRegistry()
        self.initial = {"ap": b"AP-old", "cp": b"CP-old", "resource": b"unchanged"}
        self.operations = (Operation("change-ap", "ap", b"AP-old", b"AP-new"),
                           Operation("change-cp", "cp", b"CP-old", b"CP-new"))

    def simulator(self, session="session-a", resources=("synthetic-body",)):
        return TransactionSimulator(session, resources, self.initial, self.operations, self.registry)

    def run_confirmed(self, simulator):
        simulator.prepare_next()
        simulator.simulate_result("confirmed")

    def test_prepare_record_precedes_every_mutation(self):
        simulator = self.simulator()
        with self.assertRaises(TransactionError):
            simulator.simulate_result("confirmed")
        self.assertEqual(simulator.snapshot(), self.initial)
        simulator.open()
        with self.assertRaises(TransactionError):
            simulator.simulate_result("confirmed")
        simulator.prepare_next()
        self.assertEqual(simulator.journal[-1].event, "prepared")
        self.assertEqual(simulator.snapshot(), self.initial)
        simulator.simulate_result("confirmed")
        self.assertEqual([r.event for r in simulator.journal],
                         ["session_opened", "prepared", "mutation_requested", "result_confirmed"])
        self.assertEqual([r.sequence for r in simulator.journal], [1, 2, 3, 4])

    def test_off12_duplicate_resource_owner_and_duplicate_session_refused(self):
        first = self.simulator()
        first.open()
        for duplicate in (self.simulator("session-b"), self.simulator("session-a", ("other-body",))):
            with self.subTest(duplicate=duplicate), self.assertRaisesRegex(TransactionError, "duplicate"):
                duplicate.open()
        self.assertEqual(first.snapshot(), self.initial)

    def test_disjoint_sessions_can_coexist_but_no_partial_reservation(self):
        first = self.simulator()
        first.open()
        denied = self.simulator("session-b", ("other-body", "synthetic-body"))
        with self.assertRaises(TransactionError):
            denied.open()
        separate = self.simulator("session-b", ("other-body",))
        separate.open()
        self.assertEqual(separate.state, "ready")

    def test_off12_timeout_disconnect_before_after_all_require_review(self):
        for outcome in ("timeout_before", "timeout_after", "disconnect_before", "disconnect_after"):
            with self.subTest(outcome=outcome):
                simulator = self.simulator(session=outcome, resources=(outcome,))
                simulator.open()
                simulator.prepare_next()
                simulator.simulate_result(outcome)
                self.assertEqual(simulator.state, "needs_review")
                expected_ap = b"AP-new" if outcome.endswith("after") else b"AP-old"
                self.assertEqual(simulator.snapshot()["ap"], expected_ap)
                self.assertEqual(simulator.completed_operations, 0)
                for action in (simulator.prepare_next, simulator.resume, simulator.close,
                               lambda: simulator.simulate_result("confirmed")):
                    with self.assertRaises(TransactionError):
                        action()
                self.assertEqual(simulator.snapshot()["ap"], expected_ap)

    def test_off12_partial_result_stays_unresolved_no_automatic_restore(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        simulator.simulate_result("partial", partial_bytes=b"AP-nld")
        snapshot = simulator.snapshot()
        self.assertEqual(snapshot["ap"], b"AP-nld")
        self.assertEqual(simulator.reconcile(snapshot, "fixture-observation-partial"), "partial_or_mixed_state")
        self.assertEqual(simulator.state, "needs_review")
        self.assertEqual(simulator.snapshot(), snapshot)
        with self.assertRaises(TransactionError):
            simulator.resume()
        with self.assertRaises(TransactionError):
            simulator.close()

    def test_off12_uncertain_ownership_retained_against_second_session(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        simulator.simulate_result("timeout_after")
        with self.assertRaises(TransactionError):
            self.simulator("session-b").open()

    def test_off12_reconcile_applied_requires_resume_and_does_not_repeat_mutation(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        simulator.simulate_result("timeout_after")
        self.assertEqual(simulator.reconcile(simulator.snapshot(), "fixture-observation-after"), "applied")
        self.assertEqual(simulator.state, "reconciled")
        self.assertEqual(simulator.completed_operations, 1)
        with self.assertRaises(TransactionError):
            simulator.prepare_next()
        simulator.resume()
        self.run_confirmed(simulator)
        requested = [r.operation_id for r in simulator.journal if r.event == "mutation_requested"]
        self.assertEqual(requested, ["change-ap", "change-cp"])
        self.assertEqual(simulator.state, "complete")

    def test_off12_reconciled_not_applied_allows_explicit_new_prepared_attempt_only(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        simulator.simulate_result("disconnect_before")
        self.assertEqual(simulator.reconcile(simulator.snapshot(), "fixture-before"), "not_applied")
        with self.assertRaises(TransactionError):
            simulator.simulate_result("confirmed")
        simulator.resume()
        simulator.prepare_next()
        prepared = [dict(r.facts)["attempt"] for r in simulator.journal if r.event == "prepared"]
        self.assertEqual(prepared, ["1", "2"])
        simulator.simulate_result("confirmed")
        self.assertEqual(simulator.completed_operations, 1)

    def test_reconciliation_requires_complete_matching_observation_and_reference(self):
        simulator = self.simulator()
        simulator.open()
        simulator.interrupt_boundary()
        for observed, reference in (({"ap": b"AP-old"}, "partial-set"),
                                    (dict(self.initial, cp=b"CP-new"), "invented"),
                                    (simulator.snapshot(), "UNKNOWN")):
            with self.subTest(reference=reference), self.assertRaises(TransactionError):
                simulator.reconcile(observed, reference)
        self.assertEqual(simulator.state, "needs_review")

    def test_off13_all_inter_object_boundaries_reconcile_without_implicit_atomicity(self):
        for boundary in range(len(self.operations) + 1):
            with self.subTest(boundary=boundary):
                simulator = self.simulator(f"boundary-{boundary}", (f"body-{boundary}",))
                simulator.open()
                for _ in range(boundary):
                    self.run_confirmed(simulator)
                snapshot = simulator.snapshot()
                self.assertEqual(snapshot["ap"], b"AP-new" if boundary >= 1 else b"AP-old")
                self.assertEqual(snapshot["cp"], b"CP-new" if boundary >= 2 else b"CP-old")
                simulator.interrupt_boundary()
                self.assertEqual(simulator.state, "needs_review")
                self.assertEqual(simulator.reconcile(snapshot, f"boundary-evidence-{boundary}"), "confirmed_boundary")
                self.assertEqual(simulator.snapshot(), snapshot)
                simulator.resume()
                while simulator.state != "complete":
                    self.run_confirmed(simulator)
                simulator.close()
                self.assertEqual(simulator.snapshot(), {"ap": b"AP-new", "cp": b"CP-new", "resource": b"unchanged"})

    def test_off13_prepared_before_send_boundary_is_not_assumed_applied(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        simulator.interrupt_boundary()
        self.assertEqual(simulator.snapshot(), self.initial)
        self.assertEqual(simulator.reconcile(simulator.snapshot(), "prepared-not-sent"), "not_applied")
        simulator.resume()
        self.assertEqual(simulator.completed_operations, 0)
        self.assertEqual(simulator.state, "ready")

    def test_off13_second_object_uncertainty_preserves_completed_first_object(self):
        simulator = self.simulator()
        simulator.open()
        self.run_confirmed(simulator)
        simulator.prepare_next()
        simulator.simulate_result("disconnect_before")
        snapshot = simulator.snapshot()
        self.assertEqual(snapshot["ap"], b"AP-new")
        self.assertEqual(snapshot["cp"], b"CP-old")
        self.assertEqual(simulator.reconcile(snapshot, "second-object-before"), "not_applied")
        simulator.resume()
        self.run_confirmed(simulator)
        self.assertEqual(simulator.completed_operations, 2)
        self.assertEqual([r.operation_id for r in simulator.journal if r.event == "mutation_requested"],
                         ["change-ap", "change-cp", "change-cp"])

    def test_off13_uncertain_last_object_needs_resume_before_close(self):
        simulator = self.simulator()
        simulator.open()
        self.run_confirmed(simulator)
        simulator.prepare_next()
        simulator.simulate_result("timeout_after")
        self.assertEqual(simulator.reconcile(simulator.snapshot(), "last-after"), "applied")
        with self.assertRaises(TransactionError):
            simulator.close()
        simulator.resume()
        simulator.close()
        self.assertEqual(simulator.state, "closed")
        self.simulator("replacement-session").open()

    def test_journal_snapshot_records_are_append_only_to_caller(self):
        simulator = self.simulator()
        simulator.open()
        earlier = simulator.journal
        self.run_confirmed(simulator)
        self.assertEqual(len(earlier), 1)
        self.assertEqual(simulator.journal[:len(earlier)], earlier)
        with self.assertRaises(FrozenInstanceError):
            earlier[0].event = "forged"
        snapshot = simulator.snapshot()
        snapshot["ap"] = b"forged"
        self.assertEqual(simulator.snapshot()["ap"], b"AP-new")

    def test_bad_plan_category_order_duplicate_id_and_size_refused(self):
        plans = [(Operation("one", "ap", b"wrong!", b"AP-new"),),
                 (Operation("one", "ap", b"AP-old", b"AP-new", "reboot"),),
                 (Operation("one", "ap", b"AP-old", b"larger!"),),
                 (self.operations[0], self.operations[0])]
        for plan in plans:
            with self.subTest(plan=plan), self.assertRaises(TransactionError):
                TransactionSimulator("bad", ("body",), self.initial, plan, self.registry)

    def test_invalid_partial_outcome_does_not_mutate_or_consume_prepare(self):
        simulator = self.simulator()
        simulator.open()
        simulator.prepare_next()
        for partial in (None, b"short", b"AP-old", b"AP-new"):
            with self.subTest(partial=partial), self.assertRaises(TransactionError):
                simulator.simulate_result("partial", partial_bytes=partial)
        self.assertEqual(simulator.state, "prepared")
        self.assertEqual(simulator.snapshot(), self.initial)
        self.assertFalse(simulator.device_eligible)


if __name__ == "__main__":
    unittest.main()
