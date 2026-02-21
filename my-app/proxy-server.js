const http = require('http');
const https = require('https');

const server = http.createServer((req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(200);
    res.end();
    return;
  }

  if (req.url.startsWith('/proxy/')) {
    const targetUrl = decodeURIComponent(req.url.substring(7));
    console.log('Fetching:', targetUrl);
    
    const options = {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.artic.edu/',
        'Accept': 'image/*,*/*'
      }
    };
    
    https.get(targetUrl, options, (response) => {
      console.log('Status:', response.statusCode);
      res.writeHead(response.statusCode, {
        'Content-Type': response.headers['content-type'],
        'Access-Control-Allow-Origin': '*'
      });
      response.pipe(res);
    }).on('error', (err) => {
      console.error('Proxy error:', err.message);
      res.writeHead(500);
      res.end('Error: ' + err.message);
    });
  } else {
    res.writeHead(200);
    res.end('Proxy server running');
  }
});

server.listen(3000, () => {
  console.log('Proxy server started on http://localhost:3000');
});
