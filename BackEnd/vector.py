from sentence_transformers import SentenceTransformer
import psycopg2

# 🧠 تحميل الموديل
model = SentenceTransformer('all-MiniLM-L6-v2')

# ⚙️ إعدادات قاعدة البيانات
DB_CONFIG = {
    "host": "ep-falling-credit-adzqnwm1-pooler.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_QblIehwU2tk9",
    "sslmode": "require"
}

# 🔄 تحويل المصفوفة إلى شكل يقبله pgvector
def to_pg_vector(vec):
    return vec.tolist() if vec is not None else None

# 🧩 تحديث بيانات العملاء
def embed_and_update_customers():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT customer_id, name, email, country FROM orders.customers;")
    rows = cur.fetchall()

    for i, (cid, name, email, country) in enumerate(rows, start=1):
        name_vec = model.encode(name) if name else None
        email_vec = model.encode(email) if email else None
        country_vec = model.encode(country) if country else None

        cur.execute("""
            UPDATE orders.customers
            SET name_vector = %s, email_vector = %s, country_vector = %s
            WHERE customer_id = %s
        """, (to_pg_vector(name_vec),
              to_pg_vector(email_vec),
              to_pg_vector(country_vec),
              cid))

        if i % 50 == 0:
            conn.commit()
            print(f"✅ Committed {i} customer embeddings so far...")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Customers embeddings done.")

# 🧩 تحديث بيانات المنتجات
def embed_and_update_products():
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT product_id, product_name, category FROM orders.products;")
    rows = cur.fetchall()

    for i, (pid, pname, cat) in enumerate(rows, start=1):
        pname_vec = model.encode(pname) if pname else None
        cat_vec = model.encode(cat) if cat else None

        cur.execute("""
            UPDATE orders.products
            SET product_name_vector = %s, category_vector = %s
            WHERE product_id = %s
        """, (to_pg_vector(pname_vec),
              to_pg_vector(cat_vec),
              pid))

        if i % 50 == 0:
            conn.commit()
            print(f"✅ Committed {i} product embeddings so far...")

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Products embeddings done.")

# 🚀 نقطة البداية
if __name__ == "__main__":
    embed_and_update_customers()
    embed_and_update_products()
    print("🎯 All local embeddings stored successfully in Neon DB.")
