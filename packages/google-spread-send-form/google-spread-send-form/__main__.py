from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import random
import os
import datetime
scope=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def main(args):
  scope=[
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
  ]
  #credentials_file=args.get("credentials_file","")
  #habría que poner el archivo en el front y ahcer que por detras
  #al enviar el formulario se mande el archivo también?
  file=os.getcwd()
  files=os.listdir(file)
  for f in files:
    print(f)
  
  credentials=ServiceAccountCredentials.from_json_keyfile_name(file+"/credentials.json",scope)
  #print(credentials.to_json())
  file= gspread.authorize(credentials)

  respuestas=file.open('Covas Vegetal (respuestas)')
  campos=respuestas.worksheet('Campos').get('A2:A18')
  #paso 1

  valores={
    "Fecha":datetime.date.today().strftime("%d/%m/%Y"),
    "ID_cliente":0,
    }
  print(campos)
  for campo in campos:
    valores[campo[0]]=0
  
  try:
    hoja=respuestas.worksheet('Cliente '+str(args['form']['ID_cliente'])) 
  except: 
    hoja=respuestas.add_worksheet('Cliente '+str(args['form']['ID_cliente']),rows=2,cols=30)
    hoja.update('1:1',[list(valores.keys())])
  #paso 2(rellenar conjunto de valores)
  
  for i in args['form'].keys():
    if i in valores.keys():
      valores[i]=args['form'][i]
  #buscar ultima fila vacia
  columna_1=hoja.col_values(1)
  vacia=-1
  for n,fila in enumerate(columna_1):
    if fila=="":
      vacia=n+1
      break
  if vacia==-1:
    hoja.append_row(list(valores.values())) 
  else:
    hoja.update('str(vacia):str(vacia)',list(valores.values()))

  return {
    "headers":{
      'Access-Control-Allow-Origin':"*"
    },
    "body":{"args":args,
            "valores":valores,
            'response_type': 'in_channel',
            #"files":files,
            }

  }
print(main({"form":{"ID_cliente":2,
                    "Tomate (kg)":1,
                    "lechugas":2, 
                    }}))