from flask import Flask, request, Response
from flask_ngrok import run_with_ngrok
import math, random 
import base64

app = Flask(__name__)
run_with_ngrok(app)  # Start ngrok when app is run

#Sample UI
#-------------------------------------------------------------------------------
#
# Enter length               
#   -------------------         
#   |                 |        
#   -------------------       
#
#    OUTPUT____________________
#    |                         |
#    |                         |
#    |_________________________| 
#-------------------------------------------------------------------------------


#common error handler
@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>Page not found.</p>", 404


class Code128:

   CharSetA =  {
                ' ':0, '!':1, '"':2, '#':3, '$':4, '%':5, '&':6, "'":7,
                '(':8, ')':9, '*':10, '+':11, ',':12, '-':13, '.':14, '/':15,
                '0':16, '1':17, '2':18, '3':19, '4':20, '5':21, '6':22, '7':23,
                '8':24, '9':25, ':':26, ';':27, '<':28, '=':29, '>':30, '?':31,
                '@':32, 'A':33, 'B':34, 'C':35, 'D':36, 'E':37, 'F':38, 'G':39,
                'H':40, 'I':41, 'J':42, 'K':43, 'L':44, 'M':45, 'N':46, 'O':47,
                'P':48, 'Q':49, 'R':50, 'S':51, 'T':52, 'U':53, 'V':54, 'W':55,
                'X':56, 'Y':57, 'Z':58, '[':59, '\\':60, ']':61, '^':62, '_':63,
                '\x00':64, '\x01':65, '\x02':66, '\x03':67, '\x04':68, '\x05':69, '\x06':70, '\x07':71,
                '\x08':72, '\x09':73, '\x0A':74, '\x0B':75, '\x0C':76, '\x0D':77, '\x0E':78, '\x0F':79,
                '\x10':80, '\x11':81, '\x12':82, '\x13':83, '\x14':84, '\x15':85, '\x16':86, '\x17':87,
                '\x18':88, '\x19':89, '\x1A':90, '\x1B':91, '\x1C':92, '\x1D':93, '\x1E':94, '\x1F':95,
                'FNC3':96, 'FNC2':97, 'SHIFT':98, 'Code C':99, 'Code B':100, 'FNC4':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }

   CharSetB = {
                ' ':0, '!':1, '"':2, '#':3, '$':4, '%':5, '&':6, "'":7,
                '(':8, ')':9, '*':10, '+':11, ',':12, '-':13, '.':14, '/':15,
                '0':16, '1':17, '2':18, '3':19, '4':20, '5':21, '6':22, '7':23,
                '8':24, '9':25, ':':26, ';':27, '<':28, '=':29, '>':30, '?':31,
                '@':32, 'A':33, 'B':34, 'C':35, 'D':36, 'E':37, 'F':38, 'G':39,
                'H':40, 'I':41, 'J':42, 'K':43, 'L':44, 'M':45, 'N':46, 'O':47,
                'P':48, 'Q':49, 'R':50, 'S':51, 'T':52, 'U':53, 'V':54, 'W':55,
                'X':56, 'Y':57, 'Z':58, '[':59, '\\':60, ']':61, '^':62, '_':63,
                '' :64, 'a':65, 'b':66, 'c':67, 'd':68, 'e':69, 'f':70, 'g':71,
                'h':72, 'i':73, 'j':74, 'k':75, 'l':76, 'm':77, 'n':78, 'o':79,
                'p':80, 'q':81, 'r':82, 's':83, 't':84, 'u':85, 'v':86, 'w':87,
                'x':88, 'y':89, 'z':90, '{':91, '|':92, '}':93, '~':94, '\x7F':95,
                'FNC3':96, 'FNC2':97, 'SHIFT':98, 'Code C':99, 'FNC4':100, 'Code A':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }

   CharSetC = {
                '00':0, '01':1, '02':2, '03':3, '04':4, '05':5, '06':6, '07':7,
                '08':8, '09':9, '10':10, '11':11, '12':12, '13':13, '14':14, '15':15,
                '16':16, '17':17, '18':18, '19':19, '20':20, '21':21, '22':22, '23':23,
                '24':24, '25':25, '26':26, '27':27, '28':28, '29':29, '30':30, '31':31,
                '32':32, '33':33, '34':34, '35':35, '36':36, '37':37, '38':38, '39':39,
                '40':40, '41':41, '42':42, '43':43, '44':44, '45':45, '46':46, '47':47,
                '48':48, '49':49, '50':50, '51':51, '52':52, '53':53, '54':54, '55':55,
                '56':56, '57':57, '58':58, '59':59, '60':60, '61':61, '62':62, '63':63,
                '64':64, '65':65, '66':66, '67':67, '68':68, '69':69, '70':70, '71':71,
                '72':72, '73':73, '74':74, '75':75, '76':76, '77':77, '78':78, '79':79,
                '80':80, '81':81, '82':82, '83':83, '84':84, '85':85, '86':86, '87':87,
                '88':88, '89':89, '90':90, '91':91, '92':92, '93':93, '94':94, '95':95,
                '96':96, '97':97, '98':98, '99':99, 'Code B':100, 'Code A':101, 'FNC1':102, 'START A':103,
                'START B':104, 'START C':105, 'STOP':106
           }


   ValueEncodings = {  0:'11011001100',  1:'11001101100',  2:'11001100110',
        3:'10010011000',  4:'10010001100',  5:'10001001100',
        6:'10011001000',  7:'10011000100',  8:'10001100100',
        9:'11001001000', 10:'11001000100', 11:'11000100100',
        12:'10110011100', 13:'10011011100', 14:'10011001110',
        15:'10111001100', 16:'10011101100', 17:'10011100110',
        18:'11001110010', 19:'11001011100', 20:'11001001110',
        21:'11011100100', 22:'11001110100', 23:'11101101110',
        24:'11101001100', 25:'11100101100', 26:'11100100110',
        27:'11101100100', 28:'11100110100', 29:'11100110010',
        30:'11011011000', 31:'11011000110', 32:'11000110110',
        33:'10100011000', 34:'10001011000', 35:'10001000110',
        36:'10110001000', 37:'10001101000', 38:'10001100010',
        39:'11010001000', 40:'11000101000', 41:'11000100010',
        42:'10110111000', 43:'10110001110', 44:'10001101110',
        45:'10111011000', 46:'10111000110', 47:'10001110110',
        48:'11101110110', 49:'11010001110', 50:'11000101110',
        51:'11011101000', 52:'11011100010', 53:'11011101110',
        54:'11101011000', 55:'11101000110', 56:'11100010110',
        57:'11101101000', 58:'11101100010', 59:'11100011010',
        60:'11101111010', 61:'11001000010', 62:'11110001010',
        63:'10100110000', 64:'10100001100', 65:'10010110000',
        66:'10010000110', 67:'10000101100', 68:'10000100110',
        69:'10110010000', 70:'10110000100', 71:'10011010000',
        72:'10011000010', 73:'10000110100', 74:'10000110010',
        75:'11000010010', 76:'11001010000', 77:'11110111010',
        78:'11000010100', 79:'10001111010', 80:'10100111100',
        81:'10010111100', 82:'10010011110', 83:'10111100100',
        84:'10011110100', 85:'10011110010', 86:'11110100100',
        87:'11110010100', 88:'11110010010', 89:'11011011110',
        90:'11011110110', 91:'11110110110', 92:'10101111000',
        93:'10100011110', 94:'10001011110', 95:'10111101000',
        96:'10111100010', 97:'11110101000', 98:'11110100010',
        99:'10111011110',100:'10111101110',101:'11101011110',
        102:'11110101110',103:'11010000100',104:'11010010000',
        105:'11010011100',106:'11000111010'
                        }



   def makeCode(self, code):
    """ Create the binary code return a string which contains "0" for white bar, "1" for black bar """

    current_charset = None
    pos=sum=0
    skip=False
    for c in range(len(code)):
        if skip:
            skip=False
            continue

        #Only switch to char set C if next four chars are digits
        if len(code[c:]) >=4 and code[c:c+4].isdigit() and current_charset!=self.CharSetC or len(code[c:]) >=2 and code[c:c+2].isdigit() and current_charset==self.CharSetC:
            #If char set C = current and next two chars ar digits, keep C
            if current_charset!=self.CharSetC:
                #Switching to Character set C
                if pos:
                    strCode += self.ValueEncodings[current_charset['Code C']]
                    sum  += pos * current_charset['Code C']
                else:
                    strCode= self.ValueEncodings[self.CharSetC['START C']]
                    sum = self.CharSetC['START C']
                current_charset= self.CharSetC
                pos+=1
        elif  code[c] in self.CharSetB and current_charset!=self.CharSetB and not( code[c] in self.CharSetA and current_charset==self.CharSetA):
            #If char in chrset A = current, then just keep that
            # Switching to Character set B
            if pos:
                strCode += self.ValueEncodings[current_charset['Code B']]
                sum  += pos * current_charset['Code B']
            else:
                strCode= self.ValueEncodings[self.CharSetB['START B']]
                sum = self.CharSetB['START B']
            current_charset= self.CharSetB
            pos+=1
        elif code[c] in self.CharSetA and current_charset!=self.CharSetA and not(code[c] in self.CharSetB  and current_charset==self.CharSetB):
            # if char in chrset B== current, then just keep that
            # Switching to Character set A
            if pos:
                strCode += self.ValueEncodings[current_charset['Code A']]
                sum  += pos * current_charset['Code A']
            else:
                strCode += self.ValueEncodings[self.CharSetA['START A']]
                sum = self.CharSetA['START A']
            current_charset= self.CharSetA
            pos+=1

        if current_charset==self.CharSetC:
            val= self.CharSetC[code[c:c+2]]
            skip=True
        else:
            val=current_charset[code[c]]

        sum += pos * val
        strCode += self.ValueEncodings[val]
        pos+=1

    #Checksum
    checksum= sum % 103

    strCode +=  self.ValueEncodings[checksum]

    #The stop character
    strCode += self.ValueEncodings[current_charset['STOP']]

    #Termination bar
    strCode += "11"
    return strCode



   def getImage(self, value, height = 50, extension = "PNG", path = "\\"):
      """ Get an image with PIL library value code barre value height height in pixel of the bar code extension image file extension"""
      from PIL import Image, ImageFont, ImageDraw
      import os
      # from string import lower, upper
      path = os.getcwd()
      
      # Get the bar code list
      bits = self.makeCode(value)

      # Create a new image
      position = 8
      im = Image.new("1",(len(bits)+position,height))

      # Load font/content/courB08.pil
      font = ImageFont.load(path+"/courB08.pil")

      # Create drawer
      draw = ImageDraw.Draw(im)

      # Erase image
      draw.rectangle(((0,0),(im.size[0],im.size[1])),fill=256)

      # Draw text
      draw.text((23, height-9), value, font=font, fill=0)

      # Draw the bar codes
      for bit in range(len(bits)):
         if bits[bit] == '1':
            draw.rectangle(((bit+position,0),(bit+position,height-10)),fill=0)

      # Save the result image
      im.save(path+"/"+value+"."+extension.lower(),extension.upper())
      im.show()
      from IPython.display import display
      display(im)
      return im

    
def testWithChecksum():
   """ Test bar code with checksum """
   bar = Code128()
   assert(bar.makeCode('HI345678')=='11010010000110001010001100010001010111011110100010110001110001011011000010100100001001101100011101011')

def testImage(value):
  import io
  """ Test images generation with PIL """
  bar = Code128()
  img = bar.getImage(value,50,"gif")
  fp = io.BytesIO()

  img.save(fp,"PNG")
  fp.seek(0)
  # resp = Response(fp.getvalue(),mimetype="image/png")
  # fp.close()

  # return resp
  # return bar.getImage("978221211070",50,"png"),200
  return fp.getvalue()

@app.route('/barcode', methods=['GET'])
def test():
   """ Execute all tests """
   testWithChecksum()
   value = request.args['value']
   data64 = base64.b64encode(testImage(value))
   return home(value,u'data:img/jpeg;base64,'+data64.decode('utf-8'))
   return 


@app.route('/', methods=['GET','POST'])
def home(value="AWord123",img=""):
  print(str(value))
  return '''<!DOCTYPE html>
<html>
<head>
<title>BARCODE</title>
<style>
body {
  background-color: #4db8ff;
  text-align: center;
  color: white;
  font-family: Arial, Helvetica, sans-serif;
}
span {
	color : white;
    font-style: oblique;
}
.info {
	background-color : #0099ff;
    padding : 20px;
    margin: -10px -10px 0 -10px;
}
.api_proc {
	background-color: #6600cc;
    padding:7px;
    border-radius:20px;
}
.workarea {
text-align : left;
padding : 50px;
}

input[type=text] {
  width: 80%;
  padding: 12px 20px;
  margin: 8px 0;
  display: inline-block;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  
}
input[type=submit] {
  width: 40%;
  background-color:   #00b359;
  color: white;
  padding: 10px 20px;
  margin: 8px 0;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size:17px;
}

input[type=submit]:hover {
  background-color: #00994d;
}
.response_form {
	padding-top:50px;
}
</style>
<link rel="icon" type="image/png" href="data:image/png;base64,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"/>

</head>
<body>
<div class="info">
<h1>BARCODE</h1>
<p>Returns the Image BARCODE out of the given message </p>
<p class="api_proc">API Call Format : <span>http://localhost:5000/barcode?value=AWord123</span></p>
</div>
<div class="workarea">

<form action="/barcode">
  <label for="message">Barcode Content</label><br>
  <input type="text" id="value" name="value" value="'''+value+'''"><br>
  <input type="submit" value="Submit">
</form>
<form class="response_form">
  <label for="response">Barcode</label><br>
  <img src="'''+img+'''"></img></form>
</div>

</body>
</html>
'''


if __name__ == "__main__":
   app.run()