import pdb # pdb.set_trace()
import unittest
import random
import json
from flask import Flask, jsonify
from flask import Response
from flask import request

from app import app, db
from app.mod_auth.models import User, Receta

class TestParticipant(unittest.TestCase):
    def setUp(self):
        app.config.from_object('config')
        db.session.close()
        db.drop_all()
        db.create_all()
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

    def test_obtener_receta(self):
        receta = Receta('Spaguettis', 'cocinero_vasco@arguinanogabilondourdangarin.com','Spaguettis, carne  y tomate')
        db.session.add(receta)
        db.session.commit()
        result = self.app.get('auth/todas_recetas/Spaguettis',follow_redirects=True)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        print ("  Url una receta en concreto: 200")
        list = []
        list=[]
        list.append({'Titulo' : 'Spaguettis'})
        list.append({ 'Descripcion' : 'Spaguettis, carne  y tomate' })
        list.append({  'Usuario' : 'cocinero_vasco@arguinanogabilondourdangarin.com' })
        #    list.append(receta.usuario)
        array=json.dumps(list)
        self.assertEqual(data,json.loads(array))
        #self.assertIn(array,data)
        print("Respuesta obtener receta en concreto: ok")


    def test_obtener_todas_receta(self):
        receta = Receta('Spaguettis', 'cocinero_vasco@arguinanogabilondourdangarin.com','Spaguettis, carne  y tomate')
        db.session.add(receta)
        receta = Receta('Calamares', 'pescador@arguinanogabilondourdangarin.com','Calamares')
        db.session.add(receta)
        db.session.commit()
        receta = Receta.query.order_by(Receta.date_created).all()
        list=[]
        for i in receta:
            list.append({ 'Titulo' : i.titulo })
            list.append({ 'Descripcion' : i.descripcion })
            list.append({  'Usuario' : i.usuario })
        result = self.app.get('auth/todas_recetas',follow_redirects=True)
        data = json.loads(result.data)
        self.assertEqual(result.status_code, 200)
        print ("Url todas_recetas: 200")
        array=json.dumps(list);
        self.assertEqual(data,json.loads(array))
        print("Respuesta todas_recetas: ok")


if __name__ == '__main__':
    unittest.main()
