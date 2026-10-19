import pandas as pd

df = pd.DataFrame({
    "order_no": ["EM-101", "EM-102", "EM-103"],
    "customer": ["Karim Fathy", "Hana Mostafa", "Youssef Samir"],
    "product_name": ["Organic Fertilizer", "Tomato Seeds", "Drip Irrigation Kit"],
    "amount": [5, 12, 2],
    "price": [320, 150, 1250],
    "city": ["Ismailia", "Assiut", "Cairo"],
    "date": ["2026-10-16", "2026-10-16", "2026-10-17"],
})
df.to_excel("sample_data/email_inbox/orders_branch2.xlsx", index=False)
print("Created sample_data/email_inbox/orders_branch2.xlsx")