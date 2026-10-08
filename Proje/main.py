import vericek
import tespit
import time

while True:
    
    # Önce veriler çekilsin
    vericek.calistir()

    # Sonra tespit yapılsın
    tespit.calistir()

    time.sleep(3)
