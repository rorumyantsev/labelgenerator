from flask import Flask, request, Response, render_template_string, jsonify
import qrcode
from xhtml2pdf import pisa
import base64
import io

app = Flask(__name__)

@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Generar Etiqueta</title>
    </head>
    <body>
        <h1>Generar Etiqueta</h1>
        <form method="POST" action="/test">
            <label for="order_number">Número de Orden:</label>
            <input type="text" name="order_number" required><br><br>

            <label for="name">Nombre Completo:</label>
            <input type="text" name="name" required><br><br>

            <label for="phone">Teléfono:</label>
            <input type="text" name="phone" required><br><br>

            <label for="destination_address">Dirección:</label>
            <input type="text" name="destination_address" required><br><br>

            <label for="source_address">Dirección de Origen:</label>
            <input type="text" name="source_address" required><br><br>

            <label for="comment">Observaciones:</label>
            <textarea name="comment" rows="4" cols="50" required></textarea><br><br>

            <input type="submit" value="Generar Etiqueta">
        </form>
    </body>
    </html>
    '''



@app.route('/generate_label', methods=['POST'])
def generate_label():
    try:
        if request.form:
            data = request.form
        else:
            data = request.json

        order_number = data['order_number']
        name = data['name']
        phone_number = data['phone']
        destination_address = data['destination_address']
        origin_address = data['source_address']
        comment = data['comment']

        #nombre_cliente = "PATPRIMO"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(order_number)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img = qr_img.resize((100, 100))  # Resize the QR code to 100x100px

        buffer = io.BytesIO()
        qr_img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        alternative_html = render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Label</title>
                <style>
                    @page {
                        size: a4 portrait;
                        @frame content_frame {
                            left: 10pt; width: 290pt; top: 10pt; height: 290pt;
                        }
                    }
                    
                    .label {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin: 10px;
                        padding: 10px;
                        width: 10cm;
                        height: 10cm;
                        border: 2px solid black;
                        display: grid;
                        grid-template-areas:
                            "logo logo origin"
                            "qr qr number"
                            "qr qr name"
                            ". . phone"
                            ". . destination"
                            ". . comment";
                    }
                    .logo {
                        grid-area: logo;
                        padding: 10px;
                        text-align: left;
                    }
                    .logo img {
                        width: 50px;
                        height: 50px;
                    }
                    .number {
                        grid-area: number;
                        text-align: center;
                    }
                    .origin {
                        grid-area: origin;
                        text-align: center;
                    }
                    .destination {
                        grid-area: destination;
                        text-align: center;
                    }
                    .qr {
                        grid-area: qr;
                        text-align: center;
                    }
                    .name {
                        grid-area: name;
                        text-align: center;
                    }
                    .phone {
                        grid-area: phone;
                        text-align: center;
                    }
                    .comment {
                        grid-area: comment;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="label">
                    <div class="logo">
                        <img src="yango_logo.png" alt="Yango Delivery Logo" />
                    </div>
                    <div class="qr">
                        <img src="data:image/png;base64,{{ qr_base64 }}" alt="QR code" width=100px height=100px />
                    </div>
                    <div class="number">
                        <label>Número de Orden: </label>
                        {{ order_number }}
                    </div>
                    <div class="origin">
                        <label>Dirección de Origen: </label>
                        {{ origin_address }}
                    </div>
                    <div class="destination">
                        <label>Dirección de Destino: </label>
                        {{ destination_address }}
                    </div>
                    <div class="name">
                        <label>Nombre: </label>
                        {{ name }}
                    </div>
                    <div class="phone">
                        <label>Número de teléfono: </label>
                        {{ phone_number }}
                    </div>
                    <div class="comment">
                        <label>Observaciones: </label>
                        {{ comment }}
                    </div>
                </div>
            </body>
            </html>
        ''',
        order_number=order_number,
        origin_address=origin_address,
        destination_address=destination_address,
        qr_base64=qr_base64,
        name=name,
        phone_number=phone_number,
        comment=comment
        )
        
        
        label_html = render_template_string('''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Label</title>
                <style>
                    .label {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        margin: 10px;
                        padding: 10px;
                        width: 10cm;
                        height: 10cm;
                        border: 2px solid black;
                        display: grid;
                        grid-template-areas:
                            "logo logo origin"
                            "qr qr number"
                            "qr qr name"
                            ". . phone"
                            ". . destination"
                            ". . comment";
                    }
                    .logo {
                        grid-area: logo;
                        padding: 10px;
                        text-align: left;
                    }
                    .logo img {
                        width: 100px;
                        height: 100px;
                    }
                    .number {
                        grid-area: number;
                        text-align: center;
                    }
                    .origin {
                        grid-area: origin;
                        text-align: center;
                    }
                    .destination {
                        grid-area: destination;
                        text-align: center;
                    }
                    .qr {
                        grid-area: qr;
                        text-align: center;
                    }
                    .name {
                        grid-area: name;
                        text-align: center;
                    }
                    .phone {
                        grid-area: phone;
                        text-align: center;
                    }
                    .comment {
                        grid-area: comment;
                        text-align: center;
                    }
                </style>
            </head>
            <body>
                <div class="label">
                    <div class="logo">
                        <img src="yango_logo.png" alt="Yango Delivery Logo" />
                    </div>
                    <div class="number">
                        <label>Número de Orden:</label><br>
                        {{ order_number }}
                    </div>
                    <div class="origin">
                        <label>Dirección de Origen:</label><br>
                        {{ origin_address }}
                    </div>
                    <div class="destination">
                        <label>Dirección de Destino:</label><br>
                        {{ destination_address }}
                    </div>
                    <div class="name">
                        <label>Nombre:</label><br>
                        {{ name }}
                    </div>
                    <div class="phone">
                        <label>Número de teléfono:</label><br>
                        {{ phone_number }}
                    </div>
                    <div class="comment">
                        <label>Observaciones:</label><br>
                        {{ comment }}
                    </div>
                    <div class="qr">
                        <img src="data:image/png;base64,{{ qr_base64 }}" alt="QR code" />
                    </div>
                </div>
            </body>
            </html>
        ''',
        order_number=order_number,
        origin_address=origin_address,
        destination_address=destination_address,
        qr_base64=qr_base64,
        name=name,
        phone_number=phone_number,
        comment=comment
        )
        #unusful_comment

        pdf_buffer = io.BytesIO()
        pisa.CreatePDF(alternative_html, dest=pdf_buffer)

        pdf_buffer.seek(0)
        response = Response(pdf_buffer.read(), content_type='application/pdf')
        response.headers['Content-Disposition'] = 'inline; filename=label.pdf'

        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
