from sqlalchemy import create_engine, inspect, text
import os
from tabulate import tabulate
from datetime import datetime
import pandas as pd


# ✅ Указываем или загружаем строку подключения
DATABASE_URL = "postgresql://postgres:Kogp9He!gds@database-1.ctm2g2is8193.eu-central-1.rds.amazonaws.com:5432/helth_db"

# 📂 Пути для сохранения файлов
text_output = "db_snapshot.txt"
csv_output_dir = "db_exports"

# 📁 Создаём папку для .csv, если не существует
os.makedirs(csv_output_dir, exist_ok=True)

# 🔌 Подключение к базе
engine = create_engine(DATABASE_URL)
inspector = inspect(engine)

with engine.connect() as connection, open(text_output, "w", encoding="utf-8") as f:
    f.write(f"📅 Snapshot from: {datetime.utcnow()} UTC\n")
    f.write("✅ Подключено к базе данных\n\n")

    tables = inspector.get_table_names()
    f.write(f"📋 Таблицы в БД ({len(tables)}): {tables}\n\n")

    for table_name in tables:
        f.write(f"🔎 Таблица: {table_name}\n")
        columns = inspector.get_columns(table_name)
        col_info = [(col["name"], str(col["type"]), col["nullable"]) for col in columns]
        f.write("📦 Колонки:\n")
        f.write(tabulate(col_info, headers=["Имя", "Тип", "Nullable"], tablefmt="grid"))
        f.write("\n")

        f.write("🧾 Первые 10 строк данных:\n")
        try:
            result = connection.execute(text(f'SELECT * FROM "{table_name}" LIMIT 10'))
            rows = result.fetchall()
            f.write(tabulate(rows, headers=result.keys(), tablefmt="grid"))
            f.write("\n")

            # 📥 Экспорт в CSV всей таблицы
            full_df = pd.read_sql(text(f'SELECT * FROM "{table_name}"'), connection)
            csv_path = os.path.join(csv_output_dir, f"{table_name}.csv")
            full_df.to_csv(csv_path, index=False)
        except Exception as e:
            f.write(f"⚠️ Ошибка при извлечении данных или экспорте CSV: {e}\n")
        
        f.write("\n" + "-"*80 + "\n\n")

print(f"✅ Снимок базы сохранён в {text_output}")
print(f"✅ CSV-файлы сохранены в папке: {csv_output_dir}")