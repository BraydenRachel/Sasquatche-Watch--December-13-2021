from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route('/new/sighting')
def new_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_sighting.html',user=User.get_by_id(data))


@app.route('/create/sighting',methods=['POST'])
def create_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_sasquatches(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "number": int(request.form["number"]),
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/dashboard')

@app.route('/edit/sighting/<int:id>')
def edit_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_sighting.html",edit=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/update/sighting',methods=['POST'])
def update_sighting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_sasquatches(request.form):
        return redirect('/new/sighting')
    data = {
        "location": request.form["location"],
        "what_happened": request.form["what_happened"],
        "date_of_sighting": request.form["date_of_sighting"],
        "number": request.form["number"],
        "id": request.form['id']
    }
    Recipe.update(data)
    return redirect('/dashboard')

@app.route('/sighting/<int:id>')
def show_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("show_sighting.html",recipe=Recipe.get_one(data),user=User.get_by_id(user_data))

@app.route('/destroy/sighting/<int:id>')
def destroy_sighting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')