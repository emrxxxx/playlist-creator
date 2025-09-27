import requests

urls = [
    "https://raw.githubusercontent.com/MehmetKaraGMX/Live/refs/heads/main/vizi.m3u",
    "https://raw.githubusercontent.com/karams81/voddensrb/11a2db99c0aabbb641c29672f362b14f2c674c86/trgoalas.m3u",
    "https://raw.githubusercontent.com/karams81/voddensrb/11a2db99c0aabbb641c29672f362b14f2c674c86/selcuk.m3u"
]

output_file = "channel.m3u"

def fetch_m3u_content(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.text
    except requests.RequestException:
        return ""

def merge_m3u_files(urls, output_file):
    seen_urls = set()
    out = []
    out.append("#EXTM3U")
    out.append("")
    first_source = True
    for url in urls:
        content = fetch_m3u_content(url)
        if not content:
            continue
        if not first_source:
            out.append("")
        first_source = False
        lines = content.splitlines()
        i = 0
        while i < len(lines) and lines[i].strip() == "#EXTM3U":
            i += 1
        j = i
        current_meta = []
        while j < len(lines):
            line = lines[j]
            s = line.strip()
            if s.startswith("#"):
                current_meta.append(line)
                j += 1
            elif s:
                url_s = s
                if url_s not in seen_urls:
                    seen_urls.add(url_s)
                    out.extend(current_meta)
                    out.append(line)
                    current_meta = []
                else:
                    current_meta = []
                j += 1
            else:
                if current_meta:
                    current_meta.append(line)
                j += 1
        if current_meta:
            out.extend(current_meta)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(f"{output_file} dosyası oluşturuldu.")

if __name__ == "__main__":
    merge_m3u_files(urls, output_file)
