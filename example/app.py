import logging
import sqlite3
from base64 import b64encode
from html import escape
from pathlib import Path

import streamlit as st

from order_store import load_order_history, save_order


MENU = {
    "コーヒー": 350,
    "カフェラテ": 450,
    "チーズケーキ": 500,
}

logger = logging.getLogger(__name__)

PRODUCT_DETAILS = {
    "コーヒー": ("COFFEE", "香り豊かな一杯で、気持ちを切り替える。", "coffee"),
    "カフェラテ": ("CAFFÈ LATTE", "コーヒーとミルクが出会う、やさしい時間。", "latte"),
    "チーズケーキ": ("CHEESECAKE", "ひと息つく時間に、ちょっとしたご褒美を。", "cake"),
}


def product_illustration(kind: str) -> str:
    if kind == "cake":
        drawing = (
            '<path d="M25 94h112M37 84V57l80-24v51H37Z"/>'
            '<path d="m37 57 80 2M37 72h80M99 38l-8-10"/>'
            '<circle cx="89" cy="24" r="6"/>'
        )
    else:
        drawing = (
            '<ellipse cx="70" cy="49" rx="38" ry="12"/>'
            '<path d="M32 49v30c0 25 76 25 76 0V49M108 55h9'
            'c25 0 25 30 0 30h-10M21 110h99M53 27c-8-10 8-12 0-23'
            'M72 27c-8-10 8-12 0-23M91 27c-8-10 8-12 0-23"/>'
        )
        if kind == "latte":
            drawing += '<path d="M40 77c18 10 42 10 60 0M40 86c18 10 42 10 60 0"/>'
    svg = (
        '<svg viewBox="0 0 160 140" fill="none" stroke="currentColor" '
        'stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
        f'xmlns="http://www.w3.org/2000/svg">{drawing}</svg>'
    )
    image = b64encode(svg.encode("utf-8")).decode("ascii")
    return (
        '<span class="illustration" aria-hidden="true" '
        f'style="mask-image: url(data:image/svg+xml;base64,{image}); '
        f'-webkit-mask-image: url(data:image/svg+xml;base64,{image})"></span>'
    )


def show_hero(*, dashboard: bool = False) -> None:
    title = "Sales Dashboard" if dashboard else "日常に、<br>心が動く一杯を。"
    description = (
        "一杯から生まれる、小さなストーリーを数字で。"
        if dashboard
        else "お気に入りの一杯と、とっておきのひととき。<br>ここから、あなたのカフェ時間を。"
    )
    bottom = (
        ""
        if dashboard
        else '<div class="hero-bottom"><a href="#menu" target="_self">'
        'メニューを見る <span aria-hidden="true">↗</span></a>'
        '<span>GOOD COFFEE. GREAT MOMENTS.</span></div>'
    )
    st.html(
        f'<section class="hero{" hero--compact" if dashboard else ""}">'
        '<p class="eyebrow">CAFE / EVERYDAY, A LITTLE MORE SPECIAL.</p>'
        f'<h1>{title}</h1><p class="hero-copy">{description}</p>'
        f'<div class="hero-art">{product_illustration("coffee")}</div>'
        f"{bottom}</section>"
    )


def show_cart() -> None:
    with st.container(key="cart_panel"):
        details, summary = st.columns([1.5, 1], gap="large")
        with details:
            st.html(
                '<h2 class="cart-title">Your order</h2>'
                '<p class="cart-subtitle">カート / お選びいただいた商品</p>'
            )
            total = 0
            for name, quantity in st.session_state.cart.items():
                subtotal = MENU[name] * quantity
                total += subtotal
                st.html(
                    f'<div class="cart-row"><span>{escape(name)} × {quantity}</span>'
                    f"<span>¥{subtotal:,}</span></div>"
                )
            if not st.session_state.cart:
                st.html(
                    '<p class="cart-empty">カートは空です。<br>'
                    "メニューから、お気に入りを見つけてください。</p>"
                )
        with summary:
            st.html(
                '<p class="cart-total-label">合計金額（税込）</p>'
                f'<p class="cart-total">{total:,} <small>円</small></p>'
            )
            if st.button(
                "注文を確定",
                key="confirm_order",
                type="primary",
                disabled=not st.session_state.cart,
                use_container_width=True,
            ):
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

            if st.button(
                "カートを空にする",
                key="clear_cart",
                disabled=not st.session_state.cart,
                use_container_width=True,
            ):
                st.session_state.cart = {}
                st.rerun()


def show_order_screen() -> None:
    show_hero()
    st.html(
        '<section id="menu" class="section-heading">'
        '<div><h2>Our Menu</h2><p>メニュー</p></div>'
        '<span class="section-note">いつもの一杯も、はじめての味も。<br>'
        "気分に合わせて、お選びください。</span></section>"
    )
    for index, (column, (name, price)) in enumerate(
        zip(st.columns(3, gap="large"), MENU.items()), start=1
    ):
        english, description, kind = PRODUCT_DETAILS[name]
        with column, st.container(key=f"product_{index}"):
            st.html(
                f'<div class="product-art"><span class="product-number">0{index}</span>'
                f"{product_illustration(kind)}</div>"
                f'<p class="product-en">{english}</p>'
                f'<h3 class="product-name">{escape(name)}</h3>'
                f'<p class="product-description">{description}</p>'
                f'<p class="product-price">¥{price:,}<small>税込</small></p>'
            )
            if st.button("カートに追加 ＋", key=f"add_{name}", use_container_width=True):
                st.session_state.cart[name] = st.session_state.cart.get(name, 0) + 1

    show_cart()
    if "order_total" in st.session_state:
        st.success(
            f"ご注文ありがとうございます！ 注文金額: {st.session_state.pop('order_total'):,} 円"
        )


def show_sales_dashboard() -> None:
    show_hero(dashboard=True)
    st.html(
        '<section class="section-heading"><div><h2>Sales overview</h2>'
        "<p>売上ダッシュボード</p></div></section>"
    )
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


st.set_page_config(page_title="カフェ注文シミュレーター", page_icon="☕", layout="wide")
st.html(f"<style>{Path(__file__).with_name('styles.css').read_text(encoding='utf-8')}</style>")
if "cart" not in st.session_state:
    st.session_state.cart = {}

with st.container(key="site_header"):
    brand, navigation = st.columns([1, 2], vertical_alignment="center")
    with brand:
        st.html(
            '<div class="wordmark" aria-label="cafe カフェ注文シミュレーター">'
            'cafe<span>COFFEE &amp;<br>GOOD MOMENTS</span></div>'
        )
    with navigation:
        screen = st.radio(
            "画面",
            ["注文", "売上ダッシュボード"],
            horizontal=True,
            label_visibility="collapsed",
        )
if screen == "注文":
    show_order_screen()
else:
    show_sales_dashboard()

st.html(
    '<footer class="site-footer"><span>cafe / GOOD COFFEE. GREAT MOMENTS.</span>'
    "<span>カフェ注文シミュレーター</span></footer>"
)
