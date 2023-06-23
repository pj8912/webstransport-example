# from aioquic import *
# class Response:
#     def __init__ (self):
#         self.promises = []
#         self.headers = None
#         self.data = b''

# async def run(configuration: QuicConfiguration, url: str, data: str, headers: Dict = {}, allow_push: bool = True, response: Response = None) -> None:
#     # parse URL
#     parsed = urlparse(url)
#     assert parsed.scheme in (
#         "https"
#     ), "Only https:// URLs are supported."

#     if ":" in parsed.netloc:
#         host, port_str = parsed.netloc.split(":")
#         port = int(port_str)
#     else:
#         host = parsed.netloc
#         port = 443

#     async with connect(
#         host,
#         port,
#         configuration=configuration,
#         create_protocol=HttpClient,
#         session_ticket_handler=save_session_ticket,
#     ) as client:
#         client = cast(HttpClient, client)

#         if parsed.scheme == "wss":
#             pass
#         else:
#             # perform request
#             start = time.time()
#             if data is not None:
#                 headers ['content-type'] = "application/x-www-form-urlencoded"
#                 http_events = await client.post(
#                     url,
#                     data=data.encode("utf8"),
#                     headers = headers,
#                     allow_push = allow_push
#                 )
#             else:
#                 http_events = await client.get(url, headers, allow_push)
#             elapsed = time.time() - start

#             # print speed
#             octets = 0
#             for http_event in http_events:
#                 if isinstance(http_event, DataReceived):
#                     octets += len(http_event.data)
#             logger.info(
#                 "Received %d bytes in %.1f s (%.3f Mbps)"
#                 % (octets, elapsed, octets * 8 / elapsed / 1000000)
#             )

#             # print response
#             for http_event in http_events:
#                 if isinstance(http_event, HeadersReceived):
#                     resp_headers = {}
#                     for k, v in http_event.headers:
#                         resp_headers [k.decode ()] = v.decode ()
#                     response.headers = resp_headers
#                 elif isinstance(http_event, DataReceived):
#                     response.data += http_event.data
#                 else:
#                     # server push
#                     if not allow_push:
#                         if hasattr (client._http, 'send_cancel_push'):
#                             client._http.send_cancel_push (http_event.push_id)
#                             client.transmit()
#                         continue
#                     push_headers = {}
#                     for k, v in http_event.headers:
#                         push_headers [k.decode ()] = v.decode ()
#                     response.promises.append (push_headers)


#  # prepare configuration
# configuration = QuicConfiguration(
#     is_client=True, alpn_protocols=H3_ALPN
# )
# configuration.load_verify_locations(os.path.join (os.path.dirname (__file__), 'pycacert.pem'))
# configuration.verify_mode = ssl.CERT_NONE
# try:
#     with open(SESSION_TICKET, "rb") as fp:
#         configuration.session_ticket = pickle.load(fp)
# except FileNotFoundError:
#     pass

# def _request (url, data = None, headers = {}, allow_push = True):
#     logging.basicConfig(
#         format="%(asctime)s %(levelname)s %(name)s %(message)s",
#         level=logging.INFO,
#     )
#     loop = asyncio.get_event_loop()
#     response = Response ()
#     loop.run_until_complete(
#         run(configuration=configuration, url=url, data=data, headers = headers, allow_push = allow_push, response=response)
#     )
#     return response

# def get (url, headers = {}, allow_push = True):
#     return _request (url, headers = headers, allow_push = allow_push)

# def post (url, data, headers = {}, allow_push = True):
#     return _request (url, data, headers = headers, allow_push = allow_push)