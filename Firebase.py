from firebase import firebase
firebase = firebase.FirebaseApplication('https://finalproject-607a7-default-rtdb.europe-west1.firebasedatabase.app/', None)
#update in database
def add(MAC_ADDRESS,data):
 firebase.put('python_code124/Cars/',MAC_ADDRESS,data)
#take from database as json
def retreive():
  return firebase.get('python_code124/Cars/', '')
#delete from database
def delet(MAC_ADDRESS):
  firebase.delete('python_code124/Cars/', MAC_ADDRESS)
