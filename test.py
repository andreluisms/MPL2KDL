from esp import osdebug as vendor_os_debugging_messages
from gc import collect as garbage_colector
# import esp, gc

from digitalLockerRefRef.digitalLocker_librayRef import wifi_station_connector_with_ssid_and_password, socket_connector_with_port_max_listenable_and_host, socket_accepted_connection, socket_request_receiver, web_page_loader, socket_response_sender_by_conn, init_locker, open_locker_request, close_locker_request, open_locker, close_locker

def startServer():
    vendor_os_debugging_messages(None)
    garbage_colector()

    wifi_station_connector_with_ssid_and_password('NameOfNetworkTP', '0123456789')

    locker_state, motor = init_locker()

    socket = socket_connector_with_port_max_listenable_and_host(3000, 2)

    while True:
        connection = socket_accepted_connection(socket)

        request = socket_request_receiver(connection, 1024)
        
        locker_on = open_locker_request(request)
        
        locker_off = close_locker_request(request)

        if locker_on == 6:
            locker_state = open_locker(motor)

        if locker_off == 6:
            locker_state = close_locker(motor)

        response = web_page_loader('page.html','""" + locker_state + """', locker_state)

        socket_response_sender_by_conn(connection, response)


class c:
    pass

A = "356"
B = 356
C = c()
D = [1, 2.548, "3", C] 
M = """aaaaa"""
E = True
F = (1.12312, 22.304, C)
G = {'''chave''': F}
H = None
L = []