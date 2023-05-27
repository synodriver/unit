import io


def application(env, start_response):
    start_response('200', [('Content-Length', '10')])
    return io.BytesIO(b'0123456789')
