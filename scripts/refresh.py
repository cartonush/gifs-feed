import json, re, time, urllib.request, urllib.error
from pathlib import Path

ROOT = 'https://api.redgifs.com/v2'
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/128 Safari/537.36'

def get_json(url, token=None):
    headers = {'User-Agent': UA, 'Accept': 'application/json, text/plain, */*', 'Referer': 'https://www.redgifs.com/', 'Origin': 'https://www.redgifs.com'}
    if token: headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as res: return json.loads(res.read())

def main():
    users = json.loads(Path('users').read_text(encoding='utf-8'))
    token = get_json(ROOT + '/auth/temporary')['token']
    result, errors = [], []
    for entry in users:
        raw = entry if isinstance(entry, str) else (entry.get('url') or entry.get('username') or entry.get('name', ''))
        match = re.search(r'redgifs\.com/(?:users/)?([^/?#]+)', raw, re.I)
        username = match.group(1) if match else raw.strip().lstrip('@')
        if not username: continue
        try:
            for page in range(1, 6):
                data = get_json(f'{ROOT}/users/{urllib.parse.quote(username)}/search?order=recent&count=100&page={page}', token)
                gifs = data.get('gifs', [])
                if not gifs: break
                for gif in gifs:
                    gif['user'] = gif.get('user') or {'name': username}
                    result.append(gif)
                if page >= int(data.get('pages', page)): break
                time.sleep(.2)
            print(f'{username}: catalog now {len(result)}')
        except Exception as exc:
            errors.append(f'{username}: {exc}')
            print(f'Could not fetch {username}: {exc}')
    # Deduplicate while retaining source order.
    unique = {g.get('id'): g for g in result if g.get('id')}
    Path('catalog.json').write_text(json.dumps(list(unique.values()), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if not unique and users: raise SystemExit('No gifs were fetched. Check users, RedGIFs API availability, or endpoint changes.')
    print(f'Saved {len(unique)} gifs. Errors: {len(errors)}')

if __name__ == '__main__':
    import urllib.parse
    main()
