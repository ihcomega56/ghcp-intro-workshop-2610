import streamlit as st


MENU = {
    "コーヒー": 400,
    "紅茶": 350,
    "ケーキ": 500,
}

st.set_page_config(page_title="カフェ注文", page_icon="☕")
st.title("カフェ注文シミュレーター")
st.write("商品を選んで、注文を試してみましょう。")

if "cart" not in st.session_state:
    st.session_state.cart = {}
if "ordered" not in st.session_state:
    st.session_state.ordered = False

st.subheader("メニュー")
columns = st.columns(len(MENU))

for column, (item, price) in zip(columns, MENU.items()):
    with column:
        st.write(f"**{item}**")
        st.write(f"¥{price:,}")
        if st.button(f"{item}を追加", disabled=st.session_state.ordered):
            st.session_state.cart[item] = st.session_state.cart.get(item, 0) + 1

st.subheader("カート")
if not st.session_state.cart:
    st.write("カートは空です。")
else:
    total = 0
    for item, quantity in st.session_state.cart.items():
        subtotal = MENU[item] * quantity
        total += subtotal
        st.write(f"{item} × {quantity}：¥{subtotal:,}")
    st.write(f"**合計：¥{total:,}**")

if not st.session_state.ordered:
    if st.button("注文を確定", disabled=not st.session_state.cart):
        st.session_state.ordered = True
        st.rerun()
else:
    st.success("注文を確定しました。")
