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
            </head>
            <body>
                <form method="POST" enctype="multipart/form-data" action="">
                    <input type="file" name="myfile" />
                    <br>
                    <br>
                    <input type="submit" />
                </form>
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