import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter('ignore')
    
    
from src.utils import message, read_csv

filename = r"C:\Users\carv_\Documents\programming\python\whatsapp_sender\recordatorio.csv"
df = read_csv(filename)
df.head()


msg = """Buenas tardes estimado ${nombre}.
Le saludamos de la empresa INNTEL💚💚💚,
recordarle que su mensualidad está por vencer el ${fecha}
por un monto de ${monto},
evite los cortes.
Le envío los números de cuenta de la empresa."""


import os
from src.scrapper import service_run
from src.sender import find_sidebar, send_message

driver = service_run(os.getcwd())

wsp = "https://web.whatsapp.com"
driver.get(wsp)

find_sidebar(driver)

logs = 0

for i, row in df.iterrows():
    if i == 2:
        break
    line = message(row, msg)
    link = "%s/send?phone=51%d&text=%s&source&data" % (wsp, row.celular, line)
    logs = send_message(driver, link, row.celular, logs)

print(logs)

driver.quit()