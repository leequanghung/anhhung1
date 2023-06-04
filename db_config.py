import sqlite3

# Kết nối với database
conn = sqlite3.connect('employees.db')

# Lệnh SQL để xóa bảng employees nếu nó đã tồn tại
c = conn.cursor()
c.execute('''DROP TABLE IF EXISTS employees''')

# Tạo bảng Employees
def create_employees_table():
    c.execute('''CREATE TABLE employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    position TEXT NOT NULL,
                    office TEXT NOT NULL,
                    age INTEGER NOT NULL,
                    start_date TEXT NOT NULL,
                    salary REAL NOT NULL
                    )''')

# Đóng kết nối
conn.close()
