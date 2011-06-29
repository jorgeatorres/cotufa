# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, make_response, jsonify
import imdb

from cotufa import app, db, model


@app.route('/')
@app.route('/movies/')
def movies_list():
    movies = model.Movie.query.order_by('created_on desc').limit(20)
    return render_template('list.html', movies=movies)

@app.route('/movies/<id>')
def movies_movie(id):
    movie = model.Movie.query.filter_by(id=id).first_or_404()
    return render_template('movie-body.html', movie=movie)

@app.route('/movies/<id>/cover.jpg')
def movies_cover(id):
    movie = model.Movie.query.filter_by(id=id).first_or_404()

    response = make_response(movie.cover)
    response.headers['Content-Type'] = 'image/jpg'
    response.headers['Content-Disposition'] = 'inline; filename=movie-cover-%s.jpg' % movie.id
    return response
    
@app.route('/movies/<id>/set_attr')
def movies_set_attr(id):
    movie = model.Movie.query.filter_by(id=id).first_or_404()
    
    name = request.args.get('name')
    _value = request.args.get('value')
    value = _value

    if name == 'seen_on':
        if value == '':
            value = None
        else:
            import datetime
            value = datetime.datetime.strptime(value, '%Y-%m-%d')

    setattr(movie, name, value)

    db.session.commit()

    return jsonify({'_status': u'ok', 'name': name, 'value': _value})
    
@app.route('/movies/<id>/notes/save', methods=['POST'])
def movies_notes_save(id):
    movie = model.Movie.query.filter_by(id=id).first_or_404()
    movie.notes = request.form['notes']
    db.session.commit()
    return jsonify({'_status': u'ok', 'notes': request.form['notes']})


@app.route('/movies/search', methods=['POST'])
def movies_search():
    im = imdb.IMDb()
    _results = im.search_movie(request.form['search'])
    
    results = []
    
    for m in _results[:5]:
        seen = (model.Movie.query.filter_by(id=m.movieID).count() > 0)
        im.update(m)

        cast = []
        for c in m.get('cast')[:5]:
            cast.append(c['name'])
        
        results.append({'title': m['title'],
                        'year': m['year'],
                        'id': m.movieID, 
                        'seen': seen,
                        'cover': m.get('cover url', None),
                        'cast': cast})
    
    return render_template('search-results.html', results=results)

@app.route('/movies/add/<id>')
def movies_add(id):
    data = {}
    
    im = imdb.IMDb().get_movie(id)
    
    data['id'] = int(id)
    data['cover_url'] = im.get('cover url', None)
    data['title'] = im['title']
    data['year'] = None if im['year'] == '????' else int(im['year'])
    data['directors'] = [(int(x.personID), x['name']) for x in im.get('director')]
    
    data['cast'] = []
    
    for c in im.get('cast'):
        chars = c.currentRole if isinstance(c.currentRole, list) else [c.currentRole]
        
        for ch in chars:
            data['cast'].append((int(c.personID), c['name'], ch.get('name')))
    
    
    # cover img
    cover = None
    import urllib2
    if data['cover_url'] is not None:
        cover_h = urllib2.urlopen(data['cover_url'])
        cover = cover_h.read()
        cover_h.close()
        
    movie = model.Movie.query.filter_by(id=data['id']).first()
    
    if movie is None:
        movie = model.Movie(id=data['id'], title=data['title'], year=data['year'], rating=None)
        
        for d in data['directors']:
            movie.people.append(model.MovieRole(person=model.Person.get_or_create(d[0], d[1]), role_type=u'director'))
            
        for c in data['cast']:
            movie.people.append(model.MovieRole(person=model.Person.get_or_create(c[0], c[1]),
                                                role_type=u'cast',
                                                character=c[2]))
                                                
        if cover is not None:
            movie.cover = cover
        
        db.session.add(movie)
        db.session.commit()
        
    return redirect(url_for('movies_list'))
