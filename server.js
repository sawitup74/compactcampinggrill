// Zero-dependency static server for Render.
const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname,types={'.html':'text/html; charset=utf-8','.css':'text/css','.xml':'application/xml','.txt':'text/plain','.js':'text/javascript','.png':'image/png','.svg':'image/svg+xml'};
const allow=/\.(html|css|xml|txt|png|svg)$/;
http.createServer((q,s)=>{let u=decodeURIComponent(q.url.split('?')[0]);
 if(u==='/healthz'){s.writeHead(200);return s.end('ok')}
 if(u==='/')u='/index.html'; if(!path.extname(u))u+='.html';
 const f=path.join(root,path.normalize(u));
 if(!f.startsWith(root)||!allow.test(f)||!fs.existsSync(f)){s.writeHead(404,{'content-type':types['.html']});return s.end(fs.readFileSync(path.join(root,'404.html')))}
 s.writeHead(200,{'content-type':types[path.extname(f)],'cache-control':'public, max-age=3600'});fs.createReadStream(f).pipe(s);
}).listen(process.env.PORT||3000);
