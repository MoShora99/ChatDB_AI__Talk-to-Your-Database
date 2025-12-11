from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import google.generativeai as genai
import psycopg2
from sentence_transformers import SentenceTransformer
import json
import numpy as np
from prompts import build_prompt,general_prompt
# إعداد السيرفر
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔑 إعداد مفتاح Gemini API
genai.configure(api_key="AIzaSyDB6jlLj56wexb9V4BYZjuLuUuAYiGc5N0")

DB_CONFIG={
   "host": "ep-falling-credit-adzqnwm1-pooler.c-2.us-east-1.aws.neon.tech",
    "database": "neondb",
    "user": "neondb_owner",
    "password": "npg_QblIehwU2tk9",
    "sslmode": "require"

}

embedder = SentenceTransformer('all-MiniLM-L6-v2')
def vector_search(table, columns, query_text, limit=3):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # نحول النص لـ vector
    vec = embedder.encode(query_text)
    vec_str = np.array2string(vec, separator=',')[1:-1]

    # نبني SQL للبحث
    col = columns[0]
    col_id=table.replace("orders.", "")
    sql = f"""
    select {col_id[:-1]}_id from(
    SELECT {col_id[:-1]}_id ,{col} <-> '[{vec_str}]'::vector as x
    FROM   {table})where x <0.9
    
    LIMIT {limit};
    """
    print(sql)
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    
    return [r[0] for r in rows]
    
def execute_sql(sql_query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(sql_query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()

    data = [dict(zip(columns, row)) for row in rows]
    return data
# موديل البيانات
class Message(BaseModel):
    text: str

@app.post("/chat")
async def chat_with_bot(message: Message):
    try:
        
        check=f"""
        {build_prompt}
        سؤال المستخدم:
        {message.text}
        """
        general=f"""
        {general_prompt}
        Customer message
        {message.text}
        """
        model = genai.GenerativeModel("gemini-2.5-flash")
   
        # ✅ الموديل بياخد النص جوه list فيها text part
        response_check = model.generate_content([{"text": check}])
        
        # ✅ النتيجة الصحيحة من Gemini
        response_check = response_check.text.strip()
        if "```" in response_check:
            response_check = response_check.replace("```json", "").replace("```", "").strip()
        result=json.loads(response_check) 
        print(response_check)
        if result["vector_search"]["needed"]:
            ids = vector_search(
                result["vector_search"]["table"],
                result["vector_search"]["columns"],
                result["vector_search"]["query_text"]
            )

            if not ids:  # ✅ لو مفيش نتائج من الـ vector search
                general = model.generate_content([{"text": general}])
        
                # ✅ النتيجة الصحيحة من Gemini
                general = general.text.strip()
                return {"reply": general}

            # ✅ لو فيه نتائج — نستبدل <ids> داخل الاستعلام
            sql_query = result["sql_query"].replace("<ids>", ",".join(map(str, ids)))
        else:
            # لو مش محتاج vector search
            sql_query = result["sql_query"]

        print(sql_query)
        if not sql_query or sql_query.strip() == "":
                general = model.generate_content([{"text": general}])
        
                # ✅ النتيجة الصحيحة من Gemini
                general = general.text.strip()
                return {"reply": general}

        data = execute_sql(sql_query)


        # الخطوة 4: تنسيق الرد للمستخدم
        if not data:
            return {"reply": "❌ لا توجد نتائج مطابقة في قاعدة البيانات."}
        else:
            return {"reply": data}  # يرسلها كـ array للـ frontend
    except Exception as e:
        return {"reply": f"⚠️ حصل خطأ: {str(e)}"}
