import json
import urllib
import urllib2

from flask import Flask, redirect, request
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)

client_id = '' #paste in your client id and secrect
client_secret = '' 

# change port and call back if needed otherwise use this one
redirect_uri = 'http://localhost:8080/oauth2callback'
link = 'https://accounts.google.com/o/oauth2/token'

###############
### GOOGLE AUTH
###############
class Auth(Resource):
 def get(self):
   redirect_url = 'https://accounts.google.com/o/oauth2/auth?scope=https://www.googleapis.com/auth/drive.photos.readonly&response_type=code&client_id=%s&redirect_uri=http://localhost:8080/oauth2callback&access_type=offline&approval_prompt=force' % (client_id)
   return redirect(redirect_url)


##################
### OUATH CALLBACK
##################
class Oauth2callback(Resource):
 def get(self):
   code = request.args.get('code','')
   params = {
     'code':code,
     'client_id':client_id,
     'client_secret':client_secret,
     'redirect_uri':redirect_uri,
     'grant_type':'authorization_code'
   }
   response = urllib2.urlopen(link, urllib.urlencode(params))
   json_data = json.loads(response.read())
   # look for refresh token in the logs
   print "Json Data: \n\n {0}\n".format(json_data)

   # bounce to account
   redirect("/")



api.add_resource(Auth, '/auth/google')
api.add_resource(Oauth2callback, '/oauth2callback')

if __name__ == '__main__':
  app.run(debug=True, port=8080)
