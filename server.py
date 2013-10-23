from flask import Flask, render_template
import json, parser, os

app = Flask(__name__)
laws = json.loads(open('laws.json', 'r').read())

def get_or_die(file_urn, laws):
    tmp_laws = []
    for index, l in enumerate(laws):
        if l:
            filename = l['urn'].split(';')[0][:-6]+'::'+l['urn'].split(';')[1] + '.json'
        if file_urn == filename:
            l = parser.getCamaraUrl(l)
            l = parser.getCamaraText(l)
            tmp_laws.append(l)
        else:
            tmp_laws.append(l)
    if os.path.isfile('data/'+file_urn):
        update = open('laws.json', 'w')
        update.write(json.dumps(laws, indent=4))
        update.close()
        law = json.loads(open('data/'+file_urn).read())
        return law
    else:
        return {'raw' : 'Not Found!'}
                
@app.route('/<tipo>/<numero>/<ano>')
def index(tipo, numero, ano, laws=laws):
    file_urn = 'urn:lex:br:federal:'+tipo+':'+ano+'::'+numero+'.json'
    if os.path.isfile('data/'+file_urn):
        law = json.loads(open('data/'+file_urn).read())
        return render_template('law.html', law=law)
    else:
        law = get_or_die(file_urn, laws)
        return render_template('law.html', law=law)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
