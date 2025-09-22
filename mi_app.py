from flask import Flask, render_template, request, redirect, url_for
import uuid

app = Flask(__name__)

# Almacenamiento en memoria (puedes cambiarlo a base de datos si lo deseas)
personalizaciones = {}

# Modelo de personalización (puedes expandirlo según necesidades)
class Personalizacion:
    def __init__(self, producto, color, herrajes):
        self.producto = producto
        self.color = color
        self.herrajes = herrajes

# Opciones disponibles
COLORES = ['negro', 'marron', 'marron claro']
HERRAJES = ['plata', 'dorado']


# Página principal para seleccionar carteras
@app.route('/', methods=['GET'])
def pagina_principal():
    return '''
    <style>
        body {
            background-image: url('/static/fondo.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
        }
        .navbar {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 56px;
            background: #4B2E19;
            color: #fff;
            display: flex;
            align-items: center;
            font-size: 1.3em;
            font-family: sans-serif;
            z-index: 1000;
            box-shadow: 0 2px 8px #0002;
            padding-left: 2em;
            letter-spacing: 1px;
        }
        .navbar-logo {
            height: 38px;
            width: auto;
            margin-right: 18px;
        }
        .navbar-title {
            font-weight: bold;
            letter-spacing: 2px;
        }
        .main-content {
            margin-top: 80px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 2.5em;
        }
        .modelo-container {
            display: flex;
            flex-direction: row;
            align-items: center;
            justify-content: center;
            background: rgba(255,255,255,0.92);
            border-radius: 12px;
            box-shadow: 0 0 10px #aaa;
            max-width: 700px;
            width: 95vw;
            padding: 2em 2em;
            margin: 0 auto;
        }
        .modelo-img {
            max-width: 220px;
            max-height: 260px;
            border-radius: 12px;
            box-shadow: 0 0 10px #aaa;
            margin-right: 32px;
            background: #fff;
        }
        .modelo-info {
            flex: 1;
        }
        .modelo-info h2 {
            margin-top: 0;
        }
        @media (max-width: 700px) {
            .modelo-container {
                flex-direction: column;
                align-items: center;
                padding: 1em 0.5em;
            }
            .modelo-img {
                margin-right: 0;
                margin-bottom: 1em;
            }
        }
    </style>
    <div class="navbar">
        <a href="/" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <img src="/static/logo.png" alt="Logo" class="navbar-logo">
            <span class="navbar-title">Teteu Cueros</span>
        </a>
    </div>
    <div class="main-content">
        <div class="modelo-container">
            <img src="/static/modelo1.jpg" alt="Modelo 1" class="modelo-img" onerror="this.style.display='none'">
            <div class="modelo-info">
                <h2>Modelo 1: Cartera Clásica</h2>
                <p><b>Medidas:</b> 30 de alto x 46 de ancho x 17 de profundidad</p>
                <a href="/personalizar_form?modelo=Cartera%20Cl%C3%A1sica" class="copy-btn" style="text-align:center;text-decoration:none;">Personalizar Cartera Clásica</a>
            </div>
        </div>
        <div class="modelo-container">
            <img src="/static/modelo2.jpg" alt="Modelo 2" class="modelo-img" onerror="this.style.display='none'">
            <div class="modelo-info">
                <h2>Modelo 2: Cartera Urbana</h2>
                <p><b>Medidas:</b> 26cm (ancho) x 22cm (alto) x 10cm (profundidad)</p>
                <a href="/personalizar_form?modelo=Cartera%20Urbana" class="copy-btn" style="text-align:center;text-decoration:none;">Personalizar Cartera Urbana</a>
            </div>
        </div>
    </div>
    '''

@app.route('/personalizar_form', methods=['GET'])
def formulario():
    modelo = request.args.get('modelo', 'Cartera')
    imagen = "/static/modelo1.jpg" if "Clásica" in modelo else "/static/modelo2.jpg"
    return f'''
    <style>
        body {{
            background-image: url('/static/fondo.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            margin: 0;
            padding: 0;
        }}
        .navbar {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 56px;
            background: #4B2E19;
            color: #fff;
            display: flex;
            align-items: center;
            font-size: 1.3em;
            font-family: sans-serif;
            z-index: 1000;
            box-shadow: 0 2px 8px #0002;
            padding-left: 2em;
            letter-spacing: 1px;
        }}
        .navbar-logo {{
            height: 38px;
            width: auto;
            margin-right: 18px;
        }}
        .navbar-title {{
            font-weight: bold;
            letter-spacing: 2px;
        }}
        .main-content {{
            margin-top: 80px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .form-container {{
            background: rgba(255,255,255,0.92);
            padding: 2em 2.5em;
            border-radius: 12px;
            max-width: 480px;
            width: 95vw;
            margin: 2em auto;
            box-shadow: 0 0 10px #aaa;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .modelo-img {{
            max-width: 220px;
            max-height: 250px;
            border-radius: 10px;
            box-shadow: 0 0 8px #aaa;
            display: block;
            margin: 0 auto 1em auto;
        }}
        .selector-row {{
            display: flex;
            gap: 2.5em;
            justify-content: center;
            margin-bottom: 1.5em;
        }}
        .selector-col {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .color-preview, .herrajes-preview {{
            width: 208px;
            height: 208px;
            border-radius: 8px;
            box-shadow: 0 0 6px #aaa;
            border: 1px solid #ccc;
            object-fit: cover;
            background: #eee;
            margin-top: 0.5em;
        }}
        .copy-btn {{
            padding: 0.7em 1.5em;
            font-size: 1.1em;
            border-radius: 8px;
            border: none;
            background: #222;
            color: #fff;
            cursor: pointer;
            margin-top: 1em;
            display: block;
            margin-left: auto;
            margin-right: auto;
            text-align: center;
            text-decoration: none;
            transition: background 0.2s;
        }}
        .copy-btn:hover {{
            background: #444;
        }}
        form label {{
            display: block;
            margin-bottom: 1em;
        }}
    </style>
    <div class="navbar">
        <a href="/" style="display: flex; align-items: center; text-decoration: none; color: inherit;">
            <img src="/static/logo.png" alt="Logo" class="navbar-logo">
            <span class="navbar-title">Teteu Cueros</span>
        </a>
    </div>
    <div class="main-content">
        <div class="form-container">
            <img id="carteraImg" src="{imagen}" alt="{modelo}" class="modelo-img">
            <h2>Personaliza tu {modelo}</h2>
            <form id="personalizarForm">
                <div class="selector-row">
                    <div class="selector-col">
                        <label>Color:
                            <select name="color" id="colorSelect">
                                <option value="negro">Negro</option>
                                <option value="marron">Marrón</option>
                                <option value="marron claro">Marrón Claro</option>
                            </select>
                        </label>
                        <img id="colorPreview" class="color-preview" src="/static/colors1.png" alt="Color seleccionado">
                    </div>
                    <div class="selector-col">
                        <label>Herrajes:
                            <select name="herrajes" id="herrajesSelect">
                                <option value="plata">Plata</option>
                                <option value="dorado">Dorado</option>
                            </select>
                        </label>
                        <img id="herrajesPreview" class="herrajes-preview" src="/static/h1.png" alt="Herraje seleccionado">
                    </div>
                </div>
                <button type="submit" class="copy-btn">Copiar enlace</button>
            </form>
        </div>
    </div>
    <script>
    // Cambia la imagen de color según la selección
    const colorSelect = document.getElementById('colorSelect');
    const colorPreview = document.getElementById('colorPreview');
    colorSelect.addEventListener('change', function() {{
        var img = '/static/colors1.png';
        if (this.value === 'marron') img = '/static/colors2.png';
        if (this.value === 'marron claro') img = '/static/colors3.png';
        colorPreview.src = img;
        actualizarCarteraImg();
    }});
    // Cambia la imagen de herrajes según la selección
    const herrajesSelect = document.getElementById('herrajesSelect');
    const herrajesPreview = document.getElementById('herrajesPreview');
    herrajesSelect.addEventListener('change', function() {{
        var img = '/static/h1.png';
        if (this.value === 'dorado') img = '/static/h2.png';
        herrajesPreview.src = img;
        actualizarCarteraImg();
    }});

    // Cambia la imagen de la cartera según color y herraje
    function actualizarCarteraImg() {{
        const color = colorSelect.value;
        const herraje = herrajesSelect.value;
        // Mapear color y herraje a nombre de archivo
        var colorFile = 'negro';
        if (color === 'marron') colorFile = 'marron';
        if (color === 'marron claro') colorFile = 'marron_claro';
        var herrajeFile = 'plata';
        if (herraje === 'dorado') herrajeFile = 'dorado';
        // Asumimos modelo1, puedes adaptar si hay más modelos
        var modelo = 'modelo1';
        if ('{modelo}'.toLowerCase().includes('urbana')) modelo = 'modelo2';
        const imgPath = `/static/${{modelo}}_${{colorFile}}_${{herrajeFile}}.jpg`;
        document.getElementById('carteraImg').src = imgPath;
    }}

    document.getElementById('personalizarForm').onsubmit = async function(e) {{
        e.preventDefault();
        const form = e.target;
        const data = new FormData(form);
        const params = new URLSearchParams(data);
        const modelo = encodeURIComponent('{modelo}');
        const resp = await fetch(`/personalizar?modelo=${{modelo}}`, {{
            method: 'POST',
            body: params
        }});
        const enlace = await resp.text();
        navigator.clipboard.writeText(enlace);
        alert('¡Enlace copiado!');
    }};
    </script>
    '''


# Nueva ruta para procesar la personalización y devolver el enlace
@app.route('/personalizar', methods=['POST'])
def personalizar():
    color = request.form.get('color')
    herrajes = request.form.get('herrajes')
    modelo = request.args.get('modelo', 'Cartera')
    producto = modelo
    id_personalizacion = str(uuid.uuid4())
    personalizaciones[id_personalizacion] = Personalizacion(producto, color, herrajes)
    enlace = url_for('ver_personalizacion', id=id_personalizacion, _external=True)
    return enlace

# Ruta para ver la personalización
@app.route('/ver/<id>')
def ver_personalizacion(id):
    p = personalizaciones.get(id)
    if not p:
        return '<h2>Personalización no encontrada</h2>', 404
    # Determinar el nombre de archivo de la imagen según modelo, color y herrajes
    modelo = 'modelo1'
    if p.producto and 'urbana' in p.producto.lower():
        modelo = 'modelo2'
    color_file = 'negro'
    if p.color == 'marron':
        color_file = 'marron'
    elif p.color == 'marron claro':
        color_file = 'marron_claro'
    herraje_file = 'plata'
    if p.herrajes == 'dorado':
        herraje_file = 'dorado'
    img_path = f"/static/{modelo}_{color_file}_{herraje_file}.jpg"
    return f'''
    <h2>Tu {p.producto} Personalizada</h2>
    <img src="{img_path}" alt="Cartera personalizada" style="max-width:320px;max-height:340px;border-radius:12px;box-shadow:0 0 10px #aaa;margin-bottom:1em;display:block;">
    <ul>
        <li><b>Modelo:</b> {p.producto}</li>
        <li><b>Color:</b> {p.color}</li>
        <li><b>Herrajes:</b> {p.herrajes}</li>
    </ul>
    '''

# Bloque para ejecutar la app
if __name__ == "__main__":
    app.run(debug=True)
