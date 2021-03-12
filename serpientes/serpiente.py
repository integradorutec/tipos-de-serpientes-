import web
import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

urls = ('/upload', 'Upload')

class Upload():
    def GET(self):
        web.header("Content-Type","text/html; charset=utf-8")
        return """
        <html>
            <head>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width">
                <title>Serpentario</title>
                <h1 class="display-1" align="center">Bienvenido al serpentario</h1>
            </head>
            <body style="background-color:#33D4FF;">
                <div align="center" style="width:50px; height:50px;"><img src= "static/cobra.jpg"/> </div>
                    <div align="center">
                        <br>
                        <br>
                        <h3> Suba la imagen a analizar </h3>
                        <form method="POST" enctype="multipart/form-data" action="">
                            <input type="file" name="myfile" />
                            <br>
                            <br>
                            <input type="submit" />
                        </form>
                    </div>
                </div>
            </body>
        </html>"""
    def POST(self):
        x = web.input(myfile={})
        filedir = 'static' # change this to the directory you want to store the file in.
        if 'myfile' in x: # to check if the file-object is created
            filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
            filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
            fout = open(filedir +'/'+ filename,'wb') # creates the file where the uploaded file should be stored
            fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
            fout.close() # closes the file, upload complete.
        
        np.set_printoptions(suppress=True)
        model = tensorflow.keras.models.load_model('static/keras_model.h5')
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        image = Image.open('static/'+ filename)
        size = (224, 224)
        image = ImageOps.fit(image, size, Image.ANTIALIAS)
        image_array = np.asarray(image)
        image.show()
        normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
        data[0] = normalized_image_array
        prediction = model.predict(data)

        for i in prediction:
            if i[0] > 0.7:
                resultado = "Es una cobra: "
            elif i[1] > 0.7:
                resultado = "Es una boa: "
            elif i[2] > 0.7:
                resultado = "Es una coralillo: "
            else:
                resultado = "No se encontro coincidencias:"
        return resultado
        raise web.seeother('/upload')

if __name__ == "__main__":
   app = web.application(urls, globals()) 
   app.run()