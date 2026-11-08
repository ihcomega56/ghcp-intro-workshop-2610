import logging
import sqlite3

import streamlit as st

from order_store import load_order_history, save_order


MENU = {
    "コーヒー": 350,
    "カフェラテ": 450,
    "チーズケーキ": 500,
}

logger = logging.getLogger(__name__)


def show_order_screen() -> None:
    st.title("☕ カフェ注文シミュレーター")
    st.header("メニュー")
    for name, price in MENU.items():
        label, action = st.columns([3, 1])
        label.write(f"{name} — {price:,} 円")
        if action.button("追加", key=f"add_{name}"):
            st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

    st.header("カート")
    if st.session_state.cart:
        total = 0
        for name, quantity in st.session_state.cart.items():
            subtotal = MENU[name] * quantity
            total += subtotal
            st.write(f"{name} × {quantity} — {subtotal:,} 円")
        st.write(f"**合計金額: {total:,} 円**")
    else:
        st.info("カートは空です。メニューから商品を追加してください。")
        st.write("**合計金額: 0 円**")

    order, clear = st.columns(2)
    if order.button("注文を確定", disabled=not st.session_state.cart):
        try:
            total = save_order(st.session_state.cart, MENU)
        except (sqlite3.Error, OSError, ValueError):
            logger.exception("Failed to save order")
            st.error(
                "注文を保存できませんでした。カートはそのままです。"
                "保存先の空き容量やアクセス権を確認して、再度お試しください。"
            )
        else:
            st.session_state.order_total = total
            st.session_state.cart = {}
            st.rerun()

    if clear.button("カートを空にする", disabled=not st.session_state.cart):
        st.session_state.cart = {}
        st.rerun()

    if "order_total" in st.session_state:
        st.success(
            f"ご注文ありがとうございます！ 注文金額: {st.session_state.pop('order_total'):,} 円"
        )


def show_sales_dashboard() -> None:
    st.title("売上ダッシュボード")
    st.caption("保存された全期間の注文を集計しています。")
    try:
        history = load_order_history()
    except (sqlite3.Error, OSError):
        logger.exception("Failed to load order history")
        st.error(
            "注文履歴を読み込めませんでした。"
            "保存先のファイルやアクセス権を確認して、再度お試しください。"
        )
        return

    total = sum(row["subtotal"] for row in history)
    st.metric("合計売上", f"{total:,} 円")
    if not history:
        st.info("注文履歴はまだありません。注文画面で注文を確定すると記録されます。")
        return

    sales: dict[str, dict[str, int]] = {}
    for row in history:
        product = sales.setdefault(row["product"], {"販売数": 0, "売上（円）": 0})
        product["販売数"] += row["quantity"]
        product["売上（円）"] += row["subtotal"]
    chart_data = [
        {"商品": name, **values} for name, values in sorted(sales.items())
    ]
    st.header("商品別の販売数")
    st.bar_chart(chart_data, x="商品", y="販売数", x_label="商品", y_label="販売数（個）")
    st.header("商品別の売上")
    st.bar_chart(chart_data, x="商品", y="売上（円）", x_label="商品", y_label="売上（円）")

    st.header("注文履歴")
    st.caption("新しい注文から表示します。同じ注文 ID の行が1件の注文の明細です。")
    st.dataframe(
        [
            {
                "注文 ID": row["order_id"],
                "日時": row["ordered_at"],
                "商品": row["product"],
                "数量": row["quantity"],
                "単価（円）": row["unit_price"],
                "明細金額（円）": row["subtotal"],
                "注文合計（円）": row["order_total"],
            }
            for row in history
        ],
        hide_index=True,
    )


st.set_page_config(page_title="カフェ注文シミュレーター", page_icon="☕")
if "cart" not in st.session_state:
    st.session_state.cart = {}

screen = st.sidebar.radio("画面", ["注文", "売上ダッシュボード"])
if screen == "注文":
    show_order_screen()
else:
    show_sales_dashboard()
