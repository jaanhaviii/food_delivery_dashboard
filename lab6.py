import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Food Delivery Analytics Dashboard")
st.write("Analyze food delivery data using interactive charts.")

df = pd.read_csv(r"C:\Users\doma9235\Downloads\food_delivery_dataset.csv")

st.sidebar.header("Filters")

location = st.sidebar.selectbox(
    "Select Location",
    ["All"] + list(df["location"].unique())
)

method = st.sidebar.selectbox(
    "Delivery Method",
    ["All"] + list(df["delivery_method"].unique())
)

rating = st.sidebar.slider(
    "Minimum Customer Rating",
    float(df["customer_rating"].min()),
    float(df["customer_rating"].max()),
    float(df["customer_rating"].min())
)

filtered_df = df.copy()

if location != "All":
    filtered_df = filtered_df[filtered_df["location"] == location]

if method != "All":
    filtered_df = filtered_df[filtered_df["delivery_method"] == method]

filtered_df = filtered_df[
    filtered_df["customer_rating"] >= rating
]

st.subheader("Filtered Dataset")
st.dataframe(filtered_df)

st.subheader("Summary Statistics")
st.write(filtered_df.describe())

st.subheader("Average Order Value by Delivery Method")

fig, ax = plt.subplots()

filtered_df.groupby("delivery_method")["order_value"].mean().plot(
    kind="bar",
    ax=ax
)

ax.set_ylabel("Average Order Value")

st.pyplot(fig)

st.subheader("Traffic Condition Distribution")

fig, ax = plt.subplots()

filtered_df["traffic_condition"].value_counts().plot(
    kind="pie",
    autopct="%1.1f%%",
    ax=ax
)

ax.set_ylabel("")

st.pyplot(fig)

st.subheader("Delivery Delay Distribution")

fig, ax = plt.subplots()

filtered_df["delivery_delay"].hist(
    bins=10,
    ax=ax
)

ax.set_xlabel("Delivery Delay")

st.pyplot(fig)

st.subheader("Delivery Delay vs Order Value")

fig, ax = plt.subplots()

ax.scatter(
    filtered_df["delivery_delay"],
    filtered_df["order_value"]
)

ax.set_xlabel("Delivery Delay")
ax.set_ylabel("Order Value")

st.pyplot(fig)

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered CSV",
    data=csv,
    file_name="filtered_food_delivery.csv",
    mime="text/csv"
)