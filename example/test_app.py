import sqlite3
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from order_store import load_order_history, save_order


class CafeAppTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = self.enterContext(TemporaryDirectory())
        self.db = Path(directory) / "orders.db"
        self.save = self.enterContext(
            patch(
                "order_store.save_order",
                side_effect=lambda cart, menu: save_order(cart, menu, self.db),
            )
        )
        self.load = self.enterContext(
            patch(
                "order_store.load_order_history",
                side_effect=lambda: load_order_history(self.db),
            )
        )
        self.app = AppTest.from_file(
            str(Path(__file__).with_name("app.py")), default_timeout=30
        ).run()
        self.assertFalse(self.app.exception)

    def test_cart_and_navigation(self) -> None:
        self.assertTrue(self.app.button(key="confirm_order").disabled)
        self.assertTrue(self.app.button(key="clear_cart").disabled)
        self.app.button(key="add_コーヒー").click().run()
        self.app.button(key="add_コーヒー").click().run()
        self.assertEqual(self.app.session_state.cart, {"コーヒー": 2})
        self.app.radio[0].set_value("売上ダッシュボード").run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.metric[0].value, "0 円")
        self.app.radio[0].set_value("注文").run()
        self.assertEqual(self.app.session_state.cart, {"コーヒー": 2})
        self.app.button(key="clear_cart").click().run()
        self.assertEqual(self.app.session_state.cart, {})
        self.assertTrue(self.app.button(key="confirm_order").disabled)

    def test_checkout_and_dashboard(self) -> None:
        for name in ("コーヒー", "コーヒー", "カフェラテ", "チーズケーキ"):
            self.app.button(key=f"add_{name}").click().run()
        self.app.button(key="confirm_order").click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state.cart, {})
        self.assertIn("1,650", self.app.success[0].value)
        history = load_order_history(self.db)
        self.assertEqual(sum(row["subtotal"] for row in history), 1650)
        self.assertEqual(len(history), 3)
        self.app.radio[0].set_value("売上ダッシュボード").run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.metric[0].value, "1,650 円")
        self.assertEqual(len(self.app.dataframe[0].value), 3)

    def test_failed_checkout_preserves_cart(self) -> None:
        self.app.button(key="add_コーヒー").click().run()
        self.save.side_effect = OSError("Test write failure")
        with self.assertLogs(level="ERROR"):
            self.app.button(key="confirm_order").click().run()
        self.assertFalse(self.app.exception)
        self.assertEqual(self.app.session_state.cart, {"コーヒー": 1})
        self.assertIn("注文を保存できませんでした", self.app.error[0].value)
        self.assertFalse(self.db.exists())

    def test_dashboard_read_failure(self) -> None:
        self.load.side_effect = sqlite3.DatabaseError("Test read failure")
        with self.assertLogs(level="ERROR"):
            self.app.radio[0].set_value("売上ダッシュボード").run()
        self.assertFalse(self.app.exception)
        self.assertIn("注文履歴を読み込めませんでした", self.app.error[0].value)


if __name__ == "__main__":
    unittest.main()
