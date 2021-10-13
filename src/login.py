import execjs
import requests


def generate_visitor_id():
    js = """
      const jsdom = require("jsdom");
      const { JSDOM } = jsdom;
      const dom = new JSDOM(`<!DOCTYPE html><p>Hello world</p>`);
      window = dom.window;
      document = window.document;
      function r()
      {
      function t()
      {
      return n?15&n[e++]:16*Math.random()|0
      }
      var n=null,e=0,r=window.crypto||window.msCrypto;
      r&&r.getRandomValues&&(n=r.getRandomValues(new Uint8Array(31)));
      for(var o,i="xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx",a="",s=0;s<i.length;s++)
      o=i[s],"x"===o?a+=t().toString(16):"y"===o?(o=3&t()|8,a+=o.toString(16)):a+=o;
      return a
      }
      """
    p = execjs.compile(js, cwd=r"./node_modules")
    return p.call("r")


def get_cookies():
    session = requests.Session()
    headers = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "content-length": "170",
        "content-type": "application/json",
        "origin": "https://www.nike.com",
        "referer": "https://www.nike.com.br/lebron-xviii-low-153-169-211-349959?gridPosition=K1",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
    }
    url = "http://www.nike.com/cn"
    resp = session.get(url=url, headers=headers)
    cookies = resp.request.headers.get("Cookie")
    _abck = "8E3BB569CE1B5C00C640D546508EB5B7~-1~YAAQdg8tF8uDLVh8AQAA8Vn8dQYRHrQE4xCvwh7SbcTv+7UZGHX2Oe7F6+yVoCVuwc0OD1cFQpNG68goMetCeqMpH4aSwub0MCncfs0m0eXLOg9+ukqauJfOmO3XEoXN0VpILPhvyxuVIUuA2m97g+D3oNQUg8Ifl3+JHyZ6vSUUyuz2AbrQkU7xWFVQa7ErztlDnl5MVzgQt196epL8m/dIjTsbtOUbBVJ+Se6LEIA7SINl+2/gOjMxjTztgMkGQxO81FPuq2MigdR4eX7vK/Sy6zkBzz0Usf6rj8G26WemdWm8843y4cuwrBJ1QWBmm8dlFyw5y6fzacAJQiMJji3Knr+zoa94j6IIuMxNauJnXl7AGjw7okOSVt9FFF6jnFKvE1kdcYK3KstepIJyQYFJJYBfYvAS8p2WHTXKDj760Ou3RAmZkAm9HNLpzyxrv4ECokOq+6du6q1/RjsYQko6ZvJhaVwEjUSGjPAYWvLSrddDE2GfD1YketOb1Q==~-1~-1~-1"
    bm_sz = cookies.split(";")[3]
    return {"_abck": _abck, "bm_sz": bm_sz}
