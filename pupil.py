"""
Receive data from Pupil server broadcast over TCP
test script to see what the stream looks like
and for debugging
"""
import zmq
import pygame
from msgpack import packb, unpackb


class Connection(object):
    """docstring for Connection"""
    def __init__(self, surface_name='pupil-demo', addr='127.0.0.1', req_port="50020"):
        super().__init__()
        # setup sockets
        context = zmq.Context()
        self.req = context.socket(zmq.REQ)
        self.req.connect("tcp://{}:{}".format(addr, req_port))
        self.req.send_string('SUB_PORT')
        sub_port = self.req.recv_string()

        self.sub = context.socket(zmq.SUB)
        self.sub.connect("tcp://{}:{}".format(addr, sub_port))
        self.sub.setsockopt_string(zmq.SUBSCRIBE, 'surface')

        # setup surface
        self.surface_name = surface_name
        self.tell_capture_to_create_surface()

    def tell_capture_to_create_surface(self):
        self.notify_capture({'subject': 'start_plugin', 'name': 'Surface_Tracker',
                             'args': {'min_marker_perimeter': 100, 'invert_image': False}})

    def recent_events(self):
        events = []
        while self.sub.get(zmq.EVENTS) & zmq.POLLIN:
            topic = self.sub.recv_string()  # required since we are recv 2-part msg
            msg = self.sub.recv()  # bytes
            surfaces = unpackb(msg, encoding='utf-8')
            filtered_surface = {k: v for k, v in surfaces.items() if surfaces['name'] == self.surface_name}
            try:
                # note that we may have more than one gaze position data point (this is expected behavior)
                gaze_positions = filtered_surface['gaze_on_srf']
                for gaze_pos in gaze_positions:
                    events.append(gaze_pos['norm_pos'])
            except KeyError:
                pass
        return events

    def notify_capture(self, notification):
        topic = 'notify.' + notification['subject']
        payload = packb(notification, use_bin_type=True)
        self.req.send_string(topic, flags=zmq.SNDMORE)
        self.req.send(payload)
        self.req.recv_string()


class Surface_Markers(object):
    def __init__(self, markers=['09', '21', '27', '43'], marker_size=(100, 100)):
        super().__init__()

        self.marker_images = []
        for m_id in markers:
            m_img = pygame.image.load('markers/marker {}.png'.format(m_id))
            pygame.transform.scale(m_img, marker_size)
            self.marker_images.append(m_img)

    def draw(self, game_surface):
        for idx, m_img in enumerate(self.marker_images):
            border_x = m_img.get_width() // 5
            border_y = m_img.get_height() // 5

            x, y = border_x, border_y
            if idx == 1:
                x = game_surface.get_width() - m_img.get_width() - border_x
            elif idx == 2:
                x = game_surface.get_width() - m_img.get_width() - border_x
                y = game_surface.get_height() - m_img.get_height() - border_y
            elif idx == 3:
                y = game_surface.get_height() - m_img.get_height() - border_y

            pygame.draw.rect(game_surface, (255, 255, 255), [x - border_x, y - border_y, m_img.get_width() + 2 * border_x, m_img.get_height() + 2 * border_y])
            game_surface.blit(m_img, (x, y))
