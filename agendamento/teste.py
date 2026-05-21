from escpos.printer import Network

p = Network("192.168.0.201")

p.text("TESTE IMPRESSAO\n\n")

p.cut()