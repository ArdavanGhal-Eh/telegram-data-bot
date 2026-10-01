import http from 'http';

const server = http.createServer((req, res) => {
  if (req.url === '/webhook' && req.method === 'POST') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ACK', engine: 'TypeScript Edge Gateway' }));
  } else {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Telegram Webhook Gateway Active');
  }
});

server.listen(3000, () => {
  console.log('🚀 TypeScript Webhook Gateway listening on port 3000');
});
