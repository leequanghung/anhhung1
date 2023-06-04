from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees')
    employees = c.fetchall()
    return render_template('index.html', employees=employees)

@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        office = request.form['office']
        age = request.form['age']
        start_date = request.form['start_date']
        salary = request.form['salary']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('INSERT INTO employees (name, position, office, age, start_date, salary) VALUES (?, ?, ?, ?, ?, ?)',
            (name, position, office, age, start_date, salary))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees WHERE id = ?', (id,))
    employee = c.fetchone()

    if request.method == 'POST':
        name = request.form['name']
        position = request.form['position']
        office = request.form['office']
        age = request.form['age']
        start_date = request.form['start_date']
        salary = request.form['salary']

        c.execute('UPDATE employees SET name = ?, position = ?, office = ?, age = ?, start_date = ?, salary = ? WHERE id = ?',
            (name, position, office, age, start_date, salary, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
        
    return render_template('edit.html', employee=employee)

@app.route('/delete/<int:id>')
def delete_employee(id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('DELETE FROM employees WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))
@app.route('/search', methods=['GET', 'POST'])
def search():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Lấy các tham số đã truyền qua phương thức GET
    search_term = request.args

    # Thiết lập các giá trị mặc định cho các trường
    name = search_term.get('name', '')
    position = search_term.get('position', '')
    office = search_term.get('office', '')
    age = int(search_term.get('age', 0))
    start_date = search_term.get('start_date', '1900-01-01')
    salary = float(search_term.get('salary', 0))

    # Tạo truy vấn SQL dựa trên các giá trị được cung cấp
    query = "SELECT * FROM employees WHERE name LIKE ? AND position LIKE ? AND office LIKE ? AND age >= ? AND start_date >= ? AND salary >= ?"

    # Thực thi truy vấn SQL với các tham số được cung cấp
    c.execute(query, ('%'+name+'%', '%'+position+'%', '%'+office+'%', age, start_date, salary))
    results = c.fetchall()

    # Giải phóng các tài nguyên
    c.close()
    conn.close()

    # Kiểm tra kết quả tìm kiếm
    if results:
        return render_template('search.html', results=results, search_term=search_term)
    else:
        message = "Không tìm thấy kết quả cho từ khóa: '{}'".format(' '.join(search_term.values()))
        return render_template('search.html', message=message)





if __name__ == '__main__':
    app.run(debug=True)
