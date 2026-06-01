import os
from cryptography.fernet import Fernet
import shutil
print("All notes must be in Plain ASCII")

key = "KEY"

class tmpvars:
  tmp = "IMAPASSWORD"
  pswdtmp = "IMAPASSWORDTOO"
  notestmp = "IMSOMENOTES"
  filetmp = "IMAFILEPATH"

tv = tmpvars()

os.makedirs(".dat", exist_ok=True)
os.makedirs(".dat/DAT", exist_ok=True)
os.makedirs(".dat/DAT_OLD", exist_ok=True)

if os.path.exists(".dat/key.dll"):
  with open(".dat/key.dll", "r+b") as KF:
    key = KF.read()
  EDK = Fernet(key)  
else:
  with open(".dat/key.dll", "wb") as KF:
    print("Generating key.dll")
    KF.write(Fernet.generate_key())
  with open(".dat/key.dll", "rb") as KF:
    key = KF.read()
  EDK = Fernet(key)

if os.path.exists(".dat/PIN.dll"):
  with open(".dat/PIN.dll", "r") as PIN:
    pin = PIN.read()
else:
  with open(".dat/PIN.dll", "w") as PIN:
    PIN.write(input("Set PIN (Permanant) If entered incorrectly too many times all passwords are deleted : "))
  with open(".dat/PIN.dll", "r") as PIN:
    pin = PIN.read()

def exmp():
  message = b"Top secret data"
  cipher_text = EDK.encrypt(message)
  print(f"Encrypted: {cipher_text}")
  plain_text = EDK.decrypt(cipher_text)
  print(f"Decrypted: {plain_text.decode()}")
    
def addpswd(pswd, notes, file):
  with open(f".dat/DAT/{file}.PDAT", "ab+") as PDAT:
    print("Do Not Close Window")
    tv.tmp = EDK.encrypt(pswd)
    PDAT.write(tv.tmp)
  with open(f".dat/DAT_OLD/{file}.NDAT_OLD", "ab+") as NDAT_OLD:
    tv.tmp = EDK.encrypt(notes)
    NDAT_OLD.write(tv.tmp)
    print("Now ok to close the window")

def getfile():
  while True:
    tv.filetmp = (input("Password Name (File Name)"))
    if os.path.exists(f".dat/DAT/{tv.filetmp}.PDAT"):
      print(f"Choose a new file name. {tv.filetmp} Is taken.")
    else:
      break
  return(tv.filetmp)

def findpswds():
  pswds = os.listdir(".dat/DAT")
  print(pswds)

def viewpswd(file):
  with open(f".dat/DAT/{file}.PDAT", "rb") as PDAT:
    pswd = EDK.decrypt(PDAT.read())
    print(pswd.decode())
  with open(f".dat/DAT_OLD/{file}.NDAT_OLD", "rb") as NDAT_OLD:
    notes = EDK.decrypt(NDAT_OLD.read())
    print(notes.decode())

def main():
  while True:
    if input("Add password? (y/n) ") == "y":
      tv.pswdtmp = str.encode(input("Password "))
      tv.notestmp = str.encode(input("Notes "))
      tv.filetmp = getfile()
      addpswd(tv.pswdtmp, tv.notestmp, tv.filetmp)
    else:
      findpswds()
      viewpswd(input("File Name of password to view: "))
      
      

def checkpin():
  with open(".dat/PIN.dll", "r") as PIN:
    saved_pin = PIN.read().strip()
  attempts = 0
  while attempts < 3:
    entry = input("Enter PIN: ").strip()
    if entry == saved_pin:
      main()
      return
    attempts += 1
    print("Incorrect PIN")
  print("Too many incorrect attempts. Deleting saved passwords.")
  shutil.rmtree(".dat")

checkpin()
