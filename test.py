@app.route('/user/<id>/edit', methods = ['GET', 'POST'])
def edit_u(id):
    with pdms.connect_db() as conn:
        usr = pdms.get_user(conn, id)
        if not usr:
            abort(404)
        name = usr[1]
        email = usr[2]
        password = usr[3]
        errors = {}
        if request.method == 'POST':
            name = request.form.get('name')
            if not name:
                errors['name'] = 'empty name'
            email = request.form.get('email')
            if not email:
                errors['email'] = 'empty email'
            password = request.form.get('password')
            if not password:
                errors['password'] = 'empty password'
            if len(password) < 8:
                errors['password'] = 'Password too short (minimum = 8)'
            conf_password = request.form.get('conf_password')
            if password != conf_password:
                errors['conf_password'] = 'Passwords not matching'
            if len(errors) == 0:
                pdms.update_user(conn, id, name, email, password)
                return redirect('/')
        return render_template('user-edit.html', user=usr,
                                name=name, email=email, password=password, errors=errors)
